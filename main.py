import re


def removeSpacesFromString(input_string):
    """
    This function removes all spaces from the input string.
     :param input_string:
    :return: the input string without spaces
    """
    return input_string.replace(' ', '')


def isUpperCase(input_string):
    """
    This function checks if the input string contains lower case letters.
     :param input_string:
    :return: boolean corresponding to the presence of lowercase letters
    """
    return input_string.isupper()


def doesNotContainSpecialCharacter(input_string):
    """
     This function checks if the input string contains any special characters.
      :param input_string:
    :return: boolean corresponding to the presence of special characters
    """
    return input_string.isalnum()


def isValidCounty(county_string):
    """
    This function checks if the county string is valid.
        :param county_string:
    :return: boolean corresponding to the validity of the county string
    """
    counties = ["AB", "AR", "AG", "BC", "BH", "BN", "BT", "BV", "BR", "B", "BZ", "CS", "CL", "CJ", "CT", "CV", "DB",
                "DJ", "GL", "GR", "GJ", "HR", "HD", "IL", "IS", "IF", "MM", "MH", "MS", "NT", "OT", "PH", "SM", "SJ",
                "SB", "SV", "TR", "TM", "TL", "VS", "VL", "VN"]
    return county_string in counties


def verifyPlateFormat(text_plate):
    # ----- removing all spaces from the input string -----
    text_plate = removeSpacesFromString(text_plate)

    # ----- checking if there is any lowercase letters -----
    if isUpperCase(text_plate) == False:
        print("[ERROR] there are lower case letters")
        return

        # ----- checking if there are special characters -----
    if doesNotContainSpecialCharacter(text_plate) == False:
        print("[ERROR] there are special characters")
        return

    plateEntry = {"region": "", "number": "", "string": ""}

    i = 0

    # ----- extracting the county from the string -----
    if text_plate[i + 1].isdigit():

        if text_plate[i] == 'B':
            # cazul bucuresti -- citesti un singur caracter pentru judet
            plateEntry['region'] = text_plate[i]

        else:
            print("[ERROR] nu merge frate")
            return

    else:
        # citesti 2 caractere pentru judet 
        plateEntry['region'] = f"{text_plate[i]}{text_plate[i + 1]}"
        i = i + 1

    i = i + 1

    # ----- extracting the number from the string -----
    if text_plate[i].isalpha() or text_plate[i + 1].isalpha():
        print("[ERROR] you can't have characters for the numbers")
        return

    plateEntry['number'] = f"{text_plate[i]}{text_plate[i + 1]}"
    i = i + 2

    if text_plate[i].isdigit():
        plateEntry['number'] = f"{plateEntry['number']}{text_plate[i]}"
        i = i + 1

    # ----- extracting the plate string from the string -----
    if text_plate[i].isdigit() or text_plate[i + 1].isdigit() or text_plate[i + 2].isdigit():
        print("[ERROR] you can't have characters for the numbers")
        return

    if i < len(text_plate) - 2:
        print("[ERROR] not small enough character")
        return

    plateEntry['string'] = f"{text_plate[i]}{text_plate[i + 1]}{text_plate[i + 2]}"

    # ----- checking if the county extracted from the plate is valid -----
    if isValidCounty(plateEntry['region']) == False:
        print("[ERROR] the county format is not valid")
        return

    print(plateEntry)


if __name__ == "__main__":
    # ----- testing some scenarios -----
    print(verifyPlateFormat("B767  NTT"))
    # print(verifyPlateFormat("0M17NTT"))
    # print(verifyPlateFormat("TM162NTT"))
    # print(verifyPlateFormat("Bm162NTT"))
    # print(verifyPlateFormat("B162NTT"))
