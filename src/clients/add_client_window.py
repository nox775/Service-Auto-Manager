import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
# Importam ambele functii: insert si update
from database.repository import insert_client, update_client

def open_client_form(parent, db_conn, refresh_callback, client_to_edit=None):
    """
    Fereastra universala pentru Adaugare sau Editare client.
    """
    if not db_conn or not db_conn.is_connected():
        messagebox.showerror("Eroare", "Nu esti conectat la baza de date!")
        return

    win = ttk.Toplevel(parent)
    
    is_edit_mode = client_to_edit is not None
    
    if is_edit_mode:
        win.title("Editeaza Client")
        lbl_text = "Modificare date client"
    else:
        win.title("Adauga Client Nou")
        lbl_text = "Date client nou"
        
    win.geometry("500x700")

    ttk.Label(win, text=lbl_text, font="Calibri 14 bold").pack(pady=10)

    # --- Variabile Formular ---
    nume_var = tk.StringVar()
    prenume_var = tk.StringVar()
    tel_var = tk.StringVar()
    email_var = tk.StringVar()
    adresa_var = tk.StringVar()
    tip_client_var = tk.StringVar(value="Persoana fizica")
    cui_var = tk.StringVar()

    # --- Daca e editare, pre-completam valorile ---
    client_id = None
    if is_edit_mode:
        # client_to_edit vine din Treeview: (ID, Nume, Prenume, Telefon, Email, Tip, CUI)
        client_id = client_to_edit[0]
        nume_var.set(client_to_edit[1])
        prenume_var.set(client_to_edit[2])
        tel_var.set(client_to_edit[3])
        # Verificam daca email e 'None' string sau gol
        email_val = client_to_edit[4]
        if email_val == "None": email_val = ""
        email_var.set(email_val)
        
        tip_client_var.set(client_to_edit[5])
        
        cui_val = client_to_edit[6]
        if cui_val == "None": cui_val = ""
        cui_var.set(cui_val)
        
        # Adresa nu e in tabelul principal in acest moment, o lasam goala sau ar trebui luata cu un select separat.
        # Pentru simplitate, o lasam goala la editare momentan.

    # --- Helper Generare Campuri ---
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

    f_tip = ttk.Frame(win)
    f_tip.pack(pady=5, fill="x", padx=20)
    ttk.Label(f_tip, text="Tip client:", width=15, anchor="w").pack(side="left")
    ttk.Combobox(
        f_tip, textvariable=tip_client_var, 
        values=["Persoana fizica", "Persoana juridica"], state="readonly"
    ).pack(side="left", fill="x", expand=True)

    add_field("CUI (firme):", cui_var)

    def save_action():
        # Validari
        if not nume_var.get().strip() or not tel_var.get().strip():
            messagebox.showwarning("Incomplet", "Numele si Telefonul sunt obligatorii!")
            return

        if is_edit_mode:
            # UPDATE
            succes = update_client(
                db_conn,
                client_id,
                nume_var.get().strip(),
                prenume_var.get().strip(),
                tel_var.get().strip(),
                email_var.get().strip(),
                adresa_var.get().strip(),
                tip_client_var.get(),
                cui_var.get().strip()
            )
            msg_succes = "Client actualizat cu succes!"
        else:
            # INSERT
            succes = insert_client(
                db_conn,
                nume_var.get().strip(),
                prenume_var.get().strip(),
                tel_var.get().strip(),
                email_var.get().strip(),
                adresa_var.get().strip(),
                tip_client_var.get(),
                cui_var.get().strip()
            )
            msg_succes = "Client adaugat cu succes!"

        if succes:
            messagebox.showinfo("Succes", msg_succes)
            win.destroy()
            refresh_callback()
        else:
            messagebox.showerror("Eroare", "Operatia a esuat. Verifica consola pentru detalii (Duplicate?).")

    btn_text = "Salveaza Modificari" if is_edit_mode else "Adauga Client"
    ttk.Button(win, text=btn_text, command=save_action, bootstyle="success").pack(pady=20)