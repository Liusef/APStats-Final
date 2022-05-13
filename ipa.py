from espeakng import ESpeakNG

IPAVowels = ['i', 'y', 'ɨ', 'ʉ', 'ɯ', 'u', 'ɪ', 'ʏ', 'ʊ', 'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o', 'ə', 'ɛ', 'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ', 'æ', 'a', 'ɐ', 'ɶ', 'ä', 'ɑ', 'ɒ']
NasalVowels = ['ĩ', 'ỹ', 'ɨ̃', 'ʉ̃', 'ɯ̃', 'ũ', 'ɪ̃', 'ʏ̃', 'ʊ̃', 'ẽ', 'ø̃', 'ɘ̃', 'ɵ̃', 'ɤ̃', 'õ', 'ə̃', 'ɛ̃', 'œ̃', 'ɜ̃', 'ɞ̃', 'ʌ̃', 'ɔ̃', 'æ̃', 'ã', 'ɐ̃', 'ɶ̃', 'ä̃', 'ɑ̃', 'ɒ̃']
IPAOther = ['ɚ', 'ɹ', 'ᵻ']
spChar = ['à', 'â', 'ä', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'î', 'ï', 'ô', 'œ', 'ù', 'û', 'ü']
stChar = ['a', 'a', 'a', 'ae', 's', 'e', 'eh', 'e', 'e', 'i', 'i', 'o', 'œ', 'u', 'u', 'u']
punc = ['. ', ', ', ':', ';', '...', '».', '«',  '»', '"', '[', ']', '—', '!', '?', '“', '”']
ws = [' ', '\n', '\t']

class ipa():
    def noSpChar(self, str):
        for i in range(len(spChar)):
            str = str.replace(spChar[i], stChar[i])
        return str

    def noPunc(self, str):
        str = str.strip()
        for i in range(len(punc)):
            str = str.replace(punc[i], ' ')
        for i in range(1, len(ws)):
            str = str.replace(ws[i], ' ')
        str = str.strip()
        for idx in range(len(str)):
            try:
                str[idx]
            except: break
            if str[idx] == ' ':
                i = 0
                while True:
                    if (str[idx + i + 1] == ' '):
                        i += 1
                    else:
                        if (i == 0):
                            break
                        else:
                            str = str[0:idx] + str[idx + i:]
                            break
        # str = str.replace("  ", ' ')
        # str = str.replace("   ", ' ')
        # str = str.replace("     ", " ")
        return str

    def convIpa(self, str):
        str = str.lower()
        rs = self.e.g2p(str, 2)
        for s in ["(͡e͡n)", "(͡f͡r)", '͡']:
            rs = rs.replace(s, '')
        return(rs)

    def noNasal(self, str):
        for i in range(len(NasalVowels)):
            str = str.replace(NasalVowels[i], IPAVowels[i])
        str = str.replace("iɪn", "i ɪn")
        return str

    def vowels(self, str):
        rStr = ''
        for c in str:
            if (c in IPAVowels or c in ws or c in IPAOther):
                rStr += c
        return rStr

    def convList(self, str):
        str = str.lower()
        str = str.replace('\n', ' ')
        str = str.replace('\t', ' ')
        str = str.strip()
        # self.ar = ["on the", "in the", "of the", "for a", "that the", 'did not', 'of a', 'parce que']
        # self.br = ["onthe", "inthe", "ofthe", "fora", "thatthe", 'didnot', 'ofa', 'parceque']
        # self.cr = ["onthe", "inthe", "ofthe", "fora", "thatthe", 'didnot', 'ofa']
        # for i in range(len(self.ar)):
        #     str = str.replace(self.ar[i], self.br[i])
        lst = str.split()
        for i in range(len(lst)):
            lst[i].replace(' ', '')
        return lst

    def wordSyllables(self, word):
        count = 0
        vowels = 'aeiouy'
        word = word.lower().strip('.:;?!"')
        # if word in self.cr:
        #     count += 1
        try:
            a = word[0]
        except:
            return 0
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in '12345689':
                count += 1
            elif word[index] in '70':
                count += 2
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count += 1
        if count == 0:
            count += 1
        return count

    def syllables(self, lst):
        sylLst = []
        for i in lst:
            sylLst.append(self.wordSyllables(i))
        return sylLst

    def printAll(self):
        print(self.lang)
        print()
        print(self.inStr)
        print()
        print(self.nSPChar)
        print()
        print(self.nPuncStr)
        print()
        # print(self.ipaStr)
        # print()
        # print(self.ipaNNStr)
        # print()
        # print(self.ipaVowelStr)
        print()
        print(self.strList)
        print()
        print(self.sylList)
        print()

    def __init__(self, str, language):
        self.inStr = str
        self.lang = language
        self.e = ESpeakNG()
        self.e.voice = self.lang


        self.nSPChar = self.noSpChar(self.inStr)
        self.nPuncStr = self.noPunc(self.nSPChar)
        # self.ipaStr = self.convIpa(self.nPuncStr)
        # self.ipaNNStr = self.noNasal(self.ipaStr)
        # self.ipaVowelStr = self.vowels(self.ipaNNStr)

        self.strList = self.convList(self.noPunc(self.inStr))
        self.sylList = self.syllables(self.strList)
        self.ipaList = []
        for i in self.strList:
            self.ipaList.append(self.noNasal(self.convIpa(i).replace(" ", "")))
        self.ipaVowelList = []
        for i in self.ipaList:
            self.ipaVowelList.append(self.vowels(i))


    def __add__(self, other):
        self.inStr += " " + other.inStr
        self.nSPChar += " " + other.nSPChar
        self.nPuncStr += " " + other.nPuncStr
        # self.ipaStr += " " + other.ipaStr
        # self.ipaNNStr += " " + other.ipaNNStr
        # self.ipaVowelStr += " " + other.ipaVowelStr
        self.strList.extend(other.strList)
        self.sylList.extend(other.sylList)
        self.ipaList.extend(other.ipaList)
        self.ipaVowelList.extend(other.ipaVowelList)
        return self

# Documentation!!!!
#
# This class is for the text that user wants to input into the thingy
# The user can input text and a desired language and when the object is created, the class will automatically parse the
#     string into the necessary components.
#
# Notes:
#     1.  Currently only has compatibility with 3 languages (en, en-us, fr)
#
# Object Variables:
#     User Inputs
#     (str) self.inStr:       string that the user input into the object
#     (str) self.lang:        desired language for parsing (yes this matters) (refer to Notes:1)
#
#     All remaining variables are automatically generated when the object is created
#     (str) self.nSPChar:     the user string, but with many special characters that ESpeakNG cannot parse (listed in
#                             spChar), replaced with standard characters (listed in stChar, indexes correspond)
#     (str) self.nPuncStr:    the user string, but with afore mentioned special characters replaced, and some punctuation
#                             removed (listed in punc)
#     (str) self.ipaStr:      self.nPuncStr converted into IPA (Internation Phonetic Alphabet) script in their respective
#                             language in self.lang
#     (str) self.ipaNNStr:    self.ipaStr except with nasal vowel designations (~) replaced with standard vowels
#                             (replaced items listed in NasalVowels and IPAVowels)
#     (str) self.ipaVowelStr: self.ipaNNStr except all characters except characters listed as vowels or as other IPA
#                             characters that significantly affect tongue position (listed in IPAVowels and IPAOther)
#     (list) strList:         a list where each element is a group of characters from self.nPuncStr (split by whitespace)
#     (list) sylList:         a list of equal length to strList, where each element is the number of syllables in the word
#                             of the corresponding index in strList
#
# Class Variables:
#     (list) IPAVowels:       A list of vowels listed in the standard IPA Vowel chart
#     (list) NasalVowels:     A list of vowels with the same vowels as IPAVowels in the same positions, but with the IPA
#                             nasal indicator (~)
#     (list) IPAOther:        A list of IPA characters that aren't in the standard IPA Vowels chat but still have a major
#                             effect on tongue position when pronouncing words
#     (list) spChar:          A list of special characters that are common in french and english that ESpeakNG cannot parse
#     (list) stChar:          A list of standard characters that elements in spChar can be replaced by (in corresponding
#                             indexes), so that text can be properly parsed by ESpeakNG
#     (list) punc:            A list of punctuation that ESpeakNG has issues parsing through
#     (list) ws:              A list of common whitespace characters
#
# Class Methods:
#       noSpChar(String str):		Iterates through text in str and replaces any characters that are within spChar
#                                   with the character(s) in stChar with the same index
# 						            String str: string to be parsed and edited
# 						            returns string
#       noPunc(String str):			Iterates through text in str and replaces any characters that are within punc with
#                                   " "
# 						            String str: string to be parsed and edited
# 						            returns string
#       convIpa(String str):		Creates an ESpeakNG wrapper and translates str into IPA script. Some characters that
#                                   are added as a side effect and have no effect on pronunciation will be removed
#                                   (primarily "(͡e͡n)", "(͡f͡r)", '͡')
# 						            String str: string to be translated
# 						            returns string
#       noNasal(String str):		Iterates through str and replaces nasal vowels in NasalVowels with vowels in
#                                   IPAVowels in corresponding index
# 						            String str: string to be parsed and edited
# 						            returns string
#       vowels(String str):			parses through IPA script and adds characters in IPAVowels and IPAOther into a new
#                                   string to be returned
# 						            String str: string to be parsed
# 						            returns string
#       convList(String str):		Splits string into list elements by whitespace
# 						            String str: string to be split
# 						            returns list
#       wordSyllables(String word):	Takes 1 word and approximates integer value of # of syllables in word
# 						            String word: word to be parsed
# 						            returns string
#       syllables(list lst):		Iterates through lst and appends number of syllables in each list element
#                                   (using wordSyllables()) to a new list
# 						            list lst: list with words created by convList
# 						            returns list
#       printAll():				    Prints out values from all object variables
# 						            no inputs
# 						            returns None
