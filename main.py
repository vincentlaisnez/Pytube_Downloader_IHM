from PySide6 import QtCore
from PySide6.QtCore import QObject, QThread
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QLineEdit, QPushButton, QProgressBar, \
    QVBoxLayout, QProgressDialog, QMessageBox

from sounds_download import directory_change, download


class Worker(QObject):
    url_downloaded = QtCore.Signal(object, bool)
    finished = QtCore.Signal()

    def __init__(self, url_to_download):
        super().__init__()
        self.url_to_download = url_to_download
        self.finish = False

    def url_download(self):
        for url in self.url_to_download:
            success = download(item=url)
            self.url_downloaded.emit(url, success)

        self.finished.emit()
        self.finish = True


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pytube Downloader")
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.lbl_list_urls = QLabel("Liste des URLS YT:")
        self.lw_urls = QListWidget()
        self.lbl_url = QLabel("URL YT:")
        self.le_url = QLineEdit()
        self.pg_bar = QProgressBar(maximum=100)
        self.bn_dl = QPushButton("Télécharger")

    def create_layouts(self):
        self.main_layout = QVBoxLayout(self)

    def modify_widgets(self):
        self.pg_bar.setVisible(False)
        self.le_url.setPlaceholderText("Ajouter/coller un lien YT puis touche 'entrée' pour valider")

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lbl_list_urls)
        self.main_layout.addWidget(self.lw_urls)
        self.main_layout.addWidget(self.lbl_url)
        self.main_layout.addWidget(self.le_url)
        self.main_layout.addWidget(self.pg_bar)
        self.main_layout.addWidget(self.bn_dl)

    def setup_connections(self):
        QShortcut(QKeySequence("Delete"), self.lw_urls, self.delete_selected_items)
        self.le_url.returnPressed.connect(self.add_url_to_list)
        self.bn_dl.clicked.connect(self.lunch_download)

    def lunch_download(self):
        directory_change()
        self.items = [self.lw_urls.item(i).text() for i in range(self.lw_urls.count())]
        if not self.items:
            return
        self.thread = QThread()
        self.worker = Worker(self.items)
        self.worker.moveToThread(self.thread)
        self.worker.url_downloaded.connect(self.url_to_download)
        self.thread.started.connect(self.worker.url_download)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()

        self.prg_dialog = QProgressDialog("téléchargement en cours... ", "Annuler", 1, len(self.items))
        self.prg_dialog.canceled.connect(self.abort)
        self.prg_dialog.show()

    def abort(self):
        self.thread.quit()

    def add_url_to_list(self):
        if self.le_url.text().startswith("https://www.youtube.com/") or self.le_url.text().startswith("https://youtu.be/"):
            self.lw_urls.addItem(self.le_url.text())
        self.le_url.clear()

    def url_to_download(self):
        self.prg_dialog.setValue(self.prg_dialog.value() + 1)
        if len(self.items) == 1:
            self.prg_dialog.destroy()

        if self.worker.finish:
            self.lw_urls.clear()
            msg_box = QMessageBox()
            msg_box.setText("Musique(s) téléchargée(s)")
            msg_box.exec()

    def delete_selected_items(self):
        for lw_item in self.lw_urls.selectedItems():
            row = self.lw_urls.row(lw_item)
            self.lw_urls.takeItem(row)


if __name__ == '__main__':
    app = QApplication()
    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.show()
    app.exec()
