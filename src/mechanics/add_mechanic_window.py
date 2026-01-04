import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from database.repository import insert_mechanic, update_mechanic

def open_mechanic_form(parent, db_conn, refresh_callback, data_to_edit=None):
    win = ttk.Toplevel(parent)
    is_edit = data_to_edit is not None
    win.title("Editare Mecanic" if is_edit else "Adaugă Mecanic")
    win.geometry("400x350") # Mai mic putin

    ttk.Label(win, text="Date Mecanic", font="Calibri 14 bold").pack(pady=10)

    nume_var = tk.StringVar()
    prenume_var = tk.StringVar()
    # spec_var = tk.StringVar()  <-- SCOS
    data_var = tk.StringVar()

    if is_edit:
        # data_to_edit vine acum fara specializare: (ID, Nume, Prenume, Data)
        nume_var.set(data_to_edit[1])
        prenume_var.set(data_to_edit[2])
        data_var.set(data_to_edit[3]) 

    def add_f(label, var):
        f = ttk.Frame(win)
        f.pack(pady=5, fill="x", padx=20)
        ttk.Label(f, text=label, width=15).pack(side="left")
        ttk.Entry(f, textvariable=var).pack(side="left", fill="x", expand=True)

    add_f("Nume:", nume_var)
    add_f("Prenume:", prenume_var)
    # add_f("Specializare:", spec_var) <-- SCOS
    add_f("Data Angajarii:", data_var)
    ttk.Label(win, text="(Format: YYYY-MM-DD)", font="Arial 8").pack()

    def save():
        if not nume_var.get():
            messagebox.showwarning("!", "Nume obligatoriu")
            return
        
        # Apelam functiile actualizate (fara parametru specializare)
        if is_edit:
            ok = update_mechanic(db_conn, data_to_edit[0], nume_var.get(), prenume_var.get(), data_var.get())
        else:
            ok = insert_mechanic(db_conn, nume_var.get(), prenume_var.get(), data_var.get())
        
        if ok:
            win.destroy()
            refresh_callback()
        else:
            messagebox.showerror("Eroare", "Operatia a esuat")

    ttk.Button(win, text="Salveaza", command=save, bootstyle="success").pack(pady=20)