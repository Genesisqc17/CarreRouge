import Modele as mod
import Vue as vue

class Controleur():
    def __init__(self):
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self, self.modele)
        self.vue.root.mainloop()
        self.modele.creer_doc_score_si_nexiste_pas()

    def creer_carre(self):
        self.modele.demarrer_partie()
        self.vue.afficher_blocs()
        # print(len(self.modele.carres))

    def deplacer_rectangles(self):
        self.modele.deplacer_rectangles()
        self.vue.afficher_blocs()

    def animer(self):
        self.modele.deplacer_rectangles()
        self.vue.afficher_blocs()
        self.vue.root.after(5, self.animer)

    def changer_position(self, new_pos):
        self.modele.changer_position(new_pos)

    def fixer_difficulte(self, niveau):
        self.modele.fixer_difficulte(niveau)
        self.creer_carre()

    def show_score(self):
        self.modele.organiser_scores()
        return self.modele.lire_score()

    def effacer_score(self):
        self.modele.effacer_score()

if (__name__ == "__main__"):
    c = Controleur()