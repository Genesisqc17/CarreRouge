import Modele as mod
import Vue as vue


class Controleur():
    def __init__(self):
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self, self.modele)
        self.difficulteChoisie = False
        self.animationStarted = False
        self.nextloop = None
        self.vue.root.mainloop()
        self.modele.creer_doc_score_si_nexiste_pas()


    def resetGame(self):

        self.vue.root.after_cancel(self.nextloop)
        self.difficulteChoisie = False
        self.animationStarted = False
        self.nextloop = None
        self.modele.resetGame()


    def entrer_nom(self,nom):
        self.modele.entrer_nom(nom)

    def difficulte_choisie(self):
        self.modele.creer_blocs()
        self.afficher_blocs()

    def afficher_blocs(self):
       self.vue.afficher_blocs()

    def deplacer_rectangles(self):
        self.modele.deplacer_rectangles() # contient deplacer et collision mur de Rectangle
        self.vue.afficher_blocs()

    def startGame(self):
        if not self.animationStarted:
            self.animationStarted = True

            self.animer()
            self.modele.startTimer()

    def animer(self):
        if self.animationStarted:
            self.modele.deplacer_rectangles() # faudra le mettre dans les limites du carre noir
            self.vue.afficher_blocs()
            if not self.modele.enVie:
                self.modele.gameStop()
                self.vue.changer_frame("menu")
                self.resetGame()
                self.vue.canevasGros.unbind("<B1-Motion>")

            else:
                self.nextloop = self.vue.root.after(12, self.animer)

        else :
            if self.nextloop:
                self.vue.root.after_cancel(self.nextloop)


    def changer_position(self, new_pos):
        self.modele.changer_position(new_pos)

    def fixer_difficulte(self, niveau):
        self.modele.fixer_difficulte(niveau)
        # self.modele.creer_blocs()

    def show_score(self):
        self.modele.organiser_scores()
        return self.modele.lire_score()

    def effacer_score(self):
        self.modele.effacer_score()

    def update_score(self):
        self.vue.update_score()

if (__name__ == "__main__"):
    c = Controleur()