from random import *
from SAD_Case import *

def resize(fenetre, canvas, new_width, new_height):
    #agrandir la fenêtre
    fenetre.geometry(f"{new_width}x{new_height}")
    #agrandir le canvas
    canvas.config(width = new_width, height = new_height)

class Grille():
    
    def __init__(self, nb_lignes=10, nb_colonnes=10, nb_bombes=15):
        self.nbl = nb_lignes
        self.nbc = nb_colonnes
        self.nb_bombes = nb_bombes #nombre bombes dans la grille
        self.nb_cases_vides = self.nbl*self.nbc - self.nb_bombes #nombre de cases qui ne cachent pas de bombes
        self.nb_cases_devoilee = 0 #nombre des cases qui ont été dévoilés
        self.grille = []
        self.remplir()
        self.placement_bombes()
        
    def remplir(self):#remplir avec des cases vides par défaut
        for ligne in range(self.nbl):
            ligne_case = []
            for colonne in range(self.nbc):
                c = Case()
                ligne_case.append(c)
            self.grille.append(ligne_case)

    def placement_bombes(self):
        bombes_placées = 0
        while not bombes_placées == self.nb_bombes:
            n = randint(0, self.nbl-1)
            m = randint(0, self.nbc-1)
            if self.grille[n][m].bombe == False:
                self.grille[n][m].bombe = True
                bombes_placées += 1
    
    def dessiner(self):#dessiner les cases de la grille
        for i in range(self.nbl):
            for j in range(self.nbc):
                c = self.grille[i][j]# c est une instance de case
                c.dessiner( (i, j), canevas )
                
    def liste_coords_voisins(self, position): #position = (ligne, colonne)
        liste_coord_voisins = []
        y, x = position[0], position[1]
        if y < self.nbl -1:
            liste_coord_voisins.append( (y+1, x) )
        if y > 0:
            liste_coord_voisins.append( (y-1, x) )
        if x < self.nbl -1:
            liste_coord_voisins.append( (y, x+1) )
        if x > 0:
            liste_coord_voisins.append( (y, x-1) )
        if x < self.nbl -1 and y < self.nbl -1:
            liste_coord_voisins.append( (y+1,x+1) )
        if x < self.nbl -1 and y > 0:
            liste_coord_voisins.append( (y-1,x+1) )
        if x > 0 and y < self.nbl -1:
            liste_coord_voisins.append( (y+1,x-1) )
        if x > 0 and y > 0:
            liste_coord_voisins.append( (y-1,x-1) )   
        return liste_coord_voisins
    
    def inspection_voisins(self, position):
        c = self.grille[position[0]][position[1]]
        if c.etat == True:
            pass
        else:
            liste_voisins = self.liste_coords_voisins(position)
            for coords_voisin in liste_voisins:
                voisin = self.grille[coords_voisin[0]][coords_voisin[1]]
                if voisin.bombe == True:
                    c.nb_bv += 1
        #print(c.nb_bv, "bombes voisines") #<-- Test
        c.etat = True
        
    def devoilement(self, position):
        y, x = position[0], position[1]
        c = self.grille[y][x]
        if c.etat != True:
            self.inspection_voisins(position)
            #etat automatiquement mis à True avec inspection_voisins
            c.dessiner( (y,x), canevas )
            if not c.bombe:
                if c.nb_bv != 0:
                    if c.nb_bv == 1: coul = 'blue'
                    elif c.nb_bv == 2: coul ='green'
                    elif c.nb_bv == 3: coul ='red'
                    elif c.nb_bv == 4: coul = 'purple'
                    else : coul = 'black'
                    canevas.create_text(x*28 + 14, y*28 + 14, text=str(c.nb_bv), fill=coul)
                self.nb_cases_devoilee += 1
                liste_voisins = self.liste_coords_voisins(position)
                if c.nb_bv == 0: #la case n'a pas de mine parmis ses voisines
                    for voisin in liste_voisins:
                        self.devoilement( (voisin[0], voisin[1]) )
        
    def Perdu(self): #une case avec une bombe à été dévoilée
        #faire apparaître texte "Perdu !" au milieu de la fenêtre ( et empêcher
        #toute autre interractions à part celles de recommencer une partie si possible )
        canevas.create_text(self.nbl*28 / 2, self.nbc*28 / 2, text='Perdu !', fill='red', font=('Helvetica','30','bold'))
        canevas.unbind("<Button-1>")
        canevas.unbind("<Button-3>")
        
    def Gagne(self):
        #si toute les cases ont été découvertes ( hormis les cases avec les bombes ):
        #faire apparaître le texte "Bravo !" au milieu de la fenêtre
        canevas.delete(ALL)
        canevas.create_text(self.nbl*28 / 2, self.nbc*28 / 2 - 20 , text='Gagné !', fill='darkgreen', font=('Helvetica','40','bold'))
        canevas.create_text(self.nbl*28 / 2, self.nbc*28 / 2 + 35, text='Pour rejouer cliquez sur le bouton', fill='darkblue', font=('Helvetica','10','bold'))
        canevas.create_text(self.nbl*28 / 2, self.nbc*28 / 2 + 50, text='"nouvelle partie" en bas à droite', fill='darkblue', font=('Helvetica','10','bold'))
        canevas.create_text(self.nbl*28 / 2, self.nbc*28 / 2 + 65, text='ou changez de difficulté', fill='darkblue', font=('Helvetica','10','bold'))
        canevas.unbind("<Button-1>")
        canevas.unbind("<Button-3>")
    
    def clic_g(self, evt):
        x, y = evt.x // 28, evt.y // 28 # 28 correspond à la taille des cases
        #print("clique gauche détecté en ("(", y, ",",x,")") #<-- Test
        self.devoilement( (y, x) )
        if self.grille[y][x].bombe == True:
            self.Perdu()
        if self.nb_cases_devoilee == self.nb_cases_vides:
            self.Gagne()
        #appels qui servait avant création de la fonction devoilement :
        """c = self.grille[y][x]
        self.inspection_voisins( (y,x) )
        c.dessiner( (y,x), canevas )
        if not c.bombe:
            if c.nb_bv != 0:
                canevas.create_text(x*28 + 14, y*28 + 14, text=str(c.nb_bv), fill='black')"""
        
    def clic_d(self, evt):
        x, y = evt.x // 28, evt.y // 28 # 28 correspond à la taille des cases
        #print("clique droit détecté en ("(", y, ",",x,")") #<-- Test
        c = self.grille[y][x]
        c.affiche_drapeau(canevas)
        
    def difficulte(self):
        niveau = choix.get()
        #recréer la grille avec les nouvelles valeurs (selon la difficulté)
        if niveau == 1:
            self.__init__(10 , 10 , 15)
            canevas.delete(ALL)
            self.placement_bombes()
            self.dessiner()
            resize(Mafenetre, canevas, self.nbl*28, self.nbc*28)
            decompte_mines.configure(text = str(self.nb_bombes))
            canevas.bind("<Button-1>", self.clic_g)
            canevas.bind("<Button-3>", self.clic_d)
            
        elif niveau == 2:
            self.__init__(16 , 16 , 40)
            canevas.delete(ALL)
            self.placement_bombes()
            self.dessiner()
            resize(Mafenetre, canevas, self.nbl*28, self.nbc*28)
            decompte_mines.configure(text = str(self.nb_bombes))
            canevas.bind("<Button-1>", self.clic_g)
            canevas.bind("<Button-3>", self.clic_d)
            
        elif niveau == 3:
            self.__init__(25, 25, 100)
            canevas.delete(ALL)
            self.placement_bombes()
            self.dessiner()
            resize(Mafenetre, canevas, self.nbl*28, self.nbc*28)
            decompte_mines.configure(text = str(self.nb_bombes))
            canevas.bind("<Button-1>", self.clic_g)
            canevas.bind("<Button-3>", self.clic_d)
            
        elif niveau == 4:
            self.__init__(30, 30, 150)
            canevas.delete(ALL)
            self.placement_bombes()
            self.dessiner()
            resize(Mafenetre, canevas, self.nbl*28, self.nbc*28)
            decompte_mines.configure(text = str(self.nb_bombes))
            canevas.bind("<Button-1>", self.clic_g)
            canevas.bind("<Button-3>", self.clic_d)
    
    def new_game(self):
        #démarrer une nouvelle partie: effacer tout ce qui est déjà présent pour tout refaire
        canevas.delete(ALL)
        self.grille = []
        self.remplir()
        self.placement_bombes()
        self.dessiner()
        decompte_mines.configure(text = str(self.nb_bombes))
        canevas.bind("<Button-1>", self.clic_g)
        canevas.bind("<Button-3>", self.clic_d)

# ------------------------------------------------------- Programe Principal -------------------------------------------------------
grille_demineur = Grille() #appel de la grille avec difficulté facile (automatique): 10 lignes et 10 colonnes (=100cases), 15 bombes

Mafenetre = Tk()
Mafenetre.title("Démineur")

canevas = Canvas(Mafenetre, bg='grey', height= grille_demineur.nbl*28, width=grille_demineur.nbc*28)
#on considère des cases de taille 28x28 pixels
canevas.pack(side=RIGHT)


canevas.bind("<Button-1>", grille_demineur.clic_g)
canevas.bind("<Button-3>", grille_demineur.clic_d)
drapeau = PhotoImage(file='drapeau.gif') #"""modifier les couleurs"""
mine = PhotoImage(file='mine.gif')
grille_demineur.dessiner()

"""#test fonction_attribut liste_coords_voisins:
coords_voisins = grille_demineur.liste_coords_voisins( (3,3) )
print(coords_voisins)
for v in coords_voisins:
    c = grille_demineur.grille[v[0]][v[1]]
    c.etat = True
    c.dessiner(v)
"""

# Frames à  gauche de la grille de jeu pour disposer les fonctions supplémentaires
f2 = Frame(Mafenetre)
# Création de cases à  cocher pour le niveau
choix=IntVar()
choix.set(1)
case1=Radiobutton(f2)
case1.configure(text='Facile', command = grille_demineur.difficulte, variable = choix, value=1)
case1.pack(anchor= NW ,padx=30)
case2=Radiobutton(f2)
case2.configure(text='Moyen', padx=3, command = grille_demineur.difficulte, variable = choix, value=2)
case2.pack(anchor= NW, padx=30)
case3=Radiobutton(f2)
case3.configure(text='Difficile', padx=3, command = grille_demineur.difficulte, variable = choix, value=3)
case3.pack(anchor= NW ,padx=30)
case4=Radiobutton(f2)
case4.configure(text='Extrême', padx=3, command = grille_demineur.difficulte, variable = choix, value=4)
case4.pack(anchor= NW ,padx=30)
f2.pack()

# Champ pour l'affichage du nombre de mines selon la difficulté
f3 = Frame(Mafenetre)
texte_mines = Label (f3, text = "nombre de Mines :")
decompte_mines = Label (f3, text = str(grille_demineur.nb_bombes) )
texte_mines.grid(row=4,column=1)
decompte_mines.grid(row=5,column=1, padx=50)
f3.pack()

# bouton nouvelle partie
f1 = Frame(Mafenetre)
bou1 = Button(f1, width=14, text="Nouvelle partie", font="Arial 10" , command = grille_demineur.new_game)
bou1.pack(side=BOTTOM, padx=5, pady=5)
f1.pack(side=BOTTOM)

# image
f4 = Frame(Mafenetre)
photo=PhotoImage(file="Mine.gif")
labl = Label(f4, image=photo)
labl.pack(side=BOTTOM)
f4.pack(side=BOTTOM)

Mafenetre.mainloop()