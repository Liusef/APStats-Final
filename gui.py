from tkinter import *
from tkinter import scrolledtext as tkst
import time
import math
import string
from inst import inst
from ipa import ipa
import csv

class gui():
    def __init__(self, instvar):
        print("The GUI Window should open soon! Sometimes it opens in the background, so check your taskbar for any new windows.")
        self.inst = instvar
        self.initInst = instvar
        self.bStr = ''
        self.wdist = 0
        self.adist = 0
        self.worddist = 0

        self.inc = 0
        self.speed = 2
        self.tx = None
        self.ty = None
        self.ox = None
        self.oy = None
        self.dx = 0
        self.dy = 0
        self.every = []

        self.fps = 120
        self.mainDelay = 1000 // self.fps
        self.dl = self.mainDelay

        self.mwx = 950
        self.mwy = 420

        self.root = Tk()
        self.rootConfig(self.mwx, self.mwy, "#FFFFFF")

        self.setSectors()
        self.createButtons()
        self.createLabels()
        ipaImg = PhotoImage(file="ipa.png")
        self.ipaWin.create_image(0, 0, image=ipaImg, anchor=NW)
        self.id = self.ipaWin.create_oval(20, 60, 40, 80, fill='cyan')

        self.root.mainloop()

    def rootConfig(self, x, y, bg):
        self.root.geometry("{}x{}".format(x, y))
        # self.root.configure(bg=bg)
        #self.root.resizable(False, False)

    def setSectors(self):
        self.ipaWin = Canvas(self.root, width=2 * self.mwx // 3, height=self.mwy/2, bg="#FFFFFF", bd=2, relief="groove")
        self.ipaWin.place(anchor=NE, x=2 * self.mwx // 3, y=0, width = 2 * self.mwx // 3, height = self.mwy)
        self.txtWin = tkst.ScrolledText(self.root, width = 28, height = 9, bd = 2, relief = 'groove', wrap=WORD)
        self.txtWin.place(anchor=NW, x = 2 * self.mwx // 3, width = self.mwx // 3, height = 2 * self.mwy // 5 - 7)
        self.txtWin.insert(INSERT, self.inst.ipa.inStr)
        self.txtWin.config(state=DISABLED)
        # self.lWin = Canvas(self.root, width = self.mwx //3, height = self.mwy//2, bg = "#44daff", bd = 0)
        # self.lWin.place(anchor=NW, x = 2 * self.mwx // 3, y = 2 * self.mwy // 5, width = self.mwx // 3, height = 3 * self.mwy // 5)
        # self.placeholder = Canvas(self.root, width = 1, height = self.mwy)
        # self.placeholder.grid(row = 0, column = 3, rowspan = 2,  sticky = 'nsew')

        # self.txtWin = Canvas(self.root, width)

    def createButtons(self):
        self.sb = Button(self.root, text="Start", command=self.start)
        self.sb.place(height = 24, width = 40, x = 2 * self.mwx // 3, y = self.mwy - 24)
        self.readFile = IntVar(self.root, 1)
        self.rFCb = Checkbutton(self.root, text = 'Read File?', variable=self.readFile, onvalue = 1, offvalue = 0, command=self.updateRF)
        self.rFCb.place(height = 24, width=90, x = 2 * self.mwx // 3 + 40, y = self.mwy - 24)
        self.readbox = Button(self.root, text = 'Read txtBox', command=self.readTxtBox)
        self.readbox.place(height=24, width=90, x = 2 * self.mwx // 3 + 130, y = self.mwy - 24)
        Label(self.root, text = "Speed (1 - 31): ").place(x = 650, y = 181)
        self.spSlider = Scale(self.root, from_=1, to=31, orient=HORIZONTAL)
        self.spSlider.place(x=750, y=160)
        self.writeCSV = Button(self.root, text = 'Write CSV', command = self.csv)
        self.writeCSV.place(height = 24, width = 90, x = 2 * self.mwx // 3 + 220, y = self.mwy - 24)
        self.writeCSV['state'] = DISABLED
        self.updateRF()

    def createLabels(self):
        top = 200
        self.status = Label(self.root, text = "Status: Stopped\tLang: {}".format(self.inst.ipa.lang), justify = LEFT)
        self.status.place(x = 650, y = top + 24 * 0 + 3)
        self.distC = Label(self.root, text = "Distance: {}".format(self.inst.dist))
        self.distC.place(x = 650, y = top + 24 * 1)
        self.cWordi = Label(self.root, text = "Words Processed Index: {}".format(self.inst.wsi), justify=LEFT)
        self.cWordi.place(x = 650, y = top + 24 * 2)
        self.cWord = Label(self.root, text = 'Current Word: "{}"'.format(self.inst.ipa.strList[self.inst.wsi]))
        self.cWord.place(x = 650, y = top + 24 * 3)
        self.nSyl = Label(self.root, text = "Syllables Processed*: {}".format(self.inst.nSyl))
        self.nSyl.place(x = 650, y = top + 24 * 4)
        self.DpW = Label(self.root, text = "Avg Distance per Word: {}".format(self.inst.DpW))
        self.DpW.place(x = 650, y = top + 24 * 5)
        self.DpS = Label(self.root, text = "Mean of Avg Dist per Syl per Word: {}".format(self.inst.liveeavg))
        self.DpS.place(x = 650, y = top + 24 * 6)
        # self.std = Label(self.root, text="Standard Deviation: Not Available Yet")
        # self.std.place(x=650, y=top + 24 * 7)

    def started(self):
        self.status.configure(text = "Status: Running\tLang: {}".format(self.inst.ipa.lang))
        self.status.update()

    def stopped(self):
        self.status.configure(text = "Status: Stopped\tLang: {}".format(self.inst.ipa.lang))
        self.status.update()
        
    def loading(self):
        self.status.configure(text="Status: Loading\tLang: {}".format(self.inst.ipa.lang))
        self.status.update()

    def getSpeed(self):
        return self.spSlider.get()

    def updateLabels(self):
        self.inst.SpW = self.inst.nSyl / (self.inst.wsi + 1)
        self.inst.DpW = self.inst.dist / (self.inst.wsi + 1)
        self.inst.dist = round(self.inst.dist, 3)
        self.wdist = round(self.wdist, 3)
        self.inst.SpW = round(self.inst.SpW, 3)
        self.inst.DpW = round(self.inst.DpW, 3)
        self.inst.liveeavg = self.inst.eavgs / (self.inst.wsi + 1)
        # self.inst.DpS = round(self.inst.DpS, 3)
        self.distC.configure(text = "Distance: {}".format(self.inst.dist))
        self.distC.update()
        self.cWordi.configure(text = "Words Processed Index: {}".format(self.inst.wsi))
        self.cWordi.update()
        try:
            self.cWord.configure(text = 'Current Word: "{}"'.format(self.inst.ipa.strList[self.inst.wsi]))
            self.cWord.update()
        except: pass
        self.nSyl.configure(text = "Syllables Processed*: {}".format(self.inst.nSyl))
        self.nSyl.update()
        self.DpW.configure( text = "Mean Distance per Word: {}".format(self.inst.DpW))
        self.DpW.update()
        self.DpS.configure(text = "Mean of Avg Dist per Syl per Word: {}".format(self.inst.liveeavg))
        self.DpS.update()

    def disableButtons(self):
        self.sb['state']=DISABLED
        self.rFCb['state']=DISABLED
        self.readbox['state']=DISABLED

    def enableButtons(self):
        self.sb['state'] = NORMAL
        self.rFCb['state'] = NORMAL
        self.readbox['state'] = NORMAL

    def updateRF(self):
        if self.readFile.get() == 1:
            if self.inc != 0:
                try:
                    self.loading()
                except:
                  pass
                self.sb['state'] = NORMAL
                file = open(self.inst.ipa.lang[0:2] + ".txt", encoding='utf-8')
                s = file.read()
                if len(s) > 30000:
                    cannb = []
                    for i in range(len(s) // 30000 + 1):
                        cannb.append(s[30000 * i:30000 * (i + 1)])
                    cannb_ipa = []
                    for i in cannb:
                        cannb_ipa.append(ipa(i, self.inst.ipa.lang))
                    f = cannb_ipa[0]
                    for i in range(1, len(cannb_ipa)):
                        f += cannb_ipa[i]
                else:
                    f = ipa(s, self.inst.ipa.lang)
                self.inst = inst(f)
            self.inc += 1
            self.txtWin.delete(1.0, END)
            self.txtWin.insert(INSERT, self.inst.ipa.inStr)
            self.txtWin.configure(state=DISABLED)
            self.readbox['state'] = DISABLED
        else:
            self.sb['state'] = DISABLED
            self.txtWin.configure(state=NORMAL)
            self.txtWin.delete(1.0, END)
            self.readbox['state'] = NORMAL
        try:
            self.stopped()
        except:
            pass

    def readTxtBox(self):
        self.sb['state'] = NORMAL
        self.bStr = self.txtWin.get("1.0", END)
        self.inst = inst(ipa(self.bStr, self.inst.ipa.lang))

    def avg(self, a, b):
        return ((a + b)/2)

    def pyt(self, a, b):
        return math.sqrt(a**2 + b**2)

    def dist(self):
        return self.pyt(self.dx, self.dy)

    def getTarget(self, c):
        c1 = ['i', 'y', 'ɨ', 'ʉ', 'ɯ', 'u',
              'ɪ', 'ʏ', 'ʊ',
              'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o',
              'ə',
              'ɛ', 'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ',
              'æ', 'a',
              'ɐ', 'ɶ', 'ä', 'ɑ', 'ɒ',
              'ɚ', 'ɹ', 'ᵻ']
        c2 = [(37, 22), (37, 22), (293, 22), (293, 22), (549, 22), (549, 22),
              (187, 82), (187, 82), (437, 82),
              (123, 141), (123, 141), (336, 141), (336, 141), (549, 141), (549, 141),
              (358, 206),
              (208, 260), (208, 260), (378, 260), (378, 260), (549, 260), (549, 260),
              (251, 320), (402, 320),
              (293, 379), (293, 379), (293, 379), (549, 379), (549, 379),
              (549, 22), (549, 22), (358, 206)]
        i = c1.index(c)
        return c2[i]

    def getStDev(self, mean, dlst, n):
        sgma = 0
        for i in dlst:
            sgma += (i - mean)**2
        try:
            sgma /= (n-1 + 1)
        except:
            return None
        sgma = math.sqrt(sgma)
        return sgma

    def csv(self):
        with open("csv.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.inst.eavg)
            writer.writerow(self.inst.ipa.strList)
            print("Done! CSV written to csv.csv")

    def start(self):
        # self.std.configure(text="Standard Deviation: Not Available Yet")
        self.inst.reset()
        self.writeCSV['state'] = DISABLED
        self.sb['state'] = DISABLED
        self.started()
        self.worddist = 0

        self.idCoords = self.ipaWin.coords(self.id)
        self.ipaWin.move(self.id, self.getTarget('ə')[0] - self.avg(self.idCoords[0], self.idCoords[2]), self.getTarget('ə')[1] - self.avg(self.idCoords[1], self.idCoords[3]))

        # for c in self.inst.ipa.ipaVowelStr:
        #     self.speed = self.getSpeed()
        #     if self.speed == 31:
        #         self.speed = 30
        #         self.dl = 0
        #     else: self.dl = self.mainDelay
        #
        #     if c == " ":
        #         if (self.inst.wsi < len(self.inst.ipa.strList) - 1):
        #             self.inst.every.append(self.worddist)
        #             self.inst.eavg.append(self.inst.every[self.inst.wsi] / self.inst.ipa.sylList[self.inst.wsi])
        #             self.inst.eavgs += self.inst.eavg[self.inst.wsi]
        #             self.inst.nSyl += self.inst.ipa.sylList[self.inst.wsi]
        #             self.inst.freq[int(self.inst.eavg[self.inst.wsi] // self.inst.SPLITCONST)] += 1
        #             if(self.inst.eavg[self.inst.wsi] > 1125):
        #                 print(str(self.inst.wsi), self.inst.ipa.strList[self.inst.wsi])
        #             self.inst.wsi += 1
        #             self.worddist = 0
        #     else:
        #         self.tx, self.ty = self.getTarget(c)
        #         self.idCoords = self.ipaWin.coords(self.id)
        #         self.ox = self.avg(self.idCoords[0], self.idCoords[2])
        #         self.oy = self.avg(self.idCoords[1], self.idCoords[3])
        #         self.dx = 4 * self.speed * (self.tx - self.ox) / self.fps
        #         self.dy = 4 * self.speed * (self.ty - self.oy) / self.fps
        #
        #         for i in range(int(1/(4 * self.speed/self.fps))):
        #             self.ipaWin.after(self.dl, self.ipaWin.move(self.id, self.dx, self.dy))
        #             self.ipaWin.update()
        #             self.inst.dist += self.pyt(self.dx, self.dy)
        #             self.wdist += self.pyt(self.dx, self.dy)
        #             self.updateLabels()
        #
        #         cannb = self.ipaWin.coords(self.id)
        #         self.ipaWin.move(self.id, self.tx - self.avg(cannb[0], cannb[2]), self.ty - self.avg(cannb[1], cannb[3]))
        #         self.inst.dist += self.pyt(self.tx - self.avg(cannb[0], cannb[2]), self.ty - self.avg(cannb[1], cannb[3]))
        #         self.wdist += self.pyt(self.tx - self.avg(cannb[0], cannb[2]), self.ty - self.avg(cannb[1], cannb[3]))
        #         self.adist = self.pyt((self.tx-self.ox), (self.ty - self.oy))
        #         self.worddist += self.adist
        #         self.inst.dist -= self.wdist
        #         self.inst.dist += self.adist
        #         self.updateLabels()
        #         self.wdist = 0
        #         self.adist = 0

        for s in self.inst.ipa.ipaVowelList:
            self.speed = self.getSpeed()
            if self.speed == 31:
                self.speed = 30
                self.dl = 0
            else:
                self.dl = self.mainDelay
            for c in s:
                self.tx, self.ty = self.getTarget(c)
                self.idCoords = self.ipaWin.coords(self.id)
                self.ox = self.avg(self.idCoords[0], self.idCoords[2])
                self.oy = self.avg(self.idCoords[1], self.idCoords[3])
                self.dx = 4 * self.speed * (self.tx - self.ox) / self.fps
                self.dy = 4 * self.speed * (self.ty - self.oy) / self.fps

                for i in range(int(1 / (4 * self.speed / self.fps))):
                    self.ipaWin.after(self.dl, self.ipaWin.move(self.id, self.dx, self.dy))
                    self.ipaWin.update()
                    self.inst.dist += self.pyt(self.dx, self.dy)
                    self.wdist += self.pyt(self.dx, self.dy)
                    self.updateLabels()

                cannb = self.ipaWin.coords(self.id)
                self.ipaWin.move(self.id, self.tx - self.avg(cannb[0], cannb[2]), self.ty - self.avg(cannb[1], cannb[3]))
                self.inst.dist += self.pyt(self.tx - self.avg(cannb[0], cannb[2]), self.ty - self.avg(cannb[1], cannb[3]))
                self.wdist += self.pyt(self.tx - self.avg(cannb[0], cannb[2]), self.ty - self.avg(cannb[1], cannb[3]))
                self.adist = self.pyt((self.tx-self.ox), (self.ty - self.oy))
                self.worddist += self.adist
                self.inst.dist -= self.wdist
                self.inst.dist += self.adist
                self.updateLabels()
                self.wdist = 0
                self.adist = 0

            self.inst.every.append(self.worddist)
            try:
                self.inst.eavg.append(self.inst.every[self.inst.wsi] / self.inst.ipa.sylList[self.inst.wsi])
            except: pass
            self.inst.eavgs += self.inst.eavg[self.inst.wsi]
            self.inst.nSyl += self.inst.ipa.sylList[self.inst.wsi]
            self.inst.freq[int(self.inst.eavg[self.inst.wsi] // self.inst.SPLITCONST)] += 1
            if(self.inst.eavg[self.inst.wsi] > 1125):
                print(str(self.inst.wsi), self.inst.ipa.strList[self.inst.wsi])
            self.inst.wsi += 1
            self.worddist = 0

        self.inst.wsi = len(self.inst.ipa.strList) - 1
        self.updateLabels()
        # self.std.configure(text = "Standard Deviation: {}".format(self.getStDev(self.inst.DpS, self.inst.eavg, self.inst.wsi)))
        self.inst.printSDM(self.inst.freq)
        self.writeCSV['state'] = NORMAL
        self.sb['state'] = NORMAL
        self.stopped()


