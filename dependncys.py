# makes shure all of the modules are installed

import os

def Load():
    print('checking depenencys...')
    # make shure pip is uptodate
    print('checking for updates')
    os.system('python -m pip install --upgrade pip')
    #tkinter
    global messagebox , filedialog
    print('checking tkinter...',end='')
    try: from tkinter import messagebox , filedialog
    except ImportError :
        print('installing tkinter')
        os.system('pip install tkinter')
        from tkinter import messagebox , filedialog
    else: print('installed!')
    #customtkinter
    global ct
    print('checking customtinter..',end='')
    try: import customtkinter as ct
    except ImportError :
        print('installing customtkinter')
        os.system('pip install customtkinter')
        import customtkinter as ct
    else: print('installed!')
    print('Done checking depenencys')

if __name__ == '__main__' : 
    Load()


