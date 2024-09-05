import json
import uuid
import random

def gerar_matricula():
    # matricula com 8 digitos
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])


class Livro:
    def __init__(self, nome, edicao, autor, ano_publicacao, localizacao, numero_de_copias, numero_de_copias_alugadas = 0, identificador = None):
        self.identificador = identificador if identificador else str(uuid.uuid4())
        self.nome = nome
        self.edicao = edicao
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.localizacao = localizacao
        self.numero_de_copias = numero_de_copias
        self.numero_de_copias_alugadas = numero_de_copias_alugadas

    def __str__(self):
        return f"Livro: {self.nome}; Autor: {self.autor}"

    def para_dict(self):
        return self.__dict__

class Usuario:
    def __init__(self, nome, sobrenome, numero_de_matricula, multa, dias_alugando, livros_alugados=None):
        self.nome = nome
        self.sobrenome = sobrenome
        self.numero_de_matricula = numero_de_matricula
        self.multa = multa
        self.dias_alugando = dias_alugando
        self.livros_alugados = livros_alugados if livros_alugados else []
        self.db = Database()

    def __str__(self):
        return f"{self.nome} {self.sobrenome} Matrícula: {self.numero_de_matricula} Multa: {self.multa}"

    def is_admin(self) -> bool:
        return self.numero_de_matricula == "00000000"

    def cadastra_livro(self, livro: Livro):
        if self.is_admin():
            self.db.adiciona_livro(livro)

    def remove_livro(self, livro_id: str):
        if self.is_admin():
            self.db.remove_livro(livro_id)
    
    def lista_livros(self):
        return self.db.lista_livros()
    
    def para_dict(self):
        return {
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "numero_de_matricula": self.numero_de_matricula,
            "multa": self.multa,
            "dias_alugando": self.dias_alugando,
            "livros_alugados": self.livros_alugados
        }
    
class Admin(Usuario):
    def __init__(self, nome, sobrenome):
        super().__init__(nome, sobrenome, "00000000", 0, 0)

    def lista_alunos(self):
        return [usuario for usuario in self.db.lista_usuarios() if not usuario.is_admin()]

    def busca_aluno(self, matricula: str):
        return self.db.busca_usuario(matricula)
    

class Aluno(Usuario):
    def __init__(self, nome, sobrenome, multa, dias_alugando, numero_de_matricula = None, livros_alugados=[]):
        if not numero_de_matricula:
            numero_de_matricula = gerar_matricula()

        super().__init__(nome, sobrenome, numero_de_matricula, multa, dias_alugando, livros_alugados)

    def aluga_livro(self, livro_id: str):
        # Buscar o livro na lista de livros
        livro = next((l for l in self.db.lista_livros() if l.identificador == livro_id), None)

        if livro and livro.numero_de_copias > livro.numero_de_copias_alugadas:
            self.livros_alugados.append(livro.identificador)
            livro.numero_de_copias_alugadas += 1
            self.db.atualiza_livro(livro)  # Atualiza o livro no banco de dados
            self.db.atualiza_usuario(self)  # Atualiza o usuário no banco de dados
            return "Livro alugado com sucesso"
        else:
            return "Livro não disponível para aluguel"

    def devolve_livro(self, livro_id: str):
        if livro_id in self.livros_alugados:
            self.livros_alugados.remove(livro_id)
            livro = next((l for l in self.db.lista_livros() if l.identificador == livro_id), None)
            if livro:
                livro.numero_de_copias_alugadas -= 1
                self.db.atualiza_livro(livro)  # Atualiza o livro no banco de dados
                self.db.atualiza_usuario(self)  # Atualiza o usuário no banco de dados
                return "Livro devolvido com sucesso"
        return "O livro não está alugado"

    def esta_alugado(self, livro_id: str):
        return livro_id in self.livros_alugados


class Database:
    def __init__(self):
        self.carregar_db()

    def carregar_db(self):
        with open("db.json", "r") as f:
            self.db = json.load(f)

    def salva_db(self):
        with open("db.json", "w") as f:
            json.dump(self.db, f)

    def adiciona_livro(self, livro: Livro):
        self.db["db_livros"].append(vars(livro))
        self.salva_db()

    def remove_livro(self, livro_id: str):
        self.db["db_livros"] = [livro for livro in self.db["db_livros"] if livro['identificador'] != livro_id]
        self.salva_db()

    def lista_livros(self):
        return [Livro(**dados_livro) for dados_livro in self.db["db_livros"]]

    def lista_usuarios(self):
        return [Usuario(**dados_usuario) for dados_usuario in self.db["db_usuarios"]]

    def busca_aluno(self, matricula: str):
        for dados_usuario in self.db["db_usuarios"]:
            if dados_usuario['numero_de_matricula'] == matricula:
                return Aluno(**dados_usuario)
        return None

    def adiciona_aluno(self, aluno: Aluno):
        self.db["db_usuarios"].append(aluno.para_dict())
        self.salva_db()
    
    def atualiza_livro(self, livro_atualizado: Livro):
        for i, livro in enumerate(self.db["db_livros"]):
            if livro['identificador'] == livro_atualizado.identificador:
                self.db["db_livros"][i] = livro_atualizado.para_dict()
                self.salva_db()
                break
    
    def atualiza_usuario(self, usuario_atualizado: Usuario):
        for i, usuario in enumerate(self.db["db_usuarios"]):
            if usuario['numero_de_matricula'] == usuario_atualizado.numero_de_matricula:
                self.db["db_usuarios"][i] = usuario_atualizado.para_dict()
                self.salva_db()
                break
