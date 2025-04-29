
from src.validator import *
from src.recognizer import *

if __name__ == "__main__":

    # Example usage:
    recognizer = NumberPlateRecognizer()
    # plate_img, plate_number = recognizer.recognizePlateNumber("images/car2.jpeg")
    print("Detected Plate:", recognizer.recognizePlateNumber("images/car1.jpg")[1])
    print("Detected Plate:", recognizer.recognizePlateNumber("images/car2.jpeg")[1])
    print("Detected Plate:", recognizer.recognizePlateNumber("images/car3.png")[1])
    print("Detected Plate:", recognizer.recognizePlateNumber("images/car4.jpeg")[1])
    print("Detected Plate:", recognizer.recognizePlateNumber("images/car5.jpg")[1])
    print("Detected Plate:", recognizer.recognizePlateNumber("images/car6.jpeg")[1])

    while True:

        cv2.imshow("image1", recognizer.recognizePlateNumber("images/car1.jpg")[0])
        # cv2.imshow("image2", recognizer.recognizePlateNumber("images/car2.jpeg")[0])
        cv2.imshow("image3", recognizer.recognizePlateNumber("images/car3.png")[0])
        # cv2.imshow("image4", recognizer.recognizePlateNumber("images/car4.jpeg")[0])
        cv2.imshow("image5", recognizer.recognizePlateNumber("images/car5.jpg")[0])
        cv2.imshow("image6", recognizer.recognizePlateNumber("images/car6.jpeg")[0])



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ----- testing some scenarios -----
    # validator = RomanianLicensePlateValidator()
    # print(validator.verifyPlateFormat("B767NTT"))   # Valid
    # print(validator.verifyPlateFormat("TM17NTT"))   # Valid
    # print(validator.verifyPlateFormat("TM1NTT"))    # Invalid - number too short
    # print(validator.verifyPlateFormat("Bm162NTT"))  # Invalid - lowercase
    # print(validator.verifyPlateFormat("B162N1T"))   # Invalid - last part must be letters
