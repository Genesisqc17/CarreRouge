import Modele as mod
import Vue as vue

class Controleur():
    def __init__(self):
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self, self.modele)
        # self.creer_blocs()  # le dit au modele, qui instancie un carre, et les rectangles et la vue les affiche


        self.difficulteChoisie = False
        self.animationStarted = False


        # self.modele.creer_blocs()
        # print("blocs crees dans le controleur")
        # self.afficher_blocs()
        # print("blocs afifches dans le controleur")
        self.vue.root.mainloop()
        self.modele.creer_doc_score_si_nexiste_pas()

    def difficulte_choisie(self):
        print("dans difficulte choisie()")
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

    def fixer_difficulte(self, niveau):
        self.modele.fixer_difficulte(niveau)
        # self.modele.creer_blocs()

    def show_score(self):
        self.modele.organiser_scores()
        return self.modele.lire_score()

    def effacer_score(self):
        self.modele.effacer_score()

if (__name__ == "__main__"):
    c = Controleur()