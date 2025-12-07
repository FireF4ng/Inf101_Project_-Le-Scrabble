# Projet Scrabble - INF101

**Groupe :** ima04_B
**Fichier :** `i11_Daniel_Nikolai_projet.py`

**Auteurs :**
* **Daniel Centov** (Daniel.Centov@etu.univ-grenoble-alpes.fr)
* **Nikolai Kolenbet** (Nikolai.Kolenbet@etu.univ-grenoble-alpes.fr)


## Description
Implémentation complète du jeu de Scrabble en Python avec interface graphique.
Le projet inclut un mode Joueur vs Joueur, une IA (Joueur vs Ordi), la gestion des sauvegardes et des statistiques détaillées.


## Fichiers requis
Assurez-vous que ces fichiers sont présents dans le même dossier avant de lancer le jeu :
1. `i11_Daniel_Nikolai_projet.py` (Script principal)
2. `littre.txt` (Dictionnaire)
3. `lettres.txt` (Valeurs des lettres)


## Instructions d'exécution

### Windows
Ouvrez l'invite de commande (CMD) ou PowerShell dans le dossier du projet et tapez :

```bash
python i11_Daniel_Nikolai_projet.py
```

### Linux (Ubuntu/Debian)
Assurez-vous que le module tkinter est installé (souvent requis séparément sur Linux) :

```Bash
sudo apt-get install python3-tk
```

Puis lancez le jeu :
```Bash
python3 i11_Daniel_Nikolai_projet.py
```

### MacOS
Ouvrez le terminal dans le dossier du projet et lancez :

```Bash
python3 i11_Daniel_Nikolai_projet.py
```


## Fonctionnalités Bonus
- Sauvegarde/Chargement : Via le fichier partie_scrabble.dat (généré automatiquement).
- Statistiques : Suivi des scores et victoires dans stats_scrabble.json.
- Aide de jeu : Suggestions de mots et calcul du meilleur placement.
