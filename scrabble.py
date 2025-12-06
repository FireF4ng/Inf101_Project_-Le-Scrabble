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
import tkinter as tk
from tkinter import messagebox

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

    lettres_a_poser = tester_placement(plateau, i, j, direction, mot)
    
    if lettres_a_poser == []:
        return False, 0
        
    main_temp = list(main)
    possible = True
    index_lettre = 0

    for lett in lettres_a_poser:

        if lett in main_temp:
            main_temp.remove(lett)

        elif JOKER in main_temp:
            main_temp.remove(JOKER)

        else:
            return False, 0
            
    for lett in lettres_a_poser:

        if lett in main:
            main.remove(lett)

        else:
            main.remove(JOKER)

    score = 0
    multiplicateur_mot = 1
    nb_nouvelles_lettres = 0

    for k in range(len(mot)):

        if direction == 'H':
            lig, col = i, j + k

        else:
            lig, col = i + k, j
        
        lettre = mot[k]
        ancienne_lettre = plateau[lig][col]
        
        plateau[lig][col] = lettre
        
        val_lettre = dico.get(lettre, {'val':0})['val']
        
        if ancienne_lettre == "":
            nb_nouvelles_lettres += 1
            b = bonus[lig][col]
            
            if b == 'LD': val_lettre *= 2
            elif b == 'LT': val_lettre *= 3
            elif b == 'MD': multiplicateur_mot *= 2
            elif b == 'MT': multiplicateur_mot *= 3
            
            bonus[lig][col] = ""
            
        score += val_lettre

    score *= multiplicateur_mot
    
    if nb_nouvelles_lettres == 7:
        score += 50
        
    return True, score


# PARTIE 7 : Programme Principal Final ###################################################


def tour_joueur(name, players_infos, pioche, mots_fr, dico, plateau, bonus, pas_tour_total):
    """Q25) Gère le tour d'un joueur."""

    affiche_jetons(plateau, bonus)
    print(f"C'est à votre tour {name} de jouer !")
    flag = True

    while flag:
        print("Voici vos jetons : ", players_infos[name]['main'])
        choix = input("Entrez le mot que vous souhaitez jouer (show/hint/passer/echanger/proposer): ").lower()

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


# PARTIE 8 : BONUS ###################################################


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

    
    # IA et Aide
    def trouver_meilleur_coup(main_joueur):
        """Cherche un mot jouable avec la main qui rentre sur le plateau."""
        candidats = meilleurs_mots(mots_fr, main_joueur, dico)
        
        for mot in candidats[:50]:
            for i in range(TAILLE_PLATEAU):
                for j in range(TAILLE_PLATEAU):
                    for d in ['H', 'V']:
                        if tester_placement(plateau, i, j, d, mot):
                            return mot, i, j, d
                        
        return None

    
    def tour_ordi():
        """Logique du tour de l'ordinateur."""
        nom, infos = "Ordinateur", players["Ordinateur"]
        
        coup = trouver_meilleur_coup(infos['main'])
        
        if coup:
            mot, i, j, d = coup
            ok, pts = placer_mot(plateau, bonus, infos['main'], mot, i, j, d, dico)

            if ok:
                infos['score'] += pts
                completer_main(infos['main'], pioche)
                etat['passes_consecutifs'] = 0
                messagebox.showinfo("Ordinateur", f"L'ordi a joué {mot} pour {pts} points !")

            else:
                action_passer()
        else:

            if len(pioche) >= 7:
                echanger(infos['main'], infos['main'], pioche)
                messagebox.showinfo("Ordinateur", "L'ordi échange ses lettres.")

            else:
                action_passer()


    def get_joueur_courant():
        nom = noms_joueurs[etat['joueur_actuel_idx']]
        return nom, players[nom]

    
    def rafraichir_affichage():
        """Met à jour l'écran de jeu."""

        if etat['fin_partie']: 
            return

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
        
        nom, infos = get_joueur_courant()
        lbl_tour.config(text=f"C'est à {nom} de jouer", fg="blue")
        lbl_main.config(text=f"Main :  {' '.join(infos['main'])}")
        lbl_pioche.config(text=f"Pioche : {len(pioche)}")
        
        txt_scores = "   ".join([f"{n}: {d['score']}" for n, d in players.items()])
        lbl_scores.config(text=txt_scores)


    def changer_joueur():
        etat['joueur_actuel_idx'] = (etat['joueur_actuel_idx'] + 1) % len(noms_joueurs)
        rafraichir_affichage()
        
        if etat['mode_pc'] and get_joueur_courant()[0] == "Ordinateur":
            fenetre.after(1000, tour_ordi)


    # Actions du Joueur
    def action_passer():
        nom, _ = get_joueur_courant()
        etat['passes_consecutifs'] += 1
        
        if etat['passes_consecutifs'] >= len(noms_joueurs) * 3:
            gerer_fin("Blocage (trop de passes)")

        else:
            if nom != "Ordinateur":
                messagebox.showinfo("Passer", f"{nom} passe son tour.")

            changer_joueur()


    def action_echanger():
        nom, infos = get_joueur_courant()
        saisie = entree_echange.get().upper().strip()
        
        if not saisie: 
            return
        
        lettres = list(saisie)
        
        if len(pioche) < len(lettres):
            messagebox.showerror("Erreur", "Pioche insuffisante.")
            return
            
        copie_main = list(infos['main'])
        possible = True
        for l in lettres:

            if l in copie_main: 
                copie_main.remove(l)

            else: 
                possible = False
            
        if possible:
            nouvelle_main, _ = echanger(lettres, infos['main'], pioche)
            infos['main'] = nouvelle_main
            entree_echange.delete(0, tk.END) # Vider champ
            messagebox.showinfo("Succès", "Lettres échangées.")
            etat['passes_consecutifs'] = 0
            changer_joueur()

        else:
            messagebox.showerror("Erreur", "Vous n'avez pas ces lettres.")


    def action_jouer():
        nom, infos = get_joueur_courant()
        
        mot = entree_mot.get().upper().strip()
        s_lig = entree_lig.get().upper().strip()
        s_col = entree_col.get().strip()
        direction = entree_dir.get().upper().strip()
        
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

        ok, pts = placer_mot(plateau, bonus, infos['main'], mot, lig, col, direction, dico)
        
        if ok:
            infos['score'] += pts
            completer_main(infos['main'], pioche)
            etat['passes_consecutifs'] = 0
            messagebox.showinfo("Bravo", f"{mot} posé ! +{pts} pts.")
            
            entree_mot.delete(0, tk.END)
            entree_lig.delete(0, tk.END)
            entree_col.delete(0, tk.END)
            entree_dir.delete(0, tk.END)
            
            if not pioche and not infos['main']:
                gerer_fin("Plus de jetons")

            else:
                changer_joueur()

        else:
            messagebox.showerror("Erreur", "Placement impossible.")


    def action_indice():
        """Aide : Propose le meilleur coup possible."""
        nom, infos = get_joueur_courant()
        coup = trouver_meilleur_coup(infos['main'])
        
        if coup:
            mot, i, j, d = coup
            coord = f"{chr(i+65)}{j+1}"
            messagebox.showinfo("Indice", f"Meilleur coup trouvé : {mot} en {coord} ({d})")

        else:
            messagebox.showinfo("Indice", "Aucun coup évident trouvé (essayez d'échanger).")


    def gerer_fin(raison):
        etat['fin_partie'] = True
        msg = f"FIN DE PARTIE ({raison})\n\n"
        
        for nom, p in players.items():
            malus = sum(dico[l]['val'] for l in p['main'] if l in dico)
            p['score'] -= malus
            msg += f"{nom}: {p['score']} pts (Malus -{malus})\n"
            
        gagnant = max(players, key=lambda n: players[n]['score'])
        msg += f"\n GAGNANT : {gagnant} !"
        messagebox.showinfo("Résultats", msg)
        fenetre.quit()


    def demarrer_jeu(mode, liste_noms):
        etat['mode_pc'] = (mode == "PVE")
        
        for nom in liste_noms:
            players[nom] = {'main': piocher(pioche, 7), 'score': 0}
            noms_joueurs.append(nom)
            
        if etat['mode_pc']:
            noms_joueurs.append("Ordinateur")
            players["Ordinateur"] = {'main': piocher(pioche, 7), 'score': 0}
            
        etat['joueur_actuel_idx'] = 0
        frame_setup.pack_forget()
        frame_jeu.pack(fill="both", expand=True)
        rafraichir_affichage()


    def ecran_noms(mode):
        frame_mode.pack_forget()
        frame_setup.pack(pady=20)
        
        for w in frame_setup.winfo_children(): 
            w.destroy()
        
        tk.Label(frame_setup, text="Configuration", font=("Arial", 16)).pack(pady=10)
        entries = []


        def valider():
            noms = [e.get().strip() or f"J{k+1}" for k, e in enumerate(entries)]
            demarrer_jeu(mode, noms)

        if mode == "PVE":
            tk.Label(frame_setup, text="Votre Nom :").pack()
            e = tk.Entry(frame_setup); e.pack(); entries.append(e)
            tk.Button(frame_setup, text="JOUER", command=valider, bg="green", fg="white").pack(pady=20)

        else:
            tk.Label(frame_setup, text="Nombre de joueurs (2-4) :").pack()
            spin = tk.Spinbox(frame_setup, from_=2, to=4, width=5)
            spin.pack()
            
            f_dyn = tk.Frame(frame_setup)
            f_dyn.pack(pady=10)
            
            def gen_champs():
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

    fenetre = tk.Tk()
    fenetre.title("Projet Scrabble")
    fenetre.geometry("1100x750")

    frame_mode = tk.Frame(fenetre)
    frame_mode.pack(pady=50)
    tk.Label(frame_mode, text="SCRABBLE", font=("Arial", 30, "bold")).pack(pady=20)
    tk.Button(frame_mode, text="Joueur vs Joueur", width=20, font=("Arial", 12), bg="#4CAF50", fg="white", command=lambda: ecran_noms("PVP")).pack(pady=10)
    tk.Button(frame_mode, text="Joueur vs Ordi", width=20, font=("Arial", 12), bg="#2196F3", fg="white", command=lambda: ecran_noms("PVE")).pack(pady=10)

    frame_setup = tk.Frame(fenetre)

    frame_jeu = tk.Frame(fenetre)
    
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

    tk.Button(f_droite, text="INDICE (Meilleur coup)", bg="lightblue", command=action_indice).pack(pady=10)
    tk.Button(f_droite, text="QUITTER", command=fenetre.quit).pack(side="bottom", pady=10)

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