from ipa import ipa
from inst import inst
from gui import gui
import tkinter
from espeakng import ESpeakNG


IPAVowels = ['i', 'y', 'ɨ', 'ʉ', 'ɯ', 'u', 'ɪ', 'ʏ', 'ʊ', 'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o', 'ə', 'ɛ', 'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ', 'æ', 'ɐ', 'a', 'ɶ', 'a͡', 'ɑ', 'ɒ']
NasalVowels = ['ĩ', 'ỹ', 'ɨ̃', 'ʉ̃', 'ɯ̃', 'ũ', 'ɪ̃', 'ʏ̃', 'ʊ̃', 'ẽ', 'ø̃', 'ɘ̃', 'ɵ̃', 'ɤ̃', 'õ', 'ə̃', 'ɛ̃', 'œ̃', 'ɜ̃', 'ɞ̃', 'ʌ̃', 'ɔ̃', 'æ̃', 'ɐ̃', 'ã', 'ɶ̃', 'ã͡', 'ɑ̃', 'ɒ̃']
# OtherStuff
punc = ['.', ',', ':', ';']

def main():
    print()
    #i dunno man just put whatever u wanna test here ig
    # ipaWordTestEn()
    # print()
    # ipaWordTestFr()
    # print()
    # literallyARandomTest()
    ipaWordTestEn()


#Testing english pronunciation of stuff with streeeengs
def testEng(p=True):
    #inputStr is the only variable you really need to change
    inputStr = '''
    1 
TO THE RED COUNTRY and part of the gray country of Oklahoma
    '''
    inputStr = fixPunc(inputStr)
    esn = ESpeakNG()
    esn.voice = 'en-us'
    ipaStr = esn.g2p(inputStr, 2)
    if(p): print(ipaStr)
    return ipaStr

def testFr(p=True):
    #inputStr is the only variable you really need to change
    inputStr = '''
    « Le Mur » se situe en Espagne à l’époque de la guerre civile.  Trois hommes arrêtés par des franquistes sont 
    interrogés dans la salle d’un hôpital, puis amenés dans la cave de l’hôpital qui leur sert de cellule.  Les gardiens
     annoncent qu’ils sont condamnés à mort et qu'ils seront fusillés le lendemain matin. 
    '''
    inputStr = fixFrenchSpecialCharacters(inputStr)
    inputStr = fixPunc(inputStr)
    esn = ESpeakNG()
    esn.voice = 'fr'
    ipaStr = esn.g2p(inputStr, 2)
    if p: print(ipaStr)
    return ipaStr

def cleanFr(p=True):
    ipaStr = testFr(False)
    weirdShit1 = "(͡e͡n)"
    weirdShit2 = "(͡f͡r)"
    ipaStr = ipaStr.replace(weirdShit1, '')
    ipaStr = ipaStr.replace(weirdShit2, '')
    if p: print(ipaStr)
    return ipaStr

def testSpChars():
    inputStr = 'ÁÀĂÄÃÅĀĄÇœ'
    print(inputStr.lower())
    print(inputStr.upper())

def fixFrenchSpecialCharacters(str, p=True):
    spChar = ['à', 'â', 'ä', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'î', 'ï', 'ô', 'œ', 'ù', 'û', 'ü']
    stChar = ['a', 'a', 'a', 'ae', 's', 'e', 'eh', 'e', 'e', 'i', 'i', 'o', 'œ', 'u', 'u', 'u']
    for i in range(len(spChar)):
        str = str.replace(spChar[i], stChar[i])
    if p: print(str)
    return str

def fixPunc(str, p=True):
    for i in range(len(punc)):
        str = str.replace(punc[i], ' ')
    if p: print(str)
    return str

def ipaWordTestEn():
    inputStr = '''
        1 
TO THE RED COUNTRY and part of the gray country of Oklahoma
        '''
    en = ipa(inputStr, 'en-us')
    en.printAll()

def ipaWordTestFr():
    inputStr = '''
    Un ordinateur à la hauteur de vos ambitions. La Surface la plus puissante à ce jour combine vitesse, performances 
    graphiques et gaming immersif tout en offrant la polyvalence d’un ordinateur, d’une tablette et d’un studio 
    portable. Disponible en version 13,5" ou 15", toutes deux équipées d’un écran tactile haute résolution.'''
    fr = ipa(inputStr, 'fr')
    fr.printAll()

def literallyARandomTest():
    inpt = "<enter text for testing here>"
    lang = 'en-us'
    a = ipa(inpt, lang)
    a.printAll()

def runGui():
    gay1 = ipa('''sample text
        ''', "en-us")
    gay1.printAll()
    gay2 = inst(gay1)
    gui(gay2)


#just like don't touch
main()