# library_system_simple.py
"""
Classes
-------
Book           – catalogue entry tracking copies.
LibraryMember  – base class storing borrow logic.
StudentMember  – student with limit 3.
TeacherMember  – teacher with limit 5.
Library        – façade exposing high‑level operations.
"""

# 1.Domain entities

class Book:
    """Represents a book and how many copies are available."""

    def __init__(self, isbn, title, author, copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies # owned by the library
        self._available = copies # copies not on loan

    def checkout(self):
        """Decrease available count when this book is borrowed."""
        if self._available == 0:
            return False # no copies left
        self._available -= 1
        return True

    def checkin(self):
        """Increase available count when this book is returned."""
        if self._available < self.total_copies:
            self._available += 1

    def available(self):
        """How many copies can still be borrowed."""
        return self._available

    def __repr__(self):
        return f"<Book {self.title!r} ({self._available}/{self.total_copies})>"


# 2.Library members

class LibraryMember:
    """Base class: handles borrowing logic; limit passed via ctor."""

    def __init__(self, member_id, name, limit):
        self.member_id = member_id
        self.name = name
        self._limit = limit # maximum concurrent loans
        self._borrowed = set() # ISBNs currently on loan

    # public interface
    def borrow(self, book):
        """Try to borrow *book*; returns True/False."""
        if len(self._borrowed) >= self._limit:
            return False # reached personal cap
        if not book.checkout():
            return False # no physical copy available
        self._borrowed.add(book.isbn)
        return True

    def return_book(self, book):
        """Return *book* if it was actually borrowed by this member."""
        if book.isbn not in self._borrowed:
            return False # nothing to return
        book.checkin()
        self._borrowed.remove(book.isbn)
        return True

    # helper
    def current_loans(self):
        """Return a set of ISBNs currently on loan."""
        return self._borrowed


class StudentMember(LibraryMember):
    """Students may borrow **up to 3** books."""
    def __init__(self, member_id, name):
        super().__init__(member_id, name, limit=3)


class TeacherMember(LibraryMember):
    """Teachers may borrow **up to 5** books."""
    def __init__(self, member_id, name):
        super().__init__(member_id, name, limit=5)



# 3.Library facade

class Library:

    def __init__(self):
        self.books = {}    # isbn -> Book
        self.members = {}  # member_id -> LibraryMember

    # catalogue management
    def add_book(self, book):
        self.books[book.isbn] = book

    def add_member(self, member):
        self.members[member.member_id] = member

    # loan operations
    def borrow(self, member_id, isbn):
        member = self.members.get(member_id)
        book = self.books.get(isbn)
        if not member or not book:
            return "Member or book not found"
        return "Loan OK" if member.borrow(book) else "Loan denied"

    def return_book(self, member_id, isbn):
        member = self.members.get(member_id)
        book = self.books.get(isbn)
        if not member or not book:
            return "Member or book not found"
        return "Return OK" if member.return_book(book) else "Return denied"



# 4.Minimal demo

if __name__ == "__main__":
    lib = Library()

    # 1) populate catalogue
    lib.add_book(Book("9780132350884", "Clean Code", "Robert C. Martin", 2))

    # 2) register members
    lib.add_member(StudentMember("S01", "Misha"))
    lib.add_member(TeacherMember("T01", "Pidor"))

    # 3) borrowing cycle
    print(lib.borrow("S01", "9780132350884"))  # Loan OK
    print(lib.borrow("S01", "9780132350884"))  # Loan OK
    print(lib.borrow("S01", "9780132350884"))  # Loan denied — limit/no copies

    # 4) student returns one copy; teacher tries again
    print(lib.return_book("S01", "9780132350884"))  # Return OK
    print(lib.borrow("T01", "9780132350884")) # Loan OK