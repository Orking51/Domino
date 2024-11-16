import jeu as j
from rich.console import Console
from collections import deque
from os import system

class Test:
    """
    Classe qui contient tous les test unitaires du programme jeu.py
    """
    def __init__(self):
        """
        Instantie l'attribut console permettant d'afficher en couleur dans la console
        """
        self.console = Console()
        self.clear = lambda: system('cls||clear')

    def print_resultat_test(self, messageErreur, nom_de_la_class):
        """
        Méthode qui permet d'afficher en console la conclusion de chaque test unitaire
        Prend pour argument:
            - 'messageErreur' une String qui contient les défauts du test.
            - 'nom_de_la_class' permet de print pour qu'elle classe le test est OK ou contient de erreur
        Retourne rien
        """
        if messageErreur == " ": 
            self.console.print(f" - Class {nom_de_la_class}: ", style='green', end='')
            self.console.print("OK", style='bold green')
        else:
            self.console.print(f" \u2192 Class {nom_de_la_class}: ", style='bold red', end='')
            self.console.print(messageErreur, style='red')

    
    def test_affichage(self):
        """
        Teste pour une majorité des méthodes de l'affichage:
            1. Teste si le plateau s'intancie et est bien une deque vide
            2. Teste si la fonction print_plateau() fait planter le programme si on lui donne de mauvais arguments et si elle marche bien normallement:
                - Plante si le deck est vide
                - Plante si la file du plateau ne peut pas append à  droite ou à gauche
                - Vérifie que la  méthode marche en temps normal
            3. Teste si la méthode fin fait planter le programme si on lui donne de mauvais arguments:
                - Plante si aucun argument lui ai  donné
                - Plante si on lui donne pour argument non objet
            4. Teste si la méthode bot fait planter le programme si on lui donne de mauvais arguments:
                - Plante si le messsage ddonné pour argument à la méthode n'est pas une String
        (Méthode qui prend aucun argument et ne qui retourne rien)
        """

        objet_affichage=j.Affichage()
        self.console.clear()
        messageErreur = " "


        #test des attributs instanciés
        if not isinstance(objet_affichage.plateau, deque) or objet_affichage.plateau != deque([]):
            messageErreur += "\n   - L'instanciation du plateau est mauvaise"
        

        #La méthode input(self) est pas testable unitairement mais fonctionne bien. Si vous testait le code le curseur se déplace au bonne endroit + voir screen compte rendu

        #test de print_plateau(self)
        try: 
            objet_affichage.print_plateau()
            messageErreur += "\n   - la méthode print_plateau ne devrait pas pouvoir fonctionner avec une deck vide"
        except:
            messageErreur +=  ""
            
        try: 
            objet_affichage.plateau.append((0,5))
            objet_affichage.plateau.appendleft((1,5))
        except:
            messageErreur += "\n   - la file ne peux pas append"

        try: 
            objet_affichage.print_plateau()
        except:
            messageErreur += "\n   - la méthode print_plateau ne marche pas"


        # La méthode plateau_et_deck(...) est très complicament testable en test unitaire
        # Voir screen dans le compte rendu 


        #test méthode fin(...)
        try:  
            objet_affichage.fin([]) 
            messageErreur += "\n   - la méthode fin ne devrait pas fonctionner car aucun gagnant est contenu dans la liste qui lui est envoyé"
        except:
            messageErreur  += ""
        
        try:  
            objet_affichage.fin(["208051"]) 
            messageErreur += "\n   - la méthode fin ne devrait pas fonctionner car la liste fournie ne contient pas un objet"
        except:
            messageErreur  += ""

        # Voir screen pour la méthode fin()

        #test méthode bot(...)
        try:  
            objet_affichage.bot([2]) 
            messageErreur += "\n   - la méthode bot ne devrait pas fonctionner car l'agument envoyé est une liste et nom une String"
        except:
            messageErreur  += ""


        # Affichage console des résultats des tests
        self.clear()
        self.print_resultat_test(messageErreur, "Affichage")


    def test_domino(self):
        """
        Teste si les dominos créés respectent bien les consignes du jeu:
            - Un domino a 2 valeures entières comprises entre 0 et 6 inclu
        (Méthode qui prend aucun argument et qui retourne rien)
        """

        messageErreur = " "
        liste_de_test_pour_instantie_un_objet_domino = [("Banane", "Noix de coco"),({1:3,2:4}, 3),(3,12),(-1,5),(deque([3]),[2])]

        #Test l'intanciation de l'objet
        for i in range(len(liste_de_test_pour_instantie_un_objet_domino)):
            try: 
                objet_domino = j.Domino(liste_de_test_pour_instantie_un_objet_domino[i][0], liste_de_test_pour_instantie_un_objet_domino[i][1])
                messageErreur += "\n   - le domino s'intantie avec  des valeurs non valide, elle devrait accepter seulement des entiers comprient entre 0 et 6"
            except:
                messageErreur += ""    
        try:
            objet_domino = j.Domino(1)
            messageErreur += "\n   - Pour creer un domino il faut 2arguments pas moins"
        except:
            messageErreur += ""
        try: objet_domino = j.Domino(1,2) 
        except: messageErreur += "\n   - Le domino ne se creer pas avec une saisie correcte"


        self.print_resultat_test(messageErreur, "Domino")


    def test_pioche(self):
        """
        Test la class Pioche:
            1. Teste si à l'instantiation la pioche:
                - Check si l'attribut domino est bien une liste
                - Check si l'attribut domino contient 28 dominos
                - Check si les domino stockés dans la pioche sont bien sous forme de tuple
            2. Teste la méthode piocher()
                - Le domino retourné doit être un tuple
                - Le domino retourné ne doit plus être dans la pioche
                - La pioche doit avoir perdu un domino
        (Méthode qui prend aucun argument et qui retourne rien)
        """

        objet_pioche = j.Pioche()
        messageErreur = " "

        # test de l'instantiation de l'objet 'objet_pioche'
        if len(objet_pioche.dominos) != 28:
            messageErreur += "\n   - La pioche ne contient pas 28 dominos"    
        if not isinstance(objet_pioche.dominos, list):
            messageErreur += "\n   - L'attribut dominos n'est pas du bon type" 
        if not isinstance(objet_pioche.dominos[3], tuple):
            messageErreur += "\n   - L'attribut dominos ne contient pas le bon type" 

        # test de piocher()
        domino_piocher = objet_pioche.piocher()
        if not isinstance(domino_piocher, tuple):
            messageErreur += "\n   - Lorsqu'on pioche un dominos on n'a pas un tuple"   
        if domino_piocher in objet_pioche.dominos:
            messageErreur += "\n   - La pioche ne perd pas le domino pioché"
        if len(objet_pioche.dominos) ==28:
            messageErreur += "\n   - La pioche n'a pas réduit de taille alors que on a pioché"

        self.print_resultat_test(messageErreur, "Pioche")
        
    def test_joueur_bot(self):
        """
        Cette méthode teste la class 'Bot' et 'Joueur' en même temps car la class 'Bot' est fille de la class 'Joueur' et ne contient aucune méthode particulière
        Par consequent tester si une propriété fonctionne pour un objet 'Bot' implique que cette même propriété fonctionne pour un objet 'Joueur' et inversement
        Test:
            1. Cherche si méthode crash avec des mauvais input
            2. Check si la méthode fonctionne avec de bons input
        (Méthode qui prend aucun argument et qui retourne rien)
        """
        messageErreur = " "

        #test de mauvaise l'instanciation des objets Joueur et Bot
        try: 
            objet_joueur = j.Joueur([(3,4),(4,5)], "👍", 5)
            messageErreur += "\n   - la méthode n'est pas censé accépté une list pour argument"
        except: 
            messageErreur += ""
        try:
            objet_bot = j.Bot(j.Pioche(), 5, "5")
            messageErreur += "\n   - la méthode doit prend en troisième argument 7 ou 5"
        except:
            messageErreur += ""
        try:
            objet_joueur = j.Joueur(j.Pioche(), "Bot", 8)
            messageErreur += "\n   - la méthode doit prend en troisème argument 7 ou 5"
        except:
            messageErreur += ""

        # Test si l'instanciation marche normalement
        try:
            objet_joueur = j.Bot(j.Pioche(), "Bot", 7)
            messageErreur += ""
        except:
            messageErreur += "\n   - les arguments saisie était bon la méthode n'aurait pas du planter"
        
        self.print_resultat_test(messageErreur, "Joueur")
        self.print_resultat_test(messageErreur, "Bot")

    def test_jeu(self):

        messageErreur = " "
        self.console.print("Pour tester la méthode 'Jeu' vous devez remplire quelques input qui permetterons de verifier l'instanciation de l'objet \n>>> OK", style='blue', end='')
        input("")
        
        #instanciation
        try: jeu = j.Jeu()
        except: messageErreur += "\n   - Erreur lors de l'instanciation des inputs"
        if not isinstance(jeu.participant, list) or jeu.participant == []:
            messageErreur += "\n   - la liste des participant est mal instancié"
        if jeu.tour!=0:
            messageErreur += "\n   - les tours sont mal instancié"
        if jeu.infoExceptionnelle != None:
            messageErreur += "\n   - l'infoExceptionnelle est mal instancié"
        if jeu.infoErreur != None:
            messageErreur += "\n   - l'infoErreur est mal instancié"
        if jeu.info != None:
            messageErreur += "\n   - l'info est mal instancié"
        if jeu.passer != 0:
            messageErreur += "\n   - le compteur passer est mal instancié"

        #
        # test de vérifie()
        #

        jeu.affichage.plateau = deque([(1, 2), (2, 3)])
        domino_joue = (1, 5)
        resultat, placement = jeu.vérifie(domino_joue)
        if not (resultat and ('left', 1, 0) in placement):
            messageErreur += "\n   - Le domino (1, 5) aurait dû être jouable à gauche."

        # Le domino peut être joué à droite
        domino_joue = (3, 6)
        resultat, placement = jeu.vérifie(domino_joue)
        if not (resultat and (None, 0, 1) in placement):
            messageErreur += "\n   - Le domino (3, 6) aurait dû être jouable à droite."

        # Un domino double peut être joué à gauche
        domino_joue = (1, 1)
        resultat, placement = jeu.vérifie(domino_joue)
        if not (resultat and placement == [('left', 1, 0)]):
            messageErreur += "\n   - Le domino double (1, 1) aurait dû être jouable à gauche."

        # Un domino double peut être joué à droite
        domino_joue = (3, 3)
        resultat, placement = jeu.vérifie(domino_joue)
        if not (resultat and placement == [(None, 1, 0)]):
            messageErreur += "\n   - Le domino double (3, 3) aurait dû être jouable à droite."

        # Un domino qui ne peut pas être joué
        domino_joue = (4, 5)
        resultat, placement = jeu.vérifie(domino_joue)
        if not (not resultat and placement is None):
            messageErreur += "\n   - Le domino (4, 5) n'aurait pas dû être jouable."


        #
        # test de jouer_piocher()
        # 

        jeu.pioche = j.Pioche()  
        joueur = j.Joueur(jeu.pioche, "Test Joueur", 5)
        jeu.participant.append(joueur)

        # Si la pioche contient des dominos
        jeu.pioche.dominos = [(3,4)]
        jeu.jouer_piocher(joueur)
        if joueur.deck[-3] != (3, 4):
            messageErreur += "\n   - Le joueur n'a pas pioché correctement"

        # si La pioche est vide
        jeu.pioche.dominos = []
        jeu.jouer_piocher(joueur)
        if joueur.deck[-1] != "PASSER":
            messageErreur += "\n   - L'option 'PIOCHER' n'a pas été remplacée par 'PASSER' quand la pioche est passé vide."
        if jeu.infoExceptionnelle != "La pioche est maintenant vide. Si vous ne pouvais pas joueur, vous passez votre tour":
            messageErreur += "\n   - L'infoExceptionnelle n'est pas correcttement mis à jour"

        #
        # test de jouer_passer()
        # 

        jeu.nombre_de_participant = 3
        jeu.passer = 0
        jeu.pioche = j.Pioche()
        joueur1 = j.Joueur(jeu.pioche, "Joueur 1", 5)
        joueur2 = j.Joueur(jeu.pioche, "Joueur 2",  5)
        joueur3 = j.Joueur(jeu.pioche, "Joueur 3", 5)
        joueur1.deck = [(1, 2), (2, 3), "PASSER"]  
        joueur2.deck = [(3, 4), (4, 5), "PASSER"]  
        joueur3.deck = [(5, 6), (6, 1), "PASSER"]  
        jeu.participant = [joueur1, joueur2, joueur3]

        # Cas où personne ne peut jouer
        jeu.vérifie = lambda domino: (False, None) 
        jeu.jouer_passer()
        if jeu.passer != 1:
            messageErreur += "\n   - Le compteur 'passer' n'a pas été incrémenté correctement."

        
        #
        # test de jouer_piocher()
        # 

        joueur_qui_joue = jeu.participant[0]
        test = jeu.jouer_un_domino(joueur_qui_joue, (1,2), 0)
        if test == True or test == False:
            messageErreur+= ""
        else:
            messageErreur += "\n   - La méthode jouer_un_domino() ne retourne pas un  boolean."


        #
        # le test de jouer() n'est pas possible car elle permet simplement de rediriger vers des fonctions en fonction des input utilisateur, ce qui marche comme on peut le voir en lancant le programme.
        #
        #
        # test de jouerBot() méthode qui n'apporterais rien si elle l'était car on remarque en jouant que le bot fait toujours un bon coup + difficile à tester proprement.
        #
        #
        # test de partie() qui fait juste alterner entre les joueurs qui jouent uns par uns et fait jouer le premier tour ce qui marche si on lance le programme. Aucun test est necessaire et est fesable.
        #
           #
        ##### Pour les 3méthode voir screen dans le compte rendu
           #
       
        self.print_resultat_test(messageErreur, "Jeu")



test = Test()
test.test_affichage()
test.test_domino()
test.test_pioche()
test.test_joueur_bot()
test.test_jeu()
    