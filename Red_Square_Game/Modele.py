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
        self.creer_blocs()

    def creer_blocs(self):
        self.creer_carre()
        for i in range(self.nbRect):
            self.creer_rectangle_aleatoire()

        # self.parent.afficher_blocs()
        # print(len(self.modele.carres))

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
    # def deplacer_rectangles2(self):
    #     for r in self.blocs:
    #         if (isinstance(r, Rectangle)):
    #             r.deplacer()
    #             r.collision_mur()
    #             r.collision_carre()]


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

        current_pos = self.parent.blocs[0].posX,self.parent.blocs[0].posY,self.parent.blocs[0].posX + self.taille, self.parent.blocs[0].posY + self.taille
        # ZONE BLANCHE
        if ((current_pos[0] <= (self.parent.largeurGrand - self.parent.largeurPetit) / 2) or
                (current_pos[1] <= (self.parent.hauteurGrand - self.parent.hauteurPetit) / 2) or
                (current_pos[2] >= (self.parent.largeurGrand - self.parent.largeurPetit) / 2 + self.parent.largeurPetit) or
                (current_pos[3] >= (self.parent.hauteurGrand - self.parent.hauteurPetit) / 2 + self.parent.hauteurPetit)):
                self.parent.enVie = False
                print("Collision mur blanc")





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
        self.collision_mur()
        self.collision_carre()




    def collision_mur(self):

        canvas_width = self.parent.largeurGrand # parent du rectangle = modele
        canvas_height = self.parent.hauteurGrand # Grand = carre noir


        if self.posX <= 0 or self.posX + self.width >= canvas_width:
            self.vitesseX = -self.vitesseX
        if canvas_height - self.posY <= self.height or self.posY <= 0:
            self.vitesseY = -self.vitesseY

    def collision_carre(self):
        pos_carre = self.parent.blocs[0].posX, self.parent.blocs[0].posY, self.parent.blocs[0].posX + self.parent.blocs[
            0].taille, self.parent.blocs[0].posY + self.parent.blocs[0].taille

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
