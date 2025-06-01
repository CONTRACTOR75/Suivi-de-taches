Suivi de Tâches – API C# & Interface Python
Présentation
Ce projet est une application de gestion de tâches composée de :

Une API REST développée en C# (.NET) avec Entity Framework Core et MariaDB/MySQL.
Une interface graphique conviviale en Python (Tkinter) pour interagir avec l’API.
Fonctionnalités
Ajouter, modifier, supprimer et afficher des tâches.
Afficher la description d’une tâche au survol dans l’interface.
Confirmation avant de quitter l’application.
Interface moderne et intuitive.
Prérequis
.NET 8 SDK
Python 3.8+
MariaDB/MySQL (ou un serveur MySQL)
Les modules Python : requests, tkinter (inclus avec Python standard)
Installation
1. Base de données
Crée une base de données (ex : suivi_taches) via phpMyAdmin ou en ligne de commande.
Mets à jour la chaîne de connexion dans Program.cs si besoin.
2. API C#
L’API sera accessible sur http://localhost:5209/api/SuiviDeTaches (ou le port affiché).

3. Interface Python
Utilisation
Lance l’API C# (dotnet run)
Lance l’interface Python (python interface.py)
Utilise l’interface pour gérer tes tâches : ajout, modification, suppression, affichage.
Survole une tâche pour voir sa description.
Personnalisation
Tu peux modifier les couleurs, la taille de la fenêtre, ou ajouter d’autres fonctionnalités dans interface.py.
Pour changer la base de données, adapte la chaîne de connexion dans Program.cs.
Auteurs
Mathias (et contributeurs)
Licence
Projet éducatif – libre de réutilisation pour l’apprentissage.