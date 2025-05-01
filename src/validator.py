
class RomanianLicensePlateValidator:
    def __init__(self):
        
        self.county_prefixes = [
            "AB", "AR", "AG", "BC", "BH", "BN", "BT", "BV", "BR", "B", "BZ", "CS", "CL", "CJ", "CT", "CV", "DB",
            "DJ", "GL", "GR", "GJ", "HR", "HD", "IL", "IS", "IF", "MM", "MH", "MS", "NT", "OT", "PH", "SM", "SJ",
            "SB", "SV", "TR", "TM", "TL", "VS", "VL", "VN"
        ]
        self.special_prefixes = ["A", "FA", "ALA", "MAI"]
        self.diplomatic_prefixes= ["CD", "TC", "CO"]

    def removeSpacesFromString(self, input_string):
        """
        This function removes all spaces from the input string.
         :param input_string:
        :return: the input string without spaces
        """
        return input_string.replace(' ', '')

    def isUpperCase(self, input_string):
        """
        This function checks if the input string contains lower case letters.
         :param input_string:
        :return: boolean corresponding to the presence of lowercase letters
        """
        return input_string.isupper()

    def doesNotContainSpecialCharacter(self, input_string):
        """
         This function checks if the input string contains any special characters.
          :param input_string:
        :return: boolean corresponding to the presence of special characters
        """
        return input_string.isalnum()

    def isValid3LetterString(self, string_in_plate):
        """
        This function checks if the last 3 letter string in the plate is correct
            In romania: 
                    -Letter Q cannot be used
                    -First letter canot be I or O
                    -III and OOO combinations are not valid
                    
            :param string_in_plate:
        :return: boolean corresponding to the validity 3 letter string
        """
        
        if string_in_plate[0]=='I' or string_in_plate[0]=='O':
            print('3 letter string cannot begin with "O" or "I"')
            return False
           
        elif "Q" in string_in_plate:
            print('3 letter string cannot contain letter "Q"')
            return False
            
        elif string_in_plate=="III" or  string_in_plate=="OOO":
            print('3 cannot equal string "III or "OOO"')
            return False
        else:
            return True 

    def isValidSpecialPlate(self, prefix):
        """
        This function checks if the prefix is for diplomatic plates.
            :param county_string:
        :return: boolean corresponding to the validity of the prefix string
        """
        return prefix in self.special_prefixes

    def isValidDiplomaticPlate(self, prefix):
        """
        This function checks if the prefix is for special organization].
            :param county_string:
        :return: boolean corresponding to the validity of the prefix string
        """
        return prefix in self.diplomatic_prefixes

    def isValidCounty(self, prefix):
        """
        This function checks if the county string is valid.
            :param county_string:
        :return: boolean corresponding to the validity of the county string
        """
        return prefix in self.county_prefixes

    # -----------------------------------------------------------------
    # ---------- MAIN VERIFICATION FUNCTION FOR ROMANIAN PLATES -------
    # -----------------------------------------------------------------
    def verifyPlateFormat(self, text_plate):
        # ----- removing all spaces from the input string -----
        text_plate = self.removeSpacesFromString(text_plate)

        # ----- checking if there is any lowercase letters -----
        if not self.isUpperCase(text_plate):
            return "[ERROR] The plate contains lowercase letters."

            # ----- checking if there are special characters -----
        if not self.doesNotContainSpecialCharacter(text_plate):
            return "[ERROR] The plate contains special characters."

        plateEntry = {"region": "", "number": "", "string": ""}

        i = 0
        length = len(text_plate)

        # ----- extracting the county from the string -----
        if text_plate[1].isdigit():

            plateEntry['region'] = text_plate[0]
            i = 1

        # case MAI and ALA license plates
        elif length and text_plate[0:3].isalpha():
            plateEntry['region'] = text_plate[0:3]
            i = 3
                
        elif length and text_plate[0:2].isalpha():
            plateEntry['region'] = text_plate[0:2]
            i = 2
       
        else:
            return "[ERROR] Invalid county format."

        # ----- Checking if the plate is regular or special and its validity -----

        # Case Normal Plate
        if self.isValidCounty(plateEntry['region']):
            # ----- extracting the number from the string -----
            number = ""
            while i < length and text_plate[i].isdigit() and len(number) < 6:
                number += text_plate[i]
                i += 1

            # Case normal plate(including bucharest)
            if len(number)==2 or (len(number)==3 and plateEntry['region']=="B"):
                plateEntry['number'] = number

            # Case temporary plate
            elif len(number) >= 3 and len(number)<=6 and number[0]=="0" and number[len(number)-1]!="0":
                plateEntry['number'] = number
                return plateEntry

            else:
                return "[ERROR] Number part is too short or too long"
            
            # ----- extracting the plate string from the string -----
            remaining = text_plate[i:]
            if len(remaining) != 3 or not remaining.isalpha():
                return "[ERROR] The last part must be exactly 3 letters."

            plateEntry["string"] = remaining
            
            if self.isValid3LetterString(plateEntry["string"]):
                return plateEntry
            else: 
                return "[ERROR] License plate 3 letter string format"
        
        # Case Special Organization Plate
        elif self.isValidSpecialPlate(plateEntry['region']):
            digitArray = text_plate[len(plateEntry['region']):]

            if 3 <= len(digitArray) <= 7 and digitArray.isdigit():
                plateEntry["number"] = digitArray
                return plateEntry

            else:
                return "[ERROR] Numbers in military plate incorrect"

        # Case Diplomatic Plate
        elif self.isValidDiplomaticPlate(plateEntry['region']):
            digitArray = text_plate[len(plateEntry['region']):]
            if len(digitArray) == 6 and digitArray.isdigit() and int(digitArray[0:3])>=101 and int(digitArray[3:6])>=101:
                     
                plateEntry["number"] = digitArray
                return plateEntry
            else:
                return "[ERROR] Numbers in diplomatic plate incorrect"

        # Incorrect Reading
        else:   
            return "[ERROR] Invalid county, organization or diplomatic prefix at the beginning of the license plate."


def main():
    validator = RomanianLicensePlateValidator()

    # print(validator.verifyPlateFormat("B12OBC"))      # Standard plate
    # print(validator.verifyPlateFormat("MAI153"))      # Special plate
    # print(validator.verifyPlateFormat("CD123156"))    # Correct Diplomatic plate
    # print(validator.verifyPlateFormat("CD023156"))    # Inorrect Diplomatic plate
    print(validator.verifyPlateFormat("CD12A156"))    # Inorrect Diplomatic plate
    # print(validator.verifyPlateFormat("CJ0567"))      # Temporary plate

if __name__ == "__main__":
    main()
    
    
