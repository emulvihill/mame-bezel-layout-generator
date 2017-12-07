# import the necessary packages
import os

import numpy as np
import cv2
import csv

import shutil

dirName = "C:/Users/ericm/Desktop/arcade-bezel-overlays/"

MAX_DISPLAY_H = 1920
MAX_DISPLAY_V = 1080

xy1 = ()
xy2 = ()
bezelImage = np.array([])
gameName = ""
mouseIsDown = False


def drawRect(img, xy_1, xy_2):
    if xy_1 != () and xy_2 != ():
        cv2.rectangle(img, xy_1, xy_2, (0, 255, 0), 2)


def makeTemplate(name, img, xy_1, xy_2):
    width = img.shape[1]
    height = img.shape[0]

    template = f'''<!-- {name}.lay -->
            <mamelayout version="2">
              <element name="bezel">
                <image file="{name}.png" />
              </element>
              <view name="Bezel Artwork">
                <bezel element="bezel">
                  <bounds left="0" top="0" right="{width}" bottom="{height}" />
                </bezel>
                <screen index="0">
                  <bounds left="{xy_1[0]}" top="{xy_1[1]}" right="{xy_2[0]}" bottom="{xy_2[1]}" />
                </screen>
              </view>
            </mamelayout>'''
    return template


def parseAllGames():
    games = {}
    with open('resolutions.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            games[str(row["game_name"])] = row
    return games


def click_and_move(event, x, y, flags, param):
    global xy1, xy2, mouseIsDown, gameName, bezelImage

    if event == cv2.EVENT_LBUTTONDOWN:
        xy1 = (x, y)
        xy2 = ()
        mouseIsDown = True

    elif event == cv2.EVENT_LBUTTONUP:
        xy2 = (x, y)
        mouseIsDown = False

    elif mouseIsDown and event == cv2.EVENT_MOUSEMOVE:
        xy2 = (x, y)
        # draw a rectangle around the region of interest
        imgCopy = bezelImage.copy()
        drawRect(imgCopy, xy1, xy2)
        cv2.imshow(gameName, imgCopy)


def estimateRect(game, img):
    gw = float(game["video_x"])
    gh = float(game["video_y"])
    aspect = gw / gh

    width = img.shape[1]
    height = img.shape[0]

    top = 0.05 * height
    bottom = 0.95 * height

    vspan = bottom - top
    hspan = aspect * vspan

    left = 0.5 * (width - hspan)
    right = width - 0.5 * (width - hspan)

    return (int(left), int(top)), (int(right), int(bottom))


def mainLoop():
    global xy1, xy2, bezelImage, gameName

    all_games = parseAllGames()

    ld = os.listdir(dirName)
    for filename in ld:
        # print("opening " + dirName + filename)
        gameName = str(os.path.splitext(filename)[0])
        if gameName in all_games:
            game = all_games[gameName]
            bezelImage = cv2.imread(dirName + filename)
            cv2.namedWindow(gameName, cv2.WINDOW_NORMAL)

            width = min(MAX_DISPLAY_H, bezelImage.shape[1])
            height = min(MAX_DISPLAY_V, bezelImage.shape[0])
            cv2.resizeWindow(gameName, width, height)

            xy1, xy2 = estimateRect(game, bezelImage)

            imgCopy = bezelImage.copy()
            drawRect(imgCopy, xy1, xy2)
            cv2.imshow(gameName, imgCopy)

            cv2.setMouseCallback(gameName, click_and_move)
            cv2.waitKey(0)
            template = makeTemplate(gameName, bezelImage, xy1, xy2)

            os.makedirs(f'out/{gameName}', 0o777, True)
            f = open(f'out/{gameName}/default.lay', 'w')
            f.write(template)
            shutil.copyfile(dirName + filename, f'out/{gameName}/{filename}')
            cv2.destroyAllWindows()
        else:
            print(f'WARNING: Could not locate {gameName} in list of all known MAME entries.')


mainLoop()
