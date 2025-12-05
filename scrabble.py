#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_Daniel-Centov_Nikolai-Kolenbet_projet.py : CR projet « scrabble », groupe ima04_B

Daniel-Centov Daniel.Centov@etu.univ-grenoble-alpes.fr
Nikolai-Kolenbet Nikolai.Kolenbet@etu.univ-grenoble-alpes.fr
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers
import random
from unicodedata import name  # pour la pioche aléatoire


# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel


# PARTIE 1 : LE PLATEAU ########################################################


def symetrise_liste(lst) :
    """
    Auxilliaire pour Q1 : symétrise en place la liste lst.
    EB : modification de lst.

    >>> essai = [1,2] ; symetrise_liste(essai) ; essai
    [1, 2, 1]
    >>> essai = [1,2,3] ; symetrise_liste(essai) ; essai
    [1, 2, 3, 2, 1]
    """
    copie_lst = list(lst)
    for i in range(2, len(copie_lst)+1) : lst.append(copie_lst[-i])


def init_bonus() :
    """Q1) Initialise le plateau des bonus."""

    # Compte-tenu  de  la  double   symétrie  axiale  du  plateau,  on
    # a  7  demi-lignes  dans  le  quart  supérieur  gauche,  puis  la
    # (demi-)ligne centrale,  et finalement  le centre. Tout  le reste
    # s'en déduit par symétrie.
    plt_bonus = [  # quart-supérieur gauche + ligne et colonne centrales
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MT'],
        [''  , 'MD', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'MD', ''  , ''  , ''  , 'LD', ''],
        ['LD', ''  , ''  , 'MD', ''  , ''  , ''  , 'LD'],
        [''  , ''  , ''  , ''  , 'MD', ''  , ''  , ''],
        [''  , 'LT', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'LD', ''  , ''  , ''  , 'LD', ''],
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MD']
    ]
    # On transforme les demi-lignes du plateau en lignes :
    for ligne in plt_bonus : symetrise_liste(ligne)
    # On transforme le demi-plateau en plateau :
    symetrise_liste(plt_bonus)

    return plt_bonus


def init_jetons():
    """Q2) Initialise le plateau des jetons vide."""

    board = [['' for _ in range(TAILLE_PLATEAU)] for _ in range(TAILLE_PLATEAU)]

    return board


def affiche_jetons(table_jetons, table_bonus):
    """Q3) Affiche le plateau des jetons j. Q4) Affiche le plateau des jetons avec les bonus visibles."""

    bonus_symboles = {'MT': '*', 'MD': '+', 'LT': '-', 'LD': '/'}

    cell_width = 3
    marge_tete = " " * TAILLE_MARGE

    # entête colonnes
    print(marge_tete, end="")
    for col in range(TAILLE_PLATEAU):
        label = str(col + 1).rjust(cell_width)
        print(label, end=" ")
    print()

    # ligne séparatrice d'en-tête
    print(marge_tete + ("+" + "-" * cell_width) * TAILLE_PLATEAU + "+")


    for lig in range(TAILLE_PLATEAU):

        # numéro de ligne
        line_label = str(lig + 1).rjust(TAILLE_MARGE - 1)
        print(f"{line_label} ", end="|")

        for col in range(TAILLE_PLATEAU):
            jeton = table_jetons[lig][col]
            bonus_val = table_bonus[lig][col]
            symbole = bonus_symboles.get(bonus_val, '')

            if jeton != "":
                cell = jeton
                if symbole:
                    cell += symbole

            else:
                cell = " " + symbole if symbole else "   "

            cell = cell.ljust(cell_width)
            print(cell, end="|")
        print()


        print(marge_tete + ("+" + "-" * cell_width) * TAILLE_PLATEAU + "+")


# PARTIE 2 : LA PIOCHE #########################################################


def init_pioche_alea():
    """Q7) Initialise la pioche aléatoire des jetons. Obsolete : voir Q20."""

    liste_pioche = []

    for i in range(100):
        lettre = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        liste_pioche.append(lettre)

    if JOKER not in liste_pioche:
        liste_pioche[random.randint(0, 50)] = JOKER
        liste_pioche[random.randint(50, 99)] = JOKER

    if "ABCDEFGHIJKLMNOPQRSTUVWXYZ" not in liste_pioche:

        for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            if lettre not in liste_pioche:
                liste_pioche[random.randint(0, 99)] = lettre

    return liste_pioche


def piocher(sac, x=7):
    """Q8) Pioche x jetons du sac."""

    jetons_pioches = []
    for _ in range(x):

        if sac:
            jeton = sac.pop(random.randint(0, len(sac) - 1))
            jetons_pioches.append(jeton)

    return jetons_pioches


def completer_main(main,sac):
    """Q9) Complète la main du joueur à 7 jetons."""

    while len(main) < 7 and sac:

        jeton = sac.pop(random.randint(0, len(sac) - 1))
        main.append(jeton)

    return main


def echanger(jetons, main, sac):
    """Q10) Échange les jetons donnés entre la main et le sac."""

    for j in jetons:

        if j in main:
            main.remove(j)
            sac.append(j)

    main = completer_main(main, sac)
    return main, sac


# PARTIE 3 : CONSTRUCTIONS DE MOTS #############################################


def generer_dictfr(nf='littre.txt') :
    """Liste des mots Français en majuscules sans accent.

    >>> len(generer_dictfr())
    73085
    """
    mots = []
    with Path(nf).open(encoding='utf_8') as fich_mots :
        for line in fich_mots : mots.append(line.strip().upper())
    return mots


def select_mot_initiale(motsfr,let):
    """Q13) Sélectionne les mots commençant par la lettre let."""

    liste_mots = []

    for i in motsfr:

        if i[0] == let:
            liste_mots.append(i)

    return liste_mots


def select_mot_longueur(motsfr,lgr):
    """Q14) Sélectionne les mots de longueur lgr."""

    liste_mots = []

    for i in motsfr:

        if len(i) == lgr:
            liste_mots.append(i)

    return liste_mots


def mot_jouable(mot, ll):
    """Q15) Vérifie si le mot peut être formé avec les lettres de la liste ll."""

    liste_temp = list(ll)
    for lettre in mot:

        if lettre in liste_temp:
            liste_temp.remove(lettre)

        elif JOKER in liste_temp:
            liste_temp.remove(JOKER)

        else:
            return False
        
    return True


def mots_jouables(motsfr, ll, extra_lett=None):
    """Q16) Sélectionne les mots de motsfr pouvant être formés avec les lettres de la liste ll."""

    if extra_lett is None:
        extra_lett = []

    pool = list(ll) + list(extra_lett)
    playable = []

    max_len = len(pool)

    for mot in motsfr:

        if len(mot) <= max_len:

            if mot_jouable(mot, pool):
                playable.append(mot)

    return playable


def mot_jouable_plateau(mot, main, plateau):
    """Vérifie si le mot peut être formé avec les lettres de la main et celles déjà sur le plateau."""

    index = 0
    taille = len(mot)

    while index < taille:
        lettre = mot[index]
        trouve_plateau = False
        lig = 0

        while lig < TAILLE_PLATEAU and trouve_plateau is False:
            col = 0

            while col < TAILLE_PLATEAU and trouve_plateau is False:

                if plateau[lig][col] == lettre:
                    trouve_plateau = True

                col = col + 1
            lig = lig + 1

        if trouve_plateau is False:

            if lettre in main:
                main.remove(lettre)

            elif JOKER in main:
                main.remove(JOKER)

            else:
                return False
            
        index = index + 1

    return True


# PARTIE 4 : VALEUR D'UN MOT ###################################################


def generer_dico() :
    """Dictionnaire des jetons.

    >>> jetons = generer_dico()
    >>> jetons['A'] == {'occ': 9, 'val': 1}
    True
    >>> jetons['B'] == jetons['C']
    True
    >>> jetons['?']['val'] == 0
    True
    >>> jetons['!']
    Traceback (most recent call last):
    KeyError: '!'
    """
    jetons = {}

    with Path('lettres.txt').open(encoding='utf_8') as lettres :

        for ligne in lettres :
            l, v, o = ligne.strip().split(';')
            jetons[l] = {'occ': int(o), 'val': int(v)}

    return jetons


def init_pioche(dico):
    """Q20) Initialise la pioche des jetons selon le dictionnaire dico."""

    pioche = []

    for lettre, infos in dico.items():
        pioche.extend([lettre] * infos['occ'])

    return pioche


def valeur_mot(mot, dico):
    """Q22) Calcule la valeur du mot selon le dictionnaire dico."""

    valeur = 0

    for lettre in mot:
        valeur += dico[lettre]['val']

    if len(mot) == 7:
        valeur += 50

    return valeur


def meilleur_mot(motsfr, ll, dico, extra_lett=None):
    """Q23) Trouve le mot de plus haute valeur jouable avec les lettres de la liste ll."""

    candidats = mots_jouables(motsfr, ll, extra_lett)

    if not candidats:
        return ""

    best = candidats[0]
    best_score = valeur_mot(best, dico)

    for mot in candidats[1:]:
        s = valeur_mot(mot, dico)

        if s > best_score:
            best = mot
            best_score = s

    return best


def meilleurs_mots(motsfr, ll, dico, extra_lett=None):
    """Q24) Renvoie la liste de tous les mots ayant la même valeur maximale parmi les mots jouables avec les lettres de la liste ll."""

    candidats = mots_jouables(motsfr, ll, extra_lett)

    if not candidats:
        return []

    best_score = -1
    bests = []

    for mot in candidats:
        s = valeur_mot(mot, dico)

        if s > best_score:
            best_score = s
            bests = [mot]

        elif s == best_score:
            bests.append(mot)

    return bests


# PARTIE 5 : Premier programme principal ###################################################


def check_end_game(main_joueur, sac):
    """Q26) Vérifie si la partie doit se terminer."""

    jetons_manquants = 7 - len(main_joueur)

    if jetons_manquants <= 0:
        return False
    
    if len(sac) < jetons_manquants:
        return True
    
    return False


def next_player(current_player, players):
    """Q27) Passe au joueur suivant."""
    current_index = players.index(current_player)
    next_index = (current_index + 1) % len(players)

    return players[next_index]


# PARTIE 6 : Placement de mot ###################################################


def lire_coords():
    """Q29) Lit les coordonnées et l'orientation du placement d'un mot."""

    flag_cords = True

    while flag_cords:
        x = int(input("Entrez la coordonnée x (Colonne 1-15) : ")) - 1

        if x < 0 or x >= TAILLE_PLATEAU:
            print("Coordonnée x invalide. Veuillez réessayer.")

        else:
            y = int(input("Entrez la coordonnée y (Row 1-15) : ")) - 1

            if y < 0 or y >= TAILLE_PLATEAU:
                print("Coordonnée y invalide. Veuillez réessayer.")
            
            else:
                orientation = input("Entrez l'orientation (H pour horizontal, V pour vertical) : ").upper()
                if orientation not in ['H', 'V']:
                    print("Orientation invalide. Veuillez réessayer.")

                else:
                    flag_cords = False

    return x, y, orientation


def tester_placement(plateau, i, j, direction, mot):
    """Q30) Teste si le mot peut être placé aux coordonnées (i,j) dans la direction dir."""

    if direction == 'H':

        if j + len(mot) > TAILLE_PLATEAU:

            return []
        
    else:

        if i + len(mot) > TAILLE_PLATEAU:

            return []
    
    lettres_necessaires = []

    for k in range(len(mot)):

        if direction == 'H':
            lig = i
            col = j + k

        else:
            lig = i + k
            col = j
        
        lettre_plateau = plateau[lig][col]

        if lettre_plateau == "":
            lettres_necessaires.append(mot[k])
            
        elif lettre_plateau != mot[k]:
            return []
            

    return lettres_necessaires


def placer_mot(plateau, bonus, main, mot, i, j, direction, dico):
    """Q31) Place un mot sur le plateau si c'est possible.
    Q32) Calcule le score d'un mot placé en (i,j) en tenant compte des bonus."""

    bonus_lettre = {'LD': 2, 'LT': 3}
    bonus_mot = {'MD': 2, 'MT': 3}

    lettres_a_poser = tester_placement(plateau, i, j, direction, mot)
    
    if lettres_a_poser == []:
        return False, 0
        
    main_temp = list(main)
    jetons_a_retirer = []
    
    for lett in lettres_a_poser:

        if lett in main_temp:
            main_temp.remove(lett)
            jetons_a_retirer.append(lett)

        elif JOKER in main_temp:
            main_temp.remove(JOKER)
            jetons_a_retirer.append(JOKER)

        else:
            return False, 0
                
    for jeton in jetons_a_retirer:
        main.remove(jeton)

    score = 0
    multiplicateur_mot_total = 1
    lettres_posees = 0

    for k in range(len(mot)):

        if direction == 'V':
            lig = i + k
            col = j

        else:
            lig = i
            col = j + k
        
        lettre_mot = mot[k]
        case_actuelle = plateau[lig][col]
        bonus_case = bonus[lig][col]

        if case_actuelle == "":
            plateau[lig][col] = lettre_mot
            lettres_posees += 1

            if bonus_case in bonus_lettre:
                score += dico[lettre_mot]['val'] * bonus_lettre[bonus_case]

            else:
                score += dico[lettre_mot]['val']

            if bonus_case in bonus_mot:
                multiplicateur_mot_total *= bonus_mot[bonus_case]

        else:
            score += dico[lettre_mot]['val']

    if lettres_posees == 7:
        score += 50

    score *= multiplicateur_mot_total

    for k in range(len(mot)):

        if direction == 'V':
            lig = i + k
            col = j

        else:
            lig = i
            col = j + k

        if bonus[lig][col] != "" and plateau[lig][col] == mot[k]:
            bonus[lig][col] = ""
            
    return True, score


# PARTIE 7 : Programe Principale Final ###################################################


def tour_joueur(name, players_infos, pioche, mots_fr, dico, plateau, bonus, pas_tour_total):
    """Q25) Gère le tour d'un joueur."""

    affiche_jetons(plateau, bonus)
    print(f"C'est à votre tour {name} de jouer !")
    flag = True

    while flag:
        print("Voici vos jetons : ", players_infos[name]['main'])
        choix = input("Entrez le mot que vous souhaitez jouer (passer/echanger/proposer): ").lower()

        if choix == "passer":
            print(f"{name} a choisi de passer son tour.")
            flag = False
            pas_tour_total[0] += 1
        
        elif choix == "echanger":
            jetons_a_echanger = input("Entrez les jetons que vous souhaitez échanger (sans espace) (b4 pour revenir) : ").upper()

            if jetons_a_echanger != "B4" and jetons_a_echanger != "" and all("A" <= i <= "Z" or i == JOKER for i in jetons_a_echanger):
                players_infos[name]['main'], pioche = echanger(list(jetons_a_echanger), players_infos[name]['main'], pioche)
                print(f"{name} a échangé les jetons {jetons_a_echanger}.")
                flag = False
                pas_tour_total[0] = 0

            elif jetons_a_echanger != "B4":
                print("Jetons invalides. Veuillez réessayer.")
        
        elif choix == "proposer":
            mot_propose = input("Entrez le mot que vous souhaitez proposer (b4 pour revenir): ").upper()

            if mot_propose != "B4" and mot_propose != "" and all("A" <= i <= "Z" for i in mot_propose) and len(mot_propose) >= 2:
                main_temp = list(players_infos[name]['main'])

                if mot_jouable_plateau(mot_propose, main_temp, plateau):

                    if mot_propose in mots_fr:
                        x, y, direction = lire_coords()
                        flag_placement = True
                        
                        while flag_placement:
                            can_place, score = placer_mot(plateau, bonus, players_infos[name]['main'], mot_propose, y, x, direction, dico)

                            if can_place:
                                players_infos[name]['score'] += score
                                print(f"Le mot {mot_propose} a été placé avec succès et vous rapporte {score} points. Votre score total est maintenant de {players_infos[name]['score']} points.")
                                flag_placement = False

                            else:
                                print(f"Le mot {mot_propose} ne peut pas être placé aux coordonnées ({x+1}, {y+1}) en direction {'vertical' if direction == 'V' else 'horizontal'}. Veuillez réessayer les coordonnées et l'orientation.")
                                x, y, direction = lire_coords()                          

                        players_infos[name]['main'] = completer_main(players_infos[name]['main'], pioche)
                        flag = False
                        pas_tour_total[0] = 0

                    else:
                        print(f"Le mot {mot_propose} n'est pas dans le dictionnaire. Veuillez réessayer.")

                else:
                    print(f"Le mot {mot_propose} ne peut pas être formé avec vos jetons. Veuillez réessayer.")

            elif mot_propose != "B4":
                print("Mot invalide. Veuillez réessayer.")

        else:
            print("Choix invalide. Veuillez réessayer.")


def play_scrabble():
    """Q28) Programme principal du jeu de Scrabble."""

    flag = True

    while flag:
        nb_joueurs = int(input("Entrez le nombre de joueurs (2-4): "))

        if nb_joueurs not in (2, 3, 4):
            print("Nombre de joueurs invalide. Veuillez entrer un numero valide (2-4).")

        else:
            flag = False

    # Lecture dictionnaires
    mots_fr = generer_dictfr()
    dico = generer_dico()
    pioche = init_pioche(dico)

    # Plateau
    plateau = init_jetons()
    bonus = init_bonus()

    players = {}
    for i in range(nb_joueurs):
        name = input(f"Entrez le nom du joueur {i+1}: ")
        flag_name = True
        while flag_name:
            if name in players:
                name = input("Ce nom est déjà pris. Veuillez entrer un autre nom: ")
            
            elif name.strip() == "":
                name = f'Joueur{i+1}'

            else:
                flag_name = False

        main_joueur = piocher(pioche, 7)
        players[name] = {'main': main_joueur, 'score': 0}

    print("--------------Le jeu commence !--------------")

    player = None
    for tmp in players:
        main = players[tmp]['main']

        lettre = None
        for c in main:
            if c != '?':
                if lettre is None:
                    lettre = c

                elif c < lettre:
                    lettre = c

        if player is None:
            player = tmp
            best_letter = lettre

        if lettre < best_letter:
            player = tmp
            best_letter = lettre
    
    print(f"{player} commence la partie !")

    pas_tour_total = [0]
    play = True

    while play:

        if check_end_game(players[player]['main'], pioche):
            play = False
            print("La partie est terminée !")

        elif pas_tour_total[0] >= nb_joueurs * 3:
            play = False
            print("La partie est terminée après 3 tours consécutifs de passage !")

        else:
            print(f"Il reste {len(pioche)} jetons dans la pioche.")
            tour_joueur(player, players, pioche, mots_fr, dico, plateau, bonus, pas_tour_total)
            player = next_player(player, list(players.keys()))
    
    print("--------------Fin du jeu !--------------")

    for name, info in players.items():
        sum = 0

        for lettre in info['main']:
            sum += dico[lettre]['val']

        info['score'] -= sum
        print(f"{name} a un score de {info['score']} points.")
    
    max_score = -99999
    winners = []

    for name in players:
        score = players[name]['score']

        if score > max_score:
            max_score = score
            winners = []
            winners.append(name)

        elif score == max_score:
            winners.append(name)

    if len(winners) == 1:
        print(f"Le gagnant est {winners[0]} avec {max_score} points !")
    else:
        print(f"Il y a une égalité entre les joueurs suivants avec {max_score} points : {', '.join(winners)}")


if __name__ == "__main__":
    play_scrabble()


# DEBUG (Try functions) #######################################################

"""
# Q1) Initialiser les bonus
bonus = init_bonus()

# Q2) Initialiser les jetons
jetons = init_jetons()

# 1. Afficher le plateau vide (Q5) 
affiche_jetons(jetons, bonus)

# 2. Test Q4 : Plaçons un jeton 'A' sur un bonus 'MD'

# jetons[1][1] = 'A' # (1,1) est 'MD' -> '+'
# jetons[5][5] = 'B' # (5,5) est 'LT' -> '-'
# jetons[0][3] = 'C' # (0,3) est 'LD' -> '/'
# jetons[0][0] = 'C' # (0,0) est 'MT' -> '*'
# jetons[0][1] = 'E' # (0,1) est vide

# Affiche le plateau avec les jetons ET les bonus
affiche_jetons(jetons, bonus)


# Q7) Initialiser la pioche aléatoire
dico = generer_dico()
pioche = init_pioche(dico)
print(pioche)
print("Pioche initiale (100 jetons) :", len(pioche))

# Q8) Piocher 7 jetons
main_joueur1 = piocher(pioche, 7)
print("Main du joueur 1 (7 jetons) :", main_joueur1)
main_joueur2 = piocher(pioche, 7)
print("Main du joueur 2 (7 jetons) :", main_joueur2)

# Q11) Échanger des jetons entre la main du joueur 2 et le sac
echanger(main_joueur2[:3], main_joueur2, pioche)
print("Main du joueur 2 après échange de 3 jetons :", main_joueur2)
print("Pioche après échange :", len(pioche), "jetons restants")


# Q12) Générer le dictionnaire français
mots_fr = generer_dictfr()
print("Nombre de mots dans le dictionnaire français :", len(mots_fr))

# Q13) Sélectionner les mots commençant par 'Y'
mots_commencant_par_Y = select_mot_initiale(mots_fr, 'Y')
print("Mots commençant par 'Y' :", len(mots_commencant_par_Y))

# Q14) Sélectionner les mots de longueur 19
mots_longueur_19 = select_mot_longueur(mots_fr, 19)
print("Mots de longueur 19 :", len(mots_longueur_19))


# Q19) Générer le dictionnaire des jetons et le tester
print(dico)
print('Occurence K', dico['K']['occ'])
print('Valeur Z', dico['Z']['val'])
"""