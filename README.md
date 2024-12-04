
# YouTube Videos Downloader

## Description
YouTube Videos Downloader est une application intuitive avec une interface graphique moderne pour télécharger des vidéos YouTube. Conçu avec Python et `ttkbootstrap`, cet outil vous permet de gérer facilement les téléchargements, de choisir les formats de vidéo, de changer le dossier de destination, et bien plus encore.

---

## Fonctionnalités
- **Téléchargement de vidéos YouTube** :
  - Choix du format et de la résolution avant le téléchargement.
  - Barre de progression en temps réel avec mises à jour du statut.
- **Personnalisation** :
  - Support des thèmes clairs et sombres.
  - Configuration d'un dossier de destination par défaut.
- **Gestion des erreurs** :
  - Vérifications des entrées utilisateur et gestion des échecs.
- **Miniatures et informations** :
  - Affichage des miniatures et des détails pour chaque format.

---

## Prérequis
- **Python** (>= 3.7)
- **Dépendances Python** :
  - `yt-dlp`
  - `ttkbootstrap`
  - `Pillow`
  - `python-dotenv`

Pour installer les dépendances, utilisez la commande suivante :
```bash
pip install -r requirements.txt
```

---

## Installation
1. Clonez le dépôt :
    ```bash
    git clone https://github.com/votre-utilisateur/youtube-downloader.git
    cd yt_downloader
    ```
2. Configurez l'environnement :
    - Créez un fichier `.env` à la racine :
      ```env
      ASSETS_PATH=./assets
      ```
    - Ajoutez vos ressources (logo, etc.) dans le dossier `assets`.
3. Lancez l'application :
    ```bash
    python main.py
    ```

---

## Utilisation
### Interface utilisateur
1. **Saisissez une URL** : Entrez l'URL de la vidéo YouTube dans le champ prévu à cet effet.
2. **Choisissez le format** : Une fenêtre s'ouvrira pour afficher les formats disponibles.
3. **Téléchargez** : Cliquez sur le bouton *Download*. Suivez la progression via la barre.

### Menu
- **Thème** : Basculer entre thème clair et sombre.
- **Dossier** : Modifier le dossier de destination pour les téléchargements.

---

## Fichiers clés
### `main.py`
Gère l'interface utilisateur et les interactions principales avec l'utilisateur.

### `downloader.py`
Fournit les fonctionnalités pour extraire les formats et télécharger les vidéos YouTube.

### `utils.py`
Contient des fonctions utilitaires comme :
- `stringify_size(size)` : Convertit une taille de fichier en une chaîne lisible (e.g., "12.5 MB").
- `extract_percentage(text)` : Extrait un pourcentage à partir d'une chaîne.

---

## Contributeurs

- **Romaric** (Développeur principal)

