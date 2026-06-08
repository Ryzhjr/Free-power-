# FreePower Task Manager

FreePower Task Manager est une application Windows de gestion et de surveillance de processus écrite en Python. Elle utilise customtkinter pour l'interface graphique et psutil / GPUtil pour afficher l'utilisation de la CPU, de la RAM, du GPU et du disque.

## Description

Cette application permet de visualiser en temps réel l'activité des processus visibles, de filtrer les processus par nom, et de terminer des processus depuis l'interface. Elle inclut des alertes de notifications lorsque l'utilisation des ressources dépasse un seuil défini.

## Fonctionnalités

- Affichage en temps réel de l'utilisation du CPU, de la RAM, du GPU et de l'espace disque
- Liste des processus visibles triés par utilisation CPU
- Barre de recherche pour filtrer les processus par nom
- Bouton de terminaison pour arrêter les processus sélectionnés
- Paramètres personnalisables : intervalle de rafraîchissement, seuil d'alerte, notifications, thème clair/sombre
- Aide intégrée pour expliquer les indicateurs et l'utilisation de l'application

## Prérequis

- Windows
- Python 3.10+ (3.14 testé)
- pip

## Installation

Clonez le dépôt.

Ouvrez un terminal dans le dossier contenant main.py.

Installez les dépendances :

```bash
python -m pip install -r requirements.txt
