from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox,
    QLabel, QLineEdit, QTextEdit, QComboBox
)

class PostDialog(QDialog):
    
    def __init__(self, parent=None, post=None):
        super().__init__(parent)
        
        self.setWindowTitle("Edit Post" if post else "Tambah Post")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        # Input fields
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Masukkan title post...")
        
        self.body_input = QLineEdit()
        self.body_input.setPlaceholderText("Masukkan body post...")
        
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Masukkan author post...")
        
        self.slug_input = QLineEdit()
        self.slug_input.setPlaceholderText("Masukkan slug post...")
        
        self.status_input = QComboBox()
        self.status_input.setPlaceholderText("--Masukkan status post--")
        self.status_input.addItems([
			"published", "draft"
		])
        
        form.addRow("Title:", self.title_input)
        form.addRow("Body:", self.body_input)
        form.addRow("Author:", self.author_input)
        form.addRow("Slug:", self.slug_input)
        form.addRow("Status:", self.status_input)
        layout.addLayout(form)
        
        # Tombol OK dan Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        if post:
            self.title_input.setText(post.get('title', ''))
            self.body_input.setText(post.get('body', ''))
            self.author_input.setText(post.get('author', ''))
            self.slug_input.setText(post.get('slug', ''))
            self.status_input.setCurrentText(post.get('status', ''))
    
    def get_data(self):
        """Ambil data dari form sebagai dict siap kirim ke API."""
        return {
            'title': self.title_input.text().strip(),
            'body': self.body_input.text().strip(),
            'author': self.author_input.text().strip(),
            'slug': self.slug_input.text().strip(),
            'status': self.status_input.currentText()
        }