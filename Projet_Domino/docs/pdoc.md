Module jeu
==========

Classes
-------

`Affichage()`
:   Class qui gère tout l'affichage de la partie
    
    Initialise l'affichage avec des messages de bienvenue et instancie les attributs de la classe affichage
    Retourne rien et prend aucun argument

    ### Methods

    `bot(self, message)`
    :   Méthode qui gère l'affichage quand Bot joue
        Prend en argument: 'message' une String contenant un texte à afficher quand le Bot joue
        Retourne rien

    `fin(self, liste_gagnant)`
    :   Méthode qui gère l'affichage de la fin du jeu. Elle affiche le.s participant.s gagnant.s
        Prend en argument: 'liste_gagnant' une liste qui contient plusieur joueur si on est dans un cas d'égalité et un élément si il y a qu'un gagnant.
        Retourne rien

    `input(self)`
    :   Permet de gérer le input du joueur
        Prends aucun argument et renvoie l'input (une String) choisie par l'utilisateur

    `plateau_et_deck(self, deck, afficher_plateau, info, nom_du_joueur, infoExceptionnelle, infoErreur, afficher_deck=True, domino_droite_ou_gauche=None, afficher_menu_de_fin=False)`
    :   Méthode qui permet d'afficher le deck du joueur.
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

    `print_plateau(self)`
    :   Méthode qui affiche le plateau après que les joueurs aient joués. Donc doit présenter au moins un domino
        La méthode qui prends aucun argument

`Bot(pioche, nom, nombre_de_domino)`
:   Classe qui cree un Bot / Classe Fille de Joueur 
    clases qui existe pour un potentiel dévellopement du projet 
    
    Intancie un bot comme un joueur --> Voir __init__(...) de la class Joueur

    ### Ancestors (in MRO)

    * jeu.Joueur

`Domino(haut, bas)`
:   Classe qui crée un domino, et qui s'apparente à la class Pion demandée. 
    La méthode est inutile étant donné la structure de donné et l'algorithme adoptés mais est présente comme le stiple la consigne
    
    Méthode qui intancie un domino en lui donnant 2 cotés 'haut' et 'bas' après avoir vérifie que les valeurs donnés aux cotés des domino sont correcte

`Jeu()`
:   Classe qui gère dirige le déroulement la partie.
    
    Méthode qui instantie la partie en créant un plateau, une pioche et des participants au jeu (humain ou robot) ainsi que des attribut utile au déroulement de la partie -> voir commentaire pour plus de détail

    ### Methods

    `jouer(self, joueur_qui_joue)`
    :   Méthode qui dirige le déroulement du tour du joueur qui joue:
            1. Affiche le plateau avec le deck du joueur
            2. Redirige vers la bonne méthode en fonction de l'input du joueur:
                - 'jouer_piocher(...)' si le joueur a pioché
                - 'jouer_passer()' si le joueur passe son tour
                - 'jouer_un_domino(...)' si le joueur joue un domino
        Prend pour argument 'joueur_qui_joue' un joueur qui joue
        Retourne rien

    `jouerBot(self, joueur_qui_joue, i=0)`
    :   Méthode qui permet au bot de jouer en testant pour chaque domino si il peut être posé et si oui il arrête de tester et pose le premier domino qui fonctionne
        Prend en argument 'joueur_qui_joue' un objet issu de la classe 'Bot' et qui est un bot qui essaye de jouer
        Retourne rien

    `jouer_passer(self)`
    :   Méthode qui permet aux participants de passer leur tour. 
        Cette méthode vérifie aussi si seulement le je est finissable: si oui elle le dit au joueur, si non elle determine un ou plusieurs gagnants.
        La méthode prend aucun argument et ne retourne rien

    `jouer_piocher(self, joueur_qui_joue)`
    :   Méthode faisant piocher le participant si il choisie dans son menu PIOCHER et remplace le bouton PIOCHER par PASSER qquand la pioche est vide
        Prend en argument: l'objet 'joueur_qui_joue', qui est le participant qui est en train de jouer
        Retourne rien

    `jouer_un_domino(self, joueur_qui_joue, domino_joue, index_du_domino_joue, bot=False)`
    :   Méthode qui permet aux joueurs de jouer un domino sur le plateau après avoir vérifié avec la methode 'vérifie()' si il est correct ou non
        Prend pour argument:
            - l'objet 'joueur_qui_joue' représentant le joueur qui est en train de jouer
            - le tuple 'domino_joue' étant le domino que le joueur veut jouer
            - l'integer 'index_du_domino_joue' étant l'index du domino que le joueur veut jouer dans la liste de son deck
        La méthode retourne si un domino peux être posé ou non par un boolean (True si oui, False si non)

    `partie(self)`
    :   Méthode principale du programme: 
            1. Fait jouer le premeir joueur en lui imposant de poser un domino de son jeu
            2. Fait jouer un par un les joueurs et les bots
            3. Check si il y a un ou plusieurs gagnants et si oui redirige vers 'self.affichage.fin(...)'
        La méthode prend aucun argument et retourne rien

    `vérifie(self, domino_joue)`
    :   Méthode qui vérifie si le domino chosi peut être joué et si oui où.
        Prend en argument: 'domino_joue' un tuple qui contient les coordonnées du domino choisi
        Retourne un tuple contenant:
            - En première position un boolean: True si le domino peut être joué, False si non
            - En seconde position une liste de tuples indiquant où le domino peut être joué et dans quel sens il doit être posé
                ↪ Ex: le  tuple ('left', 1, 0) indique que le domino peux être placé à gauche en le retournant
                ↪ Ex: le  tuple (None, 0, 1) indique que le domino peux être placé à droite sans le retourner
            ↪ Cas particulié: la méthode retourne le tuple (False,None) quand le domino ne peux pas être placé

`Joueur(pioche, nom, nombre_de_domino)`
:   Classe qui crée un Joueur / Classe Mère de Bot
    
    Initialise le deck du joueur en retirant les dominos piochés dans la pioche et donne un nom au joueur
    Prend en argument:
        - l'objet 'pioche' pour creer un deck au joueur tout en  retirant les domino de la pioche
        - la String 'nom' pour donner un nom au joueur
        - l'integer 'nombre_de_domino' détermine le nombre de dominos donnés au participant

    ### Descendants

    * jeu.Bot

`Pioche()`
:   Classe qui crée une pioche de dominos, et qui s'apparente à la classe Domino demandée
    
    Instancie la pioche de 28 dominos différents puis la mélange. La pioche est une liste de tuple

    ### Methods

    `piocher(self)`
    :   Méthode qui permet de piocher un domino dans la pioche.
        Enlève le domino pioché de la pioche et renvoie le tuple du domino pioché