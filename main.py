
from src.validator import *

if __name__ == "__main__":
    validator = RomanianLicensePlateValidator()

    # ----- testing some scenarios -----
    print(validator.verifyPlateFormat("B767NTT"))   # Valid
    print(validator.verifyPlateFormat("TM17NTT"))   # Valid
    print(validator.verifyPlateFormat("TM1NTT"))    # Invalid - number too short
    print(validator.verifyPlateFormat("Bm162NTT"))  # Invalid - lowercase
    print(validator.verifyPlateFormat("B162N1T"))   # Invalid - last part must be letters
