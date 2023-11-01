import tkinter as tk
import sqlite3
from add_product import AddProduct
from manage_product import ManageProduct
from sales_form import SalesForm

def create_database():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            codigo_barras TEXT PRIMARY KEY,
            nome TEXT,
            categoria TEXT,
            quantidade INTEGER,
            preco REAL,
            validade TEXT
        )
    ''')

    connection.commit()
    connection.close()

create_database()

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Produtos")
        
        self.add_product_button = tk.Button(root, text="Adicionar Produto", command=self.open_add_product)
        self.add_product_button.pack()

        self.manage_product_button = tk.Button(root, text="Gerenciar Produto", command=self.open_manage_product)
        self.manage_product_button.pack()

        self.sales_form_button = tk.Button(root, text="Formulário de Vendas", command=self.open_sales_form)
        self.sales_form_button.pack()

    def open_add_product(self):
        add_product_window = tk.Toplevel(self.root)
        AddProduct(add_product_window)

    def open_manage_product(self):
        manage_product_window = tk.Toplevel(self.root)
        ManageProduct(manage_product_window)

    def open_sales_form(self):
        sales_form_window = tk.Toplevel(self.root)
        SalesForm(sales_form_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
