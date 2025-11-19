import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

# --- IMPORTURI ---
from database.database import db

# componente grafice (folderul UI, fisierul ui_components.py)
from UI.ui_components import create_input_row

# ferestre pentru module
from clients import clients_window
from vehicles import vehicles_window


# --- LOGICA APLICATIEI ---

def login_action():
    """
    Functia apelata la click pe butonul 'Conectare'.
    Preia datele din campuri si incearca sa faca legatura cu MySQL.
    """
    host = host_var.get()
    user = user_var.get()
    password = pass_var.get()
    port = port_var.get()
    database = db_name_var.get()

    succes = db.connect(host, user, password, port, database)
    
    if succes:
        status_var.set("Status: CONECTAT la baza de date")
        messagebox.showinfo("Succes", "Te-ai conectat cu succes la server!")
        
        # activam butoanele de module
        btn_clienti.config(state="normal")
        btn_vehicule.config(state="normal")
    else:
        status_var.set("Status: Eroare conectare")
        messagebox.showerror(
            "Eroare login",
            "Nu s-a putut realiza conexiunea la MySQL.\n"
            "Verifica daca XAMPP/MySQL este pornit si daca datele sunt corecte."
        )


def deschide_modul_clienti():
    """
    Deschide fereastra de gestiune clienti (clients_window.py).
    """
    conn = db.get_connection()
    
    if conn and conn.is_connected():
        clients_window.open_clients_window(app, conn)
    else:
        messagebox.showwarning(
            "Atentie",
            "Conexiunea s-a pierdut. Te rog sa te reconectezi."
        )


def deschide_modul_vehicule():
    """
    Deschide fereastra de gestiune vehicule (vehicles_window.py).
    """
    conn = db.get_connection()
    
    if conn and conn.is_connected():
        vehicles_window.open_vehicle_window(app, conn)
    else:
        messagebox.showwarning(
            "Atentie",
            "Conexiunea s-a pierdut. Te rog sa te reconectezi."
        )


# --- INTERFATA GRAFICA (GUI) ---

# fereastra principala
app = ttk.Window(themename="superhero")
app.title("Service Auto - Meniu principal")
app.geometry("1000x1500")

# titlu aplicatie
ttk.Label(app, text="Service Auto Manager", font=("Calibri", 26, "bold")).pack(pady=20)

# 1. zona de login
frame_login = ttk.Labelframe(app, text="1. Autentificare server", padding=15)
frame_login.pack(fill="x", padx=20, pady=5)

# variabile pentru input-uri
host_var = tk.StringVar(value="localhost")
user_var = tk.StringVar(value="root")
pass_var = tk.StringVar()
port_var = tk.StringVar(value="3306")
db_name_var = tk.StringVar(value="evidentaservice")
status_var = tk.StringVar(value="Status: Deconectat")

# aranjam input-urile pe doua coloane
grid_in = ttk.Frame(frame_login)
grid_in.pack(fill="x")

col1 = ttk.Frame(grid_in)
col1.pack(side="left", fill="x", expand=True)
create_input_row(col1, "Host:", host_var)
create_input_row(col1, "User:", user_var)

col2 = ttk.Frame(grid_in)
col2.pack(side="left", fill="x", expand=True)
create_input_row(col2, "Port:", port_var)
create_input_row(col2, "Parola:", pass_var, show="*")

create_input_row(frame_login, "Nume BD:", db_name_var)

# buton login
ttk.Button(
    frame_login,
    text="Conectare",
    command=login_action,
    bootstyle="primary"
).pack(pady=10)

ttk.Label(frame_login, textvariable=status_var, font="Arial 9 italic").pack()

# 2. zona de meniu (module)
frame_menu = ttk.Labelframe(app, text="2. Module disponibile", padding=20)
frame_menu.pack(fill="both", expand=True, padx=20, pady=10)

# buton deschidere clienti
btn_clienti = ttk.Button(
    frame_menu,
    text="Gestiune CLIENTI",
    command=deschide_modul_clienti,
    state="disabled",
    bootstyle="success outline"
)
btn_clienti.pack(fill="x", pady=5)

# buton deschidere vehicule
btn_vehicule = ttk.Button(
    frame_menu,
    text="Gestiune VEHICULE",
    command=deschide_modul_vehicule,
    state="disabled",
    bootstyle="success outline"
)
btn_vehicule.pack(fill="x", pady=5)

# buton iesire
ttk.Button(
    app,
    text="Iesire",
    command=app.destroy,
    bootstyle="danger"
).pack(side="bottom", pady=10)

# pornire aplicatie
if __name__ == "__main__":
    app.mainloop()
