# if this does not work, uninstall opencv-python and install opencv-contrib-python
import pytesseract
import cv2
import sys
import os
import time
import numpy as np
from imutils.object_detection import non_max_suppression

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 image_detection.py [image path]")
        return

    pathname = os.path.dirname(sys.argv[0])     # get pathname of file
    filename = sys.argv[1]                      # image to open

    image = cv2.imread(filename)
    image_original = image.copy()
    h, w = image.shape[:2]      # image dimensions

    (newW, newH) = (640, 640)   # resize the image, needs to be multiples of 32
    rW = w / float(newW)
    rH = h / float(newH)
    image = cv2.resize(image, (newW, newH))
    (h, w) = image.shape[:2]    # get the new height and width

    # layers that will be used
    # the first provides probabilities and the second provides box coordinates
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the text detector
    net = cv2.dnn.readNet('frozen_east_text_detection.pb')

    # create a blob of the image and use that blob for text detection
    blob = cv2.dnn.blobFromImage(image, 1.0, (w, h), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    end = time.time()

    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    minimumConfidence = 0.5     # minimum confidence level needed to accept a detection

    for i in range(0, numRows):
        # extract scores and geometry data
        scoresData = scores[0, 0, i]
        xData0 = geometry[0, 0, i]
        xData1 = geometry[0, 1, i]
        xData2 = geometry[0, 2, i]
        xData3 = geometry[0, 3, i]
        anglesData = geometry[0, 4, i]

        for j in range(0, numCols):
            # skip scores that do not reach minimum confidence
            if scoresData[j] < minimumConfidence:
                continue

            # offset made since feature maps are 4x smaller than the input
            (offsetX, offsetY) = (j * 4.0, i * 4.0)

            angle = anglesData[j]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # find width and height of bounding box
            h = xData0[j] + xData2[j]
            w = xData1[j] + xData3[j]

            # find bounding box coordinates
            endX = int(offsetX + (cos * xData1[j]) + (sin * xData2[j]))
            endY = int(offsetY - (sin * xData1[j]) + (cos * xData2[j]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add bounding boxes and confidences to their respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[j])

    # get rid of overlapping bounding boxes
    boxes = non_max_suppression(np.array(rects), probs = confidences)

    # loop over each box
    for (startX, startY, endX, endY) in boxes:
        # 2px buffer added to all sides of the rectangle
        startX = int(startX * rW - 2)
        startY = int(startY * rH - 2)
        endX = int(endX * rW + 2)
        endY = int(endY * rH + 2)
        # draw the box
        cv2.rectangle(image_original, (startX, startY), (endX, endY), (0, 255, 0), 2)
        # crop the image to just the box
        image_cropped = image_original[startY:endY, startX:endX]
        # uncomment the line below to detect black text instead of white text
        # image_cropped = cv2.bitwise_not(image_cropped)
        # image preprocessing
        image_gray = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2GRAY)
        image_blur = cv2.GaussianBlur(image_gray, (1, 1), 0)
        thresh, image_thresh = cv2.threshold(image_blur, 150, 255, cv2.THRESH_BINARY_INV)
        # fetch text from the cropped image
        print(pytesseract.image_to_string(image_thresh, config='-psm 7'))
        # show the cropped image after preprocessing is complete
        cv2.imshow('image', image_thresh)
        cv2.waitKey(0)

    # show image with bounding boxes drawn
    cv2.imshow("Text Detection", image_original)
    cv2.waitKey(0)


    cv2.destroyAllWindows()


main()