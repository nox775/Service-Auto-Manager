from mysql.connector import Error

# ==============================================================================
# --- ZONA CLIENTI ---
# ==============================================================================
def fetch_all_clients(conn):
    try:
        c = conn.cursor()
        # Selectam ID-ul pentru logica interna, dar si datele relevante
        c.execute("SELECT ClientID, Nume, Prenume, Telefon, Email, TipClient, CUI FROM CLIENTI ORDER BY Nume ASC")
        return c.fetchall()
    except Error as e:
        print(f"Err: {e}")
        return []

def search_clients(conn, term):
    try:
        c = conn.cursor()
        t = f"%{term}%"
        sql = "SELECT ClientID, Nume, Prenume, Telefon, Email, TipClient, CUI FROM CLIENTI WHERE Nume LIKE %s OR Prenume LIKE %s OR Telefon LIKE %s"
        c.execute(sql, (t, t, t))
        return c.fetchall()
    except Error: return []

def insert_client(conn, nume, prenume, tel, email, adr, tip, cui):
    try:
        c = conn.cursor()
        if not email: email = None
        if not cui or tip == "Persoana fizica": cui = None
        sql = "INSERT INTO CLIENTI (Nume, Prenume, Telefon, Email, Adresa, TipClient, CUI) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        c.execute(sql, (nume, prenume, tel, email, adr, tip, cui))
        conn.commit()
        return True
    except Error: return False

def update_client(conn, cid, nume, prenume, tel, email, adr, tip, cui):
    try:
        c = conn.cursor()
        if not email: email = None
        if not cui or tip == "Persoana fizica": cui = None
        sql = "UPDATE CLIENTI SET Nume=%s, Prenume=%s, Telefon=%s, Email=%s, Adresa=%s, TipClient=%s, CUI=%s WHERE ClientID=%s"
        c.execute(sql, (nume, prenume, tel, email, adr, tip, cui, cid))
        conn.commit()
        return True
    except Error: return False

def delete_client(conn, cid):
    try:
        c = conn.cursor(); c.execute("DELETE FROM CLIENTI WHERE ClientID=%s", (cid,)); conn.commit(); return True
    except Error: return False

# ==============================================================================
# --- ZONA VEHICULE ---
# ==============================================================================
def fetch_all_vehicles(conn):
    try:
        c = conn.cursor()
        # JOIN PENTRU A ADUCE NUMELE PROPRIETARULUI, NU ID-ul
        sql = """
        SELECT v.VehiculID, 
               v.ClientID, 
               CONCAT(c.Nume, ' ', c.Prenume) as Proprietar, 
               v.NumarInmatriculare, 
               v.SerieSasiu, 
               v.Marca, 
               v.Model, 
               v.AnFabricatie, 
               v.CodMotor, 
               v.CapacitateCilindrica, 
               v.TipCombustibil 
        FROM VEHICULE v 
        JOIN CLIENTI c ON v.ClientID = c.ClientID 
        ORDER BY v.VehiculID DESC
        """
        c.execute(sql)
        return c.fetchall()
    except Error: return []

def search_vehicles(conn, term):
    try:
        c = conn.cursor()
        t = f"%{term}%"
        # JOIN SI AICI
        sql = """
        SELECT v.VehiculID, 
               v.ClientID, 
               CONCAT(c.Nume, ' ', c.Prenume), 
               v.NumarInmatriculare, 
               v.SerieSasiu, 
               v.Marca, 
               v.Model, 
               v.AnFabricatie, 
               v.CodMotor, 
               v.CapacitateCilindrica, 
               v.TipCombustibil 
        FROM VEHICULE v 
        JOIN CLIENTI c ON v.ClientID = c.ClientID 
        WHERE v.NumarInmatriculare LIKE %s OR v.SerieSasiu LIKE %s OR c.Nume LIKE %s
        """
        c.execute(sql, (t, t, t))
        return c.fetchall()
    except Error: return []

def fetch_clients_for_combobox(conn):
    try:
        c = conn.cursor(); c.execute("SELECT ClientID, Nume, Prenume FROM CLIENTI ORDER BY Nume ASC"); return [f"{r[0]} - {r[1]} {r[2]}" for r in c.fetchall()]
    except Error: return []

def insert_vehicle(conn, cid, nr, sasiu, marca, model, an, motor, cc, comb):
    try:
        c = conn.cursor()
        sql = "INSERT INTO VEHICULE (ClientID, NumarInmatriculare, SerieSasiu, Marca, Model, AnFabricatie, CodMotor, CapacitateCilindrica, TipCombustibil) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        c.execute(sql, (cid, nr, sasiu, marca, model, an, motor, cc, comb))
        conn.commit()
        return True
    except Error: return False

def update_vehicle(conn, vid, cid, nr, sasiu, marca, model, an, motor, cc, comb):
    try:
        c = conn.cursor()
        sql = "UPDATE VEHICULE SET ClientID=%s, NumarInmatriculare=%s, SerieSasiu=%s, Marca=%s, Model=%s, AnFabricatie=%s, CodMotor=%s, CapacitateCilindrica=%s, TipCombustibil=%s WHERE VehiculID=%s"
        c.execute(sql, (cid, nr, sasiu, marca, model, an, motor, cc, comb, vid))
        conn.commit()
        return True
    except Error: return False

def delete_vehicle(conn, vid):
    try:
        c = conn.cursor(); c.execute("DELETE FROM VEHICULE WHERE VehiculID=%s", (vid,)); conn.commit(); return True
    except Error: return False

# ==============================================================================
# --- ZONA MECANICI, SERVICII, FURNIZORI ---
# ==============================================================================
def fetch_all_mechanics(conn):
    try: c = conn.cursor(); c.execute("SELECT MecanicID, Nume, Prenume, DataAngajarii FROM MECANICI ORDER BY Nume"); return c.fetchall()
    except: return []

def search_mechanics(conn, t):
    try: c = conn.cursor(); term=f"%{t}%"; c.execute("SELECT MecanicID, Nume, Prenume, DataAngajarii FROM MECANICI WHERE Nume LIKE %s OR Prenume LIKE %s", (term, term)); return c.fetchall()
    except: return []

def insert_mechanic(conn, n, p, d):
    try: c=conn.cursor(); c.execute("INSERT INTO MECANICI (Nume, Prenume, DataAngajarii) VALUES (%s,%s,%s)", (n,p,d)); conn.commit(); return True
    except: return False

def update_mechanic(conn, mid, n, p, d):
    try: c=conn.cursor(); c.execute("UPDATE MECANICI SET Nume=%s, Prenume=%s, DataAngajarii=%s WHERE MecanicID=%s", (n,p,d,mid)); conn.commit(); return True
    except: return False

def delete_mechanic(conn, mid):
    try: c=conn.cursor(); c.execute("DELETE FROM MECANICI WHERE MecanicID=%s", (mid,)); conn.commit(); return True
    except: return False

# Servicii
def fetch_all_services(conn):
    try: c=conn.cursor(); c.execute("SELECT ServiciuID, Denumire, Descriere, TarifOra, TimpEstimativ FROM SERVICII ORDER BY Denumire"); return c.fetchall()
    except: return []

def search_services(conn, t):
    try: c=conn.cursor(); term=f"%{t}%"; c.execute("SELECT ServiciuID, Denumire, Descriere, TarifOra, TimpEstimativ FROM SERVICII WHERE Denumire LIKE %s", (term,)); return c.fetchall()
    except: return []

def insert_service(conn, den, des, t, time):
    try: c=conn.cursor(); c.execute("INSERT INTO SERVICII (Denumire, Descriere, TarifOra, TimpEstimativ) VALUES (%s,%s,%s,%s)", (den,des,t,time)); conn.commit(); return True
    except: return False

def update_service(conn, sid, den, des, t, time):
    try: c=conn.cursor(); c.execute("UPDATE SERVICII SET Denumire=%s, Descriere=%s, TarifOra=%s, TimpEstimativ=%s WHERE ServiciuID=%s", (den,des,t,time,sid)); conn.commit(); return True
    except: return False

def delete_service(conn, sid):
    try: c=conn.cursor(); c.execute("DELETE FROM SERVICII WHERE ServiciuID=%s", (sid,)); conn.commit(); return True
    except: return False

# Furnizori
def fetch_all_suppliers(conn):
    try: c=conn.cursor(); c.execute("SELECT FurnizorID, NumeFurnizor, PersoanaContact, Telefon, Email, CUI FROM FURNIZORI ORDER BY NumeFurnizor"); return c.fetchall()
    except: return []

def search_suppliers(conn, t):
    try: c=conn.cursor(); term=f"%{t}%"; c.execute("SELECT FurnizorID, NumeFurnizor, PersoanaContact, Telefon, Email, CUI FROM FURNIZORI WHERE NumeFurnizor LIKE %s", (term,)); return c.fetchall()
    except: return []

def insert_supplier(conn, n, p, t, e, cui):
    try: c=conn.cursor(); c.execute("INSERT INTO FURNIZORI (NumeFurnizor, PersoanaContact, Telefon, Email, CUI) VALUES (%s,%s,%s,%s,%s)", (n,p,t,e,cui)); conn.commit(); return True
    except: return False

def update_supplier(conn, fid, n, p, t, e, cui):
    try: c=conn.cursor(); c.execute("UPDATE FURNIZORI SET NumeFurnizor=%s, PersoanaContact=%s, Telefon=%s, Email=%s, CUI=%s WHERE FurnizorID=%s", (n,p,t,e,cui,fid)); conn.commit(); return True
    except: return False

def delete_supplier(conn, fid):
    try: c=conn.cursor(); c.execute("DELETE FROM FURNIZORI WHERE FurnizorID=%s", (fid,)); conn.commit(); return True
    except: return False

# ==============================================================================
# --- ZONA RAPOARTE (JOIN-URI DEJA IMPLEMENTATE) ---
# ==============================================================================
# Acestea erau deja corecte (afisau nume, nu ID-uri), le pastram la fel.

def get_report_vehicles_owners(conn, marca_filter=None):
    c = conn.cursor()
    sql = "SELECT v.NumarInmatriculare, v.Marca, v.Model, c.Nume, c.Prenume, c.Telefon FROM VEHICULE v JOIN CLIENTI c ON v.ClientID = c.ClientID WHERE 1=1"
    p = []
    if marca_filter and marca_filter.strip():
        sql += " AND v.Marca LIKE %s"
        p.append(f"%{marca_filter}%")
    sql += " ORDER BY c.Nume ASC"
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Nr. Inmat.", "Marca", "Model", "Nume Client", "Prenume", "Telefon"]

def get_report_devize_details(conn, stare_filter=None):
    c = conn.cursor()
    sql = "SELECT d.DevizID, d.DataPrimire, d.StareDeviz, v.NumarInmatriculare, c.Nume FROM DEVIZE d JOIN VEHICULE v ON d.VehiculID = v.VehiculID JOIN CLIENTI c ON v.ClientID = c.ClientID WHERE 1=1"
    p = []
    if stare_filter and stare_filter.strip():
        sql += " AND d.StareDeviz LIKE %s"
        p.append(f"%{stare_filter}%")
    sql += " ORDER BY d.DataPrimire DESC"
    c.execute(sql, tuple(p))
    return c.fetchall(), ["ID Deviz", "Data Primire", "Stare", "Nr. Auto", "Nume Client"]

def get_report_invoices(conn, an_filter=None):
    c = conn.cursor()
    sql = "SELECT f.SerieNumar, f.DataEmitere, f.TotalCuTVA, f.StarePlata, c.Nume FROM FACTURA f JOIN DEVIZE d ON f.DevizID = d.DevizID JOIN VEHICULE v ON d.VehiculID = v.VehiculID JOIN CLIENTI c ON v.ClientID = c.ClientID WHERE 1=1"
    p = []
    if an_filter and an_filter.strip():
        sql += " AND YEAR(f.DataEmitere) = %s"
        p.append(an_filter)
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Serie Factura", "Data", "Total (RON)", "Stare Plata", "Client"]

def get_report_mechanics_specs(conn, spec_filter=None):
    c = conn.cursor()
    sql = "SELECT m.Nume, m.Prenume, s.Denumire FROM MECANICI m JOIN MECANICI_SPECIALIZARI ms ON m.MecanicID = ms.MecanicID JOIN SPECIALIZARI s ON ms.SpecializareID = s.SpecializareID WHERE 1=1"
    p = []
    if spec_filter and spec_filter.strip():
        sql += " AND s.Denumire LIKE %s"
        p.append(f"%{spec_filter}%")
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Nume Mecanic", "Prenume", "Specializare"]

def get_report_parts_suppliers(conn, stoc_limit=None):
    c = conn.cursor()
    # Aici afisam Nume Furnizor, nu ID
    sql = "SELECT p.CodPiesa, p.Denumire, p.StocDisponibil, f.NumeFurnizor FROM PIESE p JOIN FURNIZORI f ON p.FurnizorID = f.FurnizorID WHERE 1=1"
    p = []
    if stoc_limit and stoc_limit.strip():
        sql += " AND p.StocDisponibil < %s"
        p.append(stoc_limit)
    sql += " ORDER BY p.StocDisponibil ASC"
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Cod Piesa", "Denumire Piesa", "Stoc", "Furnizor"]

def get_report_labor_info(conn, mecanic_filter=None):
    c = conn.cursor()
    # Afisam Nume Serviciu si Nume Mecanic
    sql = "SELECT man.DevizID, s.Denumire, m.Nume, man.OreLucrate, man.CostLinie FROM MANOPERA man JOIN SERVICII s ON man.ServiciuID = s.ServiciuID JOIN MECANICI m ON man.MecanicID = m.MecanicID WHERE 1=1"
    p = []
    if mecanic_filter and mecanic_filter.strip():
        sql += " AND m.Nume LIKE %s"
        p.append(f"%{mecanic_filter}%")
    c.execute(sql, tuple(p))
    return c.fetchall(), ["ID Deviz", "Serviciu", "Mecanic", "Ore", "Cost (RON)"]

def get_complex_clients_above_avg(conn, min_amount=None):
    c = conn.cursor()
    limit_clause = "(SELECT AVG(TotalCuTVA) FROM FACTURA)"
    p = []
    if min_amount and min_amount.strip():
        limit_clause = "%s"
        p.append(min_amount)
    sql = f"SELECT c.Nume, c.Prenume, f.SerieNumar, f.TotalCuTVA FROM CLIENTI c JOIN VEHICULE v ON c.ClientID = v.ClientID JOIN DEVIZE d ON v.VehiculID = d.VehiculID JOIN FACTURA f ON d.DevizID = f.DevizID WHERE f.TotalCuTVA > {limit_clause} ORDER BY f.TotalCuTVA DESC"
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Nume", "Prenume", "Serie Factura", "Total (RON)"]

def get_complex_unsold_parts(conn, furnizor_filter=None):
    c = conn.cursor()
    sql = "SELECT p.CodPiesa, p.Denumire, p.StocDisponibil, f.NumeFurnizor FROM PIESE p JOIN FURNIZORI f ON p.FurnizorID = f.FurnizorID WHERE p.PiesaID NOT IN (SELECT DISTINCT PiesaID FROM COMANDA_PIESE)"
    p = []
    if furnizor_filter and furnizor_filter.strip():
        sql += " AND f.NumeFurnizor LIKE %s"
        p.append(f"%{furnizor_filter}%")
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Cod Piesa", "Denumire", "Stoc (Mort)", "Furnizor"]

def get_complex_fleet_clients(conn, min_cars=None):
    c = conn.cursor()
    limit = "1"
    p = []
    if min_cars and min_cars.strip():
        limit = "%s"
        p.append(min_cars)
    sql = f"SELECT c.Nume, c.Prenume, c.Telefon, (SELECT COUNT(*) FROM VEHICULE v WHERE v.ClientID = c.ClientID) as NrMasini FROM CLIENTI c WHERE (SELECT COUNT(*) FROM VEHICULE v WHERE v.ClientID = c.ClientID) > {limit}"
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Nume", "Prenume", "Telefon", "Nr. Masini"]

def get_complex_expensive_repairs_param(conn, min_cost=None):
    c = conn.cursor()
    limit = 0
    if min_cost and min_cost.strip():
        limit = float(min_cost)
    else:
        c2 = conn.cursor()
        c2.execute("SELECT AVG(CostTotalEstimativ) FROM DEVIZE WHERE StareDeviz='Finalizata'")
        res = c2.fetchone()
        if res and res[0]: limit = res[0]
    sql = "SELECT d.DevizID, v.NumarInmatriculare, d.CostTotalEstimativ, d.DataFinalizare FROM DEVIZE d JOIN VEHICULE v ON d.VehiculID = v.VehiculID WHERE d.StareDeviz = 'Finalizata' AND d.CostTotalEstimativ > %s ORDER BY d.CostTotalEstimativ DESC"
    c.execute(sql, (limit,))
    return c.fetchall(), ["ID Deviz", "Nr. Auto", f"Cost > {limit:.0f}", "Data Finalizare"]

# ==============================================================================
# --- ZONA STATISTICI (PENTRU GRAFICE) ---
# ==============================================================================
def get_dashboard_stats_fuel(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT TipCombustibil, COUNT(*) FROM VEHICULE GROUP BY TipCombustibil")
        return c.fetchall()
    except: return []

def get_dashboard_stats_revenue(conn):
    try:
        c = conn.cursor()
        sql = "SELECT DATE_FORMAT(DataEmitere, '%Y-%m') as Luna, SUM(TotalCuTVA) FROM FACTURA WHERE StarePlata = 'Platita' GROUP BY Luna ORDER BY Luna DESC LIMIT 6"
        c.execute(sql)
        return c.fetchall()
    except: return []

def get_stats_top_mechanics(conn):
    try:
        c = conn.cursor()
        sql = "SELECT m.Nume, SUM(man.OreLucrate) as TotalOre FROM MANOPERA man JOIN MECANICI m ON man.MecanicID = m.MecanicID GROUP BY m.MecanicID ORDER BY TotalOre DESC LIMIT 5"
        c.execute(sql)
        return c.fetchall()
    except: return []

def get_stats_top_parts(conn):
    try:
        c = conn.cursor()
        sql = "SELECT p.Denumire, SUM(cp.Cantitate) as TotalVandut FROM COMANDA_PIESE cp JOIN PIESE p ON cp.PiesaID = p.PiesaID GROUP BY p.PiesaID ORDER BY TotalVandut DESC LIMIT 5"
        c.execute(sql)
        return c.fetchall()
    except: return []

def get_stats_deviz_status(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT StareDeviz, COUNT(*) FROM DEVIZE GROUP BY StareDeviz")
        return c.fetchall()
    except: return []

def get_stats_revenue_trend(conn):
    return get_dashboard_stats_revenue(conn) # Reusing same logic

# ==============================================================================
# --- ZONA ISTORIC & FACTURA (JOIN PENTRU DETALII) ---
# ==============================================================================
def get_vehicle_history_data(conn, vid):
    try:
        c = conn.cursor()
        # Aici ID-ul devizului nu deranjeaza, e istoric intern
        c.execute("SELECT DevizID, DataPrimire, StareDeviz, DescriereProblemaClient, CostTotalEstimativ FROM DEVIZE WHERE VehiculID = %s ORDER BY DataPrimire DESC", (vid,))
        devize = c.fetchall()
        
        history = []
        for dev in devize:
            did = dev[0]
            c.execute("SELECT p.Denumire, cp.Cantitate, cp.PretUnitarVanzare FROM COMANDA_PIESE cp JOIN PIESE p ON cp.PiesaID = p.PiesaID WHERE cp.DevizID=%s", (did,))
            piese = c.fetchall()
            c.execute("SELECT s.Denumire, m.Nume, man.OreLucrate FROM MANOPERA man JOIN SERVICII s ON man.ServiciuID=s.ServiciuID JOIN MECANICI m ON man.MecanicID=m.MecanicID WHERE man.DevizID=%s", (did,))
            manopera = c.fetchall()
            history.append({"deviz": dev, "piese": piese, "manopera": manopera})
        return history
    except: return []

def fetch_invoice_details_complex(conn, serie_factura):
    try:
        c = conn.cursor()
        sql_h = """SELECT f.FacturaID, f.SerieNumar, f.DataEmitere, f.TotalFaraTVA, f.ValoareTVA, f.TotalCuTVA,
                   c.Nume, c.Prenume, c.Adresa, c.Telefon, c.CUI, v.Marca, v.Model, v.NumarInmatriculare, d.DevizID
                   FROM FACTURA f JOIN DEVIZE d ON f.DevizID=d.DevizID JOIN VEHICULE v ON d.VehiculID=v.VehiculID JOIN CLIENTI c ON v.ClientID=c.ClientID
                   WHERE f.SerieNumar=%s"""
        c.execute(sql_h, (serie_factura,))
        head = c.fetchone()
        if not head: return None
        
        did = head[14]
        
        # Detalii cu JOIN pentru a avea Numele Pisei si Numele Serviciului
        sql_p = "SELECT p.Denumire, cp.Cantitate, cp.PretUnitarVanzare, (cp.Cantitate*cp.PretUnitarVanzare) FROM COMANDA_PIESE cp JOIN PIESE p ON cp.PiesaID=p.PiesaID WHERE cp.DevizID=%s"
        c.execute(sql_p, (did,))
        piese = c.fetchall()
        
        sql_m = "SELECT s.Denumire, man.OreLucrate, man.TarifOraAplicat, man.CostLinie FROM MANOPERA man JOIN SERVICII s ON man.ServiciuID=s.ServiciuID WHERE man.DevizID=%s"
        c.execute(sql_m, (did,))
        manopera = c.fetchall()
        
        return {"header": head, "piese": piese, "manopera": manopera}
    except Exception as e:
        print(e); return None