import tkinter as tk
from tkinter import messagebox, simpledialog, font, ttk
import requests
import subprocess
import sys
import os
import time

API_URL = "http://localhost:5209/api/SuiviDeTaches"  # Mets ici le port de ton API

def tester_connexion(api_url):
    try:
        requests.get(api_url, timeout=2)
        return True
    except Exception:
        return False

def lancer_api(api_path):
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_CONSOLE
    else:
        creationflags = 0
    subprocess.Popen(
        ["dotnet", "run"],
        cwd=api_path,
        creationflags=creationflags
    )
    time.sleep(3)

# --- Tooltip pour afficher la description ---
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.last_index = None

    def showtip(self, text, x, y):
        self.hidetip()
        if not text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("Segoe UI", 10))
        label.pack(ipadx=1)

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

def get_task_description(index):
    try:
        ligne = listbox.get(index)
        id_tache = ligne.split(" - ")[0]
        response = requests.get(f"{API_URL}/{id_tache}")
        if response.status_code == 200:
            t = response.json()
            return t.get("description", "")
    except Exception:
        pass
    return ""

def on_listbox_motion(event):
    index = listbox.nearest(event.y)
    if index != tooltip.last_index and 0 <= index < listbox.size():
        tooltip.last_index = index
        desc = get_task_description(index)
        if desc:
            x = event.x_root + 20
            y = event.y_root + 10
            tooltip.showtip(desc, x, y)
        else:
            tooltip.hidetip()
    elif not (0 <= index < listbox.size()):
        tooltip.hidetip()

def on_listbox_leave(event):
    tooltip.hidetip()
    tooltip.last_index = None

def rafraichir():
    try:
        listbox.delete(0, tk.END)
        response = requests.get(API_URL)
        if response.status_code == 200:
            tasks = response.json()
            if not tasks:
                listbox.insert(tk.END, "Aucune tâche enregistrée pour le moment.")
                # On ne peut pas styliser une seule ligne, alors on grise toute la Listbox si vide
                listbox.config(fg="#888888", font=('Segoe UI', 12, 'italic'), justify="center")
            else:
                listbox.config(fg="black", font=("Segoe UI", 11), justify="left")
                for t in tasks:
                    statut = "✅ Terminé" if t['isCompleted'] else "🕓 En cours"
                    listbox.insert(tk.END, f"{t['id']} - {t['title']} ({statut})")
        else:
            messagebox.showerror("Erreur", "Erreur lors de la récupération des tâches.")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erreur", "Impossible de se connecter au serveur.")

def ajouter():
    titre = simpledialog.askstring("Titre", "Titre de la tâche :", parent=root)
    if not titre:
        return
    description = simpledialog.askstring("Description", "Description de la tâche :", parent=root)
    if description is None:
        return
    data = {"title": titre, "description": description, "isCompleted": False}
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            messagebox.showinfo("Succès", "Tâche ajoutée !", parent=root)
            rafraichir()
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'ajout.", parent=root)
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erreur", "Impossible de se connecter au serveur.", parent=root)

def supprimer():
    selection = listbox.curselection()
    if not selection or listbox.get(selection[0]).startswith("Aucune tâche"):
        messagebox.showwarning("Attention", "Sélectionne une tâche à supprimer.", parent=root)
        return
    ligne = listbox.get(selection[0])
    id_tache = ligne.split(" - ")[0]
    titre = "cette tâche"
    # Optionnel : récupérer le titre réel de la tâche pour l'afficher dans le message
    if " - " in ligne:
        titre = ligne.split(" - ")[1].split(" (")[0]
    if not messagebox.askokcancel("Confirmation", f"Voulez-vous vraiment supprimer la tâche : '{titre}' ?", parent=root):
        return
    try:
        response = requests.delete(f"{API_URL}/{id_tache}")
        if response.status_code == 204:
            messagebox.showinfo("Succès", "Tâche supprimée !", parent=root)
            rafraichir()
        elif response.status_code == 404:
            messagebox.showerror("Erreur", "Tâche non trouvée.", parent=root)
        else:
            messagebox.showerror("Erreur", "Erreur lors de la suppression.", parent=root)
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erreur", "Impossible de se connecter au serveur.", parent=root)

def quitter():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application ?", parent=root):
        root.destroy()

def modifier():
    selection = listbox.curselection()
    if not selection or listbox.get(selection[0]).startswith("Aucune tâche"):
        messagebox.showwarning("Attention", "Sélectionne une tâche à modifier.", parent=root)
        return
    ligne = listbox.get(selection[0])
    id_tache = ligne.split(" - ")[0]
    # Récupérer la tâche actuelle
    try:
        response = requests.get(f"{API_URL}/{id_tache}")
        if response.status_code == 200:
            t = response.json()
            nouveau_titre = simpledialog.askstring("Modifier le titre", "Nouveau titre :", initialvalue=t['title'], parent=root)
            if not nouveau_titre:
                return
            nouvelle_description = simpledialog.askstring("Modifier la description", "Nouvelle description :", initialvalue=t['description'], parent=root)
            if nouvelle_description is None:
                return
            is_completed = messagebox.askyesno("Statut", "La tâche est-elle terminée ?", parent=root)
            data = {
                "id": t['id'],
                "title": nouveau_titre,
                "description": nouvelle_description,
                "isCompleted": is_completed
            }
            resp = requests.put(f"{API_URL}/{id_tache}", json=data)
            if resp.status_code == 204:
                messagebox.showinfo("Succès", "Tâche modifiée !", parent=root)
                rafraichir()
            elif resp.status_code == 404:
                messagebox.showerror("Erreur", "Tâche non trouvée.", parent=root)
            else:
                messagebox.showerror("Erreur", "Erreur lors de la modification.", parent=root)
        else:
            messagebox.showerror("Erreur", "Impossible de récupérer la tâche.", parent=root)
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Erreur", "Impossible de se connecter au serveur.", parent=root)

# --- Interface graphique ---
root = tk.Tk()
root.title("Suivi de Tâches")
root.geometry("700x500")
root.configure(bg="#f5f6fa")
root.resizable(False, False)  # Fenêtre non modifiable

root.protocol("WM_DELETE_WINDOW", quitter)  # Confirmation sur la croix

# Police personnalisée
titre_font = font.Font(family="Segoe UI", size=16, weight="bold")
btn_font = font.Font(family="Segoe UI", size=11, weight="bold")

titre_label = tk.Label(root, text="Gestionnaire de Tâches", font=titre_font, bg="#f5f6fa", fg="#273c75")
titre_label.pack(pady=(15, 5))

frame = tk.Frame(root, bg="#f5f6fa")
frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

listbox = tk.Listbox(
    frame, width=80, height=15, font=("Segoe UI", 11), bd=2, relief=tk.GROOVE,
    selectbackground="#dff9fb", selectforeground="black"
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

btn_frame = tk.Frame(root, bg="#f5f6fa")
btn_frame.pack(pady=10)

style = ttk.Style()
style.theme_use('clam')
style.configure("Rounded.TButton",
    font=btn_font,
    foreground="white",
    background="#40739e",
    borderwidth=0,
    focusthickness=3,
    focuscolor='none',
    padding=10,
    relief="flat"
)
style.map("Rounded.TButton",
    background=[('active', '#273c75')],
    foreground=[('active', 'white')]
)



ttk.Button(btn_frame, text="Rafraîchir", command=rafraichir, style="Rounded.TButton").pack(side=tk.LEFT, padx=7)
ttk.Button(btn_frame, text="Ajouter", command=ajouter, style="Rounded.TButton").pack(side=tk.LEFT, padx=7)
ttk.Button(btn_frame, text="Modifier", command=modifier, style="Rounded.TButton").pack(side=tk.LEFT, padx=7)
ttk.Button(btn_frame, text="Supprimer", command=supprimer, style="Rounded.TButton").pack(side=tk.LEFT, padx=7)
ttk.Button(btn_frame, text="Quitter", command=quitter, style="Rounded.TButton").pack(side=tk.LEFT, padx=7)

# Tooltip pour la description au survol
tooltip = ToolTip(listbox)
listbox.bind("<Motion>", on_listbox_motion)
listbox.bind("<Leave>", on_listbox_leave)

rafraichir()
root.mainloop()