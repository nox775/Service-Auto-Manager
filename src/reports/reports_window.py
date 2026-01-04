import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import messagebox
import os
from utils.pdf_generator import generate_invoice_pdf
from database.repository import * 
class ReportsDashboard:
    def __init__(self, parent, db_conn):
        self.db_conn = db_conn
        self.win = ttk.Toplevel(parent)
        self.win.title("Rapoarte & BI")
        self.win.geometry("1400x850")
        
        layout = ttk.Frame(self.win)
        layout.pack(fill=BOTH, expand=True)
        
        # Sidebar
        side = ttk.Frame(layout, padding=15, bootstyle="secondary")
        side.pack(side=LEFT, fill=Y)
        ttk.Label(side, text="📊 RAPOARTE", font=("Bold", 18), bootstyle="inverse-secondary").pack(pady=(0,20), anchor="w")
        
        menu = ScrolledFrame(side, autohide=True, bootstyle="secondary")
        menu.pack(fill=BOTH, expand=True)
        
        self.cfgs = [
            ("Vehicule & Proprietari", get_report_vehicles_owners, "🚗", "info", "Marca:", ""),
            ("Situație Devize", get_report_devize_details, "📋", "info", "Stare:", ""),
            ("Facturi Emise", get_report_invoices, "🧾", "info", "An:", ""),
            ("Mecanici & Specializări", get_report_mechanics_specs, "🔧", "info", "Spec:", ""),
            ("Stoc Piese", get_report_parts_suppliers, "📦", "info", "Stoc <:", "10"),
            ("Manoperă", get_report_labor_info, "🛠️", "info", "Mecanic:", ""),
            ("SEPARATOR", None, "", "", "", ""),
            ("Clienți VIP", get_complex_clients_above_avg, "💎", "warning", "Min RON:", "1000"),
            ("Piese Moarte", get_complex_unsold_parts, "💀", "warning", "Furnizor:", ""),
            ("Flote", get_complex_fleet_clients, "🏢", "warning", "Min Masini:", "1"),
            ("Devize Scumpe", get_complex_expensive_repairs_param, "💰", "danger", "Min RON:", "2000"),
        ]
        
        self.btns = []
        self.curr_func = None
        
        for t, f, i, s, l, d in self.cfgs:
            if t=="SEPARATOR":
                ttk.Separator(menu, orient="horizontal").pack(fill=X, pady=10)
                continue
            b = ttk.Button(menu, text=f"{i} {t}", command=lambda x=(t,f,i,s,l,d), idx=len(self.btns): self.setup(x, idx), bootstyle=f"{s}-outline", width=25)
            b.pack(pady=2, anchor="w"); self.btns.append(b)

        ttk.Button(side, text="EXIT", command=self.win.destroy, bootstyle="light-outline").pack(side=BOTTOM, fill=X, pady=10)

        # Content
        cont = ttk.Frame(layout, padding=20)
        cont.pack(side=LEFT, fill=BOTH, expand=True)
        self.head = ttk.Label(cont, text="Selecteaza Raport", font=("Bold", 24))
        self.head.pack(anchor="w")
        
        # Filter area
        self.filt = ttk.Labelframe(cont, text="Filtru", padding=10)
        self.filt.pack(fill=X, pady=10)
        self.f_lbl = ttk.Label(self.filt, text="Param:"); self.f_lbl.pack(side=LEFT)
        self.f_var = ttk.StringVar(); ttk.Entry(self.filt, textvariable=self.f_var).pack(side=LEFT, padx=10)
        ttk.Button(self.filt, text="Executa", command=self.run, bootstyle="success").pack(side=LEFT)
        self.pdf_btn = ttk.Button(self.filt, text="🖨️ PDF Detaliat", command=self.print_pdf, bootstyle="secondary", state="disabled")
        self.pdf_btn.pack(side=RIGHT)
        self.filt.pack_forget()

        # Table
        self.tree = ttk.Treeview(cont, show="headings", bootstyle="primary")
        sc = ttk.Scrollbar(cont, command=self.tree.yview); sc.pack(side=RIGHT, fill=Y); self.tree.config(yscroll=sc.set)
        self.tree.pack(fill=BOTH, expand=True)
        
        # Tag pt stoc critic
        self.tree.tag_configure("crit", foreground="red")

    def setup(self, cfg, idx):
        t, f, i, s, l, d = cfg
        self.curr_func = f
        self.head.config(text=f"{i} {t}", bootstyle=s)
        self.f_lbl.config(text=l)
        self.f_var.set(d)
        self.filt.pack(fill=X, pady=10)
        
        if "Facturi" in t: self.pdf_btn.config(state="normal")
        else: self.pdf_btn.config(state="disabled")

        for x, btn in enumerate(self.btns):
            bs = "info" if x<6 else ("warning" if x<9 else "danger")
            btn.config(bootstyle=f"{bs}-{'solid' if x==idx else 'outline'}")
            
        self.run()

    def run(self):
        if not self.curr_func: return
        self.tree.delete(*self.tree.get_children()); self.tree["columns"]=[]
        try:
            r, c = self.curr_func(self.db_conn, self.f_var.get())
            self.tree["columns"] = c
            stoc_idx = -1
            
            for k, col in enumerate(c):
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100 if "ID" not in col else 50)
                if "Stoc" in col: stoc_idx = k

            for row in r:
                tag = "normal"
                if stoc_idx != -1 and row[stoc_idx] < 5: tag = "crit"
                self.tree.insert("", "end", values=[x if x else "-" for x in row], tags=(tag,))
        except Exception as e: messagebox.showerror("Err", str(e))

    def print_pdf(self):
        s = self.tree.selection()
        if not s: return
        
        if "Facturi" not in self.head.cget("text"):
            messagebox.showinfo("!", "Selecteaza raportul de Facturi.")
            return

        vals = self.tree.item(s[0], "values")
        serie = vals[0] # Presupunem Seria pe col 0
        
        # Apelam functia COMPLEXA de detalii
        data = fetch_invoice_details_complex(self.db_conn, serie)
        
        if data:
            f = generate_invoice_pdf(data)
            if f: 
                messagebox.showinfo("OK", f"Generat: {f}")
                os.system(f"start {f}")
        else: messagebox.showerror("Err", "Date lipsa")

def open_reports_window(p, c): ReportsDashboard(p, c)