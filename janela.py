import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QVBoxLayout, QTableWidget, QTableWidgetItem,QHeaderView, QTabWidget,QSpinBox, QStackedWidget
from PyQt5.QtCore import Qt
from livraria import Livro, Admin, Aluno, Database


WINDOWS_STYLE = 'background-color: #000; color: #ffffff;'
BTN_STYLE = 'background-color: #ffffff; color: #000; font-size: 18px; font-weight: bold; border-radius: 25px; border: 3px solid #000; padding: 6px;'
TABELAS_STYLE = """
            QTableWidget {
                font-size: 14px;
            }
            QTableWidget QHeaderView::section {
                background-color: #000;
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #ffffff;
                padding: 4px;
            }
            QTableWidget::item {
                color: #ffffff;
                border: 1px solid #000;
            }
            QTableWidget::item:selected {
                background-color: #b0d0ff;
                color: #03459c;
            }
        """

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Form')
        self.resize(1000, 600)
        self.setStyleSheet(WINDOWS_STYLE)

        self.stacked_widget = QStackedWidget(self)
        self.initLoginForm()
        self.initCadastroAlunoForm()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)

    def initLoginForm(self):
        login_form = QWidget()
        layout = QGridLayout(login_form)

        label_name = QLabel('<font size="4"> Matricula </font>')
        self.lineEdit_matricula = QLineEdit()
        self.lineEdit_matricula.setPlaceholderText('Coloque sua matricula aqui')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_matricula, 0, 1)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.go_to)
        button_login.setFixedSize(100, 50)
        button_login.setStyleSheet(BTN_STYLE)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)
        layout.setAlignment(Qt.AlignHCenter)

        login_form.setLayout(layout)
        self.stacked_widget.addWidget(login_form)

    def initCadastroAlunoForm(self):
        self.cadastro_aluno_form = CadastroAlunoScreen()
        self.stacked_widget.addWidget(self.cadastro_aluno_form)

    def go_to(self):
        matricula = self.lineEdit_matricula.text()

        if matricula == '0':
            admin = Admin("Super", "Admin")
            self.admin_screen = AdminScreen(admin=admin)
            self.admin_screen.show()
            self.close()
        else:
            db = Database()
            aluno = db.busca_aluno(matricula)
            if aluno is None:
                self.stacked_widget.setCurrentWidget(self.cadastro_aluno_form)
            else:
                self.aluno_screen = AlunoScreen(aluno=aluno)
                self.aluno_screen.show()
                self.close()


class CadastroAlunoScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # Estilos
        label_style = "font-size: 14px; font-weight: bold; color: #ffffff;"
        input_style = "font-size: 14px; padding: 5px; border: 1px solid #cccccc; border-radius: 4px; margin: 2px;"
        button_style = "font-size: 14px; padding: 10px; border: none; background-color: #007bff; color: white;"
        title_style = "font-size: 16px; font-weight: bold; color: #ffffff;"

        # Título
        titulo_label = QLabel("Essa matrícula não existe, registre sua conta")
        titulo_label.setStyleSheet(title_style)
        layout.addWidget(titulo_label, 0, 0, 1, 2, Qt.AlignCenter)

        # Campos de entrada
        self.nome_input = QLineEdit(self)
        self.nome_input.setStyleSheet(input_style)
        self.sobrenome_input = QLineEdit(self)
        self.sobrenome_input.setStyleSheet(input_style)

        labels = [
            ('Nome:', self.nome_input),
            ('Sobrenome:', self.sobrenome_input),
        ]

        for i, (text, widget) in enumerate(labels, start=1):  # start=1 para começar após o título
            label = QLabel(text)
            label.setStyleSheet(label_style)
            layout.addWidget(label, i, 0)
            layout.addWidget(widget, i, 1)

        # Botão para criar a conta
        btn_submit = QPushButton('Nova conta', self)
        btn_submit.setStyleSheet(button_style)
        btn_submit.clicked.connect(self.cadastrar_aluno)
        layout.addWidget(btn_submit, len(labels) + 1, 0, 1, 2)

        self.setLayout(layout)

    def cadastrar_aluno(self):
        aluno = Aluno(
            self.nome_input.text(),
            self.sobrenome_input.text(),
            0,
            0,
        )
        db = Database()
        db.adiciona_aluno(aluno)
        QMessageBox.information(self, 'Conta criada', f'sua matricula é {aluno.numero_de_matricula}!')
        self.aluno_screen = AlunoScreen(aluno=aluno)
        self.aluno_screen.show()
        self.close()


class CadastroLivroScreen(QWidget):
    def __init__(self, admin):
        super().__init__()
        self.admin = admin
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        label_style = "font-size: 14px; font-weight: bold; color: #ffffff;"  # Correção na cor
        input_style = "font-size: 14px; padding: 5px; border: 1px solid #cccccc; border-radius: 4px; margin: 2px;"
        button_style = "font-size: 14px; padding: 10px; border: none; background-color: #007bff; color: white;"
        self.nome_input = QLineEdit(self)
        self.nome_input.setStyleSheet(input_style)
        self.edicao_input = QLineEdit(self)
        self.edicao_input.setStyleSheet(input_style)
        self.autor_input = QLineEdit(self)
        self.autor_input.setStyleSheet(input_style)
        self.ano_publicacao_input = QSpinBox(self)
        self.ano_publicacao_input.setRange(1900, 2100)
        self.ano_publicacao_input.setStyleSheet(input_style)
        self.localizacao_input = QLineEdit(self)
        self.localizacao_input.setStyleSheet(input_style)
        self.numero_de_copias_input = QSpinBox(self)
        self.numero_de_copias_input.setStyleSheet(input_style)

        labels = [
            ('Nome:', self.nome_input),
            ('Edição:', self.edicao_input),
            ('Autor:', self.autor_input),
            ('Ano de Publicação:', self.ano_publicacao_input),
            ('Localização:', self.localizacao_input),
            ('Número de Cópias:', self.numero_de_copias_input)
        ]

        for i, (text, widget) in enumerate(labels):
            label = QLabel(text)
            label.setStyleSheet(label_style)
            layout.addWidget(label, i, 0)
            layout.addWidget(widget, i, 1)

        btn_submit = QPushButton('Cadastrar Livro', self)
        btn_submit.setStyleSheet(button_style)
        btn_submit.clicked.connect(self.cadastrar_livro)
        layout.addWidget(btn_submit, len(labels), 0, 1, 2)

        self.setLayout(layout)

    def cadastrar_livro(self):
        livro = Livro(
            self.nome_input.text(),
            self.edicao_input.text(),
            self.autor_input.text(),
            self.ano_publicacao_input.value(),
            self.localizacao_input.text(),
            int(self.numero_de_copias_input.value()),
        )
        self.admin.cadastra_livro(livro)
        QMessageBox.information(self, 'Livro Cadastrado', f'O livro "{livro.nome}" foi cadastrado com sucesso!')

class TabelaLivrosScreen(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Nome', 'Autor', 'Edição', 'Ano', 'Localização', 'Ação'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet(TABELAS_STYLE)

        self.loadTableData()
        layout.addWidget(self.table)
    
    def loadTableData(self):
        livros = self.user.lista_livros()
        self.table.setRowCount(len(livros))
        for i, livro in enumerate(livros):
            self.table.setItem(i, 0, QTableWidgetItem(livro.nome))
            self.table.setItem(i, 1, QTableWidgetItem(livro.autor))
            self.table.setItem(i, 2, QTableWidgetItem(livro.edicao))
            self.table.setItem(i, 3, QTableWidgetItem(str(livro.ano_publicacao)))
            self.table.setItem(i, 4, QTableWidgetItem(livro.localizacao))
            
            if isinstance(self.user, Admin):
                btn_remover = QPushButton('Remover', self)
                btn_remover.clicked.connect(lambda _, row=i: self.remove_livro(row))
                self.table.setCellWidget(i, 5, btn_remover)
            else:
                if self.user.esta_alugado(livro.identificador):
                    btn_alugar = QPushButton('Devolver', self)
                    btn_alugar.clicked.connect(lambda _, row=i: self.devolve_livro(row))
                    self.table.setCellWidget(i, 5, btn_alugar)
                else:
                    btn_alugar = QPushButton('Alugar', self)
                    btn_alugar.clicked.connect(lambda _, row=i: self.alugar_livro(row))
                    self.table.setCellWidget(i, 5, btn_alugar)

    def showEvent(self, event):
        super().showEvent(event)
        self.loadTableData()

    def remove_livro(self, row):
        livro_selecionado = self.user.lista_livros()[row]
        self.user.remove_livro(livro_selecionado.identificador)
        QMessageBox.information(self, 'Livro Removido', f'O livro "{livro_selecionado.nome}" foi removido com sucesso!')
        self.loadTableData()
    
    def alugar_livro(self, row):
        livro_selecionado = self.user.lista_livros()[row]
        mensagem = self.user.aluga_livro(livro_selecionado.identificador)
        QMessageBox.information(self, 'Opa', mensagem)
        self.loadTableData()
    
    def devolve_livro(self, row):
        livro_selecionado = self.user.lista_livros()[row]
        mensagem = self.user.devolve_livro(livro_selecionado.identificador)
        QMessageBox.information(self, 'Opa', mensagem)
        self.loadTableData()


class TabelaAlunosScreen(QWidget):
    def __init__(self, admin):
        super().__init__()
        self.admin = admin
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Nome', 'Sobrenome', 'Número de Matrícula', 'Multa'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet(TABELAS_STYLE)

        alunos = self.admin.lista_alunos()
        self.table.setRowCount(len(alunos))
        for i, aluno in enumerate(alunos):
            self.table.setItem(i, 0, QTableWidgetItem(aluno.nome))
            self.table.setItem(i, 1, QTableWidgetItem(aluno.sobrenome))
            self.table.setItem(i, 2, QTableWidgetItem(aluno.numero_de_matricula))
            self.table.setItem(i, 3, QTableWidgetItem(str(aluno.multa)))

        layout.addWidget(self.table)

class AlunoInfoScreen(QWidget):
    def __init__(self, aluno):
        super().__init__()
        self.aluno = aluno
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.nome_label = QLabel(self.aluno.nome)
        self.sobrenome_label = QLabel(self.aluno.sobrenome)
        self.matricula_label = QLabel(self.aluno.numero_de_matricula)
        self.multa_label = QLabel(str(self.aluno.multa))
        self.dias_alugando_label = QLabel(str(self.aluno.dias_alugando))
        self.livros_alugados_label = QLabel(str(len(self.aluno.livros_alugados)))

        self.layout.addWidget(QLabel('Nome:'), 0, 0)
        self.layout.addWidget(self.nome_label, 0, 1)

        self.layout.addWidget(QLabel('Sobrenome:'), 1, 0)
        self.layout.addWidget(self.sobrenome_label, 1, 1)

        self.layout.addWidget(QLabel('Número de Matrícula:'), 2, 0)
        self.layout.addWidget(self.matricula_label, 2, 1)

        self.layout.addWidget(QLabel('Multa:'), 3, 0)
        self.layout.addWidget(self.multa_label, 3, 1)

        self.layout.addWidget(QLabel('Dias Alugando:'), 4, 0)
        self.layout.addWidget(self.dias_alugando_label, 4, 1)

        self.layout.addWidget(QLabel('Livros Alugados:'), 5, 0)
        self.layout.addWidget(self.livros_alugados_label, 5, 1)

    def updateInfo(self):
        # Atualiza as informações do aluno
        self.nome_label.setText(self.aluno.nome)
        self.sobrenome_label.setText(self.aluno.sobrenome)
        self.matricula_label.setText(self.aluno.numero_de_matricula)
        self.multa_label.setText(str(self.aluno.multa))
        self.dias_alugando_label.setText(str(self.aluno.dias_alugando))
        self.livros_alugados_label.setText(str(len(self.aluno.livros_alugados)))

    def showEvent(self, event):
        super().showEvent(event)
        self.updateInfo()  # Atualiza as informações sempre que a tela é mostrada


class AlunoScreen(QWidget):
    def __init__(self, aluno):
        super().__init__()
        self.aluno = aluno
        self.setWindowTitle('Aluno Screen')
        self.resize(1000, 600)

        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab_livros = TabelaLivrosScreen(self.aluno)
        self.tabs.addTab(self.tab_livros, "Listar Livros")

        self.tab_info = AlunoInfoScreen(self.aluno)
        self.tabs.addTab(self.tab_info, "Informações")

        layout.addWidget(self.tabs)

        self.setLayout(layout)


class AdminScreen(QWidget):
    def __init__(self, admin):
        super().__init__()
        self.admin = admin
        self.setWindowTitle('Admin Screen')
        self.resize(1000, 600)

        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab_cadastro_livro = CadastroLivroScreen(self.admin)
        self.tabs.addTab(self.tab_cadastro_livro, "Cadastrar Livro")

        self.tab_listagem_livros = TabelaLivrosScreen(self.admin)
        self.tabs.addTab(self.tab_listagem_livros, "Listar Livros")

        self.tab_listagem_alunos = TabelaAlunosScreen(self.admin)
        self.tabs.addTab(self.tab_listagem_alunos, "Listar Alunos")

        layout.addWidget(self.tabs)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())
