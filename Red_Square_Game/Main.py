import Modele as mod
import Vue as vue

class Controleur():
    def __init__(self):
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self, self.modele)
        self.vue.afficher_blocs()
        # self.creer_blocs()  # le dit au modele, qui instancie un carre, et les rectangles et la vue les affiche
        self.animationStarted = False
        self.vue.root.mainloop()


    def afficher_blocs(self):
       self.vue.afficher_blocs()

    def deplacer_rectangles(self):
        self.modele.deplacer_rectangles() # contient deplacer et collision mur de Rectangle

        self.vue.afficher_blocs()
    def startGame(self):
        if not self.animationStarted:
            self.animationStarted = True
            self.animer()
    def animer(self):
        if self.animationStarted:
            self.modele.deplacer_rectangles() # faudra le mettre dans les limites du carre noir
            self.vue.afficher_blocs()
            self.nextloop = self.vue.root.after(12, self.animer)
        else :
            if self.nextloop:
                self.vue.root.after_cancel(self.nextloop)


    def changer_position(self, new_pos):
        self.modele.changer_position(new_pos)


if (__name__ == "__main__"):
    c = Controleur()