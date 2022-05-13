from espeakng import ESpeakNG
from ipa import ipa
from inst import inst
from gui import gui

def main():
    run()

def run():
    print('''Enter Language Setting:
    ================================
    0: American English (en-us)
    1: British English (en)
    2: French French (fr)
    ================================
    ''')

    vi = ['0', '1', '2']
    l = ['en-us', 'en', 'fr']

    while(True):
        a = input("Enter input: ")
        a = a.strip()
        if a in vi:
            print('Launching Program...')
            if (a == '0' or a == '1'):
                file = open('en.txt', encoding='utf-8')
                s = file.read()
                if len(s) > 30000:
                    cannb = []
                    for i in range(len(s)//30000 + 1):
                        cannb.append(s[30000 * i:30000 * (i + 1)])
                    cannb_ipa = []
                    for i in cannb:
                        cannb_ipa.append(ipa(i, l[int(a)]))
                    f = cannb_ipa[0]
                    for i in range(1, len(cannb_ipa)):
                        f += cannb_ipa[i]
                else:
                    f = ipa(s, l[int(a)])
                ff = inst(f)
                gui(ff)
            if (a == '2'):
                file = open('fr.txt', encoding='utf-8')
                s = file.read()
                if len(s) > 30000:
                    cannb = []
                    for i in range(len(s) // 30000 + 1):
                        cannb.append(s[30000 * i:30000 * (i + 1)])
                    cannb_ipa = []
                    for i in cannb:
                        cannb_ipa.append(ipa(i, l[int(a)]))
                    f = cannb_ipa[0]
                    for i in range(1, len(cannb_ipa)):
                        f += cannb_ipa[i]
                else:
                    f = ipa(s, l[int(a)])
                ff = inst(f)
                gui(ff)
            break
        else:
            print("invalid input.")


if __name__ == '__main__':
    main()