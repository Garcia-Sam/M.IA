import sys
import os
from PyQt5.QtWidgets import QApplication
from UI.Interface import JanelaPrincipal

script_dir = os.path.dirname(os.path.realpath(__file__))
print(script_dir)

if __name__ == '__main__':
    # Inicialização da aplicação PyQt
    app = QApplication(sys.argv)

    janela = JanelaPrincipal()
    app.setStyleSheet(janela.estilo)
    janela.show()
    sys.exit(app.exec_())
