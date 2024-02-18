from tkinter import *
from tkinter import ttk
from Modele import Carre, Rectangle
import sv_ttk

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

        self.root.geometry("650x650")
        self.root.title("Red Square")
        #self.root.configure(background="black")

        def show_game_frame():
            self.menu_frame.place_forget()
            self.game_frame.pack()

        def show_score_frame():
            self.menu_frame.place_forget()
            self.parent.show_score()
            self.score_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        def back_to_menu():
            self.game_frame.pack_forget()
            self.menu_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        def back_to_menu2():
            self.score_frame.place_forget()
            self.menu_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        def effacer_score():
            self.parent.effacer_score()
            updated_score_array = self.parent.show_score()

            updated_score_string = "\n".join(updated_score_array)
            self.score_label.config(text=updated_score_string)


        def difficulte_facile():
            self.parent.fixer_difficulte(0)
        def difficulte_moyen():
            self.parent.fixer_difficulte(1)
        def difficulte_difficile():
            self.parent.fixer_difficulte(2)

        # Menu Frame
        self.menu_frame = Frame(self.root)
        self.menu_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.difficulte_frame = Frame(self.menu_frame)
        self.difficulte_frame.pack(pady=20)

        # Facile Button
        self.facile_button = ttk.Button(self.difficulte_frame, text="Facile", command=difficulte_facile)
        self.facile_button.pack(side=LEFT,padx=10)

        # Moyen Button
        self.moyen_button = ttk.Button(self.difficulte_frame, text="Moyen", command=difficulte_moyen)
        self.moyen_button.pack(side=LEFT,padx=10)

        # Difficile Button
        self.difficile_button = ttk.Button(self.difficulte_frame, text="Difficile", command=difficulte_difficile)
        self.difficile_button.pack(side=LEFT,padx=10)

        self.autres_frame = Frame(self.menu_frame)
        self.autres_frame.pack()

        # Game Button
        self.game_button = ttk.Button(self.autres_frame, text="Start Game", command=show_game_frame)
        self.game_button.pack(pady=10)

        # Score Button
        self.score_button = ttk.Button(self.autres_frame, text="Score", command=show_score_frame)
        self.score_button.pack(pady=10)


        # Score Frame
        self.score_frame = Frame(self.root)

        self.score_array = self.parent.show_score()

        self.score_string = "\n".join(self.score_array)

        self.score_label = ttk.Label(self.score_frame, text=self.score_string)
        self.score_label.pack(pady=10)

        self.effacer_button = ttk.Button(self.score_frame, text="Effacer Scores", command=effacer_score)
        self.effacer_button.pack()

        self.back_button2 = ttk.Button(self.score_frame, text="Back to Menu", command=back_to_menu2)
        self.back_button2.pack()

        # Game Frame
        self.game_frame = Frame(self.root)

        # Back to Menu Button
        self.back_button = ttk.Button(self.game_frame, text="Back to Menu", command=back_to_menu)
        self.back_button.pack()

        self.canevasGros = Canvas(self.game_frame, width=self.modele.largeurGrand,
                                  height=self.modele.hauteurGrand,
                                  bg="black")

        self.nomGrosCanveas = self.canevasGros.winfo_name()

        self.canevasGros.place(x=0, y=0)

        offsetX = (modele.largeurGrand - modele.largeurPetit) / 2
        offsetY = (modele.hauteurGrand - modele.hauteurPetit) / 2

        self.canevasGros.bind("<Button-1>", self.start_drag)  # bouton gauche
        self.canevasGros.bind("<B1-Motion>", self.dragging)
        self.canevasGros.bind("<ButtonRelease-1>", self.end_drag)


        self.canevasGros.create_rectangle((modele.largeurGrand - modele.largeurPetit) / 2,
                                          (modele.hauteurGrand - modele.hauteurPetit) / 2,
                                          (modele.largeurGrand - modele.largeurPetit) / 2 + modele.largeurPetit,
                                          (modele.hauteurGrand - modele.hauteurPetit) / 2 + modele.hauteurPetit,
                                          fill="white")
        self.canevasGros.pack()
        self.root.update_idletasks()

        self.game_frame.pack_forget()
        self.score_frame.place_forget()
        sv_ttk.set_theme("dark")

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
