#Muhammad Tegar Bijanta
#F1D02410081
#KELAS D

import sys
import os
from PySide6.QtWidgets import(
   	QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QSplitter, QHeaderView, QMessageBox, QDialog, QTextEdit
)
from PySide6.QtCore import Qt, QThread
from API_WORKER.api_worker import APIWorker
from Dialog.dialog import PostDialog

class PostManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Post Manager")
        self.setGeometry(100, 100, 900, 600)
        self.posts_data = []
        self._thread = None
        self._worker = None
        self.setup_ui()
        self.fetch_posts()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        head = QHBoxLayout()
        
        self.header = QLabel("Post Manager")
        self.header.setStyleSheet("font-weight: bold; padding: 4px;")
        head.addWidget(self.header)
        
        self.btn_tambah = QPushButton("+ Tambah Post")
        head.addStretch() 
        head.addWidget(self.btn_tambah)
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.setObjectName("btn_refresh")
        head.addWidget(self.btn_refresh)
        
        layout.addLayout(head)
        
        data_bawah = QHBoxLayout()
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-weight: bold; padding: 4px;")
        
        layout_table = QVBoxLayout()
        layout_btn = QHBoxLayout()
        layout_btn.addWidget(self.status_label)
        self.btn_edit = QPushButton("Edit")
        self.btn_hapus = QPushButton("Hapus")
        self.btn_edit.setObjectName("btn_edit")
        self.btn_hapus.setObjectName("btn_hapus")
        layout_btn.addWidget(self.btn_edit)
        layout_btn.addWidget(self.btn_hapus)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Title', 'Body', 'Author', 'Slug', 'Status'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 40)
        
        layout_table.addLayout(layout_btn)
        layout_table.addWidget(self.table)
        data_bawah.addLayout(layout_table)
        
        splitter = QSplitter(Qt.Horizontal)
        
        self.detail = QTextEdit()
        self.detail.setReadOnly(True)
        splitter.addWidget(self.detail)
        splitter.setSizes([400, 500])
        data_bawah.addWidget(splitter)
        
        layout.addLayout(data_bawah)
        
        self.btn_refresh.clicked.connect(self.fetch_posts)
        self.btn_tambah.clicked.connect(self.add_post)
        self.btn_edit.clicked.connect(self.edit_post)
        self.btn_hapus.clicked.connect(self.delete_post)
        self.table.currentCellChanged.connect(self.on_row_selected)
      
    def run_worker(self, action, on_success, id=None, title=None, body=None, author=None, slug=None, status=None):
        self._thread = QThread()
        self._worker = APIWorker(action, id=id, title=title, body=body, author=author, slug=slug, status=status)
        self._worker.moveToThread(self._thread)
        
        self._thread.started.connect(self._worker.run)
        self._worker.success.connect(on_success)
        self._worker.error.connect(self.on_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(lambda: self.set_loading(False))
        self.set_loading(True)
        self._thread.start()
        
    def fetch_posts(self):
        self.run_worker("get_posts", self.on_posts_loaded)
     
    def set_loading(self, is_loading):
        """Aktifkan/nonaktifkan tombol saat request berjalan."""
        for btn in [self.btn_refresh, self.btn_tambah, self.btn_edit, self.btn_hapus]:
            btn.setEnabled(not is_loading)
        if is_loading:
            self.status_label.setText("Loading...")
            self.status_label.setStyleSheet("font-weight:bold; color:#3498db; padding:4px;")
            
    def add_post(self):
        dialog = PostDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['title'] or not data['body'] or not data['author'] or not data['slug']:
                QMessageBox.warning(self, "Validasi", "Semua input wajib diisi")
                return
            self.run_worker(
				"create_post", self.on_post_created,
				title=data['title'], body=data['body'], author=data['author'], slug=data['slug'], status=data['status']
			)
    
    def on_post_created(self, result):
        QMessageBox.information(self, "Sukses", f"Post ditambahkan! ID: {result['data']['id']}")
        self.fetch_posts()
        
    def on_posts_loaded(self, posts):
        self.posts_data = posts
        self.table.setRowCount(0)
        
        for p in self.posts_data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(p['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(p['title']))
            self.table.setItem(row, 2, QTableWidgetItem(p['body']))
            self.table.setItem(row, 3, QTableWidgetItem(p['author']))
            self.table.setItem(row, 4, QTableWidgetItem(p['slug']))
            self.table.setItem(row, 5, QTableWidgetItem(p['status']))
            
        self.status_label.setText(f"{len(posts)} post dimuat")
        self.status_label.setStyleSheet("font-weight:bold; color:#27ae60; padding:4px;")
    
    def on_row_selected(self, row):
        if row < 0 or row >= len(self.posts_data):
            return
        p = self.posts_data[row]
        self.detail.setPlainText(
			f"ID	: {p['id']}\n"
			f"Title	: {p['title']}\n"
			f"Body	: {p['body']}\n"
			f"Author	: {p['author']}\n"
			f"Slug	: {p['slug']}\n"
			f"Status	: {p['status']}\n"
		)
        
    def edit_post(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih post terlebih dahulu! ")
            return
        post = self.posts_data[row]
        dialog = PostDialog(self, post)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            self.run_worker(
				"update_post", self.on_post_updated,
				id=post['id'], title=data['title'], body=data['body'], author=data['author'], slug=data['slug'], status=data['status']
			)
            
    def on_post_updated(self, result):
        QMessageBox.information(self, "Sukses", f"Post diupdate! ID: {result['data']['id']}")
        self.fetch_posts()
        
    def delete_post(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih post terlebih dahulu!")
            return
        post_id = self.posts_data[row]['id']
        reply = QMessageBox.question(
            self,"Konfirmasi",
            f"Yakin ingin menghapus post ID {post_id}?",
            QMessageBox.Yes | QMessageBox.No
		)
        if reply == QMessageBox.Yes:
            self.run_worker("delete_post", self.on_post_deleted, id=post_id)
        
    def on_post_deleted(self, result):
        QMessageBox.information(self, "Sukses", f"Post berhasil dihapus! ID :{result['data']['id']}")
        self.fetch_posts()

    def on_error(self, message):
        self.status_label.setText(f"Error: {message}")
        self.status_label.setStyleSheet("font-weight:bold; color:#e74c3c; padding:4px;")
        if "422" in message:
            QMessageBox.warning(self, "Slug Duplikat", "Slug sudah digunakan, gunakan slug lain.")
        else:
        	QMessageBox.critical(self, "API Error", message)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PostManager()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(base_dir, "style", "style_post.qss")

    with open(qss_path, "r") as f:
        app.setStyleSheet(f.read())
    window.show()
    sys.exit(app.exec())
