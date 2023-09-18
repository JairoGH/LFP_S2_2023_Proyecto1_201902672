import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from Analizador import analizador


class app:
    content = ''

    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico")

        self.line_number_bar = tk.Text(root, width=4, padx=4, takefocus=0, border=0, background='lemon chiffon', state='disabled')
        self.line_number_bar.pack(side=tk.LEFT, fill=tk.Y)

        self.text_widget = ScrolledText(self.root, wrap=tk.WORD)
        self.text_widget.pack(expand=True, fill='both')

        self.text_widget.bind('<Key>', self.update_line_numbers)
        self.text_widget.bind('<MouseWheel>', self.update_line_numbers)

        self.current_line = 1

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Abrir", command=self.open_file)
        self.file_menu.add_command(label="Guardar", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.root.quit)
        self.menu_bar.add_command(label="Analizar", command=self.analizar)
        self.menu_bar.add_command(label="Errores", command=self.Errores)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, self.content)
            self.update_line_numbers()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            self.content = self.text_widget.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(self.content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")

    def update_line_numbers(self, event=None):
        line_count = self.text_widget.get('1.0', tk.END).count('\n')
        if line_count != self.current_line:
            self.line_number_bar.config(state=tk.NORMAL)
            self.line_number_bar.delete(1.0, tk.END)
            for line in range(1, line_count + 1):
                self.line_number_bar.insert(tk.END, f"{line}\n")
            self.line_number_bar.config(state=tk.DISABLED)
            self.current_line = line_count

    def analizar(self):
        print("Analizando...")
        analizar = analizador()
        analizar.analizar_texto(self.content)

    def Errores(self):
        print("Mostrando errores...")

if __name__ == "__main__":
    root = tk.Tk()
    app = app(root)
    root.mainloop()