import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

# functiile pentru acces la baza de date
from database.repository import fetch_all_vehicle

# utilitar pentru curatarea tabelului
from UI.ui_components import clear_treeview

# fereastra pentru adaugarea vehiculelor (din folderul 'vehicles')
from vehicles import add_vehicle_window


class VehicleDashboard:
    def __init__(self, parent, db_conn):
        self.db_conn = db_conn
        
        # fereastra noua (Toplevel)
        self.win = ttk.Toplevel(parent)
        self.win.title("Gestiune vehicule")
        self.win.geometry("1800x1200")
        
        # titlu
        ttk.Label(self.win, text="Lista vehicule", font=("Calibri", 20, "bold")).pack(pady=10)

        # --- toolbar (butoane actiuni) ---
        toolbar = ttk.Frame(self.win)
        toolbar.pack(fill="x", padx=10, pady=5)

        ttk.Button(
            toolbar,
            text="+ Adauga vehicul",
            command=self.open_add_modal,
            bootstyle="success"
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="Refresh tabel",
            command=self.refresh_table,
            bootstyle="info"
        ).pack(side="left", padx=5)
        
        # --- tabel vehicule ---
        cols = (
            "VehiculID",
            "ClientID",
            "NumarInmatriculare",
            "SerieSasiu",
            "Marca",
            "Model",
            "AnFabricatie",
            "CodMotor",
            "CapacitateCilindrica",
            "TipCombustibil",
        )
        self.tree = ttk.Treeview(self.win, columns=cols, show="headings")
        
        # configurare coloane
        for col in cols:
            self.tree.heading(col, text=col)
            w = 50 if col == "VehiculID" else 150
            self.tree.column(col, width=w, anchor="w")
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # incarcam datele la deschiderea ferestrei
        self.refresh_table()

    def refresh_table(self):
        """Reincarca datele in tabel."""
        clear_treeview(self.tree)
        if self.db_conn and self.db_conn.is_connected():
            rows = fetch_all_vehicle(self.db_conn)
            for row in rows:
                self.tree.insert("", "end", values=row)
        else:
            messagebox.showerror("Eroare", "Conexiunea la baza de date a fost pierduta!")

    def open_add_modal(self):
        """Deschide fereastra pentru adaugarea unui vehicul nou."""
        # dupa adaugare, actualizam tabelul curent
        add_vehicle_window.open_add_vehicle_window(self.win, self.db_conn, self.refresh_table)


def open_vehicle_window(parent, db_conn):
    """Functie helper apelata din main.py pentru deschiderea ferestrei de vehicule."""
    VehicleDashboard(parent, db_conn)
