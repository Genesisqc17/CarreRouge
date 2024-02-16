from tkinter import *

from Modele import Carre, Rectangle


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

        self.root.geometry("850x650")
        self.root.configure(background="black")

        self.canevasGros = Canvas(self.root, width=self.modele.largeurGrand,
                                  height=self.modele.hauteurGrand,
                                  bg="black")
        self.nomGrosCanveas = self.canevasGros.winfo_name()

        self.canevasGros.place(x=0, y=0)
        self.carreBlanc = None
        self.carreRouge = None


        self.canevasGros.tag_bind("red-square", "<Button-1>", self.start_drag)  # bouton gauche sur le carré rouge
        self.canevasGros.tag_bind("red-square", "<B1-Motion>", self.dragging)  # déplacement du carré rouge
        self.canevasGros.tag_bind("red-square", "<ButtonRelease-1>",
                                  self.end_drag)  # relâchement du bouton sur le carré rouge




    def start_drag(self, event):
        # definit la valeur de offsetx et y
        if self.modele.squareHasBeenClicked == False:  # Pour ne pas que la fonction animer soit spammee et que les rect bleus aillent de pllus en plus vite
            self.parent.animer()
            self.modele.squareHasBeenClicked = True
        items_with_tag = self.canevasGros.find_withtag("red-square")

        if items_with_tag:
            self.current_carre = items_with_tag[0] # un seul carre
            self.offset_x = event.x - self.canevasGros.coords(self.current_carre)[0]
            # difference entre le click (event) et la bordure du red square
            self.offset_y = event.y - self.canevasGros.coords(self.current_carre)[1]
            print(self.offset_x, self.offset_y)





    def dragging(self, event):
        items_with_tag = self.canevasGros.find_withtag("red-square")

        if items_with_tag:

            new_x, new_y = event.x - self.offset_x, event.y - self.offset_y

            # new_x2, new_y2 = new_x + self.modele.blocs[0].taille, new_y + self.modele.blocs[0].taille
            for i in self.modele.blocs:
                if (isinstance(i, Carre)):
                    i.changer_position((new_x,new_y))
            # self.canevasGros.coords(self.current_carre, new_x, new_y, new_x2, new_y2)



    def end_drag(self, event):
        self.current_carre = None  # Clear carre

    def creer_carre(self):
        self.parent.creer_carre()  # demande cette fonction au controleur

    def afficher_blocs(self):
        self.canevasGros.delete("all")

        self.canevasGros.create_rectangle((self.modele.largeurGrand - self.modele.largeurPetit) / 2,
                                          (self.modele.hauteurGrand - self.modele.hauteurPetit) / 2,
                                          (self.modele.largeurGrand - self.modele.largeurPetit) / 2 + self.modele.largeurPetit,
                                          (self.modele.hauteurGrand - self.modele.hauteurPetit) / 2 + self.modele.hauteurPetit,
                                          fill="white")

        for i in self.modele.blocs:
            if(isinstance(i, Carre)):
                self.carreRouge = self.canevasGros.create_rectangle(i.posX, i.posY,
                                               i.posX + i.taille,
                                               i.posY + i.taille, fill="red",
                                               outline="white",
                                               tags=("red-square",))

        for rect in self.modele.blocs:
            if(isinstance(rect, Rectangle)):
                self.canevasGros.create_rectangle(rect.posX, rect.posY,
                                               rect.posX + rect.width,
                                               rect.posY + rect.height,
                                               fill=rect.color,
                                               outline="white",
                                               tags=(rect.color + "-rectangle",))
