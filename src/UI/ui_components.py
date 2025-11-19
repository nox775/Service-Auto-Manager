import ttkbootstrap as ttk

def create_input_row(parent, label_text, textvariable, show=None):
    """Helper pentru a crea rapid un rând de input (Label + Entry)."""
    frame = ttk.Frame(parent)
    frame.pack(pady=5, fill='x', padx=10)
    
    lbl = ttk.Label(frame, text=label_text, width=15, anchor='e')
    lbl.pack(side='left', padx=5)
    
    entry = ttk.Entry(frame, textvariable=textvariable, width=30, show=show)
    entry.pack(side='left', padx=5, fill='x', expand=True)
    
    return frame

def clear_treeview(tree):
    """Șterge datele vechi din tabel."""
    for row in tree.get_children():
        tree.delete(row)