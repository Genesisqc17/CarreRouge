import random
from tkinter import *
from helper import Helper as hp


##
class Vue():
    def __init__(self, parent, modele):

        self.parent = parent
        self.modele = modele
        self.root = Tk()
        # monLabel = Label(self.root, text="Le jeu du carre rouge")
        # monLabel.pack()
        self.offset_x = 0
        self.offset_y = 0
        self.current_carre = None

        self.canevasGros = Canvas(self.root, width=self.modele.largeurGrand,
                                  height=self.modele.hauteurGrand,
                                  bg="black")
        self.nomGrosCanveas = self.canevasGros.winfo_name()

        self.canevasGros.place(x=0,y=0)

        self.canevasPetit = Canvas(self.root, width=self.modele.largeurPetit,
                                   height=self.modele.hauteurPetit,
                                   bg="white")

        self.canevasPetit.bind("<Button-1>", self.start_drag) # bouton gauche
        self.canevasPetit.bind("<B1-Motion>", self.dragging)
        self.canevasPetit.bind("<ButtonRelease-1>", self.end_drag)
        offsetX = (modele.largeurGrand - modele.largeurPetit) / 2
        offsetY = (modele.hauteurGrand - modele.hauteurPetit) / 2
        self.canevasPetit.place(x=offsetX, y=offsetY)
        self.canevasPetit.lift(self.nomGrosCanveas)

        # self.canevasPetit.place(x=(self.modele.largeurGrand - self.modele.largeurPetit) / 2,
        #                         y=(self.modele.hauteurGrand - self.modele.hauteurPetit) / 2)
        self.root.update_idletasks()
        # bouton_start = Button(self.root, text="Commencer partie", command=self.creer_carre)
        # bouton_start.pack()

    def start_drag(self, event):
        # definit la valeur de offsetx et y
        items_with_tag = self.canevasPetit.find_withtag("red-square")

        if items_with_tag:
            self.current_carre = items_with_tag[0]
        self.offset_x = event.x - self.canevasPetit.coords(self.current_carre)[0]
        # difference entre le click (event) et la bordure du red square
        self.offset_y = event.y - self.canevasPetit.coords(self.current_carre)[1]
        # print(self.offset_x, self.offset_y)

    def dragging(self, event):
        # width = self.root.winfo_width()
        # height = self.root.winfo_height()
        # differenceX = width - self.modele.largeurPetit / 4
        # differenceY = height - self.modele.hauteurPetit / 2
        # event renvoie les coordonnees relatives au canvas sur lequel le event est bind
        # bouger carre pour suivre curseur
        new_x, new_y = event.x - self.offset_x, event.y - self.offset_y
        # new_x,y = difference entre la position du curseur et le top-left du red square
        # pour donner la position exacte x,y du carre
        # la coordonnee max que le coin top-left du carre rouge peut etre dans le carre blanc
        max_x = self.modele.largeurPetit - self.modele.carres[0].taille
        max_y = self.modele.hauteurPetit - self.modele.carres[0].taille


        new_x = max(0, min(new_x, max_x)) # le maximum entre 0 et la plus petite valeur entre
        # le nouveau x ou le x maximum (coin haut gauche du red square par rapport au white canvas)
        new_y = max(0, min(new_y, max_y))
        print(new_x, new_y)
        # set les nouvelles coordonnees du carre rouge
        self.canevasPetit.coords(self.current_carre, new_x, new_y, new_x + self.modele.carres[0].taille,
                            new_y + self.modele.carres[0].taille)
        # newX et y reprensentent le top left coord du carre rouge
        # new_x + self.modele.carres[0].taille et y calculent le bottom right du carre rouge
        # la methode a besoin du top left ET du top right pour dessiner le carre en mouvement

    def end_drag(self, event):
        self.current_carre = None  # Clear carre

    def creer_carre(self):
        self.parent.creer_carre()  # demande cette fonction au controleur

    def afficher_carre(self):
        for i in self.modele.carres:
            self.canevasPetit.create_rectangle(i.posX, i.posY,
                                          i.posX+i.taille,
                                          i.posY+i.taille, fill="red",
                                          outline="white",
                                          tags=("red-square",))


class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeurPetit = 450
        self.hauteurPetit = 450
        self.largeurGrand = 650
        self.hauteurGrand = 650
        self.carres = []

    def creer_carre(self):
        x = 205
        y = 205
        car = Carre(self, x, y)
        self.carres.append(car)

class Carre():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 40
        self.posX = x
        self.posY = y
        self.cibleX= None
        self.cibleY = None
        self.angle = None
        self.vitesse =5



class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self, self.modele)
        self.creer_carre()
        self.vue.root.mainloop()

    def creer_carre(self):
        self.modele.creer_carre()
        self.vue.afficher_carre()
        # print(len(self.modele.carres))


if (__name__ == "__main__"):
    c = Controleur()
