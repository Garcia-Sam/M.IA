import os
import pandas as pd
from PyQt5.QtWidgets import (
    QMainWindow, QTableView, QVBoxLayout, QWidget,
    QPushButton, QFileDialog, QProgressBar, QHBoxLayout, QLabel, QGraphicsDropShadowEffect, QMessageBox, QDesktopWidget
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtGui
import src.backend


"""Arquivo para testar ajustes na interface"""


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        print(self.script_dir)

        self.setWindowTitle('M.IA')
        self.setGeometry(0, 0, 700, 700)

        # Centralizar a janela
        self.centralizar()

        icone = QtGui.QPixmap(self.script_dir + '/image/icone_mia.png').scaled(500, 500)
        icone = QtGui.QIcon(icone)
        self.setWindowIcon(icone)

        # Configuração do widget central e layout
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout = QVBoxLayout()
        self.widget_central.setLayout(self.layout)

        # Visualizador da tabela
        self.visualizador_tabela = QTableView()
        self.visualizador_tabela.setObjectName("visualizador_tabela")

        # Adicionar título, texto informativo, sombra ao visualizador e botões
        self.adicionar_texto_titulo()

        self.layout.addWidget(self.visualizador_tabela)
        self.adicionar_texto_informativo()

        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setColor(QColor(0, 0, 0, 30))
        sombra.setOffset(3, 3)
        self.visualizador_tabela.setGraphicsEffect(sombra)

        self.adicionar_botao_carregar()

        self.adicionar_botao_salvar()

        # Inicialização de variáveis
        self.df = None
        self.caminho_arquivo = None
        self.processando = False  # Flag para indicar se está processando

        # Conectar o botão salvar ao método de iniciar processamento
        self.botao_salvar.clicked.connect(self.iniciar_processamento)

        # Adicionar rodapé
        self.adicionar_rodape()

        # Carregar o arquivo .qss
        with open(self.script_dir + '/image/estilo.qss', 'r') as arquivo:
            self.estilo = arquivo.read()
            # setStyleSheet(self.estilo)

    def centralizar(self):
        # Obtém a geometria do quadro da janela
        qr = self.frameGeometry()

        # Obtém o ponto central da tela
        cp = QDesktopWidget().availableGeometry().center()

        # Move o quadro da janela para o ponto central
        qr.moveCenter(cp)

        # Define a posição da janela de acordo com o centro do quadro
        self.move(qr.topLeft())

    def adicionar_texto_titulo(self):
        # Adicionar título ao layout
        self.texto_titulo = QLabel('Pré-visualização das primeiras 250 linhas:')
        self.texto_titulo.setObjectName("texto_previsualizacao")
        self.texto_titulo.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.texto_titulo)

    def adicionar_texto_informativo(self):
        # Adicionar texto informativo ao layout
        self.texto_informativo = QLabel('Certifique-se que no seu arquivo tenham as seguintes colunas:'
                                        ' "NUMERO PROCESSO", "VALOR UNIAO" e "DATA DE SAIDA NECAP"')
        self.texto_informativo.setObjectName("texto_informativo")
        self.texto_informativo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.texto_informativo)

    def adicionar_botao_carregar(self):
        # Adicionar botão de carregar arquivo e barra de progresso ao layout
        self.layout_carregar = QHBoxLayout()
        self.botao_carregar = QPushButton('Carregar Excel')
        self.botao_carregar.setObjectName("botao_carregar")
        self.layout_carregar.addWidget(self.botao_carregar, 1)

        self.progresso_carregar = QProgressBar(self)
        self.progresso_carregar.setObjectName("progresso_carregar")
        self.progresso_carregar.setFormat('')
        self.layout_carregar.addWidget(self.progresso_carregar, 4)

        self.layout.addLayout(self.layout_carregar)
        self.botao_carregar.clicked.connect(self.selecionar_arquivo)

    def adicionar_botao_salvar(self):
        # Adicionar botão de salvar arquivo e barra de progresso ao layout
        self.layout_salvar = QHBoxLayout()
        self.botao_salvar = QPushButton('Salvar Excel')
        self.botao_salvar.setObjectName("botao_salvar")
        self.layout_salvar.addWidget(self.botao_salvar, 1)

        self.progresso_salvar = QProgressBar(self)
        self.progresso_salvar.setObjectName("progresso_salvar")
        self.progresso_salvar.setFormat('')
        self.layout_salvar.addWidget(self.progresso_salvar, 4)

        self.layout.addLayout(self.layout_salvar)

    def selecionar_arquivo(self):
        # Método para abrir diálogo de seleção de arquivo e carregar dados
        options = QFileDialog.Options()
        self.caminho_arquivo, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo Excel", "",
                                                              "Arquivos Excel (*.xlsx *.xls)", options=options)
        if self.caminho_arquivo:
            self.carregar_dados(self.caminho_arquivo)

    def carregar_dados(self, caminho_arquivo):
        # Método para carregar dados do arquivo Excel selecionado
        self.progresso_carregar.setValue(10)  # Resetar progresso
        self.df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        self.df = self.df.head(250)  # Limita a exibição a 250 linhas

        model = ModeloPandas(self.df)
        self.visualizador_tabela.setModel(model)
        self.progresso_carregar.setValue(50)
        self.visualizador_tabela.resizeColumnsToContents()
        self.visualizador_tabela.resizeRowsToContents()
        self.progresso_carregar.setValue(100)  # Concluir progresso

    def iniciar_processamento(self):
        # Método para iniciar processamento dos dados
        if not self.caminho_arquivo:
            QMessageBox.warning(self, "Cancelado", "Nenhum arquivo foi selecionado para salvar.")
            return

        self.processando = True  # Iniciar flag de processamento
        # self.progresso_salvar.setValue(10)  # Resetar progresso
        self.thread_processamento = QThread(self)
        self.worker = ProcessamentoWorker(self.caminho_arquivo)
        self.worker.moveToThread(self.thread_processamento)

        # Conectar sinais e slots
        self.worker.progresso_atualizado.connect(self.atualizar_progresso)
        self.worker.finished.connect(self.finalizar_processamento)
        self.thread_processamento.started.connect(self.worker.run)
        self.thread_processamento.start()

    def atualizar_progresso(self, progresso):
        # Método para atualizar a barra de progresso
        self.progresso_salvar.setValue(progresso)

    def finalizar_processamento(self):
        # Método para finalizar o processamento e mostrar mensagem de sucesso
        self.processando = False
        self.progresso_salvar.setValue(100)  # Definir a barra de progresso como completa
        QMessageBox.information(self, "Sucesso", "Dados formatados e salvos com sucesso!")

        # Encerrar thread e deletar worker
        self.thread_processamento.quit()
        self.thread_processamento.wait()
        self.thread_processamento.deleteLater()
        self.worker.deleteLater()

    def adicionar_rodape(self):
        # Adicionar rodapé ao layout
        layout_rodape = QHBoxLayout()
        label_texto = QLabel("Sou M.IA, seu robô de formatação e filtragem!")
        label_texto.setObjectName("label_rodape")
        layout_rodape.addWidget(label_texto)

        label_imagem = QLabel()
        pixmap = QPixmap(self.script_dir + '/image/icone__PRU1.png')  # Substitua pelo caminho para a sua imagem
        label_imagem.setPixmap(pixmap)
        label_imagem.setScaledContents(True)
        label_imagem.setMaximumSize(130, 40)
        layout_rodape.addWidget(label_imagem)

        self.layout.addLayout(layout_rodape)


class ModeloPandas(QAbstractTableModel):
    # Modelo personalizado para exibir dados do pandas DataFrame no QTableView
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            elif orientation == Qt.Vertical:
                return str(section + 1)


class ProcessamentoWorker(QObject):
    # Worker para processamento dos dados em segundo plano
    progresso_atualizado = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, caminho_arquivo):
        super().__init__()
        self.caminho_arquivo = caminho_arquivo
        self.progresso = 0

    def run(self):
        # Simula o processamento e atualiza o progresso
        dados_processados = src.backend.processar_dados_excel(self.caminho_arquivo)

        if dados_processados:
            # Simula o salvamento dos dados com progresso
            nome_arquivo_saida, _ = QFileDialog.getSaveFileName(None, "Salvar Arquivo Excel", "",
                                                                "Arquivos Excel (*.xlsx)",
                                                                options=QFileDialog.Options())
            if nome_arquivo_saida:
                src.backend.salvar_excel(dados_processados, nome_arquivo_saida)

                # Atualize o progresso enquanto processa
                for i in range(0, 101, 5):
                    self.progresso = i
                    self.progresso_atualizado.emit(self.progresso)
                    QThread.msleep(350)  # Simula o tempo de processamento
                self.finished.emit()
            else:
                # self.progresso = 0
                pass


'''if __name__ == '__main__':
    # Inicialização da aplicação PyQt
    app = QApplication(sys.argv)

    janela = JanelaPrincipal()
    app.setStyleSheet(janela.estilo)
    janela.show()
    sys.exit(app.exec_())'''

'''if __name__ == '__main__':
    # Inicialização da aplicação PyQt
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())'''