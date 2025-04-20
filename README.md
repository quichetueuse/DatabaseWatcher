# DatabaseWatcher - Outil de sauvegarde et restauration de bases de données

## Présentation

Outil développé en python POO permettant la sauvegarde et la restauration . Ce projet a été réalisé dans le cadre de mes cours de cybersécurité de mon BTS SIO option SLAM.

## Fonctionnalités

- Sauvegarde d'une base de données entière avec possibilité de chiffrer la sauvegarde
- Restauration d'une base de données avec une sauvegarde réalisée auparavant (restauration possible même si la sauvegarde est chiffrée)

## Configuration technique

### Prérequis

- Python 3.11 (ou moins mais aucun test n'a été réalisé)
- Serveur LAMP (Linux Apache MySQL PHP)
- IDE ou lignes de commande

### Librairies utilisées

- cryptography (pour le chiffrement et le déchiffrement des données)
- colorama (pour l'affichage console en couleur)
- librairies incluses par défaut dans l'installation python

### Installation

1. Clonez le dépot git sur lequel vous êtes
2. Changez le fichier de configuration avec les valeurs adaptées à vos besoins
3. Editez le fichier main.py et décommentez la ou les fonctions souhaitées
4. Ouvrez une invite de commande et lancer l'outil
