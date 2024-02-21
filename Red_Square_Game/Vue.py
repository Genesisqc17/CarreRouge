from tkinter import *
from tkinter import ttk
from Modele import Carre, Rectangle
import sv_ttk


class Vue():
    def __init__(self, parent, modele):

        self.parent = parent
        self.modele = modele
        self.root = Tk()
        self.offset_x = 0
        self.offset_y = 0
        self.current_carre = None

        self.root.geometry("650x650")
        self.root.title("Red Square")
        self.mes_frames = {"menu":self.creer_menu_frame(),
                           "score":self.creer_score_frame(),
                           "game":self.creer_game_frame()}
        self.frame_active = None

        self.changer_frame("menu")

    def quitter_jeu(self):
        self.afficher_menu()
        self.parent.resetGame()

    def changer_frame(self, cle):
        if self.frame_active:
            self.frame_active.pack_forget()
        self.frame_active = self.mes_frames[cle]
        self.frame_active.pack()

    def afficher_menu(self):
        self.changer_frame("menu")

    def afficher_score(self):
        self.changer_frame("score")

    def afficher_game(self):
        self.parent.difficulte_choisie()
        self.changer_frame("game")
        self.canevasGros.bind("<B1-Motion>", self.dragging)

    def entrer_nom(self):
        nom = self.entre.get()
        self.parent.entrer_nom(nom)


    def creer_menu_frame(self):
        # Menu Frame
        self.menu_frame = Frame(self.root)


        self.menu_title_frame = Frame(self.menu_frame)
        self.menu_title_frame.pack(expand=True, fill="y")

        self.menu_label_title = ttk.Label(self.menu_title_frame, text="Red", font=('times new roman', 50, 'bold'),
                                          foreground="red")
        self.menu_label_title.pack(side=LEFT, padx=10)

        self.canevasTitle = Canvas(self.menu_title_frame, width=50, height=50, bg="red", borderwidth=0)
        self.canevasTitle.create_rectangle(0, 0, 50, 50, fill="red", outline="")
        self.canevasTitle.pack(side=LEFT)

        self.nom_frame = Frame(self.menu_frame)
        self.nom_frame.pack()

        self.entre = ttk.Entry(self.nom_frame)
        self.entre.pack(side=LEFT)

        self.entre_bouton = ttk.Button(self.nom_frame, text="Entrer nom", command=self.entrer_nom)
        self.entre_bouton.pack(side=LEFT)

        self.difficulte_frame = Frame(self.menu_frame)
        self.difficulte_frame.pack(pady=20)

        # Facile Button
        self.facile_button = ttk.Button(self.difficulte_frame, text="Facile", command=self.difficulte_facile)
        self.facile_button.pack(side=LEFT, padx=10)

        # Moyen Button
        self.moyen_button = ttk.Button(self.difficulte_frame, text="Moyen", command=self.difficulte_moyen)
        self.moyen_button.pack(side=LEFT, padx=10)

        # Difficile Button
        self.difficile_button = ttk.Button(self.difficulte_frame, text="Difficile", command=self.difficulte_difficile)
        self.difficile_button.pack(side=LEFT, padx=10)

        self.autres_frame = Frame(self.menu_frame)
        self.autres_frame.pack()

        # Game Button
        self.game_button = ttk.Button(self.autres_frame, text="Start Game", command=self.afficher_game)
        self.game_button.pack(pady=10)

        # Score Button
        self.score_button = ttk.Button(self.autres_frame, text="Score", command=self.afficher_score)
        self.score_button.pack(pady=10)

        sv_ttk.set_theme("dark")
        #self.menu_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        return self.menu_frame

    def creer_score_frame(self):
        # Score Frame
        self.score_frame = Frame(self.root)

        self.score_array = self.parent.show_score()

        self.score_string = "\n".join(self.score_array)

        self.score_label = ttk.Label(self.score_frame, text=self.score_string)
        self.score_label.pack(pady=10)

        self.effacer_button = ttk.Button(self.score_frame, text="Effacer Scores", command=self.effacer_score)
        self.effacer_button.pack()

        self.back_button2 = ttk.Button(self.score_frame, text="Back to Menu", command=self.afficher_menu)
        self.back_button2.pack()

        #self.score_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        sv_ttk.set_theme("dark")

        return self.score_frame

    def creer_game_frame(self):
        # Game Frame
        self.game_frame = Frame(self.root)

        # Back to Menu Button
        self.back_button = ttk.Button(self.game_frame, text="Back to Menu", command=self.quitter_jeu)
        self.back_button.pack()

        self.canevasGros = Canvas(self.game_frame, width=self.modele.largeurGrand,
                                  height=self.modele.hauteurGrand,
                                  bg="black")

        self.nomGrosCanveas = self.canevasGros.winfo_name()

        self.canevasGros.place(x=0, y=0)


        self.canevasGros.tag_bind("red-square", "<Button-1>", self.start_drag)  # bouton gauche sur le carré rouge
        # self.canevasGros.tag_bind("red-square", "<B1-Motion>", self.dragging)  # déplacement du carré rouge
        self.canevasGros.bind("<B1-Motion>", self.dragging)  # déplacement du carré rouge
        self.canevasGros.tag_bind("red-square", "<ButtonRelease-1>",
                                  self.end_drag)  # relâchement du bouton sur le carré rouge

        offsetX = (self.modele.largeurGrand - self.modele.largeurPetit) / 2
        offsetY = (self.modele.hauteurGrand - self.modele.hauteurPetit) / 2

        self.canevasGros.bind("<Button-1>", self.start_drag)  # bouton gauche
        self.canevasGros.bind("<B1-Motion>", self.dragging)
        self.canevasGros.bind("<ButtonRelease-1>", self.end_drag)

        self.canevasGros.create_rectangle((self.modele.largeurGrand - self.modele.largeurPetit) / 2,
                                          (self.modele.hauteurGrand - self.modele.hauteurPetit) / 2,
                                          (self.modele.largeurGrand - self.modele.largeurPetit) / 2 + self.modele.largeurPetit,
                                          (self.modele.hauteurGrand - self.modele.hauteurPetit) / 2 + self.modele.hauteurPetit,
                                          fill="white")
        self.canevasGros.pack()
        self.root.update_idletasks()

        sv_ttk.set_theme("dark")
        #self.game_frame.place(relx=0, rely=0)

        return self.game_frame


    def effacer_score(self):
        self.parent.effacer_score()
        self.update_score()

    def update_score(self):
        updated_score_array = self.parent.show_score()
        updated_score_string = "\n".join(updated_score_array)
        self.score_label.config(text=updated_score_string)

    def difficulte_facile(self):
        self.parent.fixer_difficulte(0)


    def difficulte_moyen(self):
        self.parent.fixer_difficulte(1)


    def difficulte_difficile(self):
        self.parent.fixer_difficulte(2)


    def start_drag(self, event):

        self.parent.startGame()

        items_with_tag = self.canevasGros.find_withtag("red-square")


        if items_with_tag:
            self.current_carre = items_with_tag[0] # un seul carre
            self.offset_x = event.x - self.canevasGros.coords(self.current_carre)[0]
            # difference entre le click (event) et la bordure du red square
            self.offset_y = event.y - self.canevasGros.coords(self.current_carre)[1]
            # print(self.offset_x, self.offset_y)





    def dragging(self, event):
      
        items_with_tag = self.canevasGros.find_withtag("red-square")

        if items_with_tag:

            new_x, new_y = event.x - self.offset_x, event.y - self.offset_y
            self.parent.changer_position((new_x,new_y))


    def end_drag(self, event):
        self.current_carre = None  # Clear carre
        # self.parent.animationStarted = False


    def afficher_blocs(self):
        self.canevasGros.delete("all")

        self.rectBlanc = self.canevasGros.create_rectangle((self.modele.largeurGrand - self.modele.largeurPetit) / 2,
                                          (self.modele.hauteurGrand - self.modele.hauteurPetit) / 2,
                                          (
                                                      self.modele.largeurGrand - self.modele.largeurPetit) / 2 + self.modele.largeurPetit,
                                          (
                                                      self.modele.hauteurGrand - self.modele.hauteurPetit) / 2 + self.modele.hauteurPetit,
                                          fill="white")

        for i in self.modele.blocs:
            if(isinstance(i, Carre)):
                self.carreRouge = self.canevasGros.create_rectangle(i.posX, i.posY,
                                               i.posX + i.taille,
                                               i.posY + i.taille, fill="red",
                                               outline="white",
                                               tags=("red-square",))
            else :
                self.canevasGros.create_rectangle(i.posX, i.posY,
                                                  i.posX + i.width,
                                                  i.posY + i.height,
                                                  fill=i.color,
                                                  outline="white",
                                                  tags=(i.color + "-rectangle",))

