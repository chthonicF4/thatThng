
import time , random

def Dothings(loadingConn,file):
    '''
    
    All this is , is a stand in for somthing that acctualy does somthing 
    right now all it is doing in reading random lines from the file you provide.
    the LoadingConn variable is what you can use to send back the satus of the proccess
    by using .send() i have it set up right now so that the window is expecting a tupple 
    with a float in the first slot ranging from 0 to 1 , representing the percentage 
    compleated and a string which is the staus message that is show below the loading
    bar. 

    when this fucntion is run , i have it in a wrapper that will take care of all of the 
    other things that need to be done when the function finishes like closing the pipe 
    between the window and the function and joining back the thread the fucntion runs on.

    '''


    total = 5000
    sum = 0
    data = file
    t = time.time()
    staus = data[:-1][random.randint(0,len(data)-2)]
    d = random.random()*2 + 1.5

    while True:

        time.sleep(random.random()*.2)
        sum += int(random.random()*10)

        if (time.time()-t) > d : 
            t = time.time()
            d = random.random()*2 + 1.5
            staus = data[:-1][random.randint(0,len(data)-2)]

        loadingConn.send((sum/total,staus))
        if sum/total >= 1 : break
