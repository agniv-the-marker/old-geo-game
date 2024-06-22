from tkinter import *
import random

Geo_file = open("GeographyStuff.txt", "r")

f1 = Geo_file.readlines()
GEO_DICT = {}
pics = {}
Country = []
Capital = []
image = []
for x in f1:
    parts = x.split(",")
    Country.append(parts[0])
    Capital.append(parts[1].rstrip())
    image.append(parts[4].rstrip())
for y in range(0,len(Country)-1):
    pics[str(Capital[y])] = str(image[y])
    GEO_DICT[str(Country[y])] = {}
    GEO_DICT[str(Country[y])]["Capital"] = str(Capital[y])
    GEO_DICT[str(Country[y])]["Image"] = "img/"+str(image[y])

class Game():
    def __init__(self, level = 1):
        global correct, wrong
        self.qgenerator = question_generator(GEO_DICT, Country, Capital)
        self.q = []
        self.tries = 0
        self.correct = 0
        self.wrong = 0
        self.level = level
        self.questframe = Frame(root)
        self.questframe.pack()
        self.iframe = Frame(root)
        self.iframe.pack()
        self.bframe = Frame(root)
        self.bframe.pack()
        self.extra = Frame(root)
        self.extra.pack()
        self.score = Label(self.extra)
        self.vari = IntVar()
        self.pictures = []
        self.picpack = []
        self.buttons = []
        self.skip = Button(self.extra)
        self.corAns = ""
        self.ans = Label(self.extra)
        self.alpha = "ABCD"
        self.qlabel = Label(self.questframe)
        self.end = Label(self.extra)
        self.lframe = Frame(root)
        self.lframe.pack()
        self.levels = []
        self.l = IntVar()
        for x in range(3):
            self.levels.append(Radiobutton(self.lframe,
                                           text = "Level "+str(x+1),
                                           variable = self.l,
                                           value = x+1,
                                           command = self.setLevel))
            self.levels[-1].pack(side=LEFT)
        self.l.set(level)

    def setLevel(self):
        self.level = self.l.get()
        self.play()
    
    def play(self):
        self.ans.destroy()
        self.level = self.l.get()
        self.score.destroy()
        self.end.destroy()
        self.skip.destroy()
        self.vari.set(-1)
        self.tries = 0
        self.qlabel.destroy()
        self.q = []
        for b in self.buttons:
            b.destroy()
        self.buttons = []
        for p in self.picpack:
            p.destroy()
        self.picpack = []
        self.pictures = []
        self.score = Label(self.extra, text = "Correct - %s    Wrong - %s" % (self.correct, self.wrong))
        if self.level == 1: # What is the capital of ______ (with names)
            self.generateQuestion()
            self.qlabel = Label(self.questframe, text="What is the capital of " + self.q[0][0]+"?")
            self.qlabel.pack()
            self.generatePictures()
            self.generateButtons()
        elif self.level == 2: # What is the capital of ______ (without names)
            self.generateQuestion()
            self.qlabel = Label(self.questframe, text="What is the capital of " + self.q[0][0]+"?")
            self.qlabel.pack()
            self.generatePictures()
            self.generateABCD()
        elif self.level == 3: # What is this city? (with names)
            self.generateQuestion()
            self.qlabel = Label(self.questframe, text="What is this city?")
            self.qlabel.pack()
            self.generatePicture()
            self.generateButtons()
        self.skip = Button(self.extra, text="Skip", command = self.play)
        self.skip.pack()
        self.score.pack()

    def wrongAns(self):
        self.tries += 1
        self.wrong += 1
        self.buttons[self.vari.get()].destroy()
        if self.level != 3:
            self.picpack[self.vari.get()].destroy()
        if self.tries == 3:
            for b in self.buttons:
                b.destroy()
            self.buttons[0] = Radiobutton(self.bframe,
                        text = self.corAns,
                        indicatoron = 0,
                        width = 20,
                        padx = 70,
                        variable = self.vari,
                        value = 0,
                        state = DISABLED,
                        command = self.correctAns)
            self.buttons[0].pack()
            self.end = Label(self.extra, text = "The correct answer was " + str(self.corAns)+".")
            self.end.pack()
            self.skip.destroy()
            self.skip = Button(self.extra, text = "Next Question?", command = self.play)
            self.skip.pack()
        self.score.destroy()
        self.score = Label(self.extra, text = "Correct - %s    Wrong - %s" % (self.correct, self.wrong))
        self.score.pack()
        
    def correctAns(self):
        self.tries += 1
        self.correct += 1
        for x in range(len(self.buttons)):
            self.buttons[x].destroy()
            if x != self.vari.get() and self.level != 3:
                self.picpack[x].destroy()
            if x == self.vari.get():
                if self.level == 2:
                    self.buttons[x] = (Radiobutton(self.bframe,
                            text = self.corAns,
                            indicatoron = 0,
                            width = 20,
                            padx = 70,
                            variable = self.vari,
                            value = x,
                            state = DISABLED,
                            command = self.correctAns))
                else:
                    self.buttons[x] = (Radiobutton(self.bframe,
                            text = self.corAns,
                            indicatoron = 0,
                            width = 20,
                            padx = 70,
                            variable = self.vari,
                            value = x,
                            state = DISABLED,
                            command = self.correctAns))
                self.buttons[x].pack()
        self.score.destroy()
        self.skip.destroy()
        self.ans.destroy()
        if self.tries == 1:
            self.ans = Label(self.extra, text = "Nice! You got it in " + str(self.tries) + " try!")
        else:
            self.ans = Label(self.extra, text = "Nice! You got it in " + str(self.tries) + " tries!")
        self.tries = 0
        self.ans.pack()
        self.skip = Button(self.extra, text = "Next Question?", command = self.play)
        self.skip.pack()
        self.score = Label(self.extra, text = "Correct - %s    Wrong - %s" % (self.correct, self.wrong))
        self.score.pack()

    def generateABCD(self):
        for x in range(len(self.q[1])):
            if self.q[1][x] == self.corAns:
                self.buttons.append(Radiobutton(self.bframe,
                        text = self.alpha[x],
                        indicatoron = 0,
                        width = 20,
                        padx = 70,
                        variable = self.vari,
                        value = x,
                        command = self.correctAns))
                self.corAns += " ("+self.alpha[x]+")"
            else:
                self.buttons.append(Radiobutton(self.bframe,
                        text = self.alpha[x],
                        indicatoron = 0,
                        width = 20,
                        padx = 70,
                        variable = self.vari,
                        value = x,
                        command = self.wrongAns))
            self.buttons[-1].pack(side=LEFT)

    def generateButtons(self):
        if self.level == 1:
            for x in range(len(self.q[1])):
                if self.q[1][x] == self.corAns:
                    self.buttons.append(Radiobutton(self.bframe,
                            text = self.q[1][x],
                            indicatoron = 0,
                            width = 20,
                            padx = 70,
                            variable = self.vari,
                            value = x,
                            command = self.correctAns))
                else:
                    self.buttons.append(Radiobutton(self.bframe,
                            text = self.q[1][x],
                            indicatoron = 0,
                            width = 20,
                            padx = 70,
                            variable = self.vari,
                            value = x,
                            command = self.wrongAns))
                self.buttons[-1].pack(side=LEFT)
        else:
            for x in range(len(self.q)):
                if self.q[x] == self.corAns:
                    self.buttons.append(Radiobutton(self.bframe,
                                                    text = self.q[x],
                                                    indicatoron = 0,
                                                    width = 20,
                                                    padx = 70,
                                                    variable = self.vari,
                                                    value = x,
                                                    command = self.correctAns))
                else:
                    self.buttons.append(Radiobutton(self.bframe,
                                                    text = self.q[x],
                                                    indicatoron = 0,
                                                    width = 20,
                                                    padx = 70,
                                                    variable = self.vari,
                                                    value = x,
                                                    command = self.wrongAns))
                self.buttons[-1].pack(side=LEFT)

    def generatePicture(self):
        self.pictures.append(PhotoImage(file="img/"+str(pics[self.corAns])+".gif"))
        self.picpack.append(Label(self.iframe, image=self.pictures[-1]))
        self.picpack[-1].pack(padx=10, pady=20, side=LEFT)

    def generatePictures(self):
        for x in range(len(self.q[1])):
            self.pictures.append(PhotoImage(file="img/"+str(pics[self.q[1][x]])+".gif"))
            self.picpack.append(Label(self.iframe, image=self.pictures[-1]))
            self.picpack[-1].pack(padx=10, pady=20, side=LEFT)
        
    def generateQuestion(self):
        try:
            if self.level == 1:
                self.q = self.qgenerator.create_question_one()
            elif self.level == 2:
                self.q = self.qgenerator.create_question_two()
            elif self.level == 3:
                self.q = self.qgenerator.create_question_three()
                self.corAns = self.q[0]
                random.shuffle(self.q)
                return
            repeat = []
            for ans in self.q[1]:
                if ans not in repeat:
                    repeat.append(ans)
                else:
                    raise Exception
            self.corAns = self.q[1][0]
            random.shuffle(self.q[1])
        except:
            self.generateQuestion()
        

class question_generator():
    def __init__(self, dictionary, country, capital):
        self.record = dictionary
        self.country = country
        self.capital = capital
        self.listb = []
        self.listc = []
        self.listd = []
        self.toReturn = []
    def create_question_one(self):
        self.listb = []
        self.listc = []
        self.listd = []
        length=len(self.country)-1
        for x in range(0,4):
            chosen = random.randint(0, length)
            bc = self.country[chosen]
            ab = self.record[bc]["Capital"]
            self.listb.append(ab)
            if x == 0:
                self.listc.append(bc)
        self.listd.append(self.listc)
        self.listd.append(self.listb)
        return self.listd
    
    def create_question_two(self):
        return self.create_question_one()

    def create_question_three(self):
        self.toReturn = [random.choice(self.capital), random.choice(self.capital), random.choice(self.capital), random.choice(self.capital)]
        repeat = []
        for x in self.toReturn:
            if x not in repeat:
                repeat.append(x)
            else:
                return self.create_question_three()
        return self.toReturn
        
def startGameOne():
    sButtons.destroy()
    g = Game(1)
    g.play()

def startGameTwo():
    sButtons.destroy()
    g = Game(2)
    g.play()

def startGameThree():
    sButtons.destroy()
    g = Game(3)
    g.play()

root = Tk()
root.minsize(300, 200)
sButtons = Frame(root)

def main():
    title = Frame(root)
    title.pack()
    t = Label(title, text = "Learn Geography!")
    t.pack()
    sButtons.pack()
    startButtons = [Button(sButtons, text = "Level 1", command = startGameOne),
                    Button(sButtons, text = "Level 2", command = startGameTwo),
                    Button(sButtons, text = "Level 3", command = startGameThree)]
    for sb in startButtons:
        sb.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
