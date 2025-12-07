#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_Daniel_Nikolai_projet.py : CR projet « scrabble », groupe ima04_B

Daniel-Centov Daniel.Centov@etu.univ-grenoble-alpes.fr
Nikolai-Kolenbet Nikolai.Kolenbet@etu.univ-grenoble-alpes.fr
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers
import random # génération aléatoire
import tkinter as tk # interface graphique
from tkinter import messagebox, simpledialog # boîtes de dialogue
import copy # copies profondes
import json   # pour les stats
import pickle

from matplotlib.pyplot import flag # pour la sauvegarde

# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

# ⚠ pas de variable globales, sauf cas exceptionnel

COULEURS = {
    'MT': '#ff3333',
    'MD': '#ffcc00',
    'LT': '#3333ff',
    'LD': '#add8e6',
    'NORMAL': '#006400',
    'LETTRE': '#f0e68c'
}

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
    haut_du_plateau = plt_bonus[:7]
    bas_du_plateau = copy.deepcopy(haut_du_plateau)
    bas_du_plateau.reverse()
    plt_bonus.extend(bas_du_plateau)

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
        line_label = chr(ord('A') + lig).ljust(TAILLE_MARGE - 1)
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

    # Génération aléatoire des lettres
    for i in range(100):
        lettre = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        liste_pioche.append(lettre)

    # Garantie de la présence des jokers et de toutes les lettres
    if JOKER not in liste_pioche:
        liste_pioche.insert(random.randint(0, 50), JOKER)
        liste_pioche.insert(random.randint(50, 99), JOKER)

    if "ABCDEFGHIJKLMNOPQRSTUVWXYZ" not in liste_pioche:

        for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            if lettre not in liste_pioche:
                flag = True

                while flag:
                    x = random.randint(0, 99)

                    if liste_pioche[x] == JOKER:
                        x = random.randint(0, 99)

                    else:
                        flag = False

                liste_pioche[x] = lettre

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
        for line in fich_mots : 
            mot = line.strip().upper()

            if mot.isalpha():
                    mots.append(mot)

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


def mots_jouables(motsfr, ll):
    """Q16) Sélectionne les mots de motsfr pouvant être formés avec les lettres de la liste ll."""

    pool = list(ll)
    playable = []

    max_len = len(pool)

    for mot in motsfr:

        if len(mot) <= max_len:

            if mot_jouable(mot, pool):
                playable.append(mot)

    return playable


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

    # Initialisation de la pioche
    for lettre, infos in dico.items():
        pioche.extend([lettre] * infos['occ'])

    return pioche


def valeur_mot(mot, dico):
    """Q22) Calcule la valeur du mot selon le dictionnaire dico."""

    valeur = 0

    # Calcul du score
    for lettre in mot:
        if lettre in dico:
            valeur += dico[lettre]['val']

    if len(mot) == 7:
        valeur += 50

    return valeur


def meilleur_mot(motsfr, ll, dico):
    """Q23) Trouve le mot de plus haute valeur jouable avec les lettres de la liste ll."""

    candidats = mots_jouables(motsfr, ll)

    if not candidats:
        return ""

    best = candidats[0]
    best_score = valeur_mot(best, dico)

    # Parcours des candidats pour trouver le meilleur mot
    for mot in candidats[1:]:
        s = valeur_mot(mot, dico)

        if s > best_score:
            best = mot
            best_score = s

    return best


def meilleurs_mots(motsfr, ll, dico):
    """Q24) Renvoie la liste de tous les mots ayant la même valeur maximale parmi les mots jouables avec les lettres de la liste ll."""

    candidats = mots_jouables(motsfr, ll)

    if not candidats:
        return []

    best_score = -1
    bests = []

    # Parcours des candidats pour trouver les meilleurs mots
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

    # Boucle de saisie des coordonnées et de l'orientation
    while flag_cords:
        x = int(input("Entrez la coordonnée x (Colonne 1-15) : ")) - 1

        if x < 0 or x >= TAILLE_PLATEAU:
            print("Coordonnée x invalide. Veuillez réessayer.")

        else:
            y = ord(input("Entrez la coordonnée y (Row A-O) : ").upper()) - ord('A')

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

    # Vérification des limites du plateau
    if direction == 'H':
        if j + len(mot) > TAILLE_PLATEAU: 
            return False, "Le mot dépasse du plateau (Horizontal)."

    elif direction == 'V':
        if i + len(mot) > TAILLE_PLATEAU: 
            return False, "Le mot dépasse du plateau (Vertical)."
        
    else:
        return False, "Direction invalide."
    
    # Vérification du plateau vide
    plateau_vide = True
    for lig in range(TAILLE_PLATEAU):
        for col in range(TAILLE_PLATEAU):
            if plateau[lig][col] != "":
                plateau_vide = False

    touche_case_centrale = False
    touche_autre_mot = False
    lettres_necessaires = []

    # Vérification des lettres nécessaires
    for k in range(len(mot)):
        if direction == 'H':
            lig, col = i, j + k

        elif direction == 'V':
            lig, col = i + k, j

        else:
            return False, "Direction invalide."

        if lig == 7 and col == 7:
            touche_case_centrale = True

        lettre_plateau = plateau[lig][col]

        if lettre_plateau != "":
            touche_autre_mot = True

            if lettre_plateau != mot[k]:
                return False, f"Conflit de lettres : {lettre_plateau} sur le plateau vs {mot[k]}."
            
        else:
            lettres_necessaires.append(mot[k])
            if lig > 0 and plateau[lig-1][col] != "": 
                touche_autre_mot = True
            elif lig < 14 and plateau[lig+1][col] != "": 
                touche_autre_mot = True
            elif col > 0 and plateau[lig][col-1] != "": 
                touche_autre_mot = True
            elif col < 14 and plateau[lig][col+1] != "": 
                touche_autre_mot = True

    # Vérifications finales
    if plateau_vide:
        if not touche_case_centrale:
            return False, "Le premier mot doit passer par l'étoile centrale (H8)."
    else:
        if not touche_autre_mot:
            return False, "Le mot doit être rattaché à un mot existant."
        
    if not lettres_necessaires and not plateau_vide:
        return False, "Le mot doit apporter au moins une nouvelle lettre."
        
    return True, lettres_necessaires

def placer_mot(plateau, bonus, main, mot, i, j, direction, dico):
    """Q31) Place un mot sur le plateau si c'est possible.
    Q32) Calcule le score d'un mot placé en (i,j) en tenant compte des bonus.
    Q33) Bonus: Calcule les scores des mots orthogonaux créés par le placement du mot."""

    ok, res = tester_placement(plateau, i, j, direction, mot)
    
    # Vérification disponibilité lettres
    if not ok:
        return False, 0, res
    
    lettres_a_poser = res

    main_temp = list(main)
    for lett in lettres_a_poser:
        if lett in main_temp:
            main_temp.remove(lett)

        elif JOKER in main_temp:
            main_temp.remove(JOKER)

        else:
            return False, 0, f"Il vous manque la lettre : {lett}"
            
    # Application
    for lett in lettres_a_poser:
        if lett in main: 
            main.remove(lett)

        else: 
            main.remove(JOKER)

    score_total = 0
    multiplicateur_mot_principal = 1
    score_mot_principal = 0
    nb_nouvelles = 0

    # Calcul du score
    for k in range(len(mot)):
        if direction == 'H': 
            lig, col = i, j + k
            dir_ortho = 'V'

        elif direction == 'V':
            lig, col = i + k, j
            dir_ortho = 'H'

        else:
            return False, 0, "Direction invalide."
        
        lettre = mot[k]
        ancienne_lettre = plateau[lig][col]
        
        plateau[lig][col] = lettre
        val_lettre = dico.get(lettre, {'val':0})['val']

        mult_lettre_principal = 1
        
        if ancienne_lettre == "":
            nb_nouvelles += 1
            b = bonus[lig][col]

            if b == 'LD': 
                mult_lettre_principal = 2

            elif b == 'LT': 
                mult_lettre_principal = 3

            elif b == 'MD': 
                multiplicateur_mot_principal = 2

            elif b == 'MT': 
                multiplicateur_mot_principal = 3

            # Q33 Calcul des mots orthogonaux
            if dir_ortho == 'V':
                voisin_av = (lig > 0 and plateau[lig-1][col] != "")
                voisin_ap = (lig < 14 and plateau[lig+1][col] != "")

            elif dir_ortho == 'H':
                voisin_av = (col > 0 and plateau[lig][col-1] != "")
                voisin_ap = (col < 14 and plateau[lig][col+1] != "")

            if voisin_av or voisin_ap:
                l_start, c_start = lig, col
                l_end, c_end = lig, col
                
                # Trouver les limites du mot adjacent
                if dir_ortho == 'V':
                    while l_start > 0 and plateau[l_start-1][col] != "": 
                        l_start -= 1

                    while l_end < 14 and plateau[l_end+1][col] != "": 
                        l_end += 1
                elif dir_ortho == 'H':
                    while c_start > 0 and plateau[lig][c_start-1] != "": 
                        c_start -= 1

                    while c_end < 14 and plateau[lig][c_end+1] != "": 
                        c_end += 1
                
                mot_ortho_str = ""
                mot_ortho_score = 0
                mot_ortho_mult = 1
                curr_l, curr_c = l_start, c_start

                flag = True
                while flag:
                    # Calcul du score du mot orthogonal
                    l_val = dico.get(plateau[curr_l][curr_c], {'val':0})['val']
                    
                    # Application des bonus si cette lettre est la nouvelle lettre posée
                    if curr_l == lig and curr_c == col:

                        if b == 'LD': 
                            l_val *= 2

                        elif b == 'LT': 
                            l_val *= 3

                        elif b == 'MD': 
                            mot_ortho_mult *= 2

                        elif b == 'MT': 
                            mot_ortho_mult *= 3
                    
                    mot_ortho_score += l_val
                    mot_ortho_str += plateau[curr_l][curr_c]
                    
                    # Avancer dans la direction orthogonale
                    if curr_l == l_end and curr_c == c_end: 
                        flag = False
                    
                    elif dir_ortho == 'V': 
                        curr_l += 1

                    elif dir_ortho == 'H':
                        curr_c += 1
                
                score_total += (mot_ortho_score * mot_ortho_mult)

            bonus[lig][col] = ""
            
        # Ajout de la lettre au score du mot principal
        score_mot_principal += (val_lettre * mult_lettre_principal)

    # Ajout du score du mot principal
    score_total += (score_mot_principal * multiplicateur_mot_principal)

    if nb_nouvelles == 7: 
        score_total += 50
        
    return True, score_total, "OK"


# PARTIE 7 : Programme Principal Final ###################################################


def tour_joueur(name, players_infos, pioche, mots_fr, dico, plateau, bonus, pas_tour_total):
    """Q25) Gère le tour d'un joueur."""

    affiche_jetons(plateau, bonus)
    print(f"C'est à votre tour {name} de jouer !")
    flag = True

    # Boucle du tour
    while flag:
        print("Voici vos jetons : ", players_infos[name]['main'])
        choix = input("Entrez le mot que vous souhaitez jouer (show/hint/passer/echanger/proposer): ").lower()

        # Traitement du choix
        if choix == "passer":
            print(f"{name} a choisi de passer son tour.")
            flag = False
            pas_tour_total[0] += 1
        
        elif choix == "hint":
            best_mots = meilleurs_mots(mots_fr, players_infos[name]['main'], dico)

            if not best_mots:
                print("Aucun mot jouable avec vos jetons.")
            else:
                best_score = valeur_mot(best_mots[0], dico)
                print(f"Meilleur(s) mot(s) jouable(s) avec vos jetons pour {best_score} points : {', '.join(best_mots)}")

        elif choix == "show":
            affiche_jetons(plateau, bonus)

        elif choix == "echanger":
            jetons_a_echanger = input("Entrez les jetons que vous souhaitez échanger (sans espace) (b4 pour revenir) : ").upper()

            # Validation des jetons à échanger
            if jetons_a_echanger != "B4" and jetons_a_echanger != "" and all("A" <= i <= "Z" or i == JOKER for i in jetons_a_echanger):
                players_infos[name]['main'], pioche = echanger(list(jetons_a_echanger), players_infos[name]['main'], pioche)
                print(f"{name} a échangé les jetons {jetons_a_echanger}.")
                flag = False
                pas_tour_total[0] = 0

            elif jetons_a_echanger != "B4":
                print("Jetons invalides. Veuillez réessayer.")
        
        elif choix == "proposer":
            mot_propose = input("Entrez le mot que vous souhaitez proposer (b4 pour revenir): ").upper()

            if mot_propose == "B4":
                print("Retour.")
            
            elif mot_propose not in mots_fr:
                print(f"Le mot {mot_propose} n'est pas dans le dictionnaire.")

            else:
                print(f"Où placer le début du mot {mot_propose} ?")
                x, y, direction = lire_coords()
                succes, score = placer_mot(plateau, bonus, players_infos[name]['main'], mot_propose, y, x, direction, dico)

                if succes:
                    print(f"Bravo ! {mot_propose} posé pour {score} points.")
                    players_infos[name]['score'] += score
                    
                    completer_main(players_infos[name]['main'], pioche)
                    
                    pas_tour_total[0] = 0
                    flag = False

                else:
                    print("Placement impossible (manque de place, lettres non correspondantes, ou lettres manquantes en main).")

        else:
            print("Choix invalide. Veuillez réessayer.")


def play_scrabble():
    """Q28) Programme principal du jeu de Scrabble."""

    flag = True

    # Nombre de joueurs
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

    # Initialisation joueurs
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

    # Détermination du premier joueur
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

    # Boucle principale de jeu
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

    # Calcul des scores finaux
    for name, info in players.items():
        sum = 0

        for lettre in info['main']:
            sum += dico[lettre]['val']

        info['score'] -= sum
        print(f"{name} a un score de {info['score']} points.")
    
    max_score = -99999
    winners = []

    # Détermination du ou des gagnants
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


# PARTIE 8 : INTERFACE GRAPHIQUE COMPLÈTE ######################################


def lancer_graphique():
    """Fonction principale de l'interface graphique (Tkinter)."""
    
    # Initialisation des données
    mots_fr = generer_dictfr()
    dico = generer_dico()
    bonus = init_bonus()
    plateau = init_jetons()
    pioche = init_pioche(dico)
    
    # Variables d'état
    noms_joueurs = []
    players = {}
    etat = {
        'joueur_actuel_idx': 0, 
        'passes_consecutifs': 0, 
        'mode_pc': False,
        'fin_partie': False
    }

    scrabbles_count = {}

    
    def trouver_meilleur_coup(main_joueur):
        """Cherche un mot jouable avec la main qui rentre sur le plateau."""

        # Recherche des candidats
        candidats = meilleurs_mots(mots_fr, main_joueur, dico)

        meilleur_coup = None
        meilleur_score = -1
        
        # Recherche du meilleur coup
        for mot in candidats[:30]:
            for i in range(TAILLE_PLATEAU):
                for j in range(TAILLE_PLATEAU):
                    for d in ['H', 'V']:
                        ok, _ = tester_placement(plateau, i, j, d, mot)
                        
                        if ok:
                            plateau_temp = copy.deepcopy(plateau)
                            bonus_temp = copy.deepcopy(bonus)
                            main_temp = list(main_joueur)

                            succes, pts, _ = placer_mot(plateau_temp, bonus_temp, main_temp, mot, i, j, d, dico)
                            
                            if succes and pts > meilleur_score:
                                meilleur_score = pts
                                meilleur_coup = (mot, i, j, d)

        return meilleur_coup
                        
    
    def tour_ordi():
        """Logique du tour de l'ordinateur."""

        nom, infos = "Ordinateur", players["Ordinateur"]
        # Recherche du meilleur coup
        coup = trouver_meilleur_coup(infos['main'])
        
        # Exécution du coup
        if coup:
            mot, i, j, d = coup
            ok, pts, msg = placer_mot(plateau, bonus, infos['main'], mot, i, j, d, dico)

            if ok:
                infos['score'] += pts
                completer_main(infos['main'], pioche)
                etat['passes_consecutifs'] = 0

                rafraichir_affichage()
                fenetre.update_idletasks()

                messagebox.showinfo("Ordinateur", f"L'ordi a joué {mot} pour {pts} points !")
                changer_joueur()

            else:
                print(f"Erreur Ordi: {msg}")
                action_passer()

        else:
            if len(pioche) >= 7:
                echanger(infos['main'], infos['main'], pioche)
                messagebox.showinfo("Ordinateur", "L'ordi échange ses lettres.")
                etat['passes_consecutifs'] += 1
                changer_joueur()

            else:
                action_passer()


    def get_joueur_courant():
        """Renvoie le nom et les infos du joueur courant."""

        nom = noms_joueurs[etat['joueur_actuel_idx']]
        return nom, players[nom]

    
    def rafraichir_affichage():
        """Met à jour l'écran de jeu."""
    
        # Vérification de fin de partie
        if etat['fin_partie']: 
            return

        # Mise à jour des éléments graphiques
        for i in range(TAILLE_PLATEAU):
            for j in range(TAILLE_PLATEAU):
                lettre = plateau[i][j]
                b_val = bonus[i][j]
                lbl = grille_labels[i][j]
                
                if lettre != "":
                    lbl.config(text=lettre, bg=COULEURS['LETTRE'], fg='black', relief="raised")

                else:
                    couleur = COULEURS.get(b_val, COULEURS['NORMAL'])
                    texte = b_val if b_val else ""
                    lbl.config(text=texte, bg=couleur, fg='white', relief="sunken")
        
        # Mise à jour des éléments graphiques hors-plateau
        nom, infos = get_joueur_courant()
        lbl_tour.config(text=f"C'est à {nom} de jouer", fg="blue")
        lbl_main.config(text=f"Main {nom} :  {' '.join(infos['main'])}")
        lbl_pioche.config(text=f"Pioche : {len(pioche)}")
        
        txt_scores = "   ".join([f"{n}: {d['score']}" for n, d in players.items()])
        lbl_scores.config(text=txt_scores)


    def action_retour_menu():
        """Arrête la partie en cours et revient au menu."""

        reponse = messagebox.askyesno("Menu Principal", "Voulez-vous vraiment quitter la partie en cours ?\nTout progrès non sauvegardé sera perdu.")

        if reponse:
            frame_jeu.pack_forget()
            frame_mode.pack(pady=50)

    
    def quitter_programme():
        """Quitte le programme."""

        reponse = messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter le jeu ?\nTout progrès non sauvegardé sera perdu.")

        if reponse:
            fenetre.quit()


    def changer_joueur():
        """Passer au joueur suivant."""

        etat['joueur_actuel_idx'] = (etat['joueur_actuel_idx'] + 1) % len(noms_joueurs)
        rafraichir_affichage()
        
        # Tour de l'ordi si necessaire
        if etat['mode_pc'] and get_joueur_courant()[0] == "Ordinateur":
            fenetre.after(1000, tour_ordi)



    def action_passer():
        """Le joueur passe son tour."""

        nom, _ = get_joueur_courant()
        etat['passes_consecutifs'] += 1
        
        # Vérification de fin de partie
        if etat['passes_consecutifs'] >= len(noms_joueurs) * 3:
            gerer_fin("Blocage (trop de passes)")

        # Sinon, passer le tour
        else:
            messagebox.showinfo("Passer", f"{nom} passe son tour.")

            changer_joueur()


    def action_echanger():
        """Le joueur échange des lettres."""

        nom, infos = get_joueur_courant()

        # Lecture de l'entrée
        saisie = entree_echange.get().upper().strip()
        
        # Vérifications basiques
        if not saisie: 
            return
        
        lettres = list(saisie)
        
        if len(pioche) < 7:
            messagebox.showwarning("Blocage", "Il reste moins de 7 lettres dans la pioche.\n" \
            "Vous ne pouvez plus échanger.\n\n" \
            "Si vous ne pouvez pas jouer de mot, cliquez sur 'PASSER TOUR'.\n (La partie finira si tous les joueurs passent).")
            return
        
        # Vérification que le joueur possède bien les lettres à échanger
        copie_main = list(infos['main'])
        possible = True
        for l in lettres:

            if l in copie_main: 
                copie_main.remove(l)

            else: 
                possible = False
            
        # Échange des lettres si possible
        if possible:
            nouvelle_main, _ = echanger(lettres, infos['main'], pioche)
            infos['main'] = nouvelle_main
            entree_echange.delete(0, tk.END)
            messagebox.showinfo("Succès", "Lettres échangées.")
            etat['passes_consecutifs'] = 0
            changer_joueur()

        else:
            messagebox.showerror("Erreur", "Vous n'avez pas ces lettres.")


    def action_jouer():
        """Le joueur tente de placer un mot."""

        nom, infos = get_joueur_courant()
        
        # Lecture des entrées
        mot = entree_mot.get().upper().strip()
        s_lig = entree_lig.get().upper().strip()
        s_col = entree_col.get().strip()
        direction = entree_dir.get().upper().strip()
        
        # Vérifications basiques
        if not (mot and s_lig and s_col and direction): 
            return
        
        if mot not in mots_fr:
            messagebox.showerror("Erreur", "Mot inconnu.")
            return

        if not s_lig or not s_col:
            messagebox.showerror("Erreur", "Coordonnées invalides.")
            return
        
        lig = ord(s_lig[0]) - 65
        col = int(s_col) - 1
        
        if lig < 0 or lig >= 15 or col < 0 or col >= 15:
            messagebox.showerror("Erreur", "Coordonnées invalides.")
            return

        if not (0 <= lig < 15 and 0 <= col < 15): 
            return

        taille_main_avant = len(infos['main'])

        # Placement du mot
        ok, pts, msg = placer_mot(plateau, bonus, infos['main'], mot, lig, col, direction, dico)
        
        if ok:
            infos['score'] += pts
            lettres_posees = taille_main_avant - len(infos['main'])

            if lettres_posees == 7:
                scrabbles_count[nom] = scrabbles_count.get(nom, 0) + 1

            completer_main(infos['main'], pioche)
            etat['passes_consecutifs'] = 0
            messagebox.showinfo("Bravo", f"{mot} posé ! +{pts} pts.")
            
            # Rafraîchissement de l'affichage
            entree_mot.delete(0, tk.END)
            entree_lig.delete(0, tk.END)
            entree_col.delete(0, tk.END)
            entree_dir.delete(0, tk.END)
            
            if not pioche and not infos['main']:
                gerer_fin("Plus de jetons", joueur_finissant=nom)

            else:
                changer_joueur()

        else:
            messagebox.showerror("Erreur Placement ", msg)


    def action_indice_mots():
        """Aide 1 : Trouve des mots jouables avec la main"""

        nom, infos = get_joueur_courant()
        
        liste_main = mots_jouables(mots_fr, infos['main'])
        liste_main = list(set(liste_main))
        liste_main.sort(key=len, reverse=True)
        
        mots_plateau = set()
        
        lettres_board_coords = []
        for i in range(TAILLE_PLATEAU):
            for j in range(TAILLE_PLATEAU):
                if plateau[i][j] != "":
                    lettres_board_coords.append((plateau[i][j], i, j))
        
        if not lettres_board_coords:
            # Premier mot : tous les mots jouables
            if not plateau[7][7]:
                 mots_plateau = set(liste_main)

        else:
            # Recherche des mots pouvant se connecter au plateau
            for lettre_p, lig_p, col_p in lettres_board_coords:
                main_virtuelle = infos['main'] + [lettre_p]
                candidats = mots_jouables(mots_fr, main_virtuelle)
                
                for mot in candidats:
                    for k in range(len(mot)):
                        if mot[k] == lettre_p:
                            if tester_placement(plateau, lig_p, col_p - k, 'H', mot)[0]:
                                mots_plateau.add(mot)
                            
                            if tester_placement(plateau, lig_p - k, col_p, 'V', mot)[0]:
                                mots_plateau.add(mot)

        liste_plateau = list(mots_plateau)
        liste_plateau.sort(key=len, reverse=True)
        
        # Affichage des résultats
        msg = ""
        
        msg += "LISTE 1 : Avec ta main uniquement \n"
        if liste_main:
            msg += ", ".join(liste_main[:20])

            if len(liste_main) > 20: 
                msg += "..."

        else:
            msg += "(Rien)"
            
        msg += "\n\n"
        msg += "LISTE 2 : En utilisant le plateau \n"

        if liste_plateau:
            msg += ", ".join(liste_plateau[:20])

            if len(liste_plateau) > 20: 
                msg += "..."

        else:
            msg += "(Aucun mot ne peut se connecter ou manque de place)"
            
        messagebox.showinfo("Indice Détaillé", msg)

    
    def action_indice_placement():
        """Aide 2 : Demande un mot et trouve son meilleur emplacement."""

        nom, infos = get_joueur_courant()
        
        # Demande du mot à placer
        mot = simpledialog.askstring("Meilleur Placement", "Quel mot veux-tu placer ?")
        if not mot: 
            return
        
        mot = mot.upper().strip()
        
        if mot not in mots_fr:
            messagebox.showwarning("Attention", "Ce mot n'est pas dans le dictionnaire !")
            return

        meilleur_score = -1
        meilleur_coord = None
        
        # Recherche du meilleur emplacement
        for i in range(TAILLE_PLATEAU):
            for j in range(TAILLE_PLATEAU):
                for d in ['H', 'V']:
                    ok, _ = tester_placement(plateau, i, j, d, mot)

                    if ok:
                        p_temp = copy.deepcopy(plateau)
                        b_temp = copy.deepcopy(bonus)
                        m_temp = list(infos['main'])
                        
                        succes, pts, _ = placer_mot(p_temp, b_temp, m_temp, mot, i, j, d, dico)
                        
                        if succes and pts > meilleur_score:
                            meilleur_score = pts
                            meilleur_coord = (i, j, d)

        # Affichage du meilleur emplacement
        if meilleur_coord:
            i, j, d = meilleur_coord
            coord = f"{chr(i+65)}{j+1}"
            messagebox.showinfo("Résultat", f"Le meilleur endroit pour '{mot}' est :\n\nCase : {coord}\nDirection : {d}\nScore : {meilleur_score} points")

        else:
            messagebox.showerror("Impossible", f"Tu ne peux pas placer '{mot}' (manque de place ou lettres manquantes).")


    def gerer_fin(raison, joueur_finissant=None):
        """Gère la fin de la partie."""

        etat['fin_partie'] = True
        msg = f"FIN DE PARTIE ({raison})\n\n"

        total_reliquat_adversaires = 0

        # Calcul des scores finaux
        for nom, p in players.items():
            valeur_main = 0
            for l in p['main']:
                if l in dico:
                    valeur_main += dico[l]['val']
            
            p['score'] -= valeur_main

            if joueur_finissant and nom != joueur_finissant:
                total_reliquat_adversaires += valeur_main

            msg += f"{nom}: {p['score']} pts (Reliquat restant : -{valeur_main})\n"
        
        # Bonus pour le joueur finissant
        if joueur_finissant:
            players[joueur_finissant]['score'] += total_reliquat_adversaires
            msg += f"\nBONUS : {joueur_finissant} a fini et récupère {total_reliquat_adversaires} pts des adversaires !\n"
            msg += f"=> Score final {joueur_finissant} : {players[joueur_finissant]['score']} pts\n"

        # Determination du gagnant
        gagnant = max(players, key=lambda n: players[n]['score'])
        msg += f"\n GAGNANT : {gagnant} !"

        # Mise à jour des stats
        mettre_a_jour_stats(gagnant)

        messagebox.showinfo("Résultats", msg)
        frame_jeu.pack_forget()
        frame_mode.pack(pady=50)


    def demarrer_jeu(mode, liste_noms):
        """Initialise et démarre une nouvelle partie."""

        # Réinitialisation des données
        etat['mode_pc'] = (mode == "PVE")
        scrabbles_count.clear()
        noms_joueurs.clear()
        players.clear()

        pioche[:] = init_pioche(dico)

        nouveau_plateau = init_jetons()
        for i in range(TAILLE_PLATEAU):
            for j in range(TAILLE_PLATEAU):
                plateau[i][j] = nouveau_plateau[i][j]

        nouveaux_bonus = init_bonus()
        for i in range(TAILLE_PLATEAU):
            for j in range(TAILLE_PLATEAU):
                bonus[i][j] = nouveaux_bonus[i][j]
        
        # Distribution des mains
        for nom in liste_noms:
            players[nom] = {'main': piocher(pioche, 7), 'score': 0}
            noms_joueurs.append(nom)
            scrabbles_count[nom] = 0
        
        # Ajout de l'ordinateur si nécessaire
        if etat['mode_pc']:
            noms_joueurs.append("Ordinateur")
            players["Ordinateur"] = {'main': piocher(pioche, 7), 'score': 0}
            
        etat['joueur_actuel_idx'] = 0

        # Lancement de la partie
        frame_setup.pack_forget()
        frame_jeu.pack(fill="both", expand=True)
        rafraichir_affichage()


    def action_sauvegarder():
        """Enregistre l'état complet du jeu."""

        nom_fichier = "partie_scrabble.dat"

        # Préparation des données
        data = {
            'plateau': plateau,
            'bonus': bonus,
            'pioche': pioche,
            'players': players,
            'noms_joueurs': noms_joueurs,
            'etat': etat,
            'scrabbles_count': scrabbles_count
        }
        
        # Sauvegarde
        with open(nom_fichier, "wb") as f:
            pickle.dump(data, f)
            
        messagebox.showinfo("Sauvegarde", f"Partie sauvegardée dans '{nom_fichier}' !")

    
    def action_charger():
        """Charge une partie existante."""

        nom_fichier = "partie_scrabble.dat"
        
        # Vérification préventive
        if Path(nom_fichier).exists():
            with open(nom_fichier, "rb") as f:
                data = pickle.load(f)
            
            # Restauration des données
            for i in range(TAILLE_PLATEAU):
                for j in range(TAILLE_PLATEAU):
                    plateau[i][j] = data['plateau'][i][j]
                    bonus[i][j] = data['bonus'][i][j]
            
            pioche[:] = data['pioche']
            
            players.clear()
            players.update(data['players'])
            
            noms_joueurs[:] = data['noms_joueurs']
            etat.update(data['etat'])
            scrabbles_count.update(data['scrabbles_count'])
            
            # Mise à jour de l'affichage
            frame_mode.pack_forget()
            frame_jeu.pack(fill="both", expand=True)
            rafraichir_affichage()
            messagebox.showinfo("Chargement", "Partie chargée avec succès !")
            
        else:
            messagebox.showwarning("Attention", "Aucun fichier de sauvegarde trouvé.")

    
    def mettre_a_jour_stats(gagnant):
        """Lit, met à jour et sauvegarde les stats globales."""

        fichier_stats = "stats_scrabble.json"
        
        # Chargement conditionnel
        if Path(fichier_stats).exists():
            with open(fichier_stats, "r") as f:
                stats = json.load(f)

        else:
            stats = {}
            
        # Initialisation des catégories
        if "PVP" not in stats:
            stats["PVP"] = {}
        if "PVE" not in stats:
            stats["PVE"] = {}

        # Sélection de la catégorie
        if etat['mode_pc']:
            categorie = "PVE"
        else:
            categorie = "PVP"

        # Mise à jour des joueurs
        for nom, data in players.items():
            if nom == "Ordinateur":
                continue 
            
            if nom not in stats[categorie]:
                stats[categorie][nom] = {'parties': 0, 'victoires': 0, 'total_score': 0, 'scrabbles': 0}
            
            s = stats[categorie][nom]
            s['parties'] += 1
            s['total_score'] += data['score']
            
            nb_scrabbles = scrabbles_count.get(nom, 0)
            s['scrabbles'] += nb_scrabbles
            
            if nom == gagnant:
                s['victoires'] += 1
                
        with open(fichier_stats, "w") as f:
            json.dump(stats, f, indent=4)


    def voir_statistiques():
        """Affiche une fenêtre avec les stats."""

        fichier_stats = "stats_scrabble.json"

        # Lecture et affichage
        if Path(fichier_stats).exists():
            with open(fichier_stats, "r") as f:
                stats = json.load(f)
            
            msg = ""
            categories = ["PVP", "PVE"]

            # Affichage par catégorie
            for cat in categories:
                if cat == "PVP":
                    titre = "JOUEUR CONTRE JOUEUR"

                else:
                    titre = "JOUEUR CONTRE ORDI"
                    
                msg += f"{titre}\n\n"
                
                # Affichage des stats par joueur
                if cat in stats and stats[cat]:
                    for nom, s in stats[cat].items():
                        moyenne = 0

                        if s['parties'] > 0:
                            moyenne = s['total_score'] // s['parties']
                            
                        msg += f"JOUEUR : {nom}\n"
                        msg += f" - Parties : {s['parties']} | Victoires : {s['victoires']}\n"
                        msg += f" - Score Moy : {moyenne} | Scrabbles : {s['scrabbles']}\n"
                        msg += "-"*25 + "\n"

                else:
                    msg += "(Aucune donnée)\n"
                
                msg += "\n\n"
                
            messagebox.showinfo("Statistiques", msg)
            
        else:
            messagebox.showinfo("Statistiques", "Aucune statistique enregistrée.")


    def ecran_noms(mode):
        """Affiche l'écran de saisie des noms des joueurs."""

        frame_mode.pack_forget()
        frame_setup.pack(pady=20)
        
        # Nettoyage de l'écran
        for w in frame_setup.winfo_children(): 
            w.destroy()
        
        tk.Label(frame_setup, text="Configuration", font=("Arial", 16)).pack(pady=10)
        entries = []

        # Validation des noms
        def valider():
            noms = [e.get().strip() or f"J{k+1}" for k, e in enumerate(entries)]
            demarrer_jeu(mode, noms)

        # Configuration selon le mode
        if mode == "PVE":
            tk.Label(frame_setup, text="Votre Nom :").pack()
            e = tk.Entry(frame_setup); e.pack(); entries.append(e)
            tk.Button(frame_setup, text="JOUER", command=valider, bg="green", fg="white").pack(pady=20)

        else:
            tk.Label(frame_setup, text="Nombre de joueurs (2-4) :").pack()
            spin = tk.Spinbox(frame_setup, from_=2, to=4, width=5)
            spin.pack()
            
            # Zone dynamique pour les champs de noms
            f_dyn = tk.Frame(frame_setup)
            f_dyn.pack(pady=10)
            
            def gen_champs():
                # Génération dynamique des champs de noms
                for w in f_dyn.winfo_children():
                    w.destroy()
                entries.clear()
                
                n = int(spin.get())
                
                for i in range(n):
                    tk.Label(f_dyn, text=f"Joueur {i+1} :").pack()
                    e = tk.Entry(f_dyn)
                    e.pack()
                    entries.append(e)
                
                btn_go.config(state="normal")
                
            tk.Button(frame_setup, text="Ok", command=gen_champs).pack()
            btn_go = tk.Button(frame_setup, text="LANCER", state="disabled", bg="green", fg="white", command=valider)
            btn_go.pack(pady=20)


    # Création de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Projet Scrabble")
    fenetre.geometry("1100x750")

    # Menu principal
    frame_mode = tk.Frame(fenetre)
    frame_mode.pack(pady=50)
    tk.Label(frame_mode, text="SCRABBLE", font=("Arial", 30, "bold")).pack(pady=20)
    tk.Button(frame_mode, text="Joueur vs Joueur", width=20, font=("Arial", 12), bg="#4CAF50", fg="white", command=lambda: ecran_noms("PVP")).pack(pady=10)
    tk.Button(frame_mode, text="Joueur vs Ordi", width=20, font=("Arial", 12), bg="#2196F3", fg="white", command=lambda: ecran_noms("PVE")).pack(pady=10)
    tk.Button(frame_mode, text="Charger une partie", width=20, font=("Arial", 12), bg="orange", command=action_charger).pack(pady=10)
    tk.Button(frame_mode, text="Voir Statistiques", width=20, font=("Arial", 12), bg="purple", fg="white", command=voir_statistiques).pack(pady=10)

    # Page Jeu
    frame_setup = tk.Frame(fenetre)

    frame_jeu = tk.Frame(fenetre)
    
    # Partie gauche (plateau)
    f_gauche = tk.Frame(frame_jeu, bg="#333", bd=2)
    f_gauche.pack(side="left", padx=10, pady=10)
    
    for j in range(TAILLE_PLATEAU):
        tk.Label(f_gauche, text=str(j+1), width=4, bg="#333", fg="white").grid(row=0, column=j+1)
    
    grille_labels = []

    for i in range(TAILLE_PLATEAU):
        tk.Label(f_gauche, text=chr(65+i), width=2, bg="#333", fg="white").grid(row=i+1, column=0)
        ligne = []

        for j in range(TAILLE_PLATEAU):
            l = tk.Label(f_gauche, width=4, height=2, relief="sunken", bd=1)
            l.grid(row=i+1, column=j+1, padx=1, pady=1)
            ligne.append(l)

        grille_labels.append(ligne)

    # Partie droite (infos et actions)
    f_droite = tk.Frame(frame_jeu, padx=20)
    f_droite.pack(side="right", fill="both", expand=True)

    lbl_tour = tk.Label(f_droite, text="...", font=("Arial", 16, "bold"))
    lbl_tour.pack(pady=10)
    lbl_scores = tk.Label(f_droite, text="...", font=("Arial", 10))
    lbl_scores.pack()
    lbl_pioche = tk.Label(f_droite, text="...")
    lbl_pioche.pack()
    
    lbl_main = tk.Label(f_droite, text="...", font=("Courier", 14, "bold"), bg="#eee", pady=10)
    lbl_main.pack(fill="x", pady=20)

    f_play = tk.LabelFrame(f_droite, text="Jouer un mot", padx=5, pady=5)
    f_play.pack(fill="x", pady=5)
    
    tk.Label(f_play, text="Mot :").grid(row=0, column=0)
    entree_mot = tk.Entry(f_play); entree_mot.grid(row=0, column=1, columnspan=3, sticky="we")
    
    tk.Label(f_play, text="Lig (A-O):").grid(row=1, column=0)
    entree_lig = tk.Entry(f_play, width=5); entree_lig.grid(row=1, column=1)
    
    tk.Label(f_play, text="Col (1-15):").grid(row=1, column=2)
    entree_col = tk.Entry(f_play, width=5); entree_col.grid(row=1, column=3)
    
    tk.Label(f_play, text="Sens (H/V):").grid(row=2, column=0)
    entree_dir = tk.Entry(f_play, width=5); entree_dir.grid(row=2, column=1)
    
    tk.Button(f_play, text="VALIDER", bg="#4CAF50", fg="white", command=action_jouer).grid(row=3, column=0, columnspan=4, sticky="we", pady=10)

    f_ech = tk.LabelFrame(f_droite, text="Actions", padx=5, pady=5)
    f_ech.pack(fill="x", pady=10)
    
    tk.Label(f_ech, text="Lettres à jeter :").pack(anchor="w")
    entree_echange = tk.Entry(f_ech); entree_echange.pack(fill="x")
    tk.Button(f_ech, text="ECHANGER", bg="orange", command=action_echanger).pack(fill="x", pady=2)
    tk.Button(f_ech, text="PASSER TOUR", bg="#f44336", fg="white", command=action_passer).pack(fill="x", pady=5)

    tk.Button(f_droite, text="INDICE 1 : Mots possibles", bg="lightblue", command=action_indice_mots).pack(pady=5)
    tk.Button(f_droite, text="INDICE 2 : Meilleur placement", bg="lightblue", command=action_indice_placement).pack(pady=5)
    tk.Button(f_droite, text="SAUVEGARDER PARTIE", bg="gray", fg="white", command=action_sauvegarder).pack(pady=10)
    tk.Button(f_droite, text="MENU PRINCIPAL", bg="#555", fg="white", command=action_retour_menu).pack(side="bottom", fill="x", pady=5)

    tk.Button(f_droite, text="QUITTER", command=quitter_programme).pack(side="bottom", pady=10)

    fenetre.mainloop()

if __name__ == "__main__":
    lancer_graphique()


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