
from src.validator import *
from src.recognizer import *
from src.utils import *
import os

if __name__ == "__main__":

    # Example usage:
    recognizer = NumberPlateRecognizer()

    images_path = "images/"

    target_paths = []
    
    //x=2

    for file in os.listdir(images_path):
        if validImageFile(file):
            target_path = os.path.join(images_path, file)
            target_paths.append(target_path)

            extracted_plate = recognizer.recognizePlateNumber(target_path)

            print(f"{target_path}: {extracted_plate[1]}")
            recognizer.plotAllSteps(target_path, save_plot=True)

    # ----- testing some scenarios -----
    # validator = RomanianLicensePlateValidator()
    # print(validator.verifyPlateFormat("B767NTT"))   # Valid
    # print(validator.verifyPlateFormat("TM17NTT"))   # Valid
    # print(validator.verifyPlateFormat("TM1NTT"))    # Invalid - number too short
    # print(validator.verifyPlateFormat("Bm162NTT"))  # Invalid - lowercase
    # print(validator.verifyPlateFormat("B162N1T"))   # Invalid - last part must be letters
