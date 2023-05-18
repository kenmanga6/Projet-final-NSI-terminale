from tkinter import *

class Case():
    
    def __init__(self, nb_bombes_voisines= 0, etat=False):
        self.bombe = False #True si la case cache une bombe
        self.nb_bv = nb_bombes_voisines #nombre entre 0 et 8, 0 par défaut
        self.etat = etat #True si la case est découverte
        self.drapeau = False #True si marqué d'un drapeau
        self.img_drapeau = None
        
    def dessiner(self, position, canevas): #position = couple(ligne, colonne)
        drapeau = PhotoImage(file='drapeau.gif')
        y=position[0]
        x=position[1]
        if self.etat == True:
            if self.bombe == True:
                color = 'red'
            else:
                color = 'gray64'
        else:
            color = 'gray26'
        canevas.create_rectangle(28*x, 28*y, 28*x+28, 28*y+28, width=1, fill=color)#cases de taille 28x28 pixels
        self.img_drapeau = canevas.create_image(x*28 + 14, y*28 + 14, image = drapeau, state='hidden')
        
    def affiche_drapeau(self, canevas):
        if self.drapeau == False:
            self.drapeau = True
            print(self.img_drapeau)
            canevas.itemconfig(self.img_drapeau, state='normal')
        else: #self.drapeau == True
            self.drapeau = False
            canevas.itemconfig(self.img_drapeau, state='hidden')