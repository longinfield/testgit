import cv2 as cv
import argparse
import datetime
import imutils
import time
import numpy as np
import matplotlib.pyplot as plt

capture = cv.VideoCapture('../Resources/luping2.mp4')
vHeight = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
vWidth = capture.get(cv.CAP_PROP_FRAME_WIDTH)
resizeWidth = vWidth / 20
resizeHeight = vHeight / 20
preGray = None
preFrame = None
frameDiff = []
frameCount = 0


# boxLB, boxRB, boxLT, boxRT = np.zeros((vHeight/20, vWidth/20, 3), dtype='unit8')

def frameContinuous(frameDiff, directory):
    start = [frameDiff[0]]
    end = []
    for i in range(len(frameDiff) - 1):
        if (frameDiff[i + 1][0] - frameDiff[i][0]) > 10:
            end.append(frameDiff[i])
            start.append(frameDiff[i + 1])
            cv.imwrite(directory + '/' + str(frameDiff[i][0]) + "_end.jpg", frameDiff[i][1])
            cv.imwrite(directory + '/' + str(frameDiff[i + 1][0]) + "_pre.jpg", frameDiff[i + 1][2])
            cv.imwrite(directory + '/' + str(frameDiff[i + 1][0]) + "_start.jpg", frameDiff[i + 1][1])
    end.append(frameDiff[-1])
    cv.imwrite(directory + '/' + str(frameDiff[-1][0]) + "_end.jpg", frameDiff[-1][1])
    cv.imwrite(directory + '/' + str(frameDiff[0][0]) + "_pre.jpg", frameDiff[0][2])
    cv.imwrite(directory + '/' + str(frameDiff[0][0]) + "_start.jpg", frameDiff[0][1])
    print(len(start) == len(end))
    return start, end


def rescaleFrame(frame, scale=0.6):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


while True:
    # lastBoxLB, lastBoxRB, lastBoxLT, lastBoxRT = np.zeros((vHeight / 20, vWidth / 20, 3), dtype='unit8')
    diffArea = 0
    area_count = 0
    isTrue, frame = capture.read()
    text = "Rest"

    if not isTrue:
        break

    # lastBoxLB = frame[int(resizeHeight):int(resizeHeight*3), 0:int(resizeWidth*2)]
    # lastBoxRB = frame[int(resizeHeight):int(resizeHeight * 3), 0:int(resizeWidth * 2)]

    frame_resized = rescaleFrame(frame)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (21, 21), 0)

    if preFrame is None:
        preFrame = frame
        preGray = gray
        frameCount = frameCount + 1
        continue
    frameDelta = cv.absdiff(preGray, gray)
    # cv.imshow("framedelta",frameDelta)

    frameCount = frameCount + 1
    thresh = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)[1]

    thresh = cv.dilate(thresh, None, iterations=2)
    # cv.imshow("dilate",thresh)
    # cv.waitKey(0)
    image, contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours:
        # if the contour is too small, ignore it
        if cv.contourArea(c) < 1000:
            continue

        # compute the bounding box for the contour, draw it on the frame
        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame, (x, y), (x + w, y + h), (100, 13, 32), 2)
        text = "Moving"
        diffArea = diffArea + cv.contourArea(c)

    cv.putText(frame, " Status: {}".format(text), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    if diffArea > 0:
        frameDiff.append((frameCount, frame, preFrame))

    preGray = gray
    preFrame = frame

    cv.imshow("Security Feed", frame)
    # cv.waitKey(0)
    # cv.imshow("Thresh", thresh)
    # cv.imshow("Frame Delta", frameDelta)
    # cv.imshow('Video', frame)
    # cv.imshow('Video Resized', frame_resized)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

# plt.scatter(range(len(frameDiff)),frameDiff)
# plt.show()
start, end = frameContinuous(frameDiff, '../key_frame/luping2')

capture.release()
cv.destroyAllWindows()
