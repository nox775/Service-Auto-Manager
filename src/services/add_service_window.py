import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from database.repository import insert_service, update_service

def open_service_form(parent, db_conn, refresh_callback, data_to_edit=None):
    win = ttk.Toplevel(parent)
    is_edit = data_to_edit is not None
    win.title("Service" if is_edit else "Adaugă Serviciu")
    win.geometry("500x500")

    nume_var = tk.StringVar()
    desc_var = tk.StringVar()
    tarif_var = tk.StringVar()
    timp_var = tk.StringVar()

    if is_edit:
        nume_var.set(data_to_edit[1])
        desc_var.set(data_to_edit[2])
        tarif_var.set(data_to_edit[3])
        timp_var.set(data_to_edit[4])

    def add_f(label, var):
        f = ttk.Frame(win)
        f.pack(pady=5, fill="x", padx=20)
        ttk.Label(f, text=label, width=15).pack(side="left")
        ttk.Entry(f, textvariable=var).pack(side="left", fill="x", expand=True)

    add_f("Denumire:", nume_var)
    add_f("Descriere:", desc_var)
    add_f("Tarif/Ora (RON):", tarif_var)
    add_f("Timp Est. (h):", timp_var)

    def save():
        if not nume_var.get() or not tarif_var.get():
            messagebox.showwarning("!", "Denumire si Tarif obligatorii")
            return
        
        if is_edit:
            ok = update_service(db_conn, data_to_edit[0], nume_var.get(), desc_var.get(), tarif_var.get(), timp_var.get())
        else:
            ok = insert_service(db_conn, nume_var.get(), desc_var.get(), tarif_var.get(), timp_var.get())
        
        if ok: win.destroy(); refresh_callback()
        else: messagebox.showerror("Err", "Eroare SQL")

    ttk.Button(win, text="Salveaza", command=save, bootstyle="success").pack(pady=20)