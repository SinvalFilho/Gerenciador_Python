import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox

class SalesForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulário de Vendas")

        self.product_list = []
        self.total_price = 0.0

        self.search_label = tk.Label(root, text="Código de Barras do Produto:")
        self.search_label.grid(row=0, column=0)
        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=0, column=1)
        self.search_button = tk.Button(root, text="Adicionar Produto", command=self.add_product)
        self.search_button.grid(row=0, column=2)

        self.cart_tree = ttk.Treeview(root, columns=("Código de Barras", "Nome", "Quantidade", "Preço Unitário", "Preço Total"))
        self.cart_tree.heading("#1", text="Código de Barras")
        self.cart_tree.heading("#2", text="Nome")
        self.cart_tree.heading("#3", text="Quantidade")
        self.cart_tree.heading("#4", text="Preço Unitário")
        self.cart_tree.heading("#5", text="Preço Total")
        self.cart_tree.column("#1", width=100)
        self.cart_tree.column("#2", width=150)
        self.cart_tree.column("#3", width=80)
        self.cart_tree.column("#4", width=100)
        self.cart_tree.column("#5", width=100)
        self.cart_tree.grid(row=2, column=0, columnspan=4)

        self.remove_button = tk.Button(root, text="Remover Produto", command=self.remove_product)
        self.remove_button.grid(row=3, column=0, columnspan=2)

        self.payment_label = tk.Label(root, text="Forma de Pagamento:")
        self.payment_label.grid(row=4, column=0)
        self.payment_var = tk.StringVar()
        self.payment_combobox = ttk.Combobox(root, textvariable=self.payment_var, values=["PIX", "Débito", "Dinheiro", "Crédito"])
        self.payment_combobox.grid(row=4, column=1)
        self.payment_combobox.set("PIX")

        self.checkout_button = tk.Button(root, text="Concluir Compra", command=self.checkout)
        self.checkout_button.grid(row=5, column=0, columnspan=2)

    def add_product(self):
        codigo_barras = self.search_entry.get()
        connection = sqlite3.connect("products.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM produtos WHERE codigo_barras=?", (codigo_barras,))
        product = cursor.fetchone()
        connection.close()

        if product:
            product_id = product[0]
            product_name = product[1]
            product_price = product[4]

            found = False
            for item in self.product_list:
                if item[0] == product_id:
                    item[2] += 1
                    item[4] = item[2] * product_price
                    found = True
                    break

            if not found:
                self.product_list.append([product_id, product_name, 1, product_price, product_price])
            
            self.display_cart()
            self.search_entry.delete(0, 'end')

        else:
            messagebox.showerror("Produto não encontrado", "Código de Barras não encontrado.")

    def remove_product(self):
        if self.cart_tree.selection():
            item = self.cart_tree.selection()[0]
            product_id = int(self.cart_tree.item(item, "values")[0])

            for item in self.product_list:
                if item[0] == product_id:
                    if item[2] > 1:
                        item[2] -= 1
                        item[4] = item[2] * item[3]
                    else:
                        self.product_list.remove(item)
                    break

            self.display_cart()
        else:
            messagebox.showerror("Nenhum produto selecionado", "Por favor, selecione um produto para remover.")

    def display_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        self.total_price = 0.0
        for item in self.product_list:
            self.cart_tree.insert("", "end", values=(item[0], item[1], item[2], item[3], item[4]))
            self.total_price += item[4]

    def checkout(self):
        if self.product_list:
            payment_method = self.payment_var.get()
            
            connection = sqlite3.connect("products.db")
            cursor = connection.cursor()

            for item in self.product_list:
                cursor.execute("SELECT quantidade FROM produtos WHERE codigo_barras=?", (item[0],))
                current_quantity = cursor.fetchone()[0]

                if item[2] > current_quantity:
                    messagebox.showerror("Erro de estoque", "Não há produtos suficientes em estoque para a compra.")
                    connection.close()
                    return
                else:
                    cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE codigo_barras=?", (item[2], item[0]))

            connection.commit()
            connection.close()

            self.record_sale(payment_method)
            self.product_list.clear()
            self.display_cart()
            messagebox.showinfo("Compra Concluída", "A compra foi registrada com sucesso.")
        else:
            messagebox.showerror("Carrinho Vazio", "Adicione produtos ao carrinho antes de concluir a compra.")

    def record_sale(self, payment_method):
        connection = sqlite3.connect("sales_history.db")
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, payment_method TEXT, total_price REAL)")

        cursor.execute("INSERT INTO sales (payment_method, total_price) VALUES (?, ?)", (payment_method, self.total_price))
        connection.commit()
        connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesForm(root)
    root.mainloop()
