import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.repository import fetch_all_vehicles, search_vehicles, delete_vehicle, get_vehicle_history_data
from vehicles import add_vehicle_window

class VehiclesDashboard:
    def __init__(self, parent, db_conn):
        self.db_conn = db_conn
        self.win = ttk.Toplevel(parent)
        self.win.title("Parc Auto")
        self.win.geometry("1200x750")

        main = ttk.Frame(self.win, padding=20); main.pack(fill=BOTH, expand=True)

        top = ttk.Frame(main); top.pack(fill=X, pady=(0, 20))
        ttk.Label(top, text="🚗 Gestiune Vehicule", font=("Bold", 20), bootstyle="primary").pack(side=LEFT)
        
        sf = ttk.Labelframe(top, text="🔍 Caută (Nr/Sasiu/Nume)", padding=10); sf.pack(side=RIGHT)
        self.s_var = ttk.StringVar()
        ttk.Entry(sf, textvariable=self.s_var, width=25).pack(side=LEFT, padx=5)
        ttk.Button(sf, text="Caută", command=self.do_search, bootstyle="info").pack(side=LEFT)
        ttk.Button(sf, text="Reset", command=self.do_reset, bootstyle="secondary-outline").pack(side=LEFT, padx=5)

        tb = ttk.Frame(main); tb.pack(fill=X, pady=(0,10))
        ttk.Button(tb, text="➕ Adaugă", command=self.add, bootstyle="success").pack(side=LEFT, padx=5)
        ttk.Button(tb, text="✏️ Editează", command=self.edit, bootstyle="warning").pack(side=LEFT, padx=5)
        ttk.Button(tb, text="❌ Șterge", command=self.delete, bootstyle="danger").pack(side=LEFT, padx=5)
        ttk.Button(tb, text="📜 ISTORIC", command=self.show_history, bootstyle="info").pack(side=LEFT, padx=20)

        # Structura query-ului: (VID, CID, PROPRIETAR, NR, SASIU, MARCA, MODEL, AN, MOTOR, CC, COMB)
        cols = ("ID", "CID", "PROPRIETAR", "NR. INMAT", "SASIU", "MARCA", "MODEL", "AN", "MOTOR", "CC", "COMB")
        self.tree = ttk.Treeview(main, columns=cols, show="headings", bootstyle="primary")
        
        for c in cols:
            # ASCUNDEM ID SI CID
            if c == "ID" or c == "CID":
                self.tree.column(c, width=0, stretch=False)
            else:
                self.tree.heading(c, text=c)
                self.tree.column(c, width=100)
        
        sy = ttk.Scrollbar(main, command=self.tree.yview); sy.pack(side=RIGHT, fill=Y)
        self.tree.config(yscroll=sy.set); self.tree.pack(fill=BOTH, expand=True)
        self.do_reset()

    def do_search(self):
        t = self.s_var.get().strip()
        self.fill(search_vehicles(self.db_conn, t) if t else fetch_all_vehicles(self.db_conn))
    def do_reset(self):
        self.s_var.set(""); self.fill(fetch_all_vehicles(self.db_conn))
    def fill(self, rows):
        self.tree.delete(*self.tree.get_children())
        for r in rows: self.tree.insert("", "end", values=r)
    def add(self): add_vehicle_window.open_vehicle_form(self.win, self.db_conn, self.do_reset)
    def edit(self):
        s = self.tree.selection()
        if s: add_vehicle_window.open_vehicle_form(self.win, self.db_conn, self.do_reset, self.tree.item(s[0], "values"))
    def delete(self):
        s = self.tree.selection()
        if s and messagebox.askyesno("?", "Stergi?"): delete_vehicle(self.db_conn, self.tree.item(s[0], "values")[0]); self.do_reset()
    def show_history(self):
        s = self.tree.selection()
        if not s: return
        r = self.tree.item(s[0], "values")
        from ttkbootstrap.scrolled import ScrolledFrame
        w = ttk.Toplevel(self.win); w.geometry("800x600"); w.title(f"Istoric {r[3]}")
        ttk.Label(w, text=f"Istoric {r[3]} ({r[5]} {r[6]})", font=("Bold", 16)).pack(pady=10)
        sf = ScrolledFrame(w); sf.pack(fill=BOTH, expand=True)
        data = get_vehicle_history_data(self.db_conn, r[0])
        if not data: ttk.Label(sf, text="Fara intrari.").pack()
        for i in data:
            d=i['deviz']
            fr = ttk.Labelframe(sf, text=f"Deviz {d[1]} | {d[2]}", padding=10)
            fr.pack(fill=X, padx=10, pady=5)
            ttk.Label(fr, text=f"Problema: {d[3]}").pack(anchor="w")
            ttk.Label(fr, text=f"Total: {d[4]} RON", bootstyle="danger").pack(anchor="e")

def open_vehicle_window(p, c): VehiclesDashboard(p, c)