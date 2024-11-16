from random  import randint, shuffle
from collections import deque
from rich.console import Console
from keyboard import is_pressed
from time import sleep
from os import system
import shutil

class Affichage():
    """
    Class qui gère tout l'affichage de la partie
    """
    def  __init__(self):
        """
        Initialise l'affichage avec des messages de bienvenue et instancie les attributs de la classe affichage
        Retourne rien et prend aucun argument
        """
        self.plateau = deque([]) # une file de tuples représentant les dominos sur le plateau.
        self.clear = lambda: system('cls||clear') # cls pour Windows et clear pour Linux
        self.console = Console()
        print("Bienvenue dans un jeu de domino.")

    def input(self):
        """
        Permet de gérer le input du joueur
        Prends aucun argument et renvoie l'input (une String) choisie par l'utilisateur
        """
        while is_pressed('droite') or is_pressed('gauche') or is_pressed('enter'): sleep(0.05)
        input = None
        while input == None:
            if is_pressed('right'): input = 'droite'
            elif is_pressed('left'): input = 'gauche'
            elif is_pressed('enter'): input = 'enter'
        return input

    def print_plateau(self):
        """
        Méthode qui affiche le plateau après que les joueurs aient joués. Donc doit présenter au moins un domino
        La méthode qui prends aucun argument
        """
        assert self.plateau != deque([])

        self.console.print("=== Plateau de dominos ===", style="bold green")
        print("")

        largeur_console = shutil.get_terminal_size().columns
        affichage_ligne = ""
        longueur_actuelle = 0

        for domino in self.plateau:
            affichage_domino = f"{domino[0]} ║ {domino[1]}"
            longueur_domino = len(affichage_domino) + 3 # +3  pour l'espace en entre les dominos

            # Si retour à la ligne
            if longueur_actuelle + longueur_domino > largeur_console:
                print("")
                print(affichage_ligne)  
                affichage_ligne = affichage_domino  
                longueur_actuelle = longueur_domino
            else:
                if affichage_ligne:
                    affichage_ligne += "   " # 3espaces entre les domino
                affichage_ligne += affichage_domino
                longueur_actuelle += longueur_domino

        # Afficher la dernière ligne s'il en une reste
        if affichage_ligne:
            print(affichage_ligne, end='')

        print("")
        print("")

    def plateau_et_deck(self, deck, afficher_plateau, info, nom_du_joueur, infoExceptionnelle, infoErreur, afficher_deck = True, domino_droite_ou_gauche = None, afficher_menu_de_fin=False):
        """
        Méthode qui permet d'afficher le deck du joueur.
        Dépend des méthodes 'print_plateau()' et 
        Prend un argument:
            - 'deck', une liste de tuples représentant les dominos du deck du joueur.
            - 'afficher_plateau', un boolean qui détermine si on doit afficher le plateau ou non.
            - 'info', une String qui indique qui est le premier joueur à jouer.
            - 'nom_du_joueur', une String du nom du joueur qui joue
            - 'infoExceptionnelle', une String qui indique quand la pioche est vide et si le jeu est terminé
            - 'infoErreur', une String qui inique si le joueur ne peux pas jouer le domino qu'il essaye de jouer
            - 'afficher_deck', un boolean qui permet d'afficher soit le deck du joueur, soit le menu pour chosir si le domino se place à droite ou à gauche
            - 'domino_droite_ou_gauche', tuple des coordonnées du domino choisi qui peut se jouer à droite ou à gauche
            - 'afficher_menu_de_fin', boolean permettant d'afficher le menu de fin ou non
        Retourne le domino choisi par le joueur et le l'index du placement du curseur.
        """
        taille_deck = len(deck)

        affichage_du_deck = [f"{domino[0]} ║ {domino[1]}" for domino in deck[:-1]]
        if infoExceptionnelle != "PREMIER TOUR": affichage_du_deck.append(deck[-1])
        else: 
            affichage_du_deck.append(f"{deck[-1][0]} ║ {deck[-1][1]}")
            infoExceptionnelle = None
        
        flèche = 0  # Représente le curseur qui permet de choisir le domino
        valide = False
        action = ["À droite", "À gauche", "Annuler"]
        choix_de_fin = ["Rejouer", "Quitter"]

        while not valide:
            self.clear()

            if infoExceptionnelle != None: self.console.print(infoExceptionnelle)
            if infoErreur != None:
                info = None
                self.console.print(infoErreur)
                print("")
            if info != None: 
                self.console.print(info)
                print("")
            if afficher_plateau == True: self.print_plateau()

            # Affichage du menu de fin
            if afficher_menu_de_fin:
                self.console.print(f"La partie est terminée. Voulez-vous rejouer ou quitter ?", end='     ')
                flèche = flèche % 2
                for i, e in enumerate(choix_de_fin):
                    if flèche == i:
                        self.console.print(f'\u2192 {e}', style="bold yellow", end='    ')
                    else:
                        self.console.print(f'  {e}', end='    ')
            # Affichage du deck avec le curseur
            elif afficher_deck:
                self.console.print(f"=== Deck de {nom_du_joueur} ===", style="bold green")
                print("")

                flèche = flèche % taille_deck
                for i, e in enumerate(affichage_du_deck):
                    if flèche == i:
                        self.console.print(f'\u2192 {e}', style="bold yellow", end='    ')
                    else:
                        self.console.print(f'  {e}', end='    ')
            # Affichage du menu pour chosir si le domino se place à droite ou à gauche
            else: 
                self.console.print(f"Où voulez-vous placer ce domino: {domino_droite_ou_gauche[0]} ║ {domino_droite_ou_gauche[1]}  ?", end='     ')
                flèche = flèche % 3
                for i, e in enumerate(action):
                    if flèche == i:
                        self.console.print(f'\u2192 {e}', style="bold yellow", end='    ')
                    else:
                        self.console.print(f'  {e}', end='    ')
            print("\n")

            # Récupère l'input de l'utilisateur
            touche = self.input()
            if touche == 'droite':
                flèche += 1
            elif touche == 'gauche':
                flèche -= 1
                if flèche < 0:
                    flèche = taille_deck - 1
            elif touche == 'enter': 
                valide = True

        input()  # Attend une nouvelle entrée pour annuler les actions de cet input

        #Récupère le domino joué et le retourne  avec son index dans la liste
        if afficher_menu_de_fin:
            return 0, flèche % 2, 
        elif affichage_du_deck:
            if (flèche % taille_deck) == taille_deck -1: domino_joue = deck[-1]
            else: domino_joue=deck[flèche % taille_deck]
            return domino_joue, flèche % taille_deck
        else:
            domino_joue=deck[flèche % 3]
            return domino_joue, flèche % 3

    def fin(self, liste_gagnant):
        """
        Méthode qui gère l'affichage de la fin du jeu. Elle affiche le.s participant.s gagnant.s
        Prend en argument: 'liste_gagnant' une liste qui contient plusieur joueur si on est dans un cas d'égalité et un élément si il y a qu'un gagnant.
        Retourne rien
        """
        assert liste_gagnant != [], "Erreur aucun gagnat n'est donné dans la liste"

        self.clear()
        if len(liste_gagnant)==1: 
            message = f"Le gagnant est {liste_gagnant[0].nom}"
        else: 
            self.console.print("Les gagnants sont:", end=' ')
            for i in range(len(liste_gagnant)):
                message = f", {liste_gagnant[i].nom}"
            message.pop(0)
            message.pop(0)
            message += " Bravo à eux!!!!"
        x, choix = self.plateau_et_deck(liste_gagnant[0].deck, None, message, None, None, None, False, None, True)
        if choix == 0: 
            self.clear()
            jeu = Jeu()
            jeu.partie()
        else: 
            self.clear()
            self.console.print("Merci d'avoir joué à notre jeu !!!")
            quit()
            
    def bot(self, message):
        """
        Méthode qui gère l'affichage quand Bot joue
        Prend en argument: 'message' une String contenant un texte à afficher quand le Bot joue
        Retourne rien
        """
        assert type(message)==str, "message doit être de type str"

        self.console.clear()
        self.console.print(message)
        self.console.print("")
        self.print_plateau()
        sleep(3)

class Domino():
    """
    Classe qui crée un domino, et qui s'apparente à la class Pion demandée. 
    La méthode est inutile étant donné la structure de donné et l'algorithme adoptés mais est présente comme le stiple la consigne
    """
    def __init__(self, haut, bas):
        """
        Méthode qui intancie un domino en lui donnant 2 cotés 'haut' et 'bas' après avoir vérifie que les valeurs donnés aux cotés des domino sont correcte
        """
        assert type(haut)==type(bas)==int, "Erreur de le type les cotées des dominos doivent être des integer"
        assert -1<haut<7 and -1<bas<7, "Erreur les valeurs donné au domino doivent être compris entre 0 et 6 comprit"
        self.haut=haut
        self.bas=bas

class Pioche():
    """
    Classe qui crée une pioche de dominos, et qui s'apparente à la classe Domino demandée
    """
    def __init__(self):
        """
        Instancie la pioche de 28 dominos différents puis la mélange. La pioche est une liste de tuple 
        """
        self.dominos = []
        for haut in range(7):
            for bas in range(haut, 7):
                objet_domino = Domino(haut,bas)
                self.dominos.append((objet_domino.haut, objet_domino.bas))
        shuffle(self.dominos)

    def piocher(self):
        """
        Méthode qui permet de piocher un domino dans la pioche.
        Enlève le domino pioché de la pioche et renvoie le tuple du domino pioché
        """
        domino_pioché = self.dominos[-1]
        self.dominos.pop()
        return domino_pioché

class Joueur():
    """
    Classe qui crée un Joueur / Classe Mère de Bot
    """
    def __init__(self, pioche, nom, nombre_de_domino):
        """
        Initialise le deck du joueur en retirant les dominos piochés dans la pioche et donne un nom au joueur
        Prend en argument:
            - l'objet 'pioche' pour creer un deck au joueur tout en  retirant les domino de la pioche
            - la String 'nom' pour donner un nom au joueur
            - l'integer 'nombre_de_domino' détermine le nombre de dominos donnés au participant
        """

        assert nombre_de_domino == 7 or nombre_de_domino == 5, "Valeur du domino doit être 5 ou 7"

        self.deck = []
        for i in range(nombre_de_domino):
            self.deck.append(pioche.piocher())
        self.deck.append("PIOCHER")
        self.nom = nom

class Bot(Joueur):
    """
    Classe qui cree un Bot / Classe Fille de Joueur 
    clases qui existe pour un potentiel dévellopement du projet 
    """
    def __init__(self, pioche, nom, nombre_de_domino):
        """
        Intancie un bot comme un joueur --> Voir __init__(...) de la class Joueur
        """
        super().__init__(pioche, nom, nombre_de_domino)
    
class Jeu():
    """
    Classe qui gère dirige le déroulement la partie.
    """
    def __init__(self):
        """
        Méthode qui instantie la partie en créant un plateau, une pioche et des participants au jeu (humain ou robot) ainsi que des attribut utile au déroulement de la partie -> voir commentaire pour plus de détail
        """
        liste_de_nom_de_bot = ["François Pignon", "Jacquouille la Fripouille", "Bernard Morin", "Godefroy de Montmirail", "Gaston Tricard", "Albert Merlot", "L'adjudant Gerber", "Tiburce", 
                               "Francis Chichmont", "Didier Jean-Marie Latour", "Pascal Eusèbe Désiré Latour", "Bernard André-Michel Latour", "Gaston Lagaffe", "Chewbacca", "Le Grand Blond avec une chaussure noire",
                               "Stéphane Marchadot", "L'Âne (Jo)", "Forrest Gump", "Mister Bean"]

        self.pioche = Pioche()
        self.affichage = Affichage()
        self.participant =  []

        # Demander le nombre de joueur
        while True:
            try:
                nombre_de_joueur = int(input("Combien de joueurs veulent participer ? (1-4) \n>>> "))
                if 1 <= nombre_de_joueur <= 4:
                    break
                else:
                    print("Le nombre de joueurs doit être compris entre 1 et 3.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide.")

        # Demander le nombre de bots
        nombre_de_bot = 0
        while True and (4 - nombre_de_joueur)>0:
            try:
                nombre_de_bot = int(input(f"Combien de bots voulez-vous ajouter ? (0-{4 - nombre_de_joueur}) \n>>> "))
                if 0 <= nombre_de_bot <= (4 - nombre_de_joueur):
                    break
                else:
                    print(f"Le nombre de bots doit être compris entre 0 et {4 - nombre_de_joueur}.")
            except ValueError:
                print("Veuillez entrer un nombre entier valide.")

        self.nombre_de_participant = nombre_de_bot  + nombre_de_joueur  # Détermine le nombre de participant à la partie

        # Détermine si les participant doivent avoir 5 où 7 domino en fonction de leur nombre (Voir règle)
        if self.nombre_de_participant == 2:
            for i in range(nombre_de_joueur):
                nom = ""
                while nom  == "":
                    nom = input(f"Veuillez entrer le nom d'un joueur non vide\n>>> ")
                self.participant.append(Joueur(self.pioche, nom, 7))
            for i in range(nombre_de_bot):
                nom = liste_de_nom_de_bot.pop(randint(0,len(liste_de_nom_de_bot)-1)) # prend un nom dans la liste des noms des bots et évite que il y ait 2 fois le meme nom
                self.participant.append(Bot(self.pioche, nom, 7))
        else:
            for i in range(nombre_de_joueur):
                nom = ""
                while nom  == "":
                    nom = input(f"Veuillez entrer le nom d'un joueur \n>>> ")
                self.participant.append(Joueur(self.pioche, nom, 5))
            for i in range(nombre_de_bot):
                nom = liste_de_nom_de_bot.pop(randint(0,len(liste_de_nom_de_bot)-1)) # Permet d'éviter que il y ait 2 fois le meme nom
                self.participant.append(Bot(self.pioche, nom, 5))
    
        shuffle(self.participant) # Mélanger les participants

        self.tour = 0 # répresente la x+1 fois que un joueur joue
        self.infoExceptionnelle = None # peux répresenter la String indiquant une potentiel erreur
        self.infoErreur = None # peux répresenter la String indiquant que le domino joué ne peux être joué
        self.info = None # peux répresenter la String indiquant qui est en train de jouer
        self.passer = 0 # Compteur du nombre de 'PASSER' jouer à la suite par les joueurs

    def vérifie(self, domino_joue):
        """
        Méthode qui vérifie si le domino chosi peut être joué et si oui où.
        Prend en argument: 'domino_joue' un tuple qui contient les coordonnées du domino choisi
        Retourne un tuple contenant:
            - En première position un boolean: True si le domino peut être joué, False si non
            - En seconde position une liste de tuples indiquant où le domino peut être joué et dans quel sens il doit être posé
                ↪ Ex: le  tuple ('left', 1, 0) indique que le domino peux être placé à gauche en le retournant
                ↪ Ex: le  tuple (None, 0, 1) indique que le domino peux être placé à droite sans le retourner
            ↪ Cas particulié: la méthode retourne le tuple (False,None) quand le domino ne peux pas être placé
        """
        
        verifaction = {1: [False,('left',1,0)], 2: [False, ('left',0,1)], 3: [False,(None,0,1)], 4: [False,(None,1,0)]} # Choix d'un dictionnaire pour dijoncter les quatres cas possible  (=> pratique)

        if domino_joue[0] == domino_joue[1] == self.affichage.plateau[0][0]: return True, [('left',1,0)]
        elif domino_joue[0] == domino_joue[1] == self.affichage.plateau[-1][1]: return True, [(None,1,0)]

        if domino_joue[0] == self.affichage.plateau[0][0]: 
            self.infoErreur = None
            verifaction[1][0]=True
        if domino_joue[1] == self.affichage.plateau[0][0]: 
            verifaction[2][0]=True
            self.infoErreur = None
        if domino_joue[0] == self.affichage.plateau[-1][1]: 
            verifaction[3][0]=True
            self.infoErreur = None
        if domino_joue[1] == self.affichage.plateau[-1][1]: 
            verifaction[4][0]=True
            self.infoErreur = None

        à_return = [0]
        for i in sorted(verifaction.keys()):
            valeur = verifaction[i]
            if valeur[0] == True:  
                à_return[0]+=1
                à_return.append(valeur[1])
        if à_return[0] >=1: 
            return True, à_return[1:] 
        return False, None

    def jouer_piocher(self, joueur_qui_joue):
        """
        Méthode faisant piocher le participant si il choisie dans son menu PIOCHER et remplace le bouton PIOCHER par PASSER qquand la pioche est vide
        Prend en argument: l'objet 'joueur_qui_joue', qui est le participant qui est en train de jouer
        Retourne rien
        """
        if self.pioche.dominos != []: 
            joueur_qui_joue.deck.insert(-2, self.pioche.piocher()) 
            self.infoErreur = None
        else: 
            for participant in self.participant:
                participant.deck[-1] = "PASSER"
            self.infoExceptionnelle = "La pioche est maintenant vide. Si vous ne pouvais pas joueur, vous passez votre tour"
            self.infoErreur = None

    def jouer_passer(self):
        """
        Méthode qui permet aux participants de passer leur tour. 
        Cette méthode vérifie aussi si seulement le je est finissable: si oui elle le dit au joueur, si non elle determine un ou plusieurs gagnants.
        La méthode prend aucun argument et ne retourne rien
        """
        self.passer +=1    
        self.infoErreur = None
        if self.passer >= self.nombre_de_participant:
            i = 0
            domino_trouvé = False  # Flag pour indiquer si un domino a été trouvé

            while i < len(self.participant) and not domino_trouvé:
                participant = self.participant[i]
                j = 0

                while j < len(participant.deck) and not domino_trouvé:
                    domino = participant.deck[j]
                    verif = self.vérifie(domino)
                    if verif[0] == True:
                        if self.passer >= 2 * self.nombre_de_participant:
                            self.infoErreur = f"\u2192 {participant.nom}, peut jouer un domino"
                        else:
                            self.infoErreur = "\u2192 Un joueur peux jouer un domino, vérifiez votre deck"
                        domino_trouvé = True  # Met à jour le flag pour arrêter les boucles
                    j += 1 # Passe au domino suivant

                i += 1  # Passe au participant suivant
            
            if not domino_trouvé: # Détermine un ou plusieur gagnant si personne ne peut joueur
                liste_gagnant = [self.participant[0]]
                for i in range(1,len(self.participant)):
                    if len(liste_gagnant[0].deck)>len(self.participant[i].deck): liste_gagnant = [self.participant[i]]
                    if len(liste_gagnant[0].deck)==len(self.participant[i].deck): liste_gagnant.append(self.participant[i])
                self.affichage.fin(liste_gagnant)       

    def jouer_un_domino(self, joueur_qui_joue, domino_joue, index_du_domino_joue, bot=False):
        """
        Méthode qui permet aux joueurs de jouer un domino sur le plateau après avoir vérifié avec la methode 'vérifie()' si il est correct ou non
        Prend pour argument:
            - l'objet 'joueur_qui_joue' représentant le joueur qui est en train de jouer
            - le tuple 'domino_joue' étant le domino que le joueur veut jouer
            - l'integer 'index_du_domino_joue' étant l'index du domino que le joueur veut jouer dans la liste de son deck
        La méthode retourne si un domino peux être posé ou non par un boolean (True si oui, False si non)
        """
        self.passer = 0
        verif = self.vérifie(domino_joue)
        if verif[0] == True: 
            if len(verif[1])==1 or bot:
                if verif[1][0][0] == None:
                    self.affichage.plateau.append((domino_joue[verif[1][0][1]],domino_joue[verif[1][0][2]]))
                else:
                    self.affichage.plateau.appendleft((domino_joue[verif[1][0][1]],domino_joue[verif[1][0][2]]))
                joueur_qui_joue.deck.pop(index_du_domino_joue)

            else:
                x, choix = self.affichage.plateau_et_deck(joueur_qui_joue.deck, True, self.info, joueur_qui_joue.nom, self.infoExceptionnelle, self.infoErreur, False, domino_joue)
                if choix == 0: 
                    self.affichage.plateau.append((domino_joue[verif[1][1][1]],domino_joue[verif[1][1][2]]))
                    joueur_qui_joue.deck.pop(index_du_domino_joue)

                if choix == 1: 
                    self.affichage.plateau.appendleft((domino_joue[verif[1][0][1]],domino_joue[verif[1][0][2]]))
                    joueur_qui_joue.deck.pop(index_du_domino_joue)

            return True
        else: return False

    def jouer(self, joueur_qui_joue):
        """
        Méthode qui dirige le déroulement du tour du joueur qui joue:
            1. Affiche le plateau avec le deck du joueur
            2. Redirige vers la bonne méthode en fonction de l'input du joueur:
                - 'jouer_piocher(...)' si le joueur a pioché
                - 'jouer_passer()' si le joueur passe son tour
                - 'jouer_un_domino(...)' si le joueur joue un domino
        Prend pour argument 'joueur_qui_joue' un joueur qui joue
        Retourne rien
        """
        
        afficher_plateau = True
        self.info = f"{joueur_qui_joue.nom} vous devez jouer"
        
        domino_joue, index_du_domino_joue = self.affichage.plateau_et_deck(joueur_qui_joue.deck, afficher_plateau, self.info, joueur_qui_joue.nom, self.infoExceptionnelle, self.infoErreur)
        if domino_joue == "PIOCHER": 
            self.jouer_piocher(joueur_qui_joue)
            self.tour+=1
        elif domino_joue == "PASSER": 
            self.jouer_passer()
            self.tour+=1
        else: 
            if self.jouer_un_domino(joueur_qui_joue, domino_joue, index_du_domino_joue) == False:
                self.infoErreur = f"Ce domino ne peux pas être joué. Veuillez rejouer {joueur_qui_joue.nom}"
            else:
                self.tour+=1        

    def jouerBot(self, joueur_qui_joue, i=0):
        """
        Méthode qui permet au bot de jouer en testant pour chaque domino si il peut être posé et si oui il arrête de tester et pose le premier domino qui fonctionne
        Prend en argument 'joueur_qui_joue' un objet issu de la classe 'Bot' et qui est un bot qui essaye de jouer
        Retourne rien 
        """
        i=0
        taille = len(joueur_qui_joue.deck)
        message = f"{joueur_qui_joue.nom} a joué {joueur_qui_joue.deck[i]}"
        while i<taille and self.jouer_un_domino(joueur_qui_joue, joueur_qui_joue.deck[i], i, True) == False:
            i+=1 
            if i==taille and joueur_qui_joue.deck[-1] == "PIOCHER": 
                message= f"{joueur_qui_joue.nom} a pioché"
                self.jouer_piocher(joueur_qui_joue)
            elif i==taille and joueur_qui_joue.deck[-1] == "PASSER": 
                message = f"{joueur_qui_joue.nom} a passé son tour"
                self.jouer_passer() 
            else:
                message = f"{joueur_qui_joue.nom} a joué {joueur_qui_joue.deck[i]}"
 
        self.affichage.bot(message)
        self.tour +=1

    def partie(self):
        """
        Méthode principale du programme: 
            1. Fait jouer le premeir joueur en lui imposant de poser un domino de son jeu
            2. Fait jouer un par un les joueurs et les bots
            3. Check si il y a un ou plusieurs gagnants et si oui redirige vers 'self.affichage.fin(...)'
        La méthode prend aucun argument et retourne rien
        """
        partie_en_cours = True
        joueur_qui_joue = self.participant[-1]

        # Initialise le jeu en fesant jouer le premier joueur
        if joueur_qui_joue.__class__.__name__ == 'Bot':
            message= f"{joueur_qui_joue.nom} à jouer le premier domino"
            self.affichage.plateau.append(joueur_qui_joue.deck.pop(0))
            self.affichage.bot(message)
        else:
            info = f"{joueur_qui_joue.nom} vous êtes le premier joueur à jouer, Posez le premier domino"
            domino_joue, index_du_domino_joue = self.affichage.plateau_et_deck(joueur_qui_joue.deck[:-1], False, info, joueur_qui_joue.nom, "PREMIER TOUR", None)
            joueur_qui_joue.deck.pop(index_du_domino_joue)
            self.affichage.plateau.append(domino_joue)
            self.affichage.print_plateau()
            sleep(1.5)


        while partie_en_cours:
            
            joueur_qui_joue = self.participant[self.tour % self.nombre_de_participant]

            if joueur_qui_joue.__class__.__name__ == 'Bot':
                self.affichage.console.clear()
                self.affichage.print_plateau()
                sleep(1.5)
                self.jouerBot(joueur_qui_joue)
            else:
                self.jouer(joueur_qui_joue)

            if joueur_qui_joue.deck == ["PIOCHER"] or joueur_qui_joue.deck == ["PASSER"]: # test si il y a un gagnant
                self.affichage.fin([joueur_qui_joue])
  