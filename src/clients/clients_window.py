import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

# importam functiile necesare
from database.repository import fetch_all_clients

# functia pentru curatarea tabelului
from UI.ui_components import clear_treeview

# fereastra pentru adaugarea clientilor (din acelasi folder 'clients')
from clients import add_client_window


class ClientsDashboard:
    def __init__(self, parent, db_conn):
        self.db_conn = db_conn
        
        # fereastra noua (Toplevel)
        self.win = ttk.Toplevel(parent)
        self.win.title("Gestiune clienti")
        self.win.geometry("900x600")
        
        # titlu
        ttk.Label(self.win, text="Lista clienti", font=("Calibri", 20, "bold")).pack(pady=10)

        # --- toolbar (butoane actiuni) ---
        toolbar = ttk.Frame(self.win)
        toolbar.pack(fill="x", padx=10, pady=5)

        ttk.Button(
            toolbar,
            text="+ Adauga client",
            command=self.open_add_modal,
            bootstyle="success"
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="Refresh tabel",
            command=self.refresh_table,
            bootstyle="info"
        ).pack(side="left", padx=5)
        
        # --- tabel clienti ---
        cols = ("ID", "Nume", "Prenume", "Telefon", "Email", "Tip", "CUI")
        self.tree = ttk.Treeview(self.win, columns=cols, show="headings")
        
        # configurare coloane
        for col in cols:
            self.tree.heading(col, text=col)
            w = 50 if col == "ID" else 120
            self.tree.column(col, width=w, anchor="w")
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # incarcam datele la deschiderea ferestrei
        self.refresh_table()

    def refresh_table(self):
        """Reincarca datele in tabel."""
        clear_treeview(self.tree)
        if self.db_conn and self.db_conn.is_connected():
            rows = fetch_all_clients(self.db_conn)
            for row in rows:
                self.tree.insert("", "end", values=row)
        else:
            messagebox.showerror("Eroare", "Conexiunea la baza de date a fost pierduta!")

    def open_add_modal(self):
        """Deschide fereastra pentru adaugarea unui client nou."""
        # dupa ce se adauga un client, se actualizeaza tabelul curent
        add_client_window.open_add_client_window(self.win, self.db_conn, self.refresh_table)


def open_clients_window(parent, db_conn):
    """Functie helper apelata din main.py pentru deschiderea ferestrei de clienti."""
    ClientsDashboard(parent, db_conn)
