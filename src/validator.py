import re

# TODO: diplomatic plate?
# TODO: military plate?
# TODO: temporary plate? (red numbers)

class RomanianLicensePlateValidator:
    def __init__(self):
        self.valid_counties = [
            "AB", "AR", "AG", "BC", "BH", "BN", "BT", "BV", "BR", "B", "BZ", "CS", "CL", "CJ", "CT", "CV", "DB",
            "DJ", "GL", "GR", "GJ", "HR", "HD", "IL", "IS", "IF", "MM", "MH", "MS", "NT", "OT", "PH", "SM", "SJ",
            "SB", "SV", "TR", "TM", "TL", "VS", "VL", "VN"
        ]

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


    def isValidCounty(self, county_string):
        """
        This function checks if the county string is valid.
            :param county_string:
        :return: boolean corresponding to the validity of the county string
        """
        counties = ["AB", "AR", "AG", "BC", "BH", "BN", "BT", "BV", "BR", "B", "BZ", "CS", "CL", "CJ", "CT", "CV", "DB",
                    "DJ", "GL", "GR", "GJ", "HR", "HD", "IL", "IS", "IF", "MM", "MH", "MS", "NT", "OT", "PH", "SM", "SJ",
                    "SB", "SV", "TR", "TM", "TL", "VS", "VL", "VN"]
        return county_string in counties


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
        elif length and text_plate[0:2].isalpha():
            plateEntry['region'] = text_plate[0:2]
            i = 2
        else:
            return "[ERROR] Invalid county format."

        # ----- checking if the county is valid -----
        if not self.isValidCounty(plateEntry['region']):
            return "[ERROR] Invalid county format."

        # ----- extracting the number from the string -----
        number = ""
        while i < length and text_plate[i].isdigit() and len(number) < 3:
            number += text_plate[i]
            i += 1

        if len(number) < 2:
            return "[ERROR] Number part is too short."

        plateEntry['number'] = number

        # ----- extracting the plate string from the string -----
        remaining = text_plate[i:]
        if len(remaining) != 3 or not remaining.isalpha():
            return "[ERROR] The last part must be exactly 3 letters."

        plateEntry["string"] = remaining

        return plateEntry
