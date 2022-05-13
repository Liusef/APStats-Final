from ipa import ipa
from espeakng import ESpeakNG
import tkinter
import math

class inst():
    def __init__(self, ipa):
        self.ipa = ipa
        self.dist = 0
        self.ici = 0
        self.wsi = 0
        self.nSyl = 0
        self.SpW = 0
        self.DpW = 0
        self.DpS = 0
        self.SPLITCONST =100
        self.freq = []
        for i in range(1201//self.SPLITCONST + 1):
            self.freq.append(0)
        self.every = []
        self.eavg = []
        self.eavgn = 0
        self.eavgs = 0
        self.liveeavg = 0


    def reset(self):
        self.dist = 0
        self.wsi = 0
        self.nSyl = 0
        self.SpW = 0
        self.DpW = 0
        self.DpS = 0
        for i in range(len(self.freq)):
            self.freq[i] = 0
        self.every = []
        self.eavg = []
        self.eavgn = 0
        self.eavgs = 0
        self.liveeavg = 0


    def printSDM(self, lst):
        i = 0
        for j in range(len(self.freq)):
            print("{} - {}: {}".format(j * self.SPLITCONST, j * self.SPLITCONST + self.SPLITCONST, self.freq[j]))

        