import sys
import pymorphy2

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from expression_means_list import EXPRESSION_MEANS

MORPH = pymorphy2.MorphAnalyzer()
ABC = 'йцукенгшщзхъфывапролджэячсмитьбюё \n'


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('linguistic analysis.ui', self)

        self.stack.setCurrentIndex(0)  # установка первой страницы

        # подключение функций
        self.starting.clicked.connect(self.starting_func)
        self.to_analysis.clicked.connect(self.to_analysis_func)
        self.to_guide.clicked.connect(self.to_guide_func)
        self.back_from_analysis.clicked.connect(self.go_back)
        self.back_from_guide.clicked.connect(self.go_back)
        self.exp_means_list.itemClicked.connect(self.guide_item_func)
        self.submit_button.clicked.connect(self.submit_text)
        self.back_from_gr.clicked.connect(self.to_analysis_func)
        self.back_from_ar.clicked.connect(self.back_from_ar_func)
        self.load_file.clicked.connect(self.load_file_func)

    def starting_func(self):
        self.stack.setCurrentIndex(1)

    def to_analysis_func(self):
        self.stack.setCurrentIndex(3)

    def to_guide_func(self):
        self.stack.setCurrentIndex(2)

    def go_back(self):
        self.stack.setCurrentIndex(1)

    def guide_item_func(self):
        self.stack.setCurrentIndex(4)
        self.means_name_output.setText(self.exp_means_list.currentItem().text())
        self.means_output.setText(EXPRESSION_MEANS[self.exp_means_list.currentItem().text()])
        self.means_name_output.setAlignment(QtCore.Qt.AlignCenter)
        self.means_output.setAlignment(QtCore.Qt.AlignCenter)

    def nouns_analysis(self, text):
        words = list(map(lambda x: MORPH.parse(x)[0].normal_form, text))
        nouns = list(set([i for i in words if 'NOUN' in MORPH.parse(i)[0].tag]))
        nouns = sorted(nouns, key=lambda x: words.count(x), reverse=True)
        self.func_out_name.setText('Частотный список существительных в тексте:')
        self.func_out_name.setAlignment(QtCore.Qt.AlignCenter)
        for i in nouns:
            item = QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            item.setFont(QFont('Comic Sans MS', 9))
            self.analysis_output.addItem(item)

    def verbs_analysis(self, text):
        words = list(map(lambda x: MORPH.parse(x)[0].normal_form, text))
        verbs = list(set([i for i in words if 'INFN' in MORPH.parse(i)[0].tag]))
        verbs = sorted(verbs, key=lambda x: words.count(x), reverse=True)
        self.func_out_name.setText('Частотный список глаголов в тексте:')
        self.func_out_name.setAlignment(QtCore.Qt.AlignCenter)
        for i in verbs:
            item = QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            item.setFont(QFont('Comic Sans MS', 9))
            self.analysis_output.addItem(item)

    def adj_analysis(self, text):
        words = list(map(lambda x: MORPH.parse(x)[0].normal_form, text))
        adj = list(set([i for i in words if 'ADJF' in MORPH.parse(i)[0].tag]))
        adj = list(filter(lambda x: 'Apro' not in MORPH.parse(x)[0].tag, adj))
        adj = sorted(adj, key=lambda x: words.count(x), reverse=True)
        self.func_out_name.setText('Частотный список прилагательных в тексте:')
        self.func_out_name.setAlignment(QtCore.Qt.AlignCenter)
        for i in adj:
            item = QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            item.setFont(QFont('Comic Sans MS', 9))
            self.analysis_output.addItem(item)

    def name_analysis(self, text):
        words = list(map(lambda x: MORPH.parse(x)[0].normal_form, text))
        nouns = list(set([i for i in words if 'NOUN' in MORPH.parse(i)[0].tag]))
        names = list(filter(lambda x: 'Name' in MORPH.parse(x)[0].tag, nouns))
        self.func_out_name.setText('Список имён в тексте:')
        self.func_out_name.setAlignment(QtCore.Qt.AlignCenter)
        for i in names:
            item = QListWidgetItem(i)
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            item.setFont(QFont('Comic Sans MS', 9))
            self.analysis_output.addItem(item)

    def func_choice_func(self):
        if self.func_choice.currentText() == 'Выдать частотный список существительных':
            self.chosen_func = self.nouns_analysis
        elif self.func_choice.currentText() == 'Выдать частотный список глаголов':
            self.chosen_func = self.verbs_analysis
        elif self.func_choice.currentText() == 'Выдать частотный список прилагательных':
            self.chosen_func = self.adj_analysis
        elif self.func_choice.currentText() == 'Выдать список имён':
            self.chosen_func = self.name_analysis

    def load_file_func(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать файл с текстом', '')[0]
            f = open(fname, 'r', encoding='utf8')
            text = f.read().lower().replace('-', ' ')
            text = ''.join([i for i in text if i in ABC]).split()
            print(text)
            self.stack.setCurrentIndex(5)
            self.func_choice_func()
            self.chosen_func(text)
        except FileNotFoundError as ex:
            self.statusBar().showMessage('Вам нужно выбрать файл для анализа')

    def submit_text(self):
        self.stack.setCurrentIndex(5)
        text = self.text_input.toPlainText().lower().replace('-', ' ')
        text = ''.join([i for i in text if i in ABC]).split()
        self.func_choice_func()
        self.chosen_func(text)

    def back_from_ar_func(self):
        self.stack.setCurrentIndex(2)
        self.text_input.clear()


def main():
    app = QApplication(sys.argv)
    project = MainWindow()
    project.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
