import tkinter as tk
from tkinter import Canvas, BOTH
import pygetwindow as gw
import pyautogui
import cv2 as cv
import pytesseract

#mouse click on button
def buttonClick(event):
    #returns a list but select only the first element in the list
    currentWindow = gw.getWindowsWithTitle("league Gold Dif Calculator")[0]
    windowCorner = [currentWindow.left, currentWindow.top]
    #title bar has 35 thickness
    blueScreenshot = pyautogui.screenshot(r"./blueScreenshot.png", region=(windowCorner[0] + 10, windowCorner[1] + 95, 100, 35))
    redScreenshot = pyautogui.screenshot(r"./redScreenshot.png", region=(windowCorner[0] + 360, windowCorner[1] + 95, 100, 30))
    screenshotList = ["./blueScreenshot.png", "./redScreenshot.png"]
    teamGold = [None] * 2

    for team, screenshot in enumerate(screenshotList):
        #read the screenshot and then prep it for scaning
        capture = cv.imread(screenshot)
        capture = cv.cvtColor(capture, cv.COLOR_BGR2GRAY)
        capture = cv.threshold(capture, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]

        #optional debug shows the images as the NN sees them
        #cv.imshow("prepared image", capture)
        #cv.waitKey(0)

        tesseractConfig = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        goldValue = pytesseract.image_to_string(capture, config=tesseractConfig, lang="eng")
        #keep only digits and then store in team gold values
        goldValue = ''.join(c for c in goldValue if c.isdigit())
        teamGold[team] = goldValue

    try:
        blueGold = float(teamGold[0]) / 10
        redGold = float(teamGold[1]) / 10
    except ValueError:
        print("Error, could not parse the given input images")
        return

    goldDifference = blueGold - redGold
    absoluteDifference = 100 * abs(goldDifference) / ((blueGold + redGold)/2)


    blueTeamGold.set(str(blueGold) + "k")
    redTeamGold.set(str(redGold) + "k")

    if blueGold > redGold:
        rawGoldLead.set("← %.2fk" % round(goldDifference, 2))
        percentGoldLead.set("← %.2f" % round(absoluteDifference, 2) + "%")
    else:
        rawGoldLead.set("→ %.2fk" % round(abs(goldDifference), 2))
        percentGoldLead.set("→ %.2f" % round(absoluteDifference, 2) + "%")
    print("")


###main


#create window
window = tk.Tk()
window.title("League Gold Dif Calculator")
window.attributes('-alpha', 0.45)
window.resizable(False,False)
width = 450
height = 200
window.geometry("x".join([str(width), str(height)]))

#create a canvas to draw shapes in the window
canvas = Canvas(window)
#blue team rectangle
canvas.create_rectangle(10, 70, 90, 100, outline="#00f", fill="")
#red team rectangle
canvas.create_rectangle(365, 70, 445, 100, outline="#f00", fill="")
canvas.pack(fill = BOTH, expand = 1)

#create the team labels
blueTeamLabel = tk.Label(text = "Blue Team Gold")
blueTeamLabel.place(x = 10, y = 45)
redTeamLabel = tk.Label(text = "Red Team Gold")
redTeamLabel.place(x = 360, y = 45)

#create blue team gold representation
blueTeamGold = tk.StringVar()
blueTeamGold.set("--.-k")
blueTeamGoldLabel = tk.Label(textvariable = blueTeamGold)
blueTeamGoldLabel.place(x = 35, y = 110)

#create red team gold representation
redTeamGold = tk.StringVar()
redTeamGold.set("--.-k")
redTeamGoldLabel = tk.Label(textvariable = redTeamGold)
redTeamGoldLabel.place(x = 390, y = 110)

#create the raw gold lead label
rawGoldLead = tk.StringVar()
rawGoldLead.set("--.-k")
rawGoldLeadLabel = tk.Label(textvariable = rawGoldLead)
rawGoldLeadLabel.place(x = 210, y = 110)

#create the percent gold lead label
percentGoldLead = tk.StringVar()
percentGoldLead.set("--%")
percentGoldLeadLabel = tk.Label(textvariable = percentGoldLead)
percentGoldLeadLabel.place(x = 210, y = 130)

#create and place button
button = tk.Button(text="Calculate Gold Dif")
button.bind("<Button-1>", buttonClick)
button.place(x = 165, y = 5)

#start the mainloop
window.mainloop()
