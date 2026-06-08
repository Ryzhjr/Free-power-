class FONT:
    DEFAULT = ("Arial", 18, "bold")

class COLOR:
    PRIMARY_GREEN = "#53D768"
    HOVER_GREEN = "#46C262"

    PRIMARY_RED = "#FD3D3A"
    HOVER_RED = "#E33437"

    PRIMARY_GRAY = "#808080"
    HOVER_GRAY = "#666666"

    BAR_OK = "#53D768"  # Green
    BAR_WARNING = "#FD3D3A"  # Red

class UTILS:
    RELOAD_INTERVAL = 1.0  # seconds
    WARNING_THRESHOLD = 80  # percent
    NOTIFICATIONS_ENABLED = True  # enable/disable notifications
    NOTIFICATION_COOLDOWN = 300  # seconds
    THEME = "dark"  # default theme

class HELP:
    TEXT = """FreePower Task Manager - Guide d'utilisation

• Vue d'ensemble :
  - Le panneau de gauche affiche les ressources système (CPU, RAM, GPU, Disque)
  - Le panneau principal liste les processus en cours d'exécution

• Fonctionnalités :
  - Recherche : Filtrez les processus par nom
  - Notifications : Alertes lors d'une utilisation élevée des ressources
  - Tri : Classement automatique par utilisation CPU

• Indicateurs :
  - Barre verte : Utilisation normale
  - Barre orange : Utilisation élevée (>80%)

• Paramètres :
  - Accédez aux réglages via le bouton ⚙
  - Personnalisez les seuils d'alerte et les notifications

• Comment interpréter les données ? :
  - CPU : Pourcentage d'utilisation du processeur 
    (c'est ce qui fait tout les calculs sur votre ordinateur)
  - RAM : Pourcentage d'utilisation de la mémoire vive
    (c'est ce qui stocke les données temporaires pour les applications)
  - GPU : Pourcentage d'utilisation de la carte graphique
    (c'est ce qui gère l'affichage et les calculs graphiques pour jeux et la 3D)
  - Disque : Pourcentage d'espace disque utilisé

• Pourquoi ces indicateurs sont-ils importants ? :
  - Le CPU est crucial pour la performance générale car il s'occupe de tous les calculs.
  - La RAM est essentielle pour la rapidité des applications, plus elle est pleine, plus votre ordinateur sera lent.
  - Le GPU est important pour les jeux et les applications graphiques, une utilisation élevée peut causer des ralentissements.
  - Le disque dur est important pour le stockage, une utilisation élevée peut ralentir les accès aux fichiers.
"""