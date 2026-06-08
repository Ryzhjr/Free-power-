# FreePower Task Manager

FreePower Task Manager est une application Windows de gestion et de surveillance de processus écrite en Python.
Elle utilise `customtkinter` pour l'interface graphique et `psutil` / `GPUtil` pour afficher l'utilisation de la CPU, de la RAM, du GPU et du disque.

## Description

Cette application permet de visualiser en temps réel l'activité des processus visibles, de filtrer les processus par nom, et de terminer des processus depuis l'interface.
Elle inclut des alertes de notifications lorsque l'utilisation des ressources dépasse un seuil défini.

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
- `pip`

## Installation

1. Clonez le dépôt.
2. Ouvrez un terminal dans le dossier contenant `main.py`.
3. Installez les dépendances :

```bash
python -m pip install -r requirements.txt
```

## Utilisation

Lancez l'application depuis le dossier racine du projet :

```bash
python main.py
```

## Configuration

Les paramètres utilisateur sont sauvegardés dans `config/settings.json`.
Vous pouvez ajuster :

- `reload_interval` : intervalle de rafraîchissement des données (en secondes)
- `warning_threshold` : seuil d'alerte en pourcentage
- `notifications_enabled` : activer/désactiver les alertes
- `notification_cooldown` : délai de réactivation des alertes (en secondes)
- `theme` : `light` ou `dark`

## Architecture du projet

- `main.py` : point d'entrée de l'application
- `process_manager.py` : collecte et traitement des données des processus
- `ui/windows/main_window.py` : fenêtre principale de l'application
- `ui/frames` : composants d'interface pour les indicateurs système et la liste des processus
- `ui/windows/settings_window.py` : fenêtre de paramètres
- `ui/windows/help_window.py` : fenêtre d'aide
- `models/models.py` : structures de données utilisées par l'application
- `utils/constants.py` : configurations et constantes globales

## Limitations

- Conçu pour Windows uniquement
- Le bouton `Maximize` est un espace réservé et n'active pas de mise au premier plan
- Certains processus protégés ou système ne peuvent pas être terminés
- Les notifications sont gérées par `winotify`, donc l'application peut ne pas fonctionner sur d'autres plateformes

## Dépendances

- `psutil`
- `GPUtil`
- `customtkinter`
- `pywin32`
- `winotify`

