import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    def __init__(self):
        self.conn = None

    def connect(self, host, user, password, port, database):
        """Face conexiunea la baza de date."""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
                port=port,
                database=database
            )
            if self.conn.is_connected():
                return True
        except Error as e:
            print(f"Eroare la conectare: {e}")
            return False
        return False

    def get_connection(self):
        """Intoarce conexiunea activa (daca exista)."""
        return self.conn

    def close(self):
        """Inchide conexiunea daca este deschisa."""
        if self.conn and self.conn.is_connected():
            self.conn.close()


# instanta globala folosita in toata aplicatia
db = DatabaseManager()
