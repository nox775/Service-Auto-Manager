import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from database.repository import insert_vehicle, update_vehicle, fetch_clients_for_combobox

def open_vehicle_form(parent, db_conn, refresh_callback, vehicle_to_edit=None):
    if not db_conn or not db_conn.is_connected():
        messagebox.showerror("Eroare", "Nu ești conectat la baza de date!")
        return

    win = ttk.Toplevel(parent)
    is_edit_mode = vehicle_to_edit is not None

    if is_edit_mode:
        win.title("Editează Vehicul")
        lbl_text = "Modificare date vehicul"
    else:
        win.title("Adaugă Vehicul Nou")
        lbl_text = "Date vehicul nou"
        
    win.geometry("500x750")

    ttk.Label(win, text=lbl_text, font="Calibri 14 bold").pack(pady=10)

    # --- Variabile ---
    client_str_var = tk.StringVar()
    nr_inmat_var = tk.StringVar()
    sasiu_var = tk.StringVar()
    marca_var = tk.StringVar()
    model_var = tk.StringVar()
    an_var = tk.StringVar()
    motor_var = tk.StringVar()
    cc_var = tk.StringVar()
    combustibil_var = tk.StringVar(value="Benzina")

    # --- Lista Clienti ---
    lista_clienti = fetch_clients_for_combobox(db_conn)

    # --- Pre-completare date daca e editare ---
    vehicul_id = None
    if is_edit_mode:
        # vehicle_to_edit are ordinea din repository: 
        # (0:VehiculID, 1:ClientID, 2:ProprietarNume, 3:NrInmat, 4:Sasiu, 5:Marca, 6:Model, 7:An, 8:Motor, 9:CC, 10:Combustibil)
        
        vehicul_id = vehicle_to_edit[0]
        client_id_existent = vehicle_to_edit[1]
        nume_proprietar = vehicle_to_edit[2]
        
        # Incercam sa setam combobox-ul pe formatul "ID - Nume"
        valoare_combo = f"{client_id_existent} - {nume_proprietar}"
        if valoare_combo in lista_clienti:
            client_str_var.set(valoare_combo)
        else:
            # Fallback daca numele s-a schimbat intre timp, macar afisam ceva
            client_str_var.set(valoare_combo)

        nr_inmat_var.set(vehicle_to_edit[3])
        sasiu_var.set(vehicle_to_edit[4])
        marca_var.set(vehicle_to_edit[5])
        model_var.set(vehicle_to_edit[6])
        an_var.set(vehicle_to_edit[7])
        
        val_motor = vehicle_to_edit[8]
        if val_motor == "None": val_motor = ""
        motor_var.set(val_motor)

        val_cc = vehicle_to_edit[9]
        if val_cc == "None" or val_cc == 0: val_cc = ""
        cc_var.set(val_cc)
        
        combustibil_var.set(vehicle_to_edit[10])

    # --- UI Formular ---
    f_client = ttk.Frame(win)
    f_client.pack(pady=5, fill="x", padx=20)
    ttk.Label(f_client, text="Proprietar:", width=15, anchor="w").pack(side="left")
    cb_client = ttk.Combobox(f_client, textvariable=client_str_var, values=lista_clienti, state="readonly")
    cb_client.pack(side="left", fill="x", expand=True)
    
    # Selectare default la adaugare
    if not is_edit_mode and lista_clienti:
        cb_client.current(0)

    def add_field(label, var):
        f = ttk.Frame(win)
        f.pack(pady=5, fill="x", padx=20)
        ttk.Label(f, text=label, width=15, anchor="w").pack(side="left")
        ttk.Entry(f, textvariable=var).pack(side="left", fill="x", expand=True)

    add_field("Nr. Înmatriculare:", nr_inmat_var)
    add_field("Serie Șasiu:", sasiu_var)
    add_field("Marca:", marca_var)
    add_field("Model:", model_var)
    add_field("An Fabricație:", an_var)
    add_field("Cod Motor:", motor_var)
    add_field("Capacitate CC:", cc_var)

    f_fuel = ttk.Frame(win)
    f_fuel.pack(pady=5, fill="x", padx=20)
    ttk.Label(f_fuel, text="Combustibil:", width=15, anchor="w").pack(side="left")
    ttk.Combobox(
        f_fuel, 
        textvariable=combustibil_var, 
        values=["Benzina", "Diesel", "Electric", "Hibrid"], 
        state="readonly"
    ).pack(side="left", fill="x", expand=True)

    def save():
        # Validari
        if not nr_inmat_var.get() or not sasiu_var.get() or not client_str_var.get():
            messagebox.showwarning("Incomplet", "Proprietarul, Nr. Înmat. și Șasiul sunt obligatorii!")
            return

        # Extragem ID-ul clientului
        selection = client_str_var.get()
        try:
            client_id = selection.split(" - ")[0]
        except:
            messagebox.showerror("Eroare", "Format client invalid!")
            return

        if is_edit_mode:
            # UPDATE
            succes = update_vehicle(
                db_conn,
                vehicul_id,
                client_id,
                nr_inmat_var.get().strip().upper(),
                sasiu_var.get().strip().upper(),
                marca_var.get().strip(),
                model_var.get().strip(),
                an_var.get().strip(),
                motor_var.get().strip(),
                cc_var.get().strip(),
                combustibil_var.get()
            )
            msg_ok = "Vehicul actualizat!"
        else:
            # INSERT
            succes = insert_vehicle(
                db_conn,
                client_id,
                nr_inmat_var.get().strip().upper(),
                sasiu_var.get().strip().upper(),
                marca_var.get().strip(),
                model_var.get().strip(),
                an_var.get().strip(),
                motor_var.get().strip(),
                cc_var.get().strip(),
                combustibil_var.get()
            )
            msg_ok = "Vehicul adăugat!"

        if succes:
            messagebox.showinfo("Succes", msg_ok)
            win.destroy()
            refresh_callback()
        else:
            messagebox.showerror("Eroare", "Operația a eșuat (posibil duplicat Nr. Înmat/Șasiu).")

    btn_txt = "Salvează Modificări" if is_edit_mode else "Adaugă Vehicul"
    ttk.Button(win, text=btn_txt, command=save, bootstyle="success").pack(pady=20)