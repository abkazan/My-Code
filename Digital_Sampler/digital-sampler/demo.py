import tkinter as tk

def on_double_click(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        value = event.widget.get(index)
        print(f"Hello, {value}!")
        # Create a new window next to the Listbox
        new_window = tk.Toplevel()
        new_window.geometry(f"+{event.widget.winfo_rootx() + event.widget.winfo_width()}+{event.widget.winfo_rooty()}")
        new_window.title(f"Item {index + 1}")

root = tk.Tk()

my_listbox = tk.Listbox(root)
my_listbox.pack()

for i in range(10):
    my_listbox.insert(tk.END, f"Item {i}")

my_listbox.bind("<Double-1>", on_double_click)

root.mainloop()
