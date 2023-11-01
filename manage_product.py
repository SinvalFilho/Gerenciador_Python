import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox

class ManageProduct:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciar Produto")

        self.search_label = tk.Label(root, text="Pesquisar Produto:")
        self.search_label.grid(row=0, column=0)
        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=0, column=1)
        self.search_button = tk.Button(root, text="Pesquisar", command=self.search_product)
        self.search_button.grid(row=0, column=2)

        self.filter_label = tk.Label(root, text="Filtrar por Categoria:")
        self.filter_label.grid(row=1, column=0)
        self.filter_var = tk.StringVar()
        self.filter_combobox = ttk.Combobox(root, textvariable=self.filter_var, values=["Todos", "alimento", "eletronico", "ferramenta"])
        self.filter_combobox.grid(row=1, column=1)
        self.filter_combobox.set("Todos")
        self.filter_button = tk.Button(root, text="Filtrar", command=self.filter_products)
        self.filter_button.grid(row=1, column=2)

        self.product_tree = ttk.Treeview(root, columns=("Código de Barras", "Nome", "Categoria", "Quantidade", "Preço", "Validade"))
        self.product_tree.heading("#1", text="Código de Barras")
        self.product_tree.heading("#2", text="Nome")
        self.product_tree.heading("#3", text="Categoria")
        self.product_tree.heading("#4", text="Quantidade")
        self.product_tree.heading("#5", text="Preço")
        self.product_tree.heading("#6", text="Validade")
        self.product_tree.column("#1", width=100)
        self.product_tree.column("#2", width=150)
        self.product_tree.column("#3", width=100)
        self.product_tree.column("#4", width=80)
        self.product_tree.column("#5", width=80)
        self.product_tree.column("#6", width=100)
        self.product_tree.grid(row=2, column=0, columnspan=3)

        self.load_products()
        self.product_tree.bind("<ButtonRelease-1>", self.select_product)
        
        self.delete_button = tk.Button(root, text="Apagar Produto", command=self.confirm_delete_product)
        self.delete_button.grid(row=3, column=0, columnspan=3)
        
        self.update_button = tk.Button(root, text="Atualizar Produto", command=self.open_update_product)
        self.update_button.grid(row=4, column=0, columnspan=3)
        
    def confirm_delete_product(self):
        if hasattr(self, "selected_product"):
            response = messagebox.askyesno("Confirmação", "Tem certeza de que deseja apagar este produto?")
            if response:
                self.delete_product()
                
    def delete_product(self):
        if hasattr(self, "selected_product"):
            codigo_barras = self.selected_product[0]
            connection = sqlite3.connect("products.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM produtos WHERE codigo_barras=?", (codigo_barras,))
            connection.commit()
            connection.close()
            self.load_products()

    def search_product(self):
        search_text = self.search_entry.get()
        connection = sqlite3.connect("products.db")
        cursor = connection.cursor()

        if self.filter_var.get() == "Todos":
            cursor.execute("SELECT * FROM produtos WHERE nome LIKE ? OR codigo_barras LIKE ?", ('%' + search_text + '%', '%' + search_text + '%'))
        else:
            cursor.execute("SELECT * FROM produtos WHERE (nome LIKE ? OR codigo_barras LIKE ?) AND categoria = ?", ('%' + search_text + '%', '%' + search_text + '%', self.filter_var.get()))

        self.display_products(cursor.fetchall())

    def filter_products(self):
        filter_type = self.filter_var.get()
        connection = sqlite3.connect("products.db")
        cursor = connection.cursor()

        if filter_type == "Todos":
            cursor.execute("SELECT * FROM produtos")
        else:
            cursor.execute("SELECT * FROM produtos WHERE categoria = ?", (filter_type,))

        self.display_products(cursor.fetchall())

    def load_products(self):
        connection = sqlite3.connect("products.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM produtos")
        self.display_products(cursor.fetchall())

    def display_products(self, products):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        for product in products:
            self.product_tree.insert("", "end", values=product)

    def select_product(self, event):
        item = self.product_tree.selection()
        if item:
            self.selected_product = self.product_tree.item(item, "values")

    def open_update_product(self):
        if hasattr(self, "selected_product"):
            EditProductDetails(self, self.selected_product)

class EditProductDetails:
    def __init__(self, manage_product, product):
        self.manage_product = manage_product
        self.product = product

        self.edit_window = tk.Toplevel()
        self.edit_window.title("Editar Produto")

        tk.Label(self.edit_window, text="Código de Barras:").grid(row=0, column=0)
        self.codigo_barras_entry = tk.Entry(self.edit_window)
        self.codigo_barras_entry.grid(row=0, column=1)
        self.codigo_barras_entry.insert(0, product[0])

        tk.Label(self.edit_window, text="Nome:").grid(row=1, column=0)
        self.nome_entry = tk.Entry(self.edit_window)
        self.nome_entry.grid(row=1, column=1)
        self.nome_entry.insert(0, product[1])

        tk.Label(self.edit_window, text="Categoria:").grid(row=2, column=0)
        self.categoria_var = tk.StringVar()
        self.categoria_combobox = ttk.Combobox(self.edit_window, textvariable=self.categoria_var, values=["alimento", "eletronico", "ferramenta"])
        self.categoria_combobox.grid(row=2, column=1)
        self.categoria_combobox.set(product[2])

        tk.Label(self.edit_window, text="Quantidade:").grid(row=3, column=0)
        self.quantidade_entry = tk.Entry(self.edit_window)
        self.quantidade_entry.grid(row=3, column=1)
        self.quantidade_entry.insert(0, product[3])

        tk.Label(self.edit_window, text="Preço:").grid(row=4, column=0)
        self.preco_entry = tk.Entry(self.edit_window)
        self.preco_entry.grid(row=4, column=1)
        self.preco_entry.insert(0, product[4])

        tk.Label(self.edit_window, text="Validade:").grid(row=5, column=0)
        self.validade_entry = tk.Entry(self.edit_window)
        self.validade_entry.grid(row=5, column=1)
        self.validade_entry.insert(0, product[5])

        save_button = tk.Button(self.edit_window, text="Salvar", command=self.save_product)
        save_button.grid(row=6, column=0, columnspan=2)

    def save_product(self):
        codigo_barras = self.codigo_barras_entry.get()
        nome = self.nome_entry.get()
        categoria = self.categoria_var.get()
        quantidade = int(self.quantidade_entry.get())
        preco = float(self.preco_entry.get())
        validade = self.validade_entry.get()

        connection = sqlite3.connect("products.db")
        cursor = connection.cursor()

        cursor.execute("UPDATE produtos SET codigo_barras=?, nome=?, categoria=?, quantidade=?, preco=?, validade=? WHERE codigo_barras=?",
                       (codigo_barras, nome, categoria, quantidade, preco, validade, self.product[0]))
        connection.commit()
        connection.close()

        self.edit_window.destroy()
        self.manage_product.load_products()

if __name__ == "__main__":
    root = tk.Tk()
    app = ManageProduct(root)
    root.mainloop()
