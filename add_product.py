import tkinter as tk
import sqlite3
from tkinter import messagebox

class AddProduct:
    def __init__(self, root):
        self.root = root
        self.root.title("Adicionar Produto")

        self.codigo_barras_label = tk.Label(root, text="Código de Barras:")
        self.codigo_barras_label.grid(row=0, column=0)
        self.codigo_barras_entry = tk.Entry(root)
        self.codigo_barras_entry.grid(row=0, column=1)
        
        self.nome_label = tk.Label(root, text="Nome do Produto:")
        self.nome_label.grid(row=1, column=0)
        self.nome_entry = tk.Entry(root)
        self.nome_entry.grid(row=1, column=1)

        self.categoria_label = tk.Label(root, text="Categoria do Produto:")
        self.categoria_label.grid(row=2, column=0)
        self.categoria_var = tk.StringVar()
        self.categoria_combobox = tk.OptionMenu(root, self.categoria_var, "alimento", "eletronico", "ferramenta")
        self.categoria_combobox.grid(row=2, column=1)

        self.quantidade_label = tk.Label(root, text="Quantidade:")
        self.quantidade_label.grid(row=3, column=0)
        self.quantidade_entry = tk.Entry(root)
        self.quantidade_entry.grid(row=3, column=1)

        self.preco_label = tk.Label(root, text="Preço:")
        self.preco_label.grid(row=4, column=0)
        self.preco_entry = tk.Entry(root)
        self.preco_entry.grid(row=4, column=1)

        self.validade_label = tk.Label(root, text="Validade (opcional):")
        self.validade_label.grid(row=5, column=0)
        self.validade_entry = tk.Entry(root)
        self.validade_entry.grid(row=5, column=1)

        self.save_button = tk.Button(root, text="Salvar", command=self.save_product)
        self.save_button.grid(row=6, column=0, columnspan=2)

    def save_product(self):
        codigo_barras = self.codigo_barras_entry.get()
        nome = self.nome_entry.get()
        categoria = self.categoria_var.get()
        quantidade = int(self.quantidade_entry.get())
        preco = float(self.preco_entry.get())
        validade = self.validade_entry.get()

        connection = sqlite3.connect("products.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO produtos (codigo_barras, nome, categoria, quantidade, preco, validade) VALUES (?, ?, ?, ?, ?, ?)",
                       (codigo_barras, nome, categoria, quantidade, preco, validade))

        connection.commit()
        connection.close()

        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        self.root.destroy()
