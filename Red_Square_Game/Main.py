import Modele as mod
import Vue as vue

class Controleur():
    def __init__(self):
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self, self.modele)
        self.creer_blocs()  # le dit au modele, qui instancie un carre, et les rectangles et la vue les affiche
        self.vue.root.mainloop()

    def creer_blocs(self):
        self.modele.creer_carre()
        for i in range(self.modele.nbRect):
            self.modele.creer_rectangle_aleatoire()

        self.vue.afficher_blocs()
        # print(len(self.modele.carres))

    def deplacer_rectangles(self):
        self.modele.deplacer_rectangles() # contient deplacer et collision mur de Rectangle

        self.vue.afficher_blocs()

    def animer(self):
        self.modele.deplacer_rectangles() # faudra le mettre dans les limites du carre noir
        self.vue.afficher_blocs()
        self.vue.root.after(5, self.animer)

    def changer_position(self, new_pos):
        self.modele.changer_position(new_pos)


if (__name__ == "__main__"):
    c = Controleur()