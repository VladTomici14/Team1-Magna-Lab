This file contains details about license plate fromat in Romania

------------------------------REGULAR PLATES----------------------------------

PREFIX:
County prefix must be from the following list:
B, AB, AG, AR, BC, BH, BN, BR, BT, BV, BZ, CJ, CL, CS, CT, CV, 
DB, DJ, GJ, GL, GR, HD, HR, IF, IL, IS, MH, MM, MS, NT, OT, PH, 
SB, SJ, SM, SV, TL, TM, TR, VL, VN, VS;

Bucharest ("B") must be treated separatly.

DIGITS:
The next digits array must contain two digits, with the exception for Bucharest, 
where numberplates with 3 digits can be found

3 LETTER ARRAY

CANNOT contain letter 'Q'
CANNOT start with 'I' or 'O'
CANNOT be "OOO" or "III"


------------------------------TEMPORARY----------------------------------
PREFIX:
County prefix must be from the following list:
B, AB, AG, AR, BC, BH, BN, BR, BT, BV, BZ, CJ, CL, CS, CT, CV, 
DB, DJ, GJ, GL, GR, HD, HR, IF, IL, IS, MH, MM, MS, NT, OT, PH, 
SB, SJ, SM, SV, TL, TM, TR, VL, VN, VS;

DIGITS:
Digits array must be of length between 3 and 6
First Digit must be 0, and the last digit must NOT be equal to 0
!MUST NOT have letters inside digit array


-----------------------------SPECIAL ORGANIZATIONS-------------------------
PREFIX:
Special organizations prefix must be from the folowing list : A, FA, ALA, MAI

DIGITS:
Digits array must be of length between 3 and 7
!MUST NOT have letters inside digit array


-----------------------------DIPLOMATIC PLATES-------------------------
PREFIX:
Special organizations prefix must be from the folowing list : CD, TC, CO

DIGITS:
Digits array must be of length 6
The number formed by the first 3 digits and the last 3 digits must be hreater than 101
!MUST NOT have letters inside digit array

