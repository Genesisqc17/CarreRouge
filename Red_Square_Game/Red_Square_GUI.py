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
        # CALL CARRE COLLISION


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
        # for rect in self.modele.carres:
        #     self.canevasPetit.create_rectangle(rect.posX, rect.posY,
        #                                        rect.posX + rect.width,
        #                                        rect.posY + rect.height,
        #                                        fill=rect.color,
        #                                        outline="white",
        #                                        tags=(rect.color + "-rectangle",))

class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeurPetit = 450
        self.hauteurPetit = 450
        self.largeurGrand = 650
        self.hauteurGrand = 650
        self.carres = []
        # self.rectangles = []

    def creer_carre(self):
        x = 205
        y = 205
        car = Carre(self, x, y)
        self.carres.append(car)

    def creer_rectangle_aleatoire(self):
        # pour avoir des size varies
        min_width = 20
        max_width = 100
        min_height = 20
        max_height = 100
        width = random.randint(min_width, max_width)
        height = random.randint(min_height, max_height)

        # Pour fitter dans le petit Canevas
        x = random.randint(0, self.largeurPetit - width)
        y = random.randint(0, self.hauteurPetit - height)


        rect = Rectangle(self, x, y, width, height, "blue")
        self.carres.append(rect)
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

class Rectangle(): # BROUILLON
    def __init__(self, parent, x, y, width, height, color="blue"):
        self.parent = parent
        self.posX = x
        self.posY = y
        self.width = width
        self.height = height
        self.color = color


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
        self.creer_carre() # le dit au modele, qui instancie un carre, et la vue laffiche
        self.vue.root.mainloop()

    def creer_carre(self):
        self.modele.creer_carre()
        self.vue.afficher_carre()
        # print(len(self.modele.carres))


if (__name__ == "__main__"):
    c = Controleur()

# foreach rec in rectangles :
# def check_collision(carrerouge, rec):
    #     # Unpack the coordinates
    #     x1, y1, x2, y2 = carre
    #     x3, y3, x4, y4 = rec
    #
    #     # Check if there is no overlap
    #     if x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1:
    #         return False  # No collision
    #     return True  # Collision detected


    # Velocite = prochaine incrementation de x et y
    # def check_wall_collision(self):
    #     # Get canvas dimensions from the parent (assuming these are stored in Modele)
    #     canvas_width = self.parent.largeurPetit
    #     canvas_height = self.parent.hauteurPetit
    #
    #     # Check for collisions with each wall and reverse direction if collided
    #     if self.posX <= 0 or self.posX + self.width >= canvas_width:
    #         self.vx = -self.vx  # Reverse X direction
    #     if self.posY <= 0 or self.posY + self.height >= canvas_height:
    #         self.vy = -self.vy  # Reverse Y direction