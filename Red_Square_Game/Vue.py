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

        #self.canevasPetit = Canvas(self.root, width=self.modele.largeurPetit,
        #                           height=self.modele.hauteurPetit,
        #                           bg="white")

        # self.canevasPetit.bind("<Button-1>", self.start_drag)  # bouton gauche
        # self.canevasPetit.bind("<B1-Motion>", self.dragging)
        # self.canevasPetit.bind("<ButtonRelease-1>", self.end_drag)
        offsetX = (modele.largeurGrand - modele.largeurPetit) / 2
        offsetY = (modele.hauteurGrand - modele.hauteurPetit) / 2
        #self.canevasPetit.place(x=offsetX, y=offsetY)
        #self.canevasPetit.lift(self.nomGrosCanveas)

        self.canevasGros.bind("<Button-1>", self.start_drag)  # bouton gauche
        self.canevasGros.bind("<B1-Motion>", self.dragging)
        self.canevasGros.bind("<ButtonRelease-1>", self.end_drag)


        self.canevasGros.create_rectangle((modele.largeurGrand - modele.largeurPetit) / 2,
                                          (modele.hauteurGrand - modele.hauteurPetit) / 2,
                                          (modele.largeurGrand - modele.largeurPetit) / 2 + modele.largeurPetit,
                                          (modele.hauteurGrand - modele.hauteurPetit) / 2 + modele.hauteurPetit,
                                          fill="white")



        # self.canevasRect = Canvas(self.root, width=self.modele.largeurGrand,
        #                           height=self.modele.hauteurGrand,
        #                           bg="transparentcolor", highlightthickness=0)
        # self.canevasRect.place(x=0, y=0)


        # self.canevasPetit.place(x=(self.modele.largeurGrand - self.modele.largeurPetit) / 2,
        #                         y=(self.modele.hauteurGrand - self.modele.hauteurPetit) / 2)
        self.root.update_idletasks()
        # bouton_start = Button(self.root, text="Commencer partie", command=self.creer_carre)
        # bouton_start.pack()

    def start_drag(self, event):
        # definit la valeur de offsetx et y
        items_with_tag = self.canevasGros.find_withtag("red-square")

        if items_with_tag:
            self.current_carre = items_with_tag[0]
            self.offset_x = event.x - self.canevasGros.coords(self.current_carre)[0]
            # difference entre le click (event) et la bordure du red square
            self.offset_y = event.y - self.canevasGros.coords(self.current_carre)[1]
            # print(self.offset_x, self.offset_y)
            self.parent.animer()

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

        new_x = max(0, min(new_x, max_x))  # le maximum entre 0 et la plus petite valeur entre
        # le nouveau x ou le x maximum (coin haut gauche du red square par rapport au white canvas)
        new_y = max(0, min(new_y, max_y))
        print(new_x, new_y)
        # set les nouvelles coordonnees du carre rouge
        #self.canevasPetit.coords(self.current_carre, new_x, new_y, new_x + self.modele.carres[0].taille,
        #                         new_y + self.modele.carres[0].taille)
        # newX et y reprensentent le top left coord du carre rouge
        # new_x + self.modele.carres[0].taille et y calculent le bottom right du carre rouge
        # la methode a besoin du top left ET du bottom right pour dessiner le carre en mouvement
        self.parent.changer_position((new_x,new_y))


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

        for i in self.modele.carres:
            if(isinstance(i, Carre)):
                self.canevasGros.create_rectangle(i.posX, i.posY,
                                               i.posX + i.taille,
                                               i.posY + i.taille, fill="red",
                                               outline="white",
                                               tags=("red-square",))
        for rect in self.modele.carres:
            if(isinstance(rect, Rectangle)):
                self.canevasGros.create_rectangle(rect.posX, rect.posY,
                                               rect.posX + rect.width,
                                               rect.posY + rect.height,
                                               fill=rect.color,
                                               outline="white",
                                               tags=(rect.color + "-rectangle",))
