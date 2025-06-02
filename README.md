# 📝 Suivi de Tâches – API C# & Interface Python

## 📌 Présentation

Ce projet est une application de **gestion de tâches** composée de :

- Une **API REST** développée en C# (.NET) avec Entity Framework Core et MariaDB/MySQL
- Une **interface graphique conviviale** en Python (Tkinter) pour interagir avec l’API

---

## ✨ Fonctionnalités

- Ajouter, modifier, supprimer et afficher des tâches
- Affichage de la **description d’une tâche au survol**
- Confirmation avant de quitter l’application
- Interface moderne et intuitive

---

## 🧰 Prérequis

- [.NET 8 SDK](https://dotnet.microsoft.com/en-us/download)
- [Python 3.8+](https://www.python.org/downloads/)
- MariaDB ou MySQL
- Modules Python :
  - `requests`
  - `tkinter` *(inclus avec Python standard)*

---

## ⚙️ Installation

### 🔹 1. Base de données

- Crée une base de données (ex. `suivi_taches`) via **phpMyAdmin** ou en ligne de commande
- Mets à jour la chaîne de connexion dans `Program.cs` si besoin (port,utilisateur, mot de passe)

### 🔹 2. API C#

- Lance l’API avec :

```bash
dotnet run
````

### 🔹 3. Interface Python

- Lance l’interface avec :

```bash
cd interface
python interface.py
````
Ou

```bash
python interface/interface.py
````
