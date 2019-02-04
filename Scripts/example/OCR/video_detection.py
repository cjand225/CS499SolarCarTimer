# if this does not work, uninstall opencv-python and install opencv-contrib-python
import pytesseract
import cv2
import numpy as np
import imutils
import time
from imutils.object_detection import non_max_suppression
from imutils.video import VideoStream, FPS


def decode_predictions(scores, geometry):
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    minimumConfidence = 0.5  # minimum confidence needed to accept a text detection

    for i in range(0, numRows):
        # get scores and geometry data for each prediction
        scoresData = scores[0, 0, i]
        xData0 = geometry[0, 0, i]
        xData1 = geometry[0, 1, i]
        xData2 = geometry[0, 2, i]
        xData3 = geometry[0, 3, i]
        anglesData = geometry[0, 4, i]

        for j in range(0, numCols):
            if scoresData[j] < minimumConfidence:  # ignore detections with scores below the minimum confidence
                continue

            # offsets since the feature maps are 4x smaller than the input
            (offsetX, offsetY) = (j * 4.0, i * 4.0)

            angle = anglesData[j]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # calculate bounding box width and height
            h = xData0[j] + xData2[j]
            w = xData1[j] + xData3[j]

            # calculate bounding box coordinates for each corner
            endX = int(offsetX + (cos * xData1[j]) + (sin * xData2[j]))
            endY = int(offsetY - (sin * xData1[j]) + (cos * xData2[j]))
            startX = int(endX - w)
            startY = int(endY - h)

            # append bounding box coordinates and their respective scores to lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[j])
    return (rects, confidences)


def main():
    # initialize frame dimensions, resized frame dimensions, and the ratio between them
    (W, H) = (None, None)
    (newW, newH) = (320, 320)  # needs to be multiples of 32
    (rW, rH) = (None, None)

    # layer names that will be used, one for output probabilities and the other for box coordinates
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # laod the text detector
    net = cv2.dnn.readNet('frozen_east_text_detection.pb')

    # start the Video stream
    vs = VideoStream(src=0).start()

    # start fps calculator
    fps = FPS().start()

    # Video processing loop
    while True:
        frame = vs.read()  # get a frame

        if frame is None:
            break

        # resize the frame
        frame = imutils.resize(frame, width=1000)
        frame_original = frame.copy()

        if W is None or H is None:
            (H, W) = frame.shape[:2]
            rW = W / float(newW)
            rH = H / float(newH)

        frame = cv2.resize(frame, (newW, newH))

        # create a blob and use it for text detection
        blob = cv2.dnn.blobFromImage(frame, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)

        # get bounding boxes for predictions that pass the minimum confidence requirement
        (rects, confidences) = decode_predictions(scores, geometry)
        # eliminate unnecessary overlapping boxes
        boxes = non_max_suppression(np.array(rects), probs=confidences)

        # loop over each box
        for (startX, startY, endX, endY) in boxes:
            # 2 px buffer added to each side of each box
            startX = int(startX * rW - 2)
            startY = int(startY * rH - 2)
            endX = int(endX * rW + 2)
            endY = int(endY * rH + 2)

            cv2.rectangle(frame_original, (startX, startY), (endX, endY), (0, 255, 0), 2)
            # crop the image to just the bounding box
            image_cropped = frame_original[startY:endY, startX:endX]
            # uncomment the line below to detect black text instead of white text
            image_cropped = cv2.bitwise_not(image_cropped)
            # attempt prepossessing on the image
            try:
                image_gray = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2GRAY)
            except:
                continue
            image_blur = cv2.GaussianBlur(image_gray, (1, 1), 0)
            # thresh, image_thresh = cv2.threshold(image_blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            thresh, image_thresh = cv2.threshold(image_blur, 150, 255, cv2.THRESH_BINARY)
            # print(pytesseract.image_to_string(image_thresh, config='-c tessedit_char_whitelist=0123456789 -psm 7'))
            # detect text in the cropped image after preprocessing is done
            print(pytesseract.image_to_string(image_thresh, config='-psm 7'))
        fps.update()

        # show the frame with bounding boxes drawn
        cv2.imshow("Text Detection", frame_original)

        # if q is pressed, quit
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    fps.stop()
    print("Elapsed Time: ", fps.elapsed())
    print("FPS: ", fps.fps())

    # stop the webcam and destroy all windows
    vs.stop()
    cv2.destroyAllWindows()


main()
