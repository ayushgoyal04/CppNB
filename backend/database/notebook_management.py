

# ---------------------------
# 🗄 Repository (data access layer)
# ---------------------------

class NotebookRepo:
    _lock = threading.Lock()
    _current: Optional[Notebook] = None

    @classmethod
    def get(cls) -> Optional[Notebook]:
        with cls._lock:
            return cls._current

    @classmethod
    def set(cls, notebook: Notebook) -> None:
        with cls._lock:
            cls._current = notebook
