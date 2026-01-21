import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.repository import get_crm_inactive_clients, get_crm_vip_clients

class CRMDashboard:
    def __init__(self, parent, db_conn):
        self.db_conn = db_conn
        self.win = ttk.Toplevel(parent)
        self.win.title("CRM & Marketing")
        self.win.geometry("1000x700")
        
        main = ttk.Frame(self.win, padding=20)
        main.pack(fill=BOTH, expand=True)
        
        ttk.Label(main, text="📢 Campanii & Fidelizare", font=("Bold", 20), bootstyle="info").pack(pady=(0,20))
        
        tabs = ttk.Notebook(main)
        tabs.pack(fill=BOTH, expand=True)
        
        
        t1 = ttk.Frame(tabs, padding=10); tabs.add(t1, text="⚠️ Clienți Inactivi")
        f1 = ttk.Frame(t1); f1.pack(fill=X, pady=10)
        ttk.Label(f1, text="Inactivi de (luni):").pack(side=LEFT)
        self.v_mon = ttk.StringVar(value="6"); ttk.Entry(f1, textvariable=self.v_mon, width=5).pack(side=LEFT, padx=5)
        ttk.Button(f1, text="Cauta (NOT IN)", command=lambda: self.run_churn(self.tr1), bootstyle="warning").pack(side=LEFT)
        self.tr1 = self.mk_tree(t1)

        t2 = ttk.Frame(tabs, padding=10); tabs.add(t2, text="💎 Clienți VIP")
        f2 = ttk.Frame(t2); f2.pack(fill=X, pady=10)
        ttk.Label(f2, text="Total cheltuit > (RON):").pack(side=LEFT)
        self.v_sum = ttk.StringVar(value="2000"); ttk.Entry(f2, textvariable=self.v_sum, width=10).pack(side=LEFT, padx=5)
        ttk.Button(f2, text="Cauta (Subcerere)", command=lambda: self.run_vip(self.tr2), bootstyle="success").pack(side=LEFT)
        self.tr2 = self.mk_tree(t2)

    def mk_tree(self, p):
        t = ttk.Treeview(p, show="headings", bootstyle="info"); t.pack(fill=BOTH, expand=True)
        return t

    def run_churn(self, t):
        try:
            r, c = get_crm_inactive_clients(self.db_conn, self.v_mon.get())
            self.fill(t, r, c)
        except Exception as e: messagebox.showerror("Err", str(e))

    def run_vip(self, t):
        try:
            r, c = get_crm_vip_clients(self.db_conn, self.v_sum.get())
            self.fill(t, r, c)
        except Exception as e: messagebox.showerror("Err", str(e))

    def fill(self, t, rows, cols):
        t.delete(*t.get_children()); t["columns"] = cols
        for c in cols: t.heading(c, text=c); t.column(c, width=150)
        for r in rows: t.insert("", "end", values=r)

def open_crm_window(p, c): CRMDashboard(p, c)