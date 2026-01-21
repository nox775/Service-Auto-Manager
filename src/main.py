import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import traceback

# --- IMPORTURI BAZA DE DATE ---
from database.database import db
from UI.ui_components import create_input_row

# --- IMPORTURI MODULE (Cu protectie la erori) ---
try:
    from clients import clients_window
    from vehicles import vehicles_window
    from mechanics import mechanics_window
    from services import services_window
    from suppliers import suppliers_window
    from reports import reports_window
    from stats import statistics_window 
    from crm import crm_window
    from audit import audit_window
except Exception as e:
    print(f"Eroare critică la importul modulelor: {e}")
   

# --- LOGICA APLICATIEI ---

def login_action():
    """ Gestioneaza conectarea la baza de date """
    h = host_var.get()
    u = user_var.get()
    p = pass_var.get()
    po = port_var.get()
    d = db_name_var.get()
    
    try:
        # Incercam conectarea
        if db.connect(h, u, p, po, d):
            status_var.set("Status: CONECTAT ✅")
            lbl_status.config(bootstyle="success inverse")
            messagebox.showinfo("Succes", "Conexiune realizată cu succes!")
            
            # Activam toate butoanele din meniu
            for btn in buttons_list: 
                btn.config(state="normal")
        else: 
            raise Exception("Date incorecte sau server MySQL oprit.")
            
    except Exception as e:
        status_var.set("Status: EROARE ❌")
        lbl_status.config(bootstyle="danger inverse")
        messagebox.showerror("Eroare Conectare", f"Nu s-a putut conecta:\n{str(e)}")

def check_open(func):
    """ Wrapper sigur: Verifica conexiunea inainte de a deschide fereastra """
    try:
        conn = db.get_connection()
        if conn and conn.is_connected():
            func(app, conn)
        else:
            messagebox.showwarning("Atenție", "Te rog să te conectezi la baza de date întâi (Login).")
    except Exception as e:
        print(traceback.format_exc())
        messagebox.showerror("Eroare Modul", f"A apărut o eroare la deschiderea modulului:\n{e}")

# --- WRAPPERS BUTOANE ---
def d_cl(): check_open(clients_window.open_clients_window)
def d_ve(): check_open(vehicles_window.open_vehicle_window)
def d_me(): check_open(mechanics_window.open_mechanics_window)
def d_se(): check_open(services_window.open_services_window)
def d_fu(): check_open(suppliers_window.open_suppliers_window)
def d_re(): check_open(reports_window.open_reports_window)
def d_st(): check_open(statistics_window.open_statistics_window)
def d_crm(): check_open(crm_window.open_crm_window)
def d_audit(): check_open(audit_window.open_audit_window)


# --- INTERFATA GRAFICA (GUI) ---

app = ttk.Window(themename="superhero")
app.title("Service Auto Manager v3.0 Ultimate")
app.geometry("1150x850")

# Container Principal
main = ttk.Frame(app, padding=20)
main.pack(fill=BOTH, expand=True)

# 1. HEADER
header = ttk.Frame(main)
header.pack(fill=X, pady=(0, 20))

ttk.Label(header, text="SERVICE AUTO MANAGER", font=("Helvetica", 28, "bold"), bootstyle="light").pack(anchor="center")
ttk.Label(header, text="Platformă Integrată: Gestiune, Marketing & Audit", font=("Helvetica", 12), bootstyle="secondary").pack(anchor="center")
ttk.Separator(main, orient="horizontal").pack(fill=X, pady=10)

# 2. ZONA LOGIN (Card Style)
login_card = ttk.Labelframe(main, text=" 🔒 Configurare Server ", padding=15, bootstyle="info")
login_card.pack(fill=X, pady=10)

# Grid Input-uri
inps = ttk.Frame(login_card)
inps.pack(fill=X)

# Variabile
host_var = tk.StringVar(value="localhost")
user_var = tk.StringVar(value="root")
pass_var = tk.StringVar()
port_var = tk.StringVar(value="3306")
db_name_var = tk.StringVar(value="evidentaservice")
status_var = tk.StringVar(value="Status: Deconectat")

# Coloana Stanga
c1 = ttk.Frame(inps)
c1.pack(side=LEFT, fill=X, expand=True, padx=10)
create_input_row(c1, "Host:", host_var)
create_input_row(c1, "User:", user_var)

# Coloana Dreapta
c2 = ttk.Frame(inps)
c2.pack(side=LEFT, fill=X, expand=True, padx=10)
create_input_row(c2, "Parola:", pass_var, show="*")
create_input_row(c2, "Bază date:", db_name_var)

# Bara Actiune Login
btn_area = ttk.Frame(login_card)
btn_area.pack(fill=X, pady=10)

ttk.Button(btn_area, text="CONECTARE SERVER", command=login_action, bootstyle="primary", width=25).pack(side=LEFT, padx=10)
lbl_status = ttk.Label(btn_area, textvariable=status_var, font=("Segoe UI", 10, "bold"), bootstyle="secondary inverse", padding=6)
lbl_status.pack(side=LEFT, padx=10)

# 3. DASHBOARD (MENIU PRINCIPAL)
dash = ttk.Frame(main)
dash.pack(fill=BOTH, expand=True, pady=20)

ttk.Label(dash, text="📦 Module Disponibile", font=("Helvetica", 16, "bold"), bootstyle="warning").pack(anchor="w", pady=(0,15))

# Grid Butoane (3 randuri x 4 coloane)
grid = ttk.Frame(dash)
grid.pack(fill=BOTH, expand=True)
for i in range(4): grid.columnconfigure(i, weight=1)
for i in range(3): grid.rowconfigure(i, weight=1)

buttons_list = []

def create_tile(parent, text, command, r, c, style):
    """ Helper pentru crearea butoanelor tip Tile """
    btn = ttk.Button(
        parent, 
        text=text, 
        command=command, 
        state="disabled", # Initial dezactivat pana la login
        bootstyle=f"{style} outline", 
        width=20
    )
    btn.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
    buttons_list.append(btn)

# --- RANDUL 1: OPERATIONAL ---
create_tile(grid, "👥\nCLIENȚI", d_cl, 0, 0, "success")
create_tile(grid, "🚗\nVEHICULE", d_ve, 0, 1, "success")
create_tile(grid, "🔧\nMECANICI", d_me, 0, 2, "warning")
create_tile(grid, "📋\nSERVICII", d_se, 0, 3, "info")

# --- RANDUL 2: LOGISTICA & RAPOARTE ---
create_tile(grid, "📦\nFURNIZORI", d_fu, 1, 0, "secondary")
create_tile(grid, "📊\nRAPOARTE OP.", d_re, 1, 1, "danger")
create_tile(grid, "📈\nSTATISTICI", d_st, 1, 2, "primary")
create_tile(grid, "📢\nCRM / MKT", d_crm, 1, 3, "info") # Modul Nou

# --- RANDUL 3: ADMIN & EXIT ---
create_tile(grid, "⚡\nAUDIT & STOC", d_audit, 2, 0, "danger")
create_tile(grid, "🚪\nIESIRE", app.destroy, 2, 3, "dark")

# Footer
foot = ttk.Frame(app, padding=10, bootstyle="dark")
foot.pack(side=BOTTOM, fill=X)
ttk.Label(foot, text="© 2025 Service Auto Manager - Versiune Licență Academică", font=("Arial", 9), bootstyle="inverse-dark").pack(side=RIGHT)

if __name__ == "__main__":
    app.mainloop()