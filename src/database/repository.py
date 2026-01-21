from mysql.connector import Error

# ==============================================================================
# --- ZONA CLIENȚI (CRUD + SEARCH) ---
# ==============================================================================
def fetch_all_clients(conn):
    """ Returneaza lista clientilor (folosit in tabel) """
    try:
        c = conn.cursor()
        c.execute("SELECT ClientID, Nume, Prenume, Telefon, Email, TipClient, CUI FROM CLIENTI ORDER BY Nume ASC")
        return c.fetchall()
    except Error as e:
        print(f"Err Clients: {e}")
        return []

def search_clients(conn, term):
    """ Cauta clienti dupa Nume, Prenume sau Telefon """
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
# --- ZONA VEHICULE (CRUD + SEARCH CU JOIN) ---
# ==============================================================================
def fetch_all_vehicles(conn):
    """ Returneaza vehiculele cu Numele Proprietarului (JOIN) """
    try:
        c = conn.cursor()
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
    """ Cauta dupa Nr. Inmat, Sasiu sau Nume Proprietar """
    try:
        c = conn.cursor()
        t = f"%{term}%"
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
    """ Helper pentru dropdown-ul de la Adaugare Vehicul """
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
# Mecanici
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
# --- ZONA RAPOARTE OPERAȚIONALE (JOIN-uri, fără ID-uri expuse) ---
# ==============================================================================

def get_report_vehicles_owners(conn, marca_filter=None):
    c = conn.cursor()
    sql = "SELECT v.NumarInmatriculare, v.Marca, v.Model, c.Nume, c.Prenume, c.Telefon FROM VEHICULE v JOIN CLIENTI c ON v.ClientID = c.ClientID WHERE 1=1"
    p = []
    if marca_filter and marca_filter.strip():
        sql += " AND v.Marca LIKE %s"; p.append(f"%{marca_filter}%")
    sql += " ORDER BY c.Nume ASC"
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Nr. Inmat.", "Marca", "Model", "Nume Client", "Prenume", "Telefon"]

def get_report_devize_details(conn, stare_filter=None):
    c = conn.cursor()
    sql = "SELECT d.DevizID, d.DataPrimire, d.StareDeviz, v.NumarInmatriculare, c.Nume FROM DEVIZE d JOIN VEHICULE v ON d.VehiculID = v.VehiculID JOIN CLIENTI c ON v.ClientID = c.ClientID WHERE 1=1"
    p = []
    if stare_filter and stare_filter.strip():
        sql += " AND d.StareDeviz LIKE %s"; p.append(f"%{stare_filter}%")
    sql += " ORDER BY d.DataPrimire DESC"
    c.execute(sql, tuple(p))
    return c.fetchall(), ["ID Deviz", "Data Primire", "Stare", "Nr. Auto", "Nume Client"]

def get_report_invoices(conn, an_filter=None):
    c = conn.cursor()
    sql = "SELECT f.SerieNumar, f.DataEmitere, f.TotalCuTVA, f.StarePlata, c.Nume FROM FACTURA f JOIN DEVIZE d ON f.DevizID = d.DevizID JOIN VEHICULE v ON d.VehiculID = v.VehiculID JOIN CLIENTI c ON v.ClientID = c.ClientID WHERE 1=1"
    p = []
    if an_filter and an_filter.strip():
        sql += " AND YEAR(f.DataEmitere) = %s"; p.append(an_filter)
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Serie Factura", "Data", "Total (RON)", "Stare Plata", "Client"]

def get_report_mechanics_specs(conn, spec_filter=None):
    c = conn.cursor()
    sql = "SELECT m.Nume, m.Prenume, s.Denumire FROM MECANICI m JOIN MECANICI_SPECIALIZARI ms ON m.MecanicID = ms.MecanicID JOIN SPECIALIZARI s ON ms.SpecializareID = s.SpecializareID WHERE 1=1"
    p = []
    if spec_filter and spec_filter.strip():
        sql += " AND s.Denumire LIKE %s"; p.append(f"%{spec_filter}%")
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Nume Mecanic", "Prenume", "Specializare"]

def get_report_parts_low_stock(conn, stoc_limit=None):
    """ Raport cu JOIN sa vedem numele Furnizorului, nu ID-ul """
    c = conn.cursor()
    sql = "SELECT p.CodPiesa, p.Denumire, p.StocDisponibil, f.NumeFurnizor FROM PIESE p JOIN FURNIZORI f ON p.FurnizorID = f.FurnizorID WHERE 1=1"
    p = []
    if stoc_limit and stoc_limit.strip():
        sql += " AND p.StocDisponibil < %s"; p.append(stoc_limit)
    sql += " ORDER BY p.StocDisponibil ASC"
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Cod Piesa", "Denumire Piesa", "Stoc", "Furnizor"]

def get_report_profit_margin(conn, min_margin=None):
    c = conn.cursor()
    limit = 0
    if min_margin: limit = float(min_margin)
    sql = """
    SELECT p.Denumire, p.PretAchizitie, p.PretVanzare, 
           (p.PretVanzare - p.PretAchizitie) as ProfitRON,
           ROUND(((p.PretVanzare - p.PretAchizitie) / p.PretAchizitie * 100), 2) as Marja
    FROM PIESE p HAVING Marja > %s ORDER BY Marja DESC
    """
    c.execute(sql, (limit,))
    return c.fetchall(), ["Piesa", "Pret Achizitie", "Pret Vanzare", "Profit (RON)", "Marja (%)"]

def get_report_fleet_clients(conn, min_cars=None):
    """ Subcerere in WHERE pentru a numara masinile """
    c = conn.cursor()
    limit = "1"
    if min_cars and min_cars.strip(): limit = min_cars
    p = [limit]
    sql = f"""
    SELECT c.Nume, c.Prenume, c.Telefon, (SELECT COUNT(*) FROM VEHICULE v WHERE v.ClientID = c.ClientID) as NrMasini
    FROM CLIENTI c
    WHERE (SELECT COUNT(*) FROM VEHICULE v WHERE v.ClientID = c.ClientID) > %s
    """
    c.execute(sql, tuple(p))
    return c.fetchall(), ["Nume", "Prenume", "Telefon", "Nr. Masini"]

# ==============================================================================
# --- ZONA CRM (MARKETING) - SUBCERERI AVANSATE ---
# ==============================================================================

def get_crm_inactive_clients(conn, months_inactive):
    """ Subcerere cu NOT IN """
    try:
        c = conn.cursor()
        sql = """
        SELECT c.Nume, c.Prenume, c.Telefon, MAX(d.DataPrimire) as UltimaVizita
        FROM CLIENTI c
        JOIN VEHICULE v ON c.ClientID = v.ClientID
        JOIN DEVIZE d ON v.VehiculID = d.VehiculID
        WHERE c.ClientID NOT IN (
            SELECT DISTINCT v2.ClientID
            FROM DEVIZE d2
            JOIN VEHICULE v2 ON d2.VehiculID = v2.VehiculID
            WHERE d2.DataPrimire > DATE_SUB(NOW(), INTERVAL %s MONTH)
        )
        GROUP BY c.ClientID
        ORDER BY UltimaVizita ASC
        """
        c.execute(sql, (months_inactive,))
        return c.fetchall(), ["Nume", "Prenume", "Telefon", "Ultima Vizită"]
    except Exception as e: print(e); return [], []

def get_crm_vip_clients(conn, min_spent):
    """ Subcerere Scalara in SELECT + WHERE """
    try:
        c = conn.cursor()
        sql = """
        SELECT c.Nume, c.Prenume, c.Telefon, 
               (SELECT SUM(f.TotalCuTVA) FROM FACTURA f JOIN DEVIZE d ON f.DevizID=d.DevizID JOIN VEHICULE v ON d.VehiculID=v.VehiculID WHERE v.ClientID=c.ClientID) as Total
        FROM CLIENTI c
        WHERE (SELECT SUM(f.TotalCuTVA) FROM FACTURA f JOIN DEVIZE d ON f.DevizID=d.DevizID JOIN VEHICULE v ON d.VehiculID=v.VehiculID WHERE v.ClientID=c.ClientID) > %s
        ORDER BY Total DESC
        """
        c.execute(sql, (min_spent,))
        return c.fetchall(), ["Nume", "Prenume", "Telefon", "Total Investit (RON)"]
    except Exception as e: print(e); return [], []

# ==============================================================================
# --- ZONA AUDIT (EFICIENTA) - SUBCERERI AVANSATE ---
# ==============================================================================

def get_audit_dead_stock(conn, furnizor_filter=None):
    """ Subcerere cu NOT IN (Piese nevandute) """
    try:
        c = conn.cursor()
        sql = """
        SELECT p.CodPiesa, p.Denumire, p.StocDisponibil, p.PretAchizitie, f.NumeFurnizor
        FROM PIESE p JOIN FURNIZORI f ON p.FurnizorID = f.FurnizorID
        WHERE p.PiesaID NOT IN (SELECT DISTINCT PiesaID FROM COMANDA_PIESE)
        """
        p = []
        if furnizor_filter and furnizor_filter.strip():
            sql += " AND f.NumeFurnizor LIKE %s"; p.append(f"%{furnizor_filter}%")
        c.execute(sql, tuple(p))
        return c.fetchall(), ["Cod Piesa", "Denumire", "Stoc Blocat", "Pret Achizitie", "Furnizor"]
    except Exception as e: print(e); return [], []

def get_audit_top_mechanics_revenue(conn):
    """ Subcerere in HAVING (Peste Media Globala) """
    try:
        c = conn.cursor()
        sql = """
        SELECT mec.Nume, mec.Prenume, SUM(m.CostLinie) as Venit
        FROM MECANICI mec JOIN MANOPERA m ON mec.MecanicID = m.MecanicID
        GROUP BY mec.MecanicID
        HAVING SUM(m.CostLinie) > (
            SELECT AVG(TotalPerMec) FROM (
                SELECT SUM(CostLinie) as TotalPerMec FROM MANOPERA GROUP BY MecanicID
            ) as SubQ
        )
        ORDER BY Venit DESC
        """
        c.execute(sql)
        return c.fetchall(), ["Nume", "Prenume", "Venit Generat (RON)"]
    except Exception as e: print(e); return [], []

# ==============================================================================
# --- ZONA STATISTICI (DASHBOARD GRAFICE) ---
# ==============================================================================

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
    try:
        c = conn.cursor()
        sql = "SELECT DATE_FORMAT(DataEmitere, '%Y-%m') as Luna, SUM(TotalCuTVA) FROM FACTURA WHERE StarePlata = 'Platita' GROUP BY Luna ORDER BY Luna DESC LIMIT 6"
        c.execute(sql)
        return c.fetchall()
    except: return []

# ==============================================================================
# --- ZONA ISTORIC & FACTURA DETALIATĂ ---
# ==============================================================================

def get_vehicle_history_data(conn, vid):
    """ Istoric complet (Devize + Piese + Manopera) """
    try:
        c = conn.cursor()
        c.execute("SELECT DevizID, DataPrimire, StareDeviz, DescriereProblemaClient, CostTotalEstimativ FROM DEVIZE WHERE VehiculID = %s ORDER BY DataPrimire DESC", (vid,))
        devize = c.fetchall()
        
        history = []
        for dev in devize:
            did = dev[0]
            # Selectam Numele Piesei, nu ID-ul
            c.execute("SELECT p.Denumire, cp.Cantitate, cp.PretUnitarVanzare FROM COMANDA_PIESE cp JOIN PIESE p ON cp.PiesaID = p.PiesaID WHERE cp.DevizID=%s", (did,))
            piese = c.fetchall()
            # Selectam Numele Serviciului si al Mecanicului
            c.execute("SELECT s.Denumire, m.Nume, man.OreLucrate FROM MANOPERA man JOIN SERVICII s ON man.ServiciuID=s.ServiciuID JOIN MECANICI m ON man.MecanicID=m.MecanicID WHERE man.DevizID=%s", (did,))
            manopera = c.fetchall()
            history.append({"deviz": dev, "piese": piese, "manopera": manopera})
        return history
    except: return []

def fetch_invoice_details_complex(conn, serie_factura):
    """ Date complete pentru PDF (Join cu Client, Vehicul, Piese, Manopera) """
    try:
        c = conn.cursor()
        # 1. Header
        sql_h = """SELECT f.FacturaID, f.SerieNumar, f.DataEmitere, f.TotalFaraTVA, f.ValoareTVA, f.TotalCuTVA,
                   c.Nume, c.Prenume, c.Adresa, c.Telefon, c.CUI, v.Marca, v.Model, v.NumarInmatriculare, d.DevizID
                   FROM FACTURA f JOIN DEVIZE d ON f.DevizID=d.DevizID JOIN VEHICULE v ON d.VehiculID=v.VehiculID JOIN CLIENTI c ON v.ClientID=c.ClientID
                   WHERE f.SerieNumar=%s"""
        c.execute(sql_h, (serie_factura,))
        head = c.fetchone()
        if not head: return None
        
        did = head[14]
        
        # 2. Piese (Join Piese)
        sql_p = "SELECT p.Denumire, cp.Cantitate, cp.PretUnitarVanzare, (cp.Cantitate*cp.PretUnitarVanzare) FROM COMANDA_PIESE cp JOIN PIESE p ON cp.PiesaID=p.PiesaID WHERE cp.DevizID=%s"
        c.execute(sql_p, (did,))
        piese = c.fetchall()
        
        # 3. Manopera (Join Servicii)
        sql_m = "SELECT s.Denumire, man.OreLucrate, man.TarifOraAplicat, man.CostLinie FROM MANOPERA man JOIN SERVICII s ON man.ServiciuID=s.ServiciuID WHERE man.DevizID=%s"
        c.execute(sql_m, (did,))
        manopera = c.fetchall()
        
        return {"header": head, "piese": piese, "manopera": manopera}
    except Exception as e:
        print(e); return None