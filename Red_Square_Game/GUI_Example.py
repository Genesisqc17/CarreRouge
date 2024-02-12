import random
from tkinter import *
from helper import Helper as hp
class Vue():
    def __init__(self, parent, modele):
        self.parent = parent
        self.modele = modele
        self.root = Tk()
        monLabel = Label(self.root, text="Bienvenue au cours de c31_intensif")
        monLabel.pack()
        monLabel2 = Button(self.root, text="Cours graphique", command=self.creer_pion)
        monLabel2.pack()
        self.canevas = Canvas(self.root, width=self.modele.largeur,
                              height=self.modele.hauteur,
                              bg="black")
        self.canevas.bind("<Button>", self.get_position) ## relier le canevas a un event
        self.canevas.pack()
        boutonDeplacer = Button(self.root, text="Deplacer", command=self.animer)
        boutonDeplacer.pack()
    def get_position(self, evt):
        chose = self.canevas.find_withtag("current")  # la chose en dessous du pointeur de la suoris
        if chose:
            print(chose, evt.x, evt.y) # item du canvas
    def creer_pion(self):
        self.parent.creer_pion() # demande cette fonction au controleur
    def afficher_pion(self):
        for i in self.modele.pions:
            # Generate random RGB values
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            # Convert RGB to a hexadecimal color string
        random_color = f'#{r:02x}{g:02x}{b:02x}'
        self.canevas.delete("all")
        for i in self.modele.pions:
            self.canevas.create_rectangle(i.posX, i.posY,
                                          i.posX+i.taille,
                                          i.posY+i.taille, fill=random_color,
                                          outline="white",
                                          tags=("pion",))
    def animer(self):
        self.parent.animer()
class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeur = 500
        self.hauteur = 500
        self.pions = []
    def creer_pions(self):
        for i in range(10):
            x = random.randrange(self.largeur)
            y = random.randrange(self.hauteur)
            p = Pion(self,x,y)
            self.pions.append(p)
    def deplacer_pions(self):
        for i in self.pions:
            i.deplacer()

class Pion():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 30
        self.posX = x
        self.posY = y
        self.cibleX= None
        self.cibleY = None
        self.angle = None
        self.vitesse = random.randrange(3,9) # distance a parcourir

    def trouver_cible(self):
        self.cibleX = random.randrange(self.parent.largeur)
        self.cibleY = random.randrange(self.parent.hauteur)
        self.angle = hp.calcAngle(self.posX, self.posY, self.cibleX, self.cibleY)

    def deplacer(self):
        if self.cibleX:
            self.posX, self.posY = hp.getAngledPoint(self.angle, self.vitesse, self.posX, self.posY)
            dist = hp.calcDistance(self.posX, self.posY, self.cibleX, self.cibleY)

            if dist <= self.vitesse:
                self.trouver_cible()
        else:
            self.trouver_cible()



class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self, self.modele)
        self.vue.root.mainloop()

    def creer_pion(self):
        self.modele.creer_pions()
        self.vue.afficher_pion()
        print("nbr pions: " +  str(len(self.modele.pions)))

    def deplacer_pions(self):
        self.modele.deplacer_pions()
        self.vue.afficher_pion()
        # self.loop = self.vue.canevas.after(10, self.deplacer_pions)
    def animer(self):
        self.modele.deplacer_pions()
        self.vue.afficher_pion()
        self.vue.root.after(44, self.animer)
if (__name__ == "__main__"):
    c = Controleur()



print("merci")


