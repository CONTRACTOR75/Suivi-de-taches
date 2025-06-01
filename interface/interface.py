import requests

API_URL = "http://localhost:5209/api/SuiviDeTaches"  # adapte le port si besoin

def afficher_taches():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            print("Affichage des tâches :")
            for t in response.json():
                print(f"{t['id']} - {t['title']} ({'Terminé' if t['isCompleted'] else 'En cours'})")
        else:
            print("Erreur lors de la récupération des tâches.")
    except requests.exceptions.ConnectionError:
        print("Erreur : Impossible de se connecter au serveur. Vérifie que l'API C# est démarrée.")

def afficher_tache_precise():
    try:
        id_tache = input("ID de la tâche à afficher : ")
        response = requests.get(f"{API_URL}/{id_tache}")
        if response.status_code == 200:
            t = response.json()
            print(f"Tache : {t['id']} - {t['title']} : {t['description']} ({'Terminé' if t['isCompleted'] else 'En cours'})")
        elif response.status_code == 404:
            print("Tâche non trouvée.")
        else:
            print("Erreur lors de la récupération de la tâche.")
    except requests.exceptions.ConnectionError:
        print("Erreur : Impossible de se connecter au serveur. Vérifie que l'API C# est démarrée.")

def ajouter_tache():
    try:
        titre = input("Titre : ")
        description = input("Description : ")
        data = {"title": titre, "description": description, "isCompleted": False}
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            print("Tâche ajoutée !")
        else:
            print("Erreur lors de l'ajout.")
    except requests.exceptions.ConnectionError:
        print("Erreur : Impossible de se connecter au serveur. Vérifie que l'API C# est démarrée.")

def modifier_tache():
    try:
        id_tache = input("ID de la tâche à modifier : ")
        titre = input("Nouveau titre : ")
        description = input("Nouvelle description : ")
        is_completed = input("Terminée ? (oui/non) : ").lower() == "oui"
        data = {"id": int(id_tache), "title": titre, "description": description, "isCompleted": is_completed}
        response = requests.put(f"{API_URL}/{id_tache}", json=data)
        if response.status_code == 204:
            print("Tâche modifiée !")
        elif response.status_code == 404:
            print("Tâche non trouvée.")
        else:
            print("Erreur lors de la modification.")
    except requests.exceptions.ConnectionError:
        print("Erreur : Impossible de se connecter au serveur. Vérifie que l'API C# est démarrée.")

def supprimer_tache():
    try:
        id_tache = input("ID de la tâche à supprimer : ")
        response = requests.delete(f"{API_URL}/{id_tache}")
        if response.status_code == 204:
            print("Tâche supprimée !")
        elif response.status_code == 404:
            print("Tâche non trouvée.")
        else:
            print("Erreur lors de la suppression.")
    except requests.exceptions.ConnectionError:
        print("Erreur : Impossible de se connecter au serveur. Vérifie que l'API C# est démarrée.")

if __name__ == "__main__":
    while True:
        print("\nSUIVI DES TACHES : Menu \n1. Afficher toutes les tâches")
        print("2. Afficher une tâche précise")
        print("3. Ajouter une tâche")
        print("4. Modifier une tâche")
        print("5. Supprimer une tâche")
        print("6. Quitter")
        choix = input("\nChoix : ")
        if choix == "1":
            afficher_taches()
        elif choix == "2":
            afficher_tache_precise()
        elif choix == "3":
            ajouter_tache()
        elif choix == "4":
            modifier_tache()
        elif choix == "5":
            supprimer_tache()
        elif choix == "6":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")