import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from database.repository import insert_supplier, update_supplier

def open_supplier_form(parent, db_conn, refresh_callback, data_to_edit=None):
    win = ttk.Toplevel(parent)
    is_edit = data_to_edit is not None
    win.title("Furnizor" if is_edit else "Adaugă Furnizor")
    win.geometry("500x550")

    nume_var = tk.StringVar()
    contact_var = tk.StringVar()
    tel_var = tk.StringVar()
    email_var = tk.StringVar()
    cui_var = tk.StringVar()

    if is_edit:
        nume_var.set(data_to_edit[1])
        contact_var.set(data_to_edit[2])
        tel_var.set(data_to_edit[3])
        email_var.set(data_to_edit[4])
        cui_var.set(data_to_edit[5])

    def add_f(label, var):
        f = ttk.Frame(win)
        f.pack(pady=5, fill="x", padx=20)
        ttk.Label(f, text=label, width=15).pack(side="left")
        ttk.Entry(f, textvariable=var).pack(side="left", fill="x", expand=True)

    add_f("Nume Firma:", nume_var)
    add_f("Pers. Contact:", contact_var)
    add_f("Telefon:", tel_var)
    add_f("Email:", email_var)
    add_f("CUI:", cui_var)

    def save():
        if not nume_var.get():
            messagebox.showwarning("!", "Nume firma obligatoriu")
            return
        
        if is_edit:
            ok = update_supplier(db_conn, data_to_edit[0], nume_var.get(), contact_var.get(), tel_var.get(), email_var.get(), cui_var.get())
        else:
            ok = insert_supplier(db_conn, nume_var.get(), contact_var.get(), tel_var.get(), email_var.get(), cui_var.get())
        
        if ok: win.destroy(); refresh_callback()
        else: messagebox.showerror("Err", "Eroare SQL")

    ttk.Button(win, text="Salveaza", command=save, bootstyle="success").pack(pady=20)