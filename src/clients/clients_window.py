import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.repository import fetch_all_clients, search_clients, delete_client
from clients import add_client_window

class ClientsDashboard:
    def __init__(self, parent, db_conn):
        self.db_conn = db_conn
        self.win = ttk.Toplevel(parent)
        self.win.title("Gestiune Clienți")
        self.win.geometry("1100x750")

        main_layout = ttk.Frame(self.win, padding=20)
        main_layout.pack(fill=BOTH, expand=True)

        # Header & Search
        top = ttk.Frame(main_layout); top.pack(fill=X, pady=(0, 20))
        ttk.Label(top, text="👥 Registru Clienți", font=("Segoe UI", 20, "bold"), bootstyle="primary").pack(side=LEFT)
        
        sf = ttk.Labelframe(top, text="🔍 Caută (Nume/Tel)", padding=10)
        sf.pack(side=RIGHT)
        self.s_var = ttk.StringVar()
        ttk.Entry(sf, textvariable=self.s_var, width=25).pack(side=LEFT, padx=5)
        ttk.Button(sf, text="Caută", command=self.do_search, bootstyle="info").pack(side=LEFT)
        ttk.Button(sf, text="Reset", command=self.do_reset, bootstyle="secondary-outline").pack(side=LEFT, padx=5)

        # Toolbar
        tb = ttk.Frame(main_layout); tb.pack(fill=X, pady=(0, 10))
        ttk.Button(tb, text="➕ Adaugă", command=self.add, bootstyle="success").pack(side=LEFT, padx=5)
        ttk.Button(tb, text="✏️ Editează", command=self.edit, bootstyle="warning").pack(side=LEFT, padx=5)
        ttk.Button(tb, text="❌ Șterge", command=self.delete, bootstyle="danger").pack(side=LEFT, padx=5)

        # Tabel
        cols = ("ID", "Nume", "Prenume", "Telefon", "Email", "Tip", "CUI")
        self.tree = ttk.Treeview(main_layout, columns=cols, show="headings", bootstyle="primary")
        
        for col in cols:
            # ASCUNDEM ID-UL (Setam latime 0)
            if col == "ID":
                self.tree.column(col, width=0, stretch=False)
            else:
                self.tree.heading(col, text=col.upper())
                self.tree.column(col, width=150)

        sc = ttk.Scrollbar(main_layout, command=self.tree.yview); sc.pack(side=RIGHT, fill=Y); self.tree.config(yscroll=sc.set)
        self.tree.pack(fill=BOTH, expand=True)
        self.do_reset()

    def do_search(self):
        t = self.s_var.get().strip()
        self.fill(search_clients(self.db_conn, t) if t else fetch_all_clients(self.db_conn))

    def do_reset(self):
        self.s_var.set("")
        self.fill(fetch_all_clients(self.db_conn))

    def fill(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows: self.tree.insert("", "end", values=r)

    def add(self): add_client_window.open_client_form(self.win, self.db_conn, self.do_reset)
    def edit(self):
        s = self.tree.selection()
        if s: add_client_window.open_client_form(self.win, self.db_conn, self.do_reset, client_to_edit=self.tree.item(s[0], "values"))
    def delete(self):
        s = self.tree.selection()
        if s and messagebox.askyesno("?", "Stergi?"): delete_client(self.db_conn, self.tree.item(s[0], "values")[0]); self.do_reset()

def open_clients_window(p, c): ClientsDashboard(p, c)