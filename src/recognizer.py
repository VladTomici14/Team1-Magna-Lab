import cv2
import pytesseract
import numpy as np
import imutils
import matplotlib.pyplot as plt
import os

class NumberPlateRecognizer:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def resizeImage(self, image, width=800):
        """
        This function resizes the input image to the specified width while maintaining the aspect ratio.
            :param image: input image
            :param width: target width (default is 800)
        :return: the resized image
        """
        # ----- checking if the input image is valid -----
        if image is None:
            raise ValueError("[ERROR] The input image is None.")

        ratio = width / image.shape[1]
        dim = (width, int(image.shape[0] * ratio))
        return cv2.resize(image, dim)

    def preprocessImage(self, image):
        """
        This function preprocesses the input image for number plate recognition.
            :param image: input image
        :return: the preprocessed image with the edges detected
        """
        # ----- checking if the input image is valid -----
        if image is None:
            raise ValueError("[ERROR] The input image is None.")

        # ----- grayscale conversion -----
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # ----- noise reduction -----
        blurred = cv2.bilateralFilter(gray, 11, 17, 17)
        #blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        #cv2.imshow("Bilateral Filter", blurred)

        # ----- edge detection -----
        edged = cv2.Canny(blurred, 30, 200)#30 200
        #cv2.imshow("Edge Detection", edged)

        return edged

    def findPlateContour(self, edged):
        """
        This function finds the contour of the number plate in the input image.
            :param edged: the preprocessed image with the edges detected
        :return: the contour of the number plate coordinates
        """
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(contours)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

        screen_cnt = None

        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)#0.018
            # if the approximated contour has four points,
            # then we can assume that we have found our
            # screen
            if len(approx) == 4:
                return approx

        return None

    def extractPlateRegion(self, image, plate_contour):
        """
        This function extracts the region of interest (ROI) for the number plate from the input image.
            :param image: input image
            :param plate_contour: the contour of the number plate
        :return: the extracted plate region
        """
        # ----- checking if the input image is valid -----
        if image is None:
            raise ValueError("[ERROR] The input image is None.")

        mask = np.zeros_like(image)
        if plate_contour is not None:
            cv2.drawContours(mask, [plate_contour], -1, (255, 255, 255), -1)
        masked = cv2.bitwise_and(image, mask)

        x, y, w, h = cv2.boundingRect(plate_contour)
        plate_region = image[y:y + h, x:x + w]

        return plate_region

    def cleanPlateForOCR(self, plate_roi):
        # TODO: think about using this function to clean the plate region
        """
        This function cleans the extracted plate region for better OCR results.
            :param plate_roi:
        :return: the cleaned plate region
        """
        # ----- checking if the input image is valid -----
        if plate_roi is None:
            raise ValueError("[ERROR] The input image is None.")

        gray = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)

        # ----- increase contrast and reducing noise -----
        gray = cv2.equalizeHist(gray)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        return thresh

    def plotAllSteps(self, image_path, show_plot=False, save_plot=False):
        """
        This function plots all the steps of the pipeline for the input image.
            :param image_path: input image path
            :param show_plot: condition for showing the plots
            :param save_plot: condition for saving the plots
        """
        original = cv2.imread(image_path)

        # ----- checking if the input image is valid -----
        if original is None:
            raise ValueError("[ERROR] The input image is None.")

        # ----- adding all the image processing steps in an array -----
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        blurred = cv2.bilateralFilter(gray, 9, 75, 75)#11 17 17
        edged = cv2.Canny(blurred, 30, 200)

        images = [original, gray, blurred, edged]
        titles = ["Original", "Grayscale", "Blurred", "Edge Detection"]

        # ----- adding the plate region (if found in the input image) -----
        plate_contour = self.findPlateContour(edged)
        extracted_plate = None
        text = "No plate found"

        if plate_contour is not None:
            extracted_plate = self.extractPlateRegion(original, plate_contour)
            if extracted_plate is not None:
                images.append(extracted_plate)
                titles.append("Extracted Plate")

        # ----- plotting all the steps images in one single plot -----
        plt.figure(figsize=(15, 6))
        for i in range(len(images)):
            if images[i] is not None:
                plt.subplot(1, len(images), i + 1)
                if len(images[i].shape) == 2:
                    plt.imshow(images[i], cmap='gray')
                else:
                    plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
                plt.title(titles[i])
                plt.axis('off')

        # ----- setting the title -----
        plt.suptitle(f"Pipeline Steps{' - Detected: ' + self.recognizePlateNumber(image_path)[1]}", fontsize=16)
        plt.tight_layout()

        # ----- condition for showing the plots -----
        if show_plot:
            plt.show()

        # ----- condition for saving the plots -----
        if save_plot:
            plt.savefig(f"results/pipeline_steps_{os.path.splitext(os.path.basename(image_path))[0]}.png")

    def recognizePlateNumber(self, image_path, image=None):
        """
        This function recognizes the number plate from the input image.
             Input image can pe image from path or image from camera feed-sent from other code   
            :param image_path: input image path
        :return: the extracted plate region and the text from the plate
        """
        if image is None:
            image = cv2.imread(image_path)

        # ----- checking if the input image is valid -----
        if image is None:
            raise ValueError(f"Cannot read image from {image_path}")

        edged = self.preprocessImage(image)
        plate_contour = self.findPlateContour(edged)

        if plate_contour is None:
            return None, "No plate contour found"

        plate_region = self.extractPlateRegion(image, plate_contour)
        #cv2.imshow("ROI", plate_region)
        plate_region_processed = self.cleanPlateForOCR(plate_region)
        text = pytesseract.image_to_string(plate_region, config='--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

        return plate_region, text.strip()


