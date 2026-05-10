from PySide6.QtCore import QObject, Signal
from API.api_service import APIservice

class APIWorker(QObject):

    # Signal untuk komunikasi balik ke Main Thread
    finished = Signal()           # selalu dipanggil di akhir (sukses maupun gagal)
    success = Signal(object)      # kirim data hasil (list/dict/bool)
    error = Signal(str)          # kirim pesan error
    
    def __init__(self, action, id=None, title=None, body=None, author=None, slug=None, status=None):
        super().__init__()
        self.action = action
        self.id = id
        self.title = title
        self.body = body
        self.author = author
        self.slug = slug
        self.status = status
        self.service = APIservice()
    
    def run(self):
        """Dijalankan oleh QThread. Panggil service sesuai action."""
        try:
            if self.action == "get_posts":
                result = self.service.get_posts()
            
            elif self.action == "create_post":
                result = self.service.create_post(self.title, self.body, self.author, self.slug, self.status)
            
            elif self.action == "update_post":
                result = self.service.update_post(self.id, self.title, self.body, self.author, self.slug, self.status)
            
            elif self.action == "delete_post":
                result = self.service.delete_post(self.id)
            
            else:
                raise ValueError(f"Action tidak dikenali: {self.action}")
            
            self.success.emit(result)  # kirim hasil ke main thread
        
        except Exception as e:
            self.error.emit(str(e))   # kirim pesan error ke main thread
        
        finally:
            self.finished.emit()