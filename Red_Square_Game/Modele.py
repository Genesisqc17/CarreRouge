import random
from helper import Helper as hp


class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.largeurPetit = 450 # renommer en zone blanc
        self.hauteurPetit = 450
        self.largeurGrand = 650 # renommer en zone jeu
        self.hauteurGrand = 650
        self.blocs = []
        self.nbRect = 4
        self.squareHasBeenClicked = False
        self.enVie = True


    def creer_carre(self):
        x = self.largeurGrand/2 - 20
        y = self.hauteurGrand/2 - 20
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

        # Pour fitter dans le petit Canevas
        x = random.randint(0, self.largeurPetit - width)
        y = random.randint(0, self.hauteurPetit - height)

        vitX = 2 * (random.randint(0,1)) - 1
        vitY = 2 * (random.randint(0,1)) - 1

        rect = Rectangle(self, x, y, vitX, vitY, width, height, "blue")
        self.blocs.append(rect)

    def deplacer_rectangles(self):
        for r in self.blocs:
            if (isinstance(r, Rectangle)):
                r.deplacer()
                r.collision_mur()
                r.collision_carre()

    def changer_position(self, new_pos): # pour carre uniquement
        self.blocs[0].changer_position(new_pos)


class Carre():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 40
        self.posX = x
        self.posY = y


    def changer_position(self, new_pos):
        self.posX, self.posY = new_pos
        # mecanique pour limiter le mouvement du rectangle blanc
        items_with_tag = self.parent.parent.vue.canevasGros.find_withtag("red-square")
        if items_with_tag:
            carre = items_with_tag[0]
            current_pos = self.parent.parent.vue.canevasGros.coords(carre)
            # print(current_pos)
            if ((current_pos[0] <= (self.parent.largeurGrand - self.parent.largeurPetit) / 2) or
                    (current_pos[1] <= (self.parent.hauteurGrand - self.parent.hauteurPetit) / 2) or
                    (current_pos[2] >= (self.parent.largeurGrand - self.parent.largeurPetit) / 2 + self.parent.largeurPetit) or
                    (current_pos[3] >= (self.parent.hauteurGrand - self.parent.hauteurPetit) / 2 + self.parent.hauteurPetit)):
                    self.parent.enVie = False
                    print(self.parent.enVie)





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


    def deplacer(self):
        self.posX += self.vitesseX
        self.posY += self.vitesseY



    def collision_mur(self):

        canvas_width = self.parent.largeurGrand # parent du rectangle = modele
        canvas_height = self.parent.hauteurGrand # Grand = carre noir


        if self.posX <= 0 or self.posX + self.width >= canvas_width:
            self.vitesseX = -self.vitesseX
        if canvas_height - self.posY <= self.height or self.posY <= 0:
            self.vitesseY = -self.vitesseY

    def collision_carre(self):
        tag_carre = self.parent.parent.vue.canevasGros.find_withtag("red-square")
        tag_rectangle = self.parent.parent.vue.canevasGros.find_withtag("blue-rectangle")
        if tag_carre and tag_rectangle:
            carre = tag_carre[0]
            for rectangle in tag_rectangle:
                current_pos_carre = self.parent.parent.vue.canevasGros.coords(carre)
                current_pos_rectangle = self.parent.parent.vue.canevasGros.coords(rectangle)
                if ((current_pos_carre[0] == current_pos_rectangle[0]) or
                    (current_pos_carre[1] == current_pos_rectangle[1]) or
                    (current_pos_carre[2] == current_pos_rectangle[2]) or
                    (current_pos_carre[3] == current_pos_rectangle[3])):
                        self.parent.enVie = False
                        print(self.parent.enVie)
