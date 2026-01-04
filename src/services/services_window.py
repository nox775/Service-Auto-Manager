import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.repository import fetch_all_services, search_services, delete_service
from services import add_service_window

class ServicesDashboard:
    def __init__(self, parent, db_conn):
        self.db_conn = db_conn
        self.win = ttk.Toplevel(parent)
        self.win.title("Catalog Servicii")
        self.win.geometry("1000x600")

        main = ttk.Frame(self.win, padding=20); main.pack(fill=BOTH, expand=True)
        top = ttk.Frame(main); top.pack(fill=X, pady=(0, 20))
        ttk.Label(top, text="📋 Catalog", font=("Bold", 20), bootstyle="info").pack(side=LEFT)
        
        sf = ttk.Labelframe(top, text="🔍 Caută", padding=10); sf.pack(side=RIGHT)
        self.s_var = ttk.StringVar()
        ttk.Entry(sf, textvariable=self.s_var).pack(side=LEFT)
        ttk.Button(sf, text="Ok", command=self.do_search, bootstyle="info").pack(side=LEFT, padx=5)
        ttk.Button(sf, text="X", command=self.do_reset, bootstyle="secondary-outline").pack(side=LEFT)

        tb = ttk.Frame(main); tb.pack(fill=X, pady=(0,10))
        ttk.Button(tb, text="➕", command=self.add, bootstyle="success").pack(side=LEFT, padx=2)
        ttk.Button(tb, text="✏️", command=self.edit, bootstyle="warning").pack(side=LEFT, padx=2)
        ttk.Button(tb, text="❌", command=self.delete, bootstyle="danger").pack(side=LEFT, padx=2)

        cols = ("ID", "DENUMIRE", "DESCRIERE", "TARIF/ORA", "ORE EST.")
        self.tree = ttk.Treeview(main, columns=cols, show="headings", bootstyle="info")
        for c in cols:
            if c == "ID": self.tree.column(c, width=0, stretch=False)
            else: self.tree.heading(c, text=c); self.tree.column(c, width=150)
            if c == "DESCRIERE": self.tree.column(c, width=300)

        self.tree.pack(fill=BOTH, expand=True)
        self.do_reset()

    def do_search(self):
        t = self.s_var.get().strip()
        self.fill(search_services(self.db_conn, t) if t else fetch_all_services(self.db_conn))
    def do_reset(self):
        self.s_var.set(""); self.fill(fetch_all_services(self.db_conn))
    def fill(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows: self.tree.insert("", "end", values=r)
    def add(self): add_service_window.open_service_form(self.win, self.db_conn, self.do_reset)
    def edit(self):
        s = self.tree.selection()
        if s: add_service_window.open_service_form(self.win, self.db_conn, self.do_reset, self.tree.item(s[0], "values"))
    def delete(self):
        s = self.tree.selection()
        if s and messagebox.askyesno("?", "Stergi?"): delete_service(self.db_conn, self.tree.item(s[0], "values")[0]); self.do_reset()

def open_services_window(p, c): ServicesDashboard(p, c)