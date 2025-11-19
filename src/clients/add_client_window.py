import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from database.repository import insert_client

def open_add_client_window(parent, db_conn, refresh_callback):
    if not db_conn or not db_conn.is_connected():
        messagebox.showerror("Eroare", "Nu esti conectat la baza de date!")
        return

    win = ttk.Toplevel(parent)
    win.title("Adauga client nou")
    win.geometry("900x1200")

    ttk.Label(win, text="Date client", font="Calibri 14 bold").pack(pady=10)

    # variabile formular
    nume_var = tk.StringVar()
    prenume_var = tk.StringVar()
    tel_var = tk.StringVar()
    email_var = tk.StringVar()
    adresa_var = tk.StringVar()
    tip_client_var = tk.StringVar(value="Persoana fizica")
    cui_var = tk.StringVar()

    # functie ajutatoare pentru randurile din formular
    def add_field(label, var):
        f = ttk.Frame(win)
        f.pack(pady=5, fill="x", padx=20)
        ttk.Label(f, text=label, width=15, anchor="w").pack(side="left")
        ttk.Entry(f, textvariable=var).pack(side="left", fill="x", expand=True)

    add_field("Nume:", nume_var)
    add_field("Prenume:", prenume_var)
    add_field("Telefon:", tel_var)
    add_field("Email:", email_var)
    add_field("Adresa:", adresa_var)

    # selectare tip client (fizica / juridica)
    f_tip = ttk.Frame(win)
    f_tip.pack(pady=5, fill="x", padx=20)
    ttk.Label(f_tip, text="Tip client:", width=15, anchor="w").pack(side="left")
    combobox = ttk.Combobox(
        f_tip,
        textvariable=tip_client_var,
        values=["Persoana fizica", "Persoana juridica"],
        state="readonly"
    )
    combobox.pack(side="left", fill="x", expand=True)

    # CUI (doar pentru firme, nu obligatoriu)
    add_field("CUI (firme):", cui_var)

    def save():
        # verificam minim nume si telefon
        if not nume_var.get().strip() or not tel_var.get().strip():
            messagebox.showwarning("Incomplet", "Numele si telefonul sunt obligatorii!")
            return

        succes = insert_client(
            db_conn,
            nume_var.get().strip(),
            prenume_var.get().strip(),
            tel_var.get().strip(),
            email_var.get().strip(),
            adresa_var.get().strip(),
            tip_client_var.get().strip(),
            cui_var.get().strip()
        )

        if succes:
            messagebox.showinfo("Succes", "Client adaugat cu succes!")
            win.destroy()
            # actualizam lista de clienti din fereastra principala
            refresh_callback()
        else:
            messagebox.showerror(
                "Eroare",
                "Inserarea a esuat. Verifica daca nu exista deja client cu acelasi telefon sau email."
            )

    ttk.Button(
        win,
        text="Salveaza client",
        command=save,
        bootstyle="success"
    ).pack(pady=20)
