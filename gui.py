import tkinter as tk
from tkinter import ttk

from app import login_fun

def on_submit():
    user = entry_user_str.get()
    password = entry_password_str.get()
    port = entry_port_str.get()
    host = entry_host_str.get()
    database = entry_database_str.get()

    login_fun(host, user, port, password, database)

#window
window = tk.Tk()
window.title("Service DB")
window.geometry('500x300')

title_label = ttk.Label(master=window, text='Database Login', font='Calibri 24')
title_label.pack()

#var
entry_user_str = tk.StringVar()
entry_password_str = tk.StringVar()
entry_port_str = tk.StringVar()
entry_host_str = tk.StringVar()
entry_database_str = tk.StringVar()

#input
entry1 = ttk.Entry(master=window, textvariable=entry_user_str)
entry2 = ttk.Entry(master=window, textvariable=entry_password_str, show="*")
entry3 = ttk.Entry(master=window, textvariable=entry_port_str)
entry4 = ttk.Entry(master=window, textvariable=entry_host_str)
entry5 = ttk.Entry(master=window, textvariable=entry_database_str)

entry1.pack()
entry2.pack()
entry3.pack()
entry4.pack()
entry5.pack()

#submit
button = ttk.Button(master=window, text='Login', command=on_submit)
button.pack(pady=10)

#output
output_string = tk.StringVar()
output_label = ttk.Label(master=window, textvariable=output_string)
output_label.pack(pady=5)

window.mainloop()
