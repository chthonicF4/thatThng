import time 
import customtkinter as ct
from tkinter import messagebox , filedialog
from threading import Thread
from multiprocessing import Pipe
from placeholder import Dothings

class Window():

    def exit(self):
        if  self.busy :
            self.running = not messagebox.askokcancel("Quit", "Are you sure you want to quit?\n(window is currently doing things)")
        else : self.running = False
     
    def __init__(self):
        self.running = False
        self.root = ct.CTk()
        self.clock = self.Clock()
        self.updates = []
        self.busy = False
        ct.set_appearance_mode('dark')
        ct.set_default_color_theme('dark-blue')

        self.root.protocol("WM_DELETE_WINDOW",self.exit)

    class Clock():
        def __init__(self):
            self.t = time.time_ns()
            self.dt = lambda : (time.time_ns()-self.t)*0.000000001
            self.Cdt = 0.00001
            pass

        def tick(self,fps=-1):
            delay = max(0,1/fps - self.dt())
            time.sleep(delay)
            self.Cdt = self.dt()
            self.t = time.time_ns()
            return self.Cdt

        def get_fps(self):
            return 1/self.Cdt

    def Run(self):
        self.root.update()
        self.running = True
        self.deltaTime = 0.0
        self.clock.tick()
        while self.running : 
            [update() for update in self.updates]
            self.root.update()
            self.deltaTime = self.clock.tick(60)
        # on window exit
        self.root.destroy()
        quit()

    def AddUpdate(self,func):
        self.updates.append(func)

    def RemoveUpdate(self,func):
        self.updates.remove(func)

class Fps ():

    def __init__(self,window:Window):
        self.root = window.root
        self.window = window
        self.FpsCounter = ct.CTkLabel(master=self.root,text=f'fps:{window.clock.get_fps():.2f}')

    def Update(self):
        self.FpsCounter.configure(text=f'fps:{window.clock.get_fps():.2f} dt:{window.deltaTime*1000:.2f}ms')

    def Pack(self):
        self.FpsCounter.place(x=0,y=0)
        self.window.AddUpdate(self.Update)

class Test():

    def __init__(self,window:Window):
        self.window = window
        self.root = window.root
        self.file = None
        # Parts

        self.Title = ct.CTkLabel(master=self.root,
                                 text=' Doing Nothing ',
                                 width=500,height=100,
                                 font=('arial',48)
                                 )
        
        self.GetFileButton = ct.CTkButton(master=self.root,
                                          text='Choose File',
                                          width=200,height=50,
                                          command=self.GetFile,
                                          font=('arial',20))
        
        self.Path = ct.CTkLabel(master=self.root,
                                text='',
                                width=500,height=10)
        
        self.loadingBar = ct.CTkProgressBar(master=self.root,
                                            width=500,height=50,
                                            corner_radius=0,
                                            mode='determinate',
                                            orientation='Horizontal')

        self.Status = ct.CTkLabel(master=self.root,
                                  text='',
                                  width=600,height=40,
                                  font=('arial',28))

        self.Restart = ct.CTkButton(master=self.root,
                                    text='Restart',
                                    width=200,height=100,
                                    command=self.StartDoing,
                                    font=('arial',20))

    def GetFile(self): # opens a file dialog 
        self.file = filedialog.askopenfile(mode='r',defaultextension='txt',title='Choose a file...')
        self.data = self.file.readlines()
        self.Path.configure(text=self.file.name)
        self.StartDoing()

    def LoadingUpdate(self): # updates loading bar while checking if the proccess has ended

        # get current progress
        try: 
            status = self.proccess.GetData()
        except BrokenPipeError : # proccess has ended , so remove loading bar from update list and close connection
            # remove loading bar from updates list
            self.window.RemoveUpdate(self.LoadingUpdate)
            self.window.busy = False
            self.Status.configure(text='Done? (proccess not responding)')
            # add restart button
            self.Restart.pack(pady=20)

        else : # update loading bar 
            if status == None : return
            self.loadingBar.set(status[0])
            self.Status.configure(text=status[1])
            
    def StartDoing(self):
        # get rid of old widgets 
        self.GetFileButton.destroy()
        self.Restart.forget()
        # place new ones 
        self.Path.pack(pady=10)
        self.loadingBar.pack(pady=10)
        self.loadingBar.set(0.0)
        self.Status.pack(pady=20)
        # change window busyness and add loading bar to update list
        self.window.busy = True
        self.window.AddUpdate(self.LoadingUpdate)
        self.proccess = BackgroundTask(Dothings)
        self.proccess.Start(self.data)

    def Pack(self):
        self.Title.pack(pady=10,side='top')
        self.GetFileButton.pack(pady=10)

class BackgroundTask () :
    def __init__(self,func):
        self.func =  func
        self.parent , self.child = Pipe()

    def Start(self,*args):

        def ProccessWrapper(func,child,*args):
            func(child,*args)
            child.close()
            self.Stop()

        self.proccess = Thread(target=ProccessWrapper,args=(self.func,self.child,*args),name=f'Background [{self.func.__name__}]',daemon=True)
        self.proccess.start()

    def Stop(self) : 
        self.parent.close()
        self.proccess.join()

    def GetData(self):
        if self.parent.poll() : return self.parent.recv()

    def isAlive(self):
        return self.proccess.is_alive()

window = Window()
window.root.geometry('1000x500')

Test(window).Pack()
Fps(window).Pack()

window.Run()