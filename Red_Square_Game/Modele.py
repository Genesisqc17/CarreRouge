import random
from helper import Helper as hp


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

        vitX = 2 * (random.randint(0,1)) - 1
        vitY = 2 * (random.randint(0,1)) - 1

        rect = Rectangle(self, x, y, vitX, vitY, width, height, "blue")
        self.carres.append(rect)

    def deplacer_rectangles(self):
        for r in self.carres:
            if (isinstance(r, Rectangle)):
                r.deplacer()

    def changer_position(self, new_pos):
        self.carres[0].changer_position(new_pos)


class Carre():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 40
        self.posX = x
        self.posY = y

        #self.cibleX= None
        #self.cibleY = None
        #self.angle = None
        #self.vitesse =5
        # pourquoi est-ce qu'on a besoin de ses params si c'est la souris qui le bouge?

    def changer_position(self, new_pos):
        self.posX, self.posY = new_pos

class Rectangle(): # BROUILLON
    def __init__(self, parent, x, y, vitX, vitY, width, height, color="blue"):
        self.parent = parent
        self.posX = x
        self.posY = y
        self.width = width
        self.height = height
        self.color = color
        #self.vitesse = None
        self.vitesseX = vitX
        self.vitesseY = vitY


    # def trouver_cible(self):
    #     self.cibleX = random.randrange(self.parent.largeur)
    #     self.cibleY = random.randrange(self.parent.hauteur)
    #     self.angle = hp.calcAngle(self.posX, self.posY, self.cibleX, self.cibleY)

    # def deplacer(self):
    #     if self.cibleX:
    #         self.posX, self.posY = hp.getAngledPoint(self.angle, self.vitesse, self.posX, self.posY)
    #         dist = hp.calcDistance(self.posX, self.posY, self.cibleX, self.cibleY)
    #
    #         if dist <= self.vitesse:
    #             self.trouver_cible()
    #     else:
    #         self.trouver_cible()

    def deplacer(self):
        self.posX += self.vitesseX
        self.posY += self.vitesseY

    def collision_mur(self):
    # Get canvas dimensions from the parent (assuming these are stored in Modele)
        canvas_width = self.parent.parent.largeurPetit
        canvas_height = self.parent.parent.hauteurPetit

    # Check for collisions with each wall and reverse direction if collided
        if self.posX <= 0 or self.posX + self.width >= canvas_width:
            self.vx = -self.vx  # Reverse X direction
        if self.posY <= 0 or self.posY + self.height >= canvas_height:
            self.vy = -self.vy  # Reverse Y direction

