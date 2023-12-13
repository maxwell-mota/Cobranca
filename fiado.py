import pyodbc
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class TelaPrincipal:
    def __init__(self, root, usuario):
        self.root = root
        self.root.geometry("600x400")
        self.root.title("Tela Principal")

        self.label_bem_vindo = tk.Label(root, text=f"Bem-vindo de volta, {usuario}!")
        self.label_bem_vindo.pack()

        self.btn_cadastrar_usuario = tk.Button(root, text="Cadastrar Usuário", command=self.abre_cadastro_usuario)
        self.btn_ver_datas_compras = tk.Button(root, text="Ver Datas de Compras", command=self.ver_datas_compras)
        self.btn_cadastrar_produto = tk.Button(root, text="Cadastrar produto comprado", command=self.abre_cadastro_produto)
        self.btn_cadastrar_usuario.pack()
        self.btn_ver_datas_compras.pack()
        self.btn_cadastrar_produto.pack()

    def abre_cadastro_usuario(self):
        
        CadastroUsuario(self)

    def ver_datas_compras(self):
        # Crie uma nova janela para exibir os resultados
        nova_tela = tk.Toplevel(self.root)
        nova_tela.title("Resultados das Compras")
        nova_tela.geometry("400x200")

        # Conectar ao banco de dados
        data = "DRIVER={SQL Server};SERVER=DESKTOP-TCNL30G;DATABASE=Clientes;"
        conexao = pyodbc.connect(data)
        conn = conexao.cursor()

        # Executar a consulta SQL
        query = "SELECT nome, prazo FROM Compras"
        conn.execute(query)
        result = conn.fetchall()

        # Exibir os resultados na nova janela
        for row in result:
            nome, prazo = row
            texto = f"Nome: {nome},  Prazo: {prazo}"
            label_prazos = tk.Label(nova_tela, text=texto)
            label_prazos.pack()

        # Fechar a conexão
        conn.close()
        self.btn_cobrar_usuario = tk.Button(nova_tela, text="Cobrar", command=self.cobrar_usuario)
        self.btn_cobrar_usuario.pack()
    def cobrar_usuario(self):
        data = "DRIVER={SQL Server};SERVER=DESKTOP-TCNL30G;DATABASE=Clientes;"
        conexao = pyodbc.connect(data)
        conn = conexao.cursor()

        query = "SELECT numero FROM Usuarios WHERE nome = 'maxwell';"
        conn.execute(query)
        resultado = conn.fetchone()

        nav = webdriver.Chrome()
        nav.get("https://web.whatsapp.com/")

        while len(nav.find_elements_by_id("side")):
            time.sleep(1)
        if resultado:
            numero_usuario = resultado.numero
            mensagem = f"Ola, passando aqui pra lembrar de suas pendencias"
            link = f"https://web.whatsapp.com/send?phone=55{numero_usuario}&text={mensagem}"
            nav.get(link)
        nav.quit()
    def abre_cadastro_produto(self):

        CadastroProduto(self)


class CadastroUsuario:
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal

        self.root = tk.Toplevel()  
        self.root.geometry("400x200")
        self.root.title("Cadastro de usuario")

        
        self.label_user = tk.Label(self.root, text="Insira o nome de usuario:")
        self.label_user.pack()
        self.new_user_label = tk.Entry(self.root)
        self.new_user_label.pack()

        self.label_phone = tk.Label(self.root, text="Digite o numero de telefone:")
        self.label_phone.pack()
        self.new_phone_label = tk.Entry(self.root)
        self.new_phone_label.pack()

       
        self.btn_cadastrar = tk.Button(self.root, text="Cadastrar", command=self.cadastrar_usuario)
        self.btn_cadastrar.pack()

    def cadastrar_usuario(self):
        
        nome_usuario = self.new_user_label.get().lower()
        numero_telefone = self.new_phone_label.get()

        
        data = "DRIVER={SQL Server};SERVER=DESKTOP-TCNL30G;DATABASE=Clientes;"
        conexao = pyodbc.connect(data)
        conn = conexao.cursor()

        query = "INSERT INTO Usuarios(nome, numero) VALUES (?, ?)"
        conn.execute(query, nome_usuario, numero_telefone)
        conexao.commit()

        
        messagebox.showinfo("Cadastro", "Usuario cadastrado com sucesso")

    

       
        self.root.destroy()

class CadastroProduto:
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal

        self.root = tk.Toplevel()  
        self.root.geometry("600x400")
        self.root.title("Cadastro de produto")

        self.label_product_name = tk.Label(self.root, text="Insira o nome do produto: ")
        self.label_product_name.pack()
        self.new_product_label = tk.Entry (self.root)
        self.new_product_label.pack()

        self.label_nome_comprador = tk.Label(self.root, text="Digite o nome do usuario: ")
        self.label_nome_comprador.pack()
        self.new_nome_comprador = tk.Entry(self.root)
        self.new_nome_comprador.pack()

        self.label_valor_produto = tk.Label(self.root, text="Digite o valor do produto: ")
        self.label_valor_produto.pack()
        self.new_valor_produto = tk.Entry(self.root)
        self.new_valor_produto.pack()

        self.label_prazo = tk.Label(self.root, text="Digite o prazo: ")
        self.label_prazo.pack()
        self.new_prazo = tk.Entry(self.root)
        self.new_prazo.pack()

        self.btn_cadastrar_produto = tk.Button(self.root, text="Cadastrar", command=self.cadastrar_produto)
        self.btn_cadastrar_produto.pack()

    def cadastrar_produto(self):
        nome_produto = self.new_product_label.get()
        nome_comprador = self.new_nome_comprador.get().lower()
        valor = self.new_valor_produto.get()
        valor_prazo = self.new_prazo.get()

        data = "DRIVER={SQL Server};SERVER=DESKTOP-TCNL30G;DATABASE=Clientes;"
        conexao = pyodbc.connect(data)
        conn = conexao.cursor()

        try:
            
            query_id_usuario = "SELECT idUsuario FROM Usuarios WHERE nome = ?"
            conn.execute(query_id_usuario, nome_comprador)
            resultado_id = conn.fetchone()

            if resultado_id is not None and resultado_id[0] is not None:
                id_usuario = resultado_id[0]

                query_cadastrar_produto = "INSERT INTO Compras(produto, idComprador, valor, prazo, nome) VALUES (?, ?, ?, ?, ?)"
                conn.execute(query_cadastrar_produto, nome_produto, id_usuario, valor, valor_prazo, nome_comprador)
                conn.commit()

                messagebox.showinfo("Cadastro produto", "Produto e prazo adicionado")
            else:
                messagebox.showerror("Erro", "Usuário não encontrado ou idUsuario é nulo")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {str(e)}")

        self.root.destroy()
class AplicacaoLogin:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x400")
        self.root.title("Login")

        self.label_usuario = tk.Label(root, text="Insira o usuário:")
        self.campo_usuario = tk.Entry(root)

        self.label_senha = tk.Label(root, text="Insira a senha:")
        self.campo_senha = tk.Entry(root, show="*")

        self.btn_login = tk.Button(root, text="Login", command=self.verifica)

        self.label_usuario.pack()
        self.campo_usuario.pack()
        self.label_senha.pack()
        self.campo_senha.pack()
        self.btn_login.pack()

    def verifica(self):
        usuario = self.campo_usuario.get()
        senha = self.campo_senha.get()

        for tentativa in range(3):
            if self.realiza_verificacao(usuario, senha):
                messagebox.showinfo("Login", "Login concluído, bem-vindo de volta admin!")
                self.abre_tela_principal(usuario)
                break
            else:
                messagebox.showerror("Login", "Tente novamente, pois algo está incorreto")
                self.campo_usuario.delete(0, tk.END)
                self.campo_senha.delete(0, tk.END)

        else:
            messagebox.showerror("Login", "Número máximo de tentativas excedido. Encerrando o programa.")
            self.root.destroy()

    def realiza_verificacao(self, usuario, senha):
        data = (
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-TCNL30G;"
            "DATABASE=Clientes;"
        )
        conexao = pyodbc.connect(data)
        conn = conexao.cursor()

        query = "SELECT COUNT(*) FROM adm WHERE usuario = ? AND senha = ?"
        conn.execute(query, usuario, senha)
        resultado = conn.fetchone()

        if resultado and resultado[0] > 0:
            print("Bem-vindo de volta!")
            return True
        else:
            return False

    def abre_tela_principal(self, usuario):
        self.root.destroy() 

        root_tela_principal = tk.Tk()
        app_tela_principal = TelaPrincipal(root_tela_principal, usuario)
        root_tela_principal.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoLogin(root)
    root.mainloop()
