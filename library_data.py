import json
from pathlib import Path
from datetime import date

DATA_FILE = Path(__file__).with_name("library_data.json")


class LibraryData:
    """Data/logic layer. Saves books and loans in a JSON file."""

    def __init__(self, path=DATA_FILE):
        self.path = Path(path)
        self.books = []
        self.loans = []
        self.load()

    def load(self):
        if not self.path.exists():
            self.books = [
                {"book_id": "B001", "title": "Python Programming", "author": "John Smith", "category": "Technology", "total": 5},
                {"book_id": "B002", "title": "Introduction to ICT", "author": "Mary Jones", "category": "Education", "total": 3},
                {"book_id": "B003", "title": "The Secret Garden", "author": "Frances Burnett", "category": "Literature", "total": 4},
            ]
            self.loans = []
            self.save()
            return
        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = data.get("books", [])
            self.loans = data.get("loans", [])
        except (OSError, json.JSONDecodeError):
            self.books, self.loans = [], []

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump({"books": self.books, "loans": self.loans}, f, indent=4)

    def find_book(self, book_id):
        return next((b for b in self.books if b["book_id"].casefold() == book_id.casefold()), None)

    def active_loans(self):
        return [loan for loan in self.loans if not loan.get("returned", False)]

    def available_copies(self, book_id):
        book = self.find_book(book_id)
        if not book:
            return 0
        borrowed = sum(1 for loan in self.active_loans() if loan["book_id"].casefold() == book_id.casefold())
        return max(0, int(book["total"]) - borrowed)

    def add_book(self, book):
        if self.find_book(book["book_id"]):
            raise ValueError("A book with this Book ID already exists.")
        self.books.append(book)
        self.save()

    def issue_book(self, book_id, student_id, student_name, due_date):
        if not self.find_book(book_id):
            raise ValueError("The selected Book ID does not exist.")
        if self.available_copies(book_id) < 1:
            raise ValueError("No copies of this book are available.")
        self.loans.append({
            "loan_id": f"L{len(self.loans) + 1:04d}",
            "book_id": book_id,
            "student_id": student_id,
            "student_name": student_name,
            "issue_date": date.today().isoformat(),
            "due_date": due_date,
            "returned": False,
            "return_date": ""
        })
        self.save()

    def return_loan(self, loan_id):
        loan = next((x for x in self.active_loans() if x["loan_id"] == loan_id), None)
        if not loan:
            raise ValueError("This borrowing record is not active.")
        loan["returned"] = True
        loan["return_date"] = date.today().isoformat()
        self.save()

    def delete_book(self, book_id):
        if any(x["book_id"].casefold() == book_id.casefold() for x in self.active_loans()):
            raise ValueError("This book has an active borrowing record and cannot be deleted.")
        self.books = [b for b in self.books if b["book_id"].casefold() != book_id.casefold()]
        self.save()
