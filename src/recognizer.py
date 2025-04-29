import cv2
import pytesseract
import numpy as np
import imutils


class NumberPlateRecognizer:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def resizeImage(self, image):
        # TODO: write this function better
        width = 800
        height = 600
        resized_image = cv2.resize(image, (width, height))
        return resized_image

    def preprocessImage(self, image):
        # ----- grayscale conversion -----
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # ----- noise reduction -----
        blurred = cv2.bilateralFilter(gray, 11, 17, 17)

        # ----- edge detection -----
        edged = cv2.Canny(blurred, 30, 200)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None

        # loop over contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            # if the approximated contour has four points,
            # then we can assume that we have found our
            # screen
            if len(approx) == 4:
                screenCnt = approx
            break

        return edged

    def findPlateContour(self, edged):
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(contours)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

        screenCnt = None

        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            # if the approximated contour has four points,
            # then we can assume that we have found our
            # screen
            if len(approx) == 4:
                screenCnt = approx
                break

        return screenCnt

    def extractPlateRegion(self, image, plate_contour):
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [plate_contour], -1, (255, 255, 255), -1)
        masked = cv2.bitwise_and(image, mask)

        x, y, w, h = cv2.boundingRect(plate_contour)
        plate_region = image[y:y + h, x:x + w]

        return plate_region

    def recognizePlateNumber(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Cannot read image from {image_path}")

        edged = self.preprocessImage(image)
        plate_contour = self.findPlateContour(edged)

        if plate_contour is None:
            return None, "No plate contour found"

        plate_region = self.extractPlateRegion(image, plate_contour)
        gray_plate = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_plate, config='--psm 8')

        return plate_region, text.strip()
