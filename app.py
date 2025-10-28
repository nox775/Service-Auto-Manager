import mysql.connector

def login_fun(host_login,user_login,port_login,password_login,database_login):
    try:
        mydb = mysql.connector.connect(
            host=host_login,       # Văzut în imaginea 2 (localhost:3306)
            user=user_login,            # Văzut în imaginea 2
            port=port_login,            # Văzut în ambele imagini
            password=password_login, # Parola setată de tine la instalare
            database=database_login   # Baza de date pe care ai creat-o
        )
    except : print("Eroare")
    print(mydb)
