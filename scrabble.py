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
import random  # pour la pioche aléatoire


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
    """
    Q1) Initialise le plateau des bonus.
    """
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

    marge_tete = " " * TAILLE_MARGE

    print(marge_tete, end="")
    for col in range(TAILLE_PLATEAU):
        if col < 9:
            print(f'  {col+1}', end=" ")
        else:
            print(f' {col+1}', end=" ") 
    print()

    print(marge_tete, end="")
    print("|" + ("---|" * TAILLE_PLATEAU))


    for lig in range(TAILLE_PLATEAU):
        
        if lig < 9:
            print(f'{lig+1}   |', end="")
        else:
            print(f'{lig+1}  |', end="") 
        

        for col in range(TAILLE_PLATEAU):
            jeton = table_jetons[lig][col]
            bonus_val = table_bonus[lig][col]
            symbole = bonus_symboles.get(bonus_val, '')

            contenu_cellule = "  "

            if jeton != "":
                contenu_cellule = jeton
                if symbole != "":
                    contenu_cellule += symbole
                else:
                    contenu_cellule += " "
            else:
                if symbole != "":
                    contenu_cellule = " " + symbole
             
            print(f'{contenu_cellule} |', end="")
        print()
        print(marge_tete + "|" + ("---|" * TAILLE_PLATEAU))
    print('-' * (TAILLE_MARGE + TAILLE_PLATEAU * 5 + 1))


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


# PARTIE 2 : LA PIOCHE #########################################################


def init_pioche_alea():
    """Q7) Initialise la pioche aléatoire des jetons."""
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


def piocher(x, sac):
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
    for jeton in jetons:
        if jeton in main:
            main.remove(jeton)
            sac.append(jeton)
    main = completer_main(main, sac)
    return main, sac


# Q7) Initialiser la pioche aléatoire
pioche = init_pioche_alea()
print("Pioche initiale (100 jetons) :", len(pioche))

# Q8) Piocher 7 jetons
main_joueur1 = piocher(7, pioche)
print("Main du joueur 1 (7 jetons) :", main_joueur1)
main_joueur2 = piocher(7, pioche)
print("Main du joueur 2 (7 jetons) :", main_joueur2)

# Q11) Échanger des jetons entre la main du joueur 2 et le sac
echanger(main_joueur2[:3], main_joueur2, pioche)
print("Main du joueur 2 après échange de 3 jetons :", main_joueur2)
print("Pioche après échange :", len(pioche), "jetons restants")


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
    """Sélectionne les mots commençant par la lettre let."""
    liste_mots = []
    for i in motsfr:
        if i[0] == let:
            liste_mots.append(i)
    return liste_mots


def select_mot_longueur(motsfr,lgr):
    """Sélectionne les mots de longueur lgr."""
    liste_mots = []
    for i in motsfr:
        if len(i) == lgr:
            liste_mots.append(i)
    return liste_mots


def mot_jouable(mot, ll):
    """Vérifie si le mot peut être formé avec les lettres de la liste ll."""
    liste_temp = list(ll)
    for lettre in mot:
        if lettre in liste_temp:
            liste_temp.remove(lettre)
        else:
            return False
    return True


def mots_jouables(motsfr, ll):
    """Sélectionne les mots de motsfr pouvant être formés avec les lettres de la liste ll."""
    liste_mots = []
    for mot in motsfr:
        if mot_jouable(mot, ll):
            liste_mots.append(mot)
    return liste_mots


# Q12) Générer le dictionnaire français
mots_fr = generer_dictfr()
print("Nombre de mots dans le dictionnaire français :", len(mots_fr))

# Q13) Sélectionner les mots commençant par 'Y'
mots_commencant_par_Y = select_mot_initiale(mots_fr, 'Y')
print("Mots commençant par 'Y' :", len(mots_commencant_par_Y))

# Q14) Sélectionner les mots de longueur 19
mots_longueur_19 = select_mot_longueur(mots_fr, 19)
print("Mots de longueur 19 :", len(mots_longueur_19))

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


# Programe principal #######################################################



