import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",       # Văzut în imaginea 2 (localhost:3306)
    user="root",            # Văzut în imaginea 2
    port="3306",            # Văzut în ambele imagini
    password="alex", # Parola setată de tine la instalare
    database="evidentaservice"   # Baza de date pe care ai creat-o
)

print(mydb)