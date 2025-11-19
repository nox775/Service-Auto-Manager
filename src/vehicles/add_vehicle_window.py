import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from database.repository import insert_vehicle


def open_add_vehicle_window(parent, db_conn, refresh_callback):
    if not db_conn or not db_conn.is_connected():
        messagebox.showerror("Eroare", "Nu esti conectat la baza de date!")
        return

    win = ttk.Toplevel(parent)
    win.title("Adauga vehicul nou")
    win.geometry("900x1200")

    ttk.Label(win, text="Date vehicul", font="Calibri 14 bold").pack(pady=10)
    # campuri: VehiculID, ClientID, NumarInmatriculare, SerieSasiu, Marca, Model, AnFabricatie,
    #          CodMotor, CapacitateCilindrica, TipCombustibil

    # --- variabile pentru formular ---
    client_id_var = tk.StringVar()
    nr_inmatriculare_var = tk.StringVar()
    serie_sasiu_var = tk.StringVar()
    marca_var = tk.StringVar()
    model_var = tk.StringVar()
    an_fabricatie_var = tk.StringVar()
    cod_motor_var = tk.StringVar()
    capacitate_cilindrica_var = tk.StringVar()
    tip_combustibil_var = tk.StringVar(value="Diesel")

    # helper mic pentru un rand eticheta + input
    def add_field(label, var):
        f = ttk.Frame(win)
        f.pack(pady=5, fill="x", padx=20)
        ttk.Label(f, text=label, width=18, anchor="w").pack(side="left")
        ttk.Entry(f, textvariable=var).pack(side="left", fill="x", expand=True)

    add_field("ID client:", client_id_var)
    add_field("Numar inmatriculare:", nr_inmatriculare_var)
    add_field("Serie sasiu:", serie_sasiu_var)
    add_field("Marca:", marca_var)
    add_field("Model:", model_var)
    add_field("An fabricatie:", an_fabricatie_var)
    add_field("Cod motor:", cod_motor_var)
    add_field("Capacitate cilindrica:", capacitate_cilindrica_var)

    # dropdown pentru tip combustibil
    f_tip = ttk.Frame(win)
    f_tip.pack(pady=5, fill="x", padx=20)
    ttk.Label(f_tip, text="Tip combustibil:", width=18, anchor="w").pack(side="left")
    combobox = ttk.Combobox(
        f_tip,
        textvariable=tip_combustibil_var,
        values=["Benzina", "Diesel", "Electric", "Hibrid"],
        state="readonly",
    )
    combobox.pack(side="left", fill="x", expand=True)

    def save():
        # validare simpla (poti adauga si altele dupa nevoie)
        if not client_id_var.get().strip():
            messagebox.showwarning("Incomplet", "ID-ul clientului este obligatoriu.")
            return
        if not nr_inmatriculare_var.get().strip():
            messagebox.showwarning("Incomplet", "Numarul de inmatriculare este obligatoriu.")
            return

        succes = insert_vehicle(
            db_conn,
            client_id_var.get().strip(),
            nr_inmatriculare_var.get().strip(),
            serie_sasiu_var.get().strip(),
            marca_var.get().strip(),
            model_var.get().strip(),
            an_fabricatie_var.get().strip(),
            cod_motor_var.get().strip(),
            capacitate_cilindrica_var.get().strip(),
            tip_combustibil_var.get().strip(),
        )

        if succes:
            messagebox.showinfo("Succes", "Vehicul adaugat.")
            win.destroy()
            # dupa salvare, actualizam tabelul din fereastra principala
            refresh_callback()
        else:
            messagebox.showerror(
                "Eroare",
                "Inserarea a esuat. Verifica daca nu exista deja vehicul cu acelasi numar de inmatriculare."
            )

    ttk.Button(
        win,
        text="Salveaza vehicul",
        command=save,
        bootstyle="success"
    ).pack(pady=20)
