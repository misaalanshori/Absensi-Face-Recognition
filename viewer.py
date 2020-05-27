#!/usr/bin/env python3
import glob
import os
import pickle
import cv2
from time import sleep
import pygame
import numpy as np

temp = {}
userDataPath = os.path.join(os.getcwd(), 'sessions') # Sets location for userData
sessionFiles = glob.glob(os.path.join(userDataPath, '*.session'))
print("Load Session:")
num = 1
for filename in sessionFiles: # Loads *.userData files
    print(str(num) + ". " + filename)
    num += 1
try:
    userInput = int(input("Input Number: ")) - 1
except:
    print("Your Input is not a number!")
    quit()

with open(sessionFiles[userInput], "rb") as fp: # Unpickling and appending to Known Lists
    data = pickle.load(fp)
font = cv2.FONT_HERSHEY_DUPLEX
print("\nLoaded Session: {}\n".format(sessionFiles[userInput]))

print("Initializing variables...")
currentFrame = 0
showFrame = True
frameTotal = len(data)
fheight, fwidth = data[0]["frame"].shape[:2]

print("Initializing PyGame..")
pygame.init()
white = (255, 255, 255) 
screen = pygame.display.set_mode((fwidth, fheight))
pygame.display.set_caption('Snapshot') 


def withoutKeys(d, keys):
    return {k: v for k, v in d.items() if k not in keys}

def printData(frameNum):
    number = 40
    os.system("clear")
    global userData, userList, userMinuteStats, data
    print("Snapshot Time: {}".format(data[frameNum]["datetime"]))
    print("Visible: ", end = " ")
    for i in userData[frameNum]:
        if userData[frameNum][i][0] == True:
            print(i + " (Accuracy: {:0.2f}%)".format(userData[frameNum][i][1]*100), end=" | ")
    print("\n")
    print("Statistics: ")
    for i in userMinuteStats:
        print("{} = {} / {} ({:0.2f})".format(i, userMinuteStats[i], frameTotal, userMinuteStats[i]/frameTotal) + " "*(number - len("{} = {} / {} ({:0.2f})".format(i, userMinuteStats[i], frameTotal, userMinuteStats[i]/frameTotal))) + "||  (Unfiltered: {:0.5f}%)".format(userPercentageStats[i]))
    return

def drawFrame(imgFrame):
    global data, screen
    if showFrame == False:
        return
    screen.fill([100,100,100])
    pyFrame = cv2.cvtColor(data[imgFrame]["frame"], cv2.COLOR_BGR2RGB)
    pyFrame = pyFrame.swapaxes(0,1)
    pyFrame = pygame.surfarray.make_surface(pyFrame)
    screen.blit(pyFrame, (0,0))
    
    pygame.display.update()

def handleInput(uInput):
    global currentFrame, showFrame, white, screen
    if uInput == "next":
        currentFrame += 1
        if currentFrame > frameTotal-1:
            currentFrame = 0
    elif uInput == "prev":
        currentFrame -= 1
        if currentFrame < 0:
            currentFrame = frameTotal - 1 
    elif uInput == "toggle":
        showFrame = not showFrame
        if not showFrame:
            pygame.quit()
        elif showFrame:
            pygame.init()
            white = (255, 255, 255) 
            screen = pygame.display.set_mode((fwidth, fheight))
            pygame.display.set_caption('Snapshot') 
    elif uInput[0:4] == "goto":
        currentFrame = int(uInput[5:]) - 1
        if currentFrame > (frameTotal - 1) or currentFrame < 0:
            currentFrame = 0

    else:
        print("NO!")

def main():
    drawFrame(currentFrame)
    printData(currentFrame)
    print("==============================================================================")
    print("\nCurrently showing frame number: {}\n".format(currentFrame + 1))
    print("next - Next Snapshot")
    print("prev - Previous Snapshot")
    print("toggle - Toggle Frame Snapshot ({})".format(showFrame))
    print("goto <num> - Go to frame number")
    print("==============================================================================")
    handleInput(input("#> "))

print("Initializing Arrays and Dictionaries...")
userData = []
for i in data: # creates list without frame and datetime data
    userData.append(withoutKeys(i, ["frame", "datetime"]))


userList = []
for i in userData[1]: # Creates list for names
    userList.append(i)

userMinuteStats = {}
for i in userList: # creates empty dictionary for storing total minutes the user was visible for
    userMinuteStats[i] = 0

for i in userData:
    for j in userList: # adds value to userMinuteStats
        userMinuteStats[j] += int(i[j][0])

userPercentageStats = {}
for i in userList: # creates empty dictionary for storing percentage of visibility
    userPercentageStats[i] = 0

for i in userData:
    for j in i:
        userPercentageStats[j] += i[j][1]

for i in userPercentageStats:
    userPercentageStats[i] = (userPercentageStats[i] / frameTotal) * 100

print("Starting...")
while True:
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        print("\nQuitting\n")
        quit()