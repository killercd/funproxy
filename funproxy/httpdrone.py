import tkinter as tk
from tkinter import ttk



class WinHTTPDrone():

    def __init__(self, root):
        self.root = root
        self.root.title("Text Area con Scrollbar, Ctrl+A e Menu Contestuale")
        
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(self.frame, wrap="word", yscrollcommand=self.scrollbar.set)
        self.text_area.pack(fill="both", expand=True)

        self.scrollbar.config(command=self.text_area.yview)

        sample_text = "Questo è un esempio di text area con una scrollbar.\n" * 20
        self.text_area.insert(tk.END, sample_text)

        self.text_area.bind("<Control-a>", self.select_all)
        self.text_area.bind("<Control-A>", self.select_all)

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copia", command=self.copy_text)
        self.context_menu.add_command(label="Taglia", command=self.cut_text)
        self.context_menu.add_command(label="Incolla", command=self.paste_text)

        self.text_area.bind("<Button-3>", self.show_context_menu)

    def select_all(event):
        event.widget.tag_add(tk.SEL, "1.0", tk.END)
        event.widget.mark_set(tk.INSERT, "1.0")
        event.widget.see(tk.INSERT)
        return 'break'

    def select_all(self, event):
        event.widget.tag_add(tk.SEL, "1.0", tk.END)
        event.widget.mark_set(tk.INSERT, "1.0")
        event.widget.see(tk.INSERT)
        return 'break'

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")


def main():
    root = tk.Tk()
    app = WinHTTPDrone(root)
    root.mainloop()

if __name__ == "__main__":
    main()
