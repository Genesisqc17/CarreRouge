import os.path
import random
from helper import Helper as hp
import csv
import time
from datetime import datetime

class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeurPetit = 450  # renommer en zone blanc
        self.hauteurPetit = 450
        self.largeurGrand = 650  # renommer en zone jeu
        self.hauteurGrand = 650
        self.blocs = []
        self.squareHasBeenClicked = False
        self.enVie = True
        self.nbRect = None
        self.difficulte = 0
        self.document = "./donnee/score.csv"
        self.document_entetes = ["Nom", "Score","Difficulte", "Date"]
        self.tempsDebut = None
        self.tempsFin = None
        self.score = None
        self.nom = "";

    def entrer_nom(self, nom):
        self.nom = nom

    def startTimer(self):
        self.tempsDebut = time.time()

    def gameStop(self):
        self.tempsFin = time.time()
        tempscore = self.tempsFin - self.tempsDebut
        formatted_score = "{:.2f}".format(tempscore)
        # self.score = float(formatted_score)

        if(self.difficulte == 0):
            dif = "Facile"
        elif(self.difficulte == 1):
            dif = "Moyen"
        else:
            dif = "Difficile"

        date = datetime.now().date().strftime("%Y-%m-%d")

        data = [self.nom, formatted_score, dif, date]
        self.ecrire_csv(data)
        self.parent.update_score()
        print("score sauvegarder")

    def resetGame(self):
        print("dans resetGame du modele")
        self.blocs.clear()
        self.squareHasBeenClicked = False
        self.enVie = True
        self.nbRect = None
        self.difficulte = 0
        self.tempsDebut = None
        self.tempsFin = None
        self.score = None

    def creer_blocs(self):
        print("dans creer-blocs")
        self.creer_carre()
        if (self.difficulte == 0):
            self.nbRect = 4
            # print("if self.difficulte == 0")

        if (self.difficulte == 1):
            self.nbRect = 6

        if (self.difficulte == 2):
            self.nbRect = 8
        for i in range(self.nbRect):
            self.creer_rectangle_aleatoire()

    def creer_carre(self):
        x = self.largeurGrand / 2 - 20
        y = self.hauteurGrand / 2 - 20
        car = Carre(self, x, y)
        self.blocs.append(car)

    def creer_rectangle_aleatoire(self):
        # pour avoir des size varies
        min_width = 20
        max_width = 100
        min_height = 20
        max_height = 100

        width = random.randint(min_width, max_width)
        height = random.randint(min_height, max_height)

        # zone de buffer autour du carre rouge
        square_buffer = 20
        square = self.blocs[0]

        # definir la zone de buffer
        buffer_x1 = square.posX - square_buffer
        buffer_y1 = square.posY - square_buffer
        buffer_x2 = square.posX + square.taille + square_buffer
        buffer_y2 = square.posY + square.taille + square_buffer

        # essaie de placer le rectangle jusqua ce que ca soit une position valide
        while True:
            x = random.randint(0, self.largeurPetit - width)
            y = random.randint(0, self.hauteurPetit - height)

            if not (x + width > buffer_x1 and x < buffer_x2 and y + height > buffer_y1 and y < buffer_y2):
                break  # position valide trouvee
        vitX = 2
        vitY = 2
        r = random.choice([-1, 1])
        vitX *= r
        vitY *= r

        rect = Rectangle(self, x, y, vitX, vitY, width, height, "blue")
        self.blocs.append(rect)

    def deplacer_rectangles(self):
        for i in self.blocs:
            if (isinstance(i, Rectangle)):
                i.deplacer()

    def changer_position(self, new_pos):  # pour carre uniquement
        self.blocs[0].changer_position(new_pos)

    def fixer_difficulte(self, niveau):
        self.difficulte = niveau

    def creer_doc_score_si_nexiste_pas(self):
        if not os.path.exists(self.document):
            with open(self.document, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.document_entetes)

    def ecrire_csv(self, data):
        with open(self.document, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def organiser_scores(self):
        # parcoure la liste et la reorganise
        with open(self.document, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip les entetes
            sorted_data = sorted(reader, key=lambda row: float(row[1]), reverse=True)

        # overwrite le fichier avec la nouvelle liste ordonnee
        with open(self.document, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.document_entetes)
            for row in sorted_data:
                writer.writerow(row)

    def lire_score(self):
        score = []
        with open(self.document, 'r', newline='') as csvfile:
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

    def changer_position(self, new_pos):
        self.posX, self.posY = new_pos

        current_pos = self.parent.blocs[0].posX, self.parent.blocs[0].posY, self.parent.blocs[0].posX + self.taille, \
                                                                            self.parent.blocs[0].posY + self.taille
        # ZONE BLANCHE
        if ((current_pos[0] <= (self.parent.largeurGrand - self.parent.largeurPetit) / 2) or
                (current_pos[1] <= (self.parent.hauteurGrand - self.parent.hauteurPetit) / 2) or
                (current_pos[2] >= (
                        self.parent.largeurGrand - self.parent.largeurPetit) / 2 + self.parent.largeurPetit) or
                (current_pos[3] >= (
                        self.parent.hauteurGrand - self.parent.hauteurPetit) / 2 + self.parent.hauteurPetit)):
            self.parent.enVie = False
            print("Collision mur blanc")

class Rectangle():  # BROUILLON
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
        self.collision_mur()
        self.collision_carre()

    def collision_mur(self):

        canvas_width = self.parent.largeurGrand  # parent du rectangle = modele
        canvas_height = self.parent.hauteurGrand  # Grand = carre noir

        if self.posX <= 0 or self.posX + self.width >= canvas_width:
            self.vitesseX = -self.vitesseX
        if canvas_height - self.posY <= self.height or self.posY <= 0:
            self.vitesseY = -self.vitesseY

    def collision_carre(self):
        pos_carre = self.parent.blocs[0].posX, self.parent.blocs[0].posY, self.parent.blocs[0].posX + \
                                                                          self.parent.blocs[
                                                                              0].taille, self.parent.blocs[0].posY + \
                                                                          self.parent.blocs[0].taille

        for bloc in self.parent.blocs[1:]:  # Skip the first bloc assuming it's the square
            if isinstance(bloc, Rectangle):  # Make sure it's a rectangle
                pos_rectangle = (bloc.posX, bloc.posY, bloc.posX + bloc.width, bloc.posY + bloc.height)

                if not (pos_rectangle[2] < pos_carre[0] or  # rectangle's right < square's left
                        pos_rectangle[0] > pos_carre[2] or  # rectangle's left > square's right
                        pos_rectangle[3] < pos_carre[1] or  # rectangle's bottom < square's top
                        pos_rectangle[1] > pos_carre[3]):  # rectangle's top > square's bottom
                    # Overlap detected
                    self.parent.enVie = False
                    print(self.parent.enVie)
                    # return  # Exit after finding any overlap to avoid unnecessary checks
