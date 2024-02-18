import os.path
import random
from helper import Helper as hp
import csv

class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeurPetit = 450
        self.hauteurPetit = 450
        self.largeurGrand = 650
        self.hauteurGrand = 650
        self.carres = []
        self.difficulte = 0
        self.document = "./donnee/score.csv"
        self.document_entetes = ["Nom","Score","Date"]
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

    def demarrer_partie(self):
        self.creer_carre()
        if(self.difficulte == 0):
            for i in range(4):
                self.creer_rectangle_aleatoire()
        if(self.difficulte == 1):
            for i in range(6):
                self.creer_rectangle_aleatoire()
        if(self.difficulte == 2):
            for i in range(8):
                self.creer_rectangle_aleatoire()

    def fixer_difficulte(self, niveau):
        self.difficulte = niveau

    def creer_doc_score_si_nexiste_pas(self):
        if not os.path.exists(self.document):
            with open(self.document,'w',newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.document_entetes)

    def ecrire_csv(self,data):
        with open(self.document,'a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)

    def organiser_scores(self):
        # parcoure la liste et la reorganise
        with open(self.document,'r',newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) # Skip les entetes
            sorted_data = sorted(reader, key=lambda row: int(row[1]),reverse=True)

        # overwrite le fichier avec la nouvelle liste ordonnee
        with open(self.document,'w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Nom", "Score", "Date"])
            for row in sorted_data:
                writer.writerow(row)

    def lire_score(self):
        score = []
        with open(self.document,'r',newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                score.append("\t".join(row))
        return score

    def effacer_score(self):
        with open(self.document, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.document_entetes)


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
        self.vitesseX = vitX
        self.vitesseY = vitY


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