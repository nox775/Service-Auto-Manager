import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.repository import get_audit_dead_stock, get_audit_top_mechanics_revenue

class AuditDashboard:
    def __init__(self, parent, db_conn):
        self.db_conn = db_conn
        self.win = ttk.Toplevel(parent)
        self.win.title("Audit & Eficiență")
        self.win.geometry("1000x700")
        
        main = ttk.Frame(self.win, padding=20)
        main.pack(fill=BOTH, expand=True)
        
        ttk.Label(main, text="⚡ Audit Intern", font=("Bold", 20), bootstyle="danger").pack(pady=(0,20))
        
        
        pan = ttk.PanedWindow(main, orient=HORIZONTAL); pan.pack(fill=BOTH, expand=True)
        
       
        f1 = ttk.Labelframe(pan, text="💀 Piese Fără Mișcare (Dead Stock)", padding=10)
        pan.add(f1, weight=1)
        
        ctrl1 = ttk.Frame(f1); ctrl1.pack(fill=X, pady=5)
        ttk.Label(ctrl1, text="Filtru Furnizor:").pack(side=LEFT)
        self.v_fur = ttk.StringVar(); ttk.Entry(ctrl1, textvariable=self.v_fur, width=15).pack(side=LEFT, padx=5)
        ttk.Button(ctrl1, text="Analizează (NOT IN)", command=lambda: self.run_ds(self.tr1), bootstyle="secondary").pack(side=LEFT)
        
        self.tr1 = self.mk_tree(f1)

        f2 = ttk.Labelframe(pan, text="🏆 Top Performanță Mecanici", padding=10)
        pan.add(f2, weight=1)
        
        ctrl2 = ttk.Frame(f2); ctrl2.pack(fill=X, pady=5)
        ttk.Button(ctrl2, text="Vezi Top (> Media Globală)", command=lambda: self.run_top(self.tr2), bootstyle="success").pack(fill=X)
        
        self.tr2 = self.mk_tree(f2)

    def mk_tree(self, p):
        t = ttk.Treeview(p, show="headings", bootstyle="secondary"); t.pack(fill=BOTH, expand=True)
        return t

    def run_ds(self, t):
        r, c = get_audit_dead_stock(self.db_conn, self.v_fur.get())
        self.fill(t, r, c)

    def run_top(self, t):
        r, c = get_audit_top_mechanics_revenue(self.db_conn)
        self.fill(t, r, c)

    def fill(self, t, rows, cols):
        t.delete(*t.get_children()); t["columns"] = cols
        for c in cols: t.heading(c, text=c); t.column(c, width=100)
        for r in rows: t.insert("", "end", values=r)

def open_audit_window(p, c): AuditDashboard(p, c)