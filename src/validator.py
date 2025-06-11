
class RomanianLicensePlateValidator:
    def __init__(self):
        
        self.county_prefixes =["AB", "AR", "AG", "BC", "BH", "BN", "BT", "BV", "BR","B",
            "BZ","CS", "CL", "CJ", "CT", "CV","DB","DJ", "GL", "GR", "GJ", 
            "HR", "HD", "IL", "IS", "IF", "MM", 
            "MH", "MS", "NT", "OT", "PH", "SM", "SJ",
            "SB", "SV", "TR", "TM", "TL", "VS", "VL", "VN"]
            
        self.special_prefixes = {"A", "FA", "ALA", "MAI"}
        self.diplomatic_prefixes= {"CD", "TC", "CO"}
        
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
           
            return False
           
        elif "Q" in string_in_plate:
            return False
            
        elif string_in_plate=="III" or  string_in_plate=="OOO":
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


    def GetFirstCharacters(self, plate, plate_index):
        result = ""

        for character in plate:
            if character.isdigit():
                break
            result += character
            plate_index += 1

        return result, plate_index
        
        
    def GetDigits(self, plate, plate_index):
        result = ""

        for index in range(plate_index, len(plate)):
            if not plate[index].isdigit():
                break
            result += plate[index]
            plate_index += 1

        return result, plate_index


    def getLastDigits(self,plate,plate_index):
        result=""
        
        for index in range(plate_index, len(plate)):
            if plate[index].isdigit():
                break
                
            result += plate[index]
            plate_index += 1
        
        return result, plate_index
    
    
    
    
    
    def CheckDiplomaticPlate(self,diplomatic_numbers,letters):
        '''
        This verifies if the diplomatic plate numbers follow the rules and there are no letters after the digits
        '''
        length=len(diplomatic_numbers)
        if length == 6 and diplomatic_numbers.isdigit() and int(diplomatic_numbers[0:3])>=101 and int(diplomatic_numbers[3:6])>=101 and letters=="":
            return True
        else:
            return False
    
    def CheckSpecialPlate(self,special_plate_numbers, letters):
        '''
        This verifies if the diplomatic plate numbers follow the rules and there are no letters after the digits
        '''
        
        length=len(special_plate_numbers)
        if length >= 3 and length<=7 and special_plate_numbers.isdigit() and letters=="":
            return True
        else: 
            return False      
            
            
            
            
    def CheckRegularPlate(self,county,number,letters):
        '''
        This verifies if the regular plates follow the template of temporary or permanent plates from bucharest and other counties
        '''
        if len(number) >= 4 and len(number)<=6 and number[0]=="0" and number[len(number)-1]!="0" and letters=="" :#Temporary plates
            return True
        elif(county=="B" and len(number) >= 2 and len(number)<=3 and len(letters)==3):#Bucharest Plates
            if(self.isValid3LetterString(letters)==True):
                return True
        elif(county!="B"and len(county)==2 and len(number) ==2  and len(letters)==3 ):#Other county permanent plates
            if(self.isValid3LetterString(letters)==True):
                return True
            
        else: return False    
        
        
        
        
        
        
        
        
                
#----------MAIN VERIFICATION FUNCTION FOR ROMANIAN PLATES-------


    def verifyPlateFormat(self, text_plate):
        
        
        
        
        # ----- removing all spaces from the input string -----
        text_plate = self.removeSpacesFromString(text_plate)

        # ----- checking if there is any lowercase letters -----
        if not self.isUpperCase(text_plate):
            return False

            # ----- checking if there are special characters -----
        if not self.doesNotContainSpecialCharacter(text_plate):
           return False


     
        '''
        FROM NOW ON, elements in variable platEntry will contain(if number is detected correctly) the 2/3 blocks of strings from a plate
        If number is not detected correctly, error is catched in the next steps
        
        '''
        
        
        
        plate_index = 0
        prefix=""
        numbers=""
        lastLetters=""
        
        prefix, plate_index = self.GetFirstCharacters(text_plate, plate_index)
        numbers, plate_index = self.GetDigits(text_plate, plate_index)
        lastLetters,plate_index=self.getLastDigits(text_plate,plate_index)
        
        if self.isValidCounty(prefix) or self.isValidSpecialPlate(prefix) or self.isValidDiplomaticPlate:
            
            
            
            if self.isValidSpecialPlate(prefix):
                return self.CheckSpecialPlate(numbers,lastLetters)
            elif self.isValidDiplomaticPlate(prefix):
                return self.CheckDiplomaticPlate(numbers,lastLetters)
            else:
                return self.CheckRegularPlate(prefix, numbers, lastLetters)
                

        else:
            return False
        
'''  

def main():
        validator = RomanianLicensePlateValidator()

        print(validator.verifyPlateFormat("VN06WWW"))
        # Standard plate
        #print(validator.verifyPlateFormat("MAI1B234"))      # Special plate
        #print(validator.verifyPlateFormat("CD123156"))    # Correct Diplomatic plate 
        #print(validator.verifyPlateFormat("CD123156"))    # Inorrect Diplomatic plate 
        #print(validator.verifyPlateFormat("CD12A156"))    # Inorrect Diplomatic plate 
        #print(validator.verifyPlateFormat("CJ0567"))      # Temporary plate
        

    


if __name__ == "__main__":
    main()
    '''
        

    



    
