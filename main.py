import sys
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QGroupBox,
    QMessageBox, QTabWidget, QDateEdit, QSpinBox, QProgressBar, QFrame,
    QAbstractItemView
)
from library_data import LibraryData

STYLE = """
QMainWindow, QWidget { background:#f4f7fb; color:#233044; font-family:"Segoe UI"; font-size:10pt; }
QLabel#title { color:#17365d; font-size:22pt; font-weight:700; }
QLabel#sub { color:#66758a; }
QGroupBox { background:white; border:1px solid #dce4ef; border-radius:9px; margin-top:12px; padding:12px; font-weight:600; }
QGroupBox::title { subcontrol-origin:margin; left:12px; padding:0 5px; }
QLineEdit,QComboBox,QDateEdit,QSpinBox { background:white; border:1px solid #cbd5e1; border-radius:6px; padding:7px; min-height:20px; }
QLineEdit:focus,QComboBox:focus,QDateEdit:focus,QSpinBox:focus { border:1px solid #3976c6; }
QPushButton { background:#e5edf8; color:#17365d; border:0; border-radius:6px; padding:9px 14px; font-weight:600; }
QPushButton:hover { background:#d4e2f4; }
QPushButton#primary { background:#2463a6; color:white; }
QPushButton#danger { background:#fce8e8; color:#a52b2b; }
QTableWidget { background:white; alternate-background-color:#f7f9fc; border:1px solid #dce4ef; gridline-color:#edf1f6; selection-background-color:#dceafe; selection-color:#17365d; }
QHeaderView::section { background:#eaf0f8; color:#294563; padding:9px; border:0; font-weight:700; }
QTabBar::tab { background:#e5edf8; padding:10px 18px; margin-right:3px; }
QTabBar::tab:selected { background:#2463a6; color:white; }
QProgressBar { border:1px solid #dce4ef; border-radius:5px; background:white; text-align:center; min-height:16px; }
QProgressBar::chunk { background:#3b82c4; border-radius:4px; }
"""

CATEGORIES = ["Technology", "Education", "Literature", "Science", "History", "Arts", "Other"]


class LibraryWindow(QMainWindow):
    """UI layer: creates widgets and connects events to LibraryData."""

    def __init__(self):
        super().__init__()
        self.data = LibraryData()
        self.setWindowTitle("Library Management System | Book Issue & Return")
        self.resize(1120, 760)
        self.setMinimumSize(850, 600)
        self.make_menu()
        self.make_ui()
        self.refresh_all()

    def make_menu(self):
        file_menu = self.menuBar().addMenu("&File")
        refresh_action = QAction("Refresh records", self)
        refresh_action.triggered.connect(self.refresh_all)
        file_menu.addAction(refresh_action)
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def stat_card(self, caption):
        card = QFrame()
        card.setStyleSheet("QFrame{background:white;border:1px solid #dce4ef;border-radius:8px;}")
        box = QVBoxLayout(card)
        value = QLabel("0")
        value.setStyleSheet("font-size:20pt;font-weight:700;color:#2463a6;border:0;")
        label = QLabel(caption)
        label.setStyleSheet("color:#66758a;border:0;")
        box.addWidget(value)
        box.addWidget(label)
        card.value_label = value
        return card

    def make_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(12)

        heading = QHBoxLayout()
        titles = QVBoxLayout()
        title = QLabel("Library Management System")
        title.setObjectName("title")
        sub = QLabel("Manage books, student borrowing and returns")
        sub.setObjectName("sub")
        titles.addWidget(title)
        titles.addWidget(sub)
        heading.addLayout(titles)
        heading.addStretch()
        self.saved_label = QLabel("● Data saved locally")
        self.saved_label.setStyleSheet("color:#26835b;font-weight:600;")
        heading.addWidget(self.saved_label)
        root.addLayout(heading)

        stats = QHBoxLayout()
        self.card_titles = self.stat_card("Book titles")
        self.card_available = self.stat_card("Available copies")
        self.card_borrowed = self.stat_card("Books on loan")
        for card in (self.card_titles, self.card_available, self.card_borrowed):
            stats.addWidget(card)
        root.addLayout(stats)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.books_page(), "Books")
        self.tabs.addTab(self.issue_page(), "Issue Book")
        self.tabs.addTab(self.returns_page(), "Returns")
        root.addWidget(self.tabs, 1)
        note = QLabel("Records are stored automatically in library_data.json beside this program.")
        note.setObjectName("sub")
        root.addWidget(note)

    def books_page(self):
        page = QWidget()
        outer = QVBoxLayout(page)

        group = QGroupBox("Add a new book")
        grid = QGridLayout(group)
        self.book_id = QLineEdit()
        self.book_id.setPlaceholderText("e.g. B004")
        self.book_title = QLineEdit()
        self.book_title.setPlaceholderText("Book title")
        self.author = QLineEdit()
        self.author.setPlaceholderText("Author name")
        self.category = QComboBox()
        self.category.addItems(CATEGORIES)
        self.copies = QSpinBox()
        self.copies.setRange(1, 500)
        self.copies.setValue(1)
        grid.addWidget(QLabel("Book ID *"), 0, 0)
        grid.addWidget(self.book_id, 0, 1)
        grid.addWidget(QLabel("Title *"), 0, 2)
        grid.addWidget(self.book_title, 0, 3)
        grid.addWidget(QLabel("Author *"), 1, 0)
        grid.addWidget(self.author, 1, 1)
        grid.addWidget(QLabel("Category"), 1, 2)
        grid.addWidget(self.category, 1, 3)
        grid.addWidget(QLabel("Total copies"), 2, 0)
        grid.addWidget(self.copies, 2, 1)
        add = QPushButton("+ Add Book")
        add.setObjectName("primary")
        add.clicked.connect(self.add_book)
        grid.addWidget(add, 2, 3)
        outer.addWidget(group)

        search_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search by ID, title, author or category...")
        self.search.textChanged.connect(self.refresh_books)
        self.available_check = QCheckBox("Available books only")
        self.available_check.stateChanged.connect(self.refresh_books)
        search_row.addWidget(QLabel("Search:"))
        search_row.addWidget(self.search, 1)
        search_row.addWidget(self.available_check)
        outer.addLayout(search_row)

        self.books_table = QTableWidget(0, 6)
        self.books_table.setHorizontalHeaderLabels(["Book ID", "Title", "Author", "Category", "Total", "Available"])
        self.setup_table(self.books_table)
        outer.addWidget(self.books_table, 1)

        bottom = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setFormat("Available inventory: %p%")
        delete = QPushButton("Delete Selected Book")
        delete.setObjectName("danger")
        delete.clicked.connect(self.delete_book)
        bottom.addWidget(self.progress, 1)
        bottom.addWidget(delete)
        outer.addLayout(bottom)
        return page

    def issue_page(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        group = QGroupBox("Issue a book to a student")
        form = QFormLayout(group)
        self.issue_combo = QComboBox()
        self.student_id = QLineEdit()
        self.student_id.setPlaceholderText("e.g. STU001")
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student full name")
        self.due_date = QDateEdit()
        self.due_date.setCalendarPopup(True)
        self.due_date.setDate(QDate.currentDate().addDays(14))
        self.due_date.setMinimumDate(QDate.currentDate())
        form.addRow("Select book *", self.issue_combo)
        form.addRow("Student ID *", self.student_id)
        form.addRow("Student name *", self.student_name)
        form.addRow("Due date *", self.due_date)
        issue = QPushButton("Issue Book")
        issue.setObjectName("primary")
        issue.clicked.connect(self.issue_book)
        form.addRow(issue)
        outer.addWidget(group)
        info = QLabel("The issue date is recorded automatically. Only books with available copies are listed.")
        info.setObjectName("sub")
        outer.addWidget(info)
        outer.addStretch()
        return page

    def returns_page(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        info = QLabel("Select an active borrowing record and confirm the return.")
        info.setObjectName("sub")
        outer.addWidget(info)
        self.loans_table = QTableWidget(0, 6)
        self.loans_table.setHorizontalHeaderLabels(["Loan ID", "Book ID", "Book title", "Student ID", "Student name", "Due date"])
        self.setup_table(self.loans_table)
        outer.addWidget(self.loans_table, 1)
        row = QHBoxLayout()
        row.addStretch()
        returned = QPushButton("Mark Selected as Returned")
        returned.setObjectName("primary")
        returned.clicked.connect(self.return_book)
        row.addWidget(returned)
        outer.addLayout(row)
        return page

    @staticmethod
    def setup_table(table):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def add_book(self):
        book_id = self.book_id.text().strip().upper()
        title = self.book_title.text().strip()
        author = self.author.text().strip()
        if not book_id or not title or not author:
            self.error("Please complete the Book ID, Title and Author fields.")
            return
        if any(ch.isspace() for ch in book_id):
            self.error("Book ID must not contain spaces.")
            return
        try:
            self.data.add_book({"book_id": book_id, "title": title, "author": author,
                                "category": self.category.currentText(), "total": self.copies.value()})
        except (ValueError, OSError) as exc:
            self.error(str(exc))
            return
        self.book_id.clear()
        self.book_title.clear()
        self.author.clear()
        self.copies.setValue(1)
        self.refresh_all()
        QMessageBox.information(self, "Book added", f'"{title}" was added successfully.')

    def issue_book(self):
        book_id = self.issue_combo.currentData()
        sid = self.student_id.text().strip().upper()
        name = self.student_name.text().strip()
        due = self.due_date.date().toString("yyyy-MM-dd")
        if not book_id:
            self.error("There are no available books to issue.")
            return
        if not sid or not name:
            self.error("Please enter both Student ID and Student name.")
            return
        if any(ch.isspace() for ch in sid):
            self.error("Student ID must not contain spaces.")
            return
        try:
            self.data.issue_book(book_id, sid, name, due)
        except (ValueError, OSError) as exc:
            self.error(str(exc))
            return
        self.student_id.clear()
        self.student_name.clear()
        self.refresh_all()
        QMessageBox.information(self, "Book issued", f"{book_id} was issued to {name}.")

    def return_book(self):
        row = self.loans_table.currentRow()
        if row < 0:
            self.error("Please select a borrowing record first.")
            return
        loan_id = self.loans_table.item(row, 0).text()
        answer = QMessageBox.question(self, "Confirm return", f"Mark loan {loan_id} as returned?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            self.data.return_loan(loan_id)
        except (ValueError, OSError) as exc:
            self.error(str(exc))
            return
        self.refresh_all()
        QMessageBox.information(self, "Return recorded", "The book has been returned successfully.")

    def delete_book(self):
        row = self.books_table.currentRow()
        if row < 0:
            self.error("Select a book from the table first.")
            return
        book_id = self.books_table.item(row, 0).text()
        answer = QMessageBox.question(self, "Confirm deletion", f"Delete book {book_id}?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            self.data.delete_book(book_id)
        except (ValueError, OSError) as exc:
            self.error(str(exc))
            return
        self.refresh_all()

    def refresh_all(self):
        self.refresh_books()
        self.refresh_issue_combo()
        self.refresh_loans()
        self.update_stats()

    def refresh_books(self, *_):
        if not hasattr(self, "books_table"):
            return
        query = self.search.text().strip().casefold()
        only_available = self.available_check.isChecked()
        rows = []
        for book in self.data.books:
            available = self.data.available_copies(book["book_id"])
            searchable = " ".join(str(book.get(k, "")) for k in ("book_id", "title", "author", "category")).casefold()
            if query and query not in searchable:
                continue
            if only_available and available == 0:
                continue
            rows.append((book, available))
        self.books_table.setRowCount(len(rows))
        for r, (book, available) in enumerate(rows):
            values = [book["book_id"], book["title"], book["author"], book["category"], str(book["total"]), str(available)]
            for c, value in enumerate(values):
                item = QTableWidgetItem(value)
                if c >= 4:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.books_table.setItem(r, c, item)
        total = sum(int(b["total"]) for b in self.data.books)
        available_total = sum(self.data.available_copies(b["book_id"]) for b in self.data.books)
        self.progress.setMaximum(max(total, 1))
        self.progress.setValue(available_total)

    def refresh_issue_combo(self):
        self.issue_combo.clear()
        for book in self.data.books:
            count = self.data.available_copies(book["book_id"])
            if count:
                self.issue_combo.addItem(f'{book["book_id"]} — {book["title"]} ({count} available)', book["book_id"])

    def refresh_loans(self):
        active = self.data.active_loans()
        self.loans_table.setRowCount(len(active))
        for r, loan in enumerate(active):
            book = self.data.find_book(loan["book_id"])
            values = [loan["loan_id"], loan["book_id"], book["title"] if book else "(missing book)",
                      loan["student_id"], loan["student_name"], loan["due_date"]]
            for c, value in enumerate(values):
                self.loans_table.setItem(r, c, QTableWidgetItem(str(value)))

    def update_stats(self):
        total_titles = len(self.data.books)
        total = sum(int(b["total"]) for b in self.data.books)
        available = sum(self.data.available_copies(b["book_id"]) for b in self.data.books)
        borrowed = len(self.data.active_loans())
        self.card_titles.value_label.setText(str(total_titles))
        self.card_available.value_label.setText(f"{available} / {total}")
        self.card_borrowed.value_label.setText(str(borrowed))

    def error(self, message):
        QMessageBox.warning(self, "Please check", message)

    def show_about(self):
        QMessageBox.about(self, "About", "Library Management System\nBuilt with Python and PyQt6.\nBook inventory, issue, return, search and JSON storage.")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)
    window = LibraryWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
