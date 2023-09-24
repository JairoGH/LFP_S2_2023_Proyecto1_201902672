import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from Analizador import analizador


class app:
    content = ''
    current_file_path = ''

    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico")
        self.root.geometry("800x600")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.open_button = tk.Button(self.button_frame, text="Abrir Archivo", command=self.open_file)
        self.open_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.button_frame, text="Guardar", command=self.save_file_current)
        self.save_button.pack(side=tk.LEFT)

        self.save_as_button = tk.Button(self.button_frame, text="Guardar Como", command=self.save_file)
        self.save_as_button.pack(side=tk.LEFT)

        self.analyze_button = tk.Button(self.button_frame, text="Analizar", command=self.analizar)
        self.analyze_button.pack(side=tk.LEFT)

        self.analyze_button = tk.Button(self.button_frame, text="Errores", command=self.errores)
        self.analyze_button.pack(side=tk.LEFT)

        self.analyze_button = tk.Button(self.button_frame, text="Reporte", command=self.reporte)
        self.analyze_button.pack(side=tk.LEFT)

        self.exit_button = tk.Button(self.button_frame, text="Salir",width=6, command=root.quit)
        self.exit_button.pack(side=tk.RIGHT)


        self.line_number_bar = tk.Text(root, width=4, padx=4, takefocus=0, border=0, background='DarkOliveGreen1',state='disabled')
        self.line_number_bar.pack(side=tk.LEFT, fill=tk.Y)

        self.text_widget = ScrolledText(self.root, wrap=tk.WORD, background='LightSteelBlue3')
        self.text_widget.pack(expand=True, fill='both')

        self.current_line = 1

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos con Formato JSON", "*.json")])
        if file_path:
            self.current_file_path = file_path
            with open(file_path, 'r') as file:
                self.content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, self.content)
            self.update_line_numbers()

    def save_file_current(self):
        if self.current_file_path:
            self.content = self.text_widget.get(1.0, tk.END)
            with open(self.current_file_path, 'w') as file:
                file.write(self.content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
        else:
            messagebox.showerror("Error", "No se ha abierto ningún archivo para guardar.")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos de con Formato JSON", "*.json")])
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
        print("Analisis terminado")
        analizar.operacion()

    def errores(self):
        print("Mostrando errores...")
        analizar = analizador()
        messagebox.showinfo("Mensaje:","Reporte de Errores Generados...")
        analizar.reporte_errores()


    def reporte(self):
        messagebox.showinfo("Mensaje:","Reporte Generado...")


if __name__ == "__main__":
    root = tk.Tk()
    app = app(root)
    root.mainloop()