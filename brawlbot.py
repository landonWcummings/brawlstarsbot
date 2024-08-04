from pyautogui import *
import pyautogui
import time
import keyboard
import random
import random
import win32api, win32con

isStuck = 0 
# brawlers left region = (20,100,200,220)
# loss exit region = (700,700,300,320)

def click(x,y):
    win32api.SetCursorPos((x+random.randint(0, 5) ,y+random.randint(0, 5)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.12) #This pauses the script for 0.1 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.03)

def attack():
    click(random.randint(1320,1330), random.randint(800,810))
    
def cloudAvg():
    cavg = [-1,-1]
    xtotal = 0
    ytotal = 0
    count = 0
    
    targcolor = 148,229,132
    pic = pyautogui.screenshot(region = (0,100,1600,1000))
    for x in range(0,1600,7):
        for y in range(0,900, 12): 
            color = pic.getpixel((x,y))
            if color == targcolor:
                xtotal += x
                ytotal += y
                count += 1
    if count >10:
        cavg[0] = (int)(xtotal/count)
        cavg[1] = (int)(ytotal/count)
        print("clouds seen")
    return cavg

def damaged(x,y):
    
    count = 0
    if x>100 and y>200:
        pic = pyautogui.screenshot(region = (400,300,800,500))
        for xa in range(0,300,7):
            for ya in range(0,400, 12): 
                color = pic.getpixel((xa,ya))
                if color[0]>200 and color[0]<237:
                    count += 1
                    
        if count >1:
            print("received damage")
            attack()
            time.sleep(0.3)
            attack()
            time.sleep(0.3)
            attack()
        
                        

def brawlMove(i,x,y):
    direction = i;
    if i==0:
        direction = random.randint(1, 4)
    
    if direction ==1:
        pyautogui.keyDown('w')
        pyautogui.keyDown('d')
        time.sleep(0.75)
        damaged(x,y)
        time.sleep(0.75)
        damaged(x,y)
        pyautogui.keyUp('w')
        pyautogui.keyUp('d')
    if direction ==2:
        pyautogui.keyDown('w')
        pyautogui.keyDown('a')
        time.sleep(0.75)
        damaged(x,y)
        time.sleep(0.75)
        damaged(x,y)
        pyautogui.keyUp('w')
        pyautogui.keyUp('a')
    if direction ==3:
        pyautogui.keyDown('s')
        pyautogui.keyDown('d')
        time.sleep(0.75)
        damaged(x,y)
        time.sleep(0.75)
        damaged(x,y)
        pyautogui.keyUp('s')
        pyautogui.keyUp('d')
    if direction ==4:
        pyautogui.keyDown('s')
        pyautogui.keyDown('a')
        time.sleep(0.75)
        damaged(x,y)
        time.sleep(0.75)
        damaged(x,y)
        pyautogui.keyUp('s')
        pyautogui.keyUp('a')

def react(sx,sy,cx,cy):
    global isStuck
    if sx == -1:
        isStuck += 1
        print("error self not detected")
        if isStuck >1:
            brawlMove(0,sx,sy)
    else:
        isStuck = 0
        if cx == -1 :
            brawlMove(0,sx,sy)
        else:
            if sx>cx:
                if sy>cy:
                    brawlMove(3,sx,sy)
                else:
                    brawlMove(1,sx,sy)
            else:
                if sy>cy:
                    brawlMove(4,sx,sy)
                else:
                    brawlMove(2,sx,sy)
    
def findObj():
    returna = [-1, -1, -1, -1]
# self place xy then cloud place xy
    cspots = cloudAvg()
    returna[2] = cspots[0]
    returna[3] = cspots[1]
    
#check for self
    try:
        selflocation = pyautogui.locateOnScreen("self.png",region = (300,204,1000,700), grayscale = False, confidence=0.6)
                                 
        if selflocation is not None:
            print("found myself")
            returna[0] = selflocation[0]
            returna[1] = selflocation[1]
                                                          
    except pyautogui.ImageNotFoundException:                
        time.sleep(0.01)
        try:
            selflocation = pyautogui.locateOnScreen("selfrightcorner.png",region = (300,204,1000,700), grayscale = False, confidence=0.6)
                                 
            if selflocation is not None:
                print("found myself")
                returna[0] = selflocation[0]
                returna[1] = selflocation[1]
        except Exception as e:
            try:
                selflocation = pyautogui.locateOnScreen("selfbush.png",region = (300,204,1000,700), grayscale = False, confidence=0.6)
                                         
                if selflocation is not None:
                    print("found myself")
                    returna[0] = selflocation[0]
                    returna[1] = selflocation[1]
                                                                  
            except pyautogui.ImageNotFoundException:                
                time.sleep(0.01)
                try:
                    selflocation = pyautogui.locateOnScreen("selfbushright.png",region = (300,204,1000,700), grayscale = False, confidence=0.6)
                                         
                    if selflocation is not None:
                        print("found myself")
                        returna[0] = selflocation[0]
                        returna[1] = selflocation[1]
                except Exception as e:
                    print(f"Unexpected error: {e}")
                                        
            except Exception as e:
                print(f"Unexpected error: {e}")
                time.sleep(0.5)
                                
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(0.5)
#look for self in bush
    
    return returna

def tryClose():
    try:
        location = pyautogui.locateOnScreen('lossExit.png',region = (700,700,300,320), grayscale = True, confidence=0.7)
        
        if location is not None:
             click(location[0], location[1])
             
             time.sleep(3)

            
             
        else:
            print("-----")
            

    except pyautogui.ImageNotFoundException:
         print("-----")
         
     
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(0.5)
#check for proceed
    try:
        location = pyautogui.locateOnScreen('proceed.png',region = (1050,785,550,250), grayscale = True, confidence=0.7)
        
        if location is not None:
             click(location[0], location[1])
             
             time.sleep(7)    
             
        else:
            print("tried to proceed but no button")
            
            

    except pyautogui.ImageNotFoundException:
         print("tried to proceed but no button")
     
    except Exception as e:
        print("error")
        
#check for real exit
    try:
        location = pyautogui.locateOnScreen('exit.png',region = (1050,785,550,250), grayscale = True, confidence=0.7)
        
        if location is not None:
             click(location[0], location[1])
             
             time.sleep(4)    
             
        else:
            print("tried to exit but no button")
            
            

    except pyautogui.ImageNotFoundException:
         print("tried to exit but no button")
     
    except Exception as e:
        print("error")

    

def isGameOver():
    try:
        location2 = pyautogui.locateOnScreen('exit.png',region = (1050,785,550,250), grayscale = True, confidence=0.7)

        if location2 is not None:
             print("exit detected")
             return True
    
    except pyautogui.ImageNotFoundException:
         time.sleep(0.01)
     
    except Exception as e:
        print("error occurs in isgameover")
        print(f"Unexpected error: {e}")
        time.sleep(0.5)
#check lossExit
    try:
        location2 = pyautogui.locateOnScreen('lossExit.png',region = (700,700,300,320), grayscale = True, confidence=0.7)

        if location2 is not None:
             print("loss exit detected")
             click(location2[0],location2[1])
             return True
    
    except pyautogui.ImageNotFoundException:
         time.sleep(0.01)
     
    except Exception as e:
        print("error occurs in isgameover")
        print(f"Unexpected error: {e}")
        time.sleep(0.5)
#check proceed
    try:
        location3 = pyautogui.locateOnScreen('proceed.png',region = (1050,785,550,250), grayscale = True, confidence=0.7)

        if location3 is not None:
             print("proceed detected")
             click(location2[0],location2[1])
             return True
        
    except pyautogui.ImageNotFoundException:
         time.sleep(0.01)
     
    except Exception as e:
        print("error occurs in isgameover")
        print(f"Unexpected error: {e}")
        time.sleep(0.5)
    return False

def inActiveGame():
    try:
        location = pyautogui.locateOnScreen('brawlersLeft.png',region =(20,100,300,220), grayscale = True, confidence=0.4)
        
        if location is not None:    
             print("in game")
             return True
        else:
            print("no game detected")
            return False

    except pyautogui.ImageNotFoundException:
         
         print("no game detected")
         return False
     
    except Exception as e:
        print("error occurs in active game")
        print(f"Unexpected error: {e}")
        time.sleep(0.5)


def battle(waitTime):
    print("setup")
    time.sleep(waitTime)
    print("began game")
    while inActiveGame() and not isGameOver():
        if keyboard.is_pressed('q'):
            break
        
        locations = findObj()
        print(locations[0])
        print(locations[1])
        print(locations[2])
        print(locations[3])
        react(locations[0],locations[1],locations[2],locations[3])
        
    
    tryClose()


    
count = 0
def reopenBrawl():
    try:
        location = pyautogui.locateOnScreen('brawlapp.png',region =(210,100,1200,520), grayscale = True, confidence=0.4)
        
        if location is not None:    
             print("reopening brawl")
             click(location[0],location[1])
             time.sleep(60)
             
        else:
            print("no game detected")
            

    except pyautogui.ImageNotFoundException:
         
         print("brawl app not detected")
         
     
    except Exception as e:
        print("error occurs in active game")
        print(f"Unexpected error: {e}")
        time.sleep(0.5)
while keyboard.is_pressed('q') == False:
    x,y = 0,104
    width, height = 1600,900
    pic = pyautogui.screenshot(region = (x,y,width,height))
    try:
         location = pyautogui.locateOnScreen('startup.png',region = (1050,785,550,250), grayscale = True, confidence=0.7)
         if location is not None:
             click(location[0]+50,location[1]+20)
             count = 0
             print("starting")
             battle(18)
         else:
             time.sleep(2)
             print("not starting")
     
    except pyautogui.ImageNotFoundException:
         
        time.sleep(2)
        print("not starting")
        count += 1
        if inActiveGame():
            battle(0)
            
        if count>=10 :
            tryClose()
        if count>10:
            reopenBrawl()
        if count>11:
            click(1500,900)
            count = 0
     
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(2)
    
