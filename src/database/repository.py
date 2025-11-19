from mysql.connector import Error

# --- Functii pentru tabela CLIENTI ---

def fetch_all_clients(conn):
    """
    Returneaza toti clientii pentru afisare.
    """
    try:
        cursor = conn.cursor()
        # luam doar coloanele de care avem nevoie in tabel
        sql = """
        SELECT ClientID, Nume, Prenume, Telefon, Email, TipClient, CUI 
        FROM CLIENTI
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
        print(f"Eroare SQL (select clienti): {e}")
        return []


def insert_client(conn, nume, prenume, telefon, email, adresa, tip_client, cui):
    """
    Adauga un client nou in tabela CLIENTI.
    """
    try:
        cursor = conn.cursor()
        
        # daca este persoana fizica, CUI nu are sens
        if tip_client == "Persoana fizica":
            cui = None

        sql = """
        INSERT INTO CLIENTI (Nume, Prenume, Telefon, Email, Adresa, TipClient, CUI)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (nume, prenume, telefon, email, adresa, tip_client, cui)
        
        cursor.execute(sql, values)
        conn.commit()  # commit obligatoriu pentru INSERT/UPDATE/DELETE
        
        affected = cursor.rowcount
        cursor.close()
        return affected > 0
    except Error as e:
        print(f"Eroare SQL (insert client): {e}")
        return False
    

# --- Functii pentru tabela VEHICULE ---


def fetch_all_vehicle(conn):
    """
    Returneaza toate vehiculele pentru afisare.
    """
    try:
        cursor = conn.cursor()
        sql = """
        SELECT VehiculID, ClientID, NumarInmatriculare, SerieSasiu, 
               Marca, Model, AnFabricatie, CodMotor, CapacitateCilindrica, TipCombustibil
        FROM VEHICULE
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as e:
        print(f"Eroare SQL (select vehicule): {e}")
        return []


def insert_vehicle(conn, client_id, nr_inmatriculare, serie_sasiu,
                   marca, model, an_fabricatie, cod_motor,
                   capacitate_cilindrica, tip_combustibil):
    """
    Adauga un vehicul nou in tabela VEHICULE.
    Presupune ca client_id exista deja in tabela CLIENTI.
    """
    try:
        cursor = conn.cursor()

        sql = """
        INSERT INTO VEHICULE (
            ClientID, NumarInmatriculare, SerieSasiu,
            Marca, Model, AnFabricatie, CodMotor,
            CapacitateCilindrica, TipCombustibil
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            client_id,
            nr_inmatriculare,
            serie_sasiu,
            marca,
            model,
            an_fabricatie,
            cod_motor,
            capacitate_cilindrica,
            tip_combustibil,
        )

        cursor.execute(sql, values)
        conn.commit()

        affected = cursor.rowcount
        cursor.close()
        return affected > 0
    except Error as e:
        print(f"Eroare SQL (insert vehicul): {e}")
        return False
