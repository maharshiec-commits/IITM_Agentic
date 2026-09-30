"""
============================================================================
 CITY LIBRARY MANAGEMENT SYSTEM  (Graded Mini Project - Part A)
============================================================================

DESIGN NOTES / ASSUMPTIONS (for the "Summary & Presentation" rubric item):

1. Data Structures
   - `books`   : dict keyed by book_id -> {title, author, genre, availability}
                 A dict gives O(1) lookup/update when issuing or returning a
                 book, which is more efficient than scanning a list.
   - `members` : dict keyed by member_id -> {name, age, contact, borrowed_books}
                 `borrowed_books` is a list of book_ids currently held by the
                 member, so a member can hold more than one book at a time.
   - `borrow_log` : a list of dict "transactions". Every borrow AND every
                 return is appended as a new record (never overwritten), so
                 it behaves as a true historical log/audit trail. This is
                 what powers the "most popular genre" and "who has borrowed
                 books" reports.

2. Validation rules implemented
   - A book cannot be issued if it is already "Issued".
   - A book/member ID must exist before it can be used in any operation.
   - A book cannot be added twice with the same Book ID.
   - A member cannot be added twice with the same Member ID.
   - Returning a book only succeeds if that member is actually the one
     currently holding it.

3. Code organisation
   - All logic lives in small, single-purpose, reusable functions (as asked
     for in the brief) rather than one giant script, so each requirement
     maps to one function that can be unit-tested or reused independently.
   - A thin CLI menu (`main_menu`) sits on top and simply calls these
     functions - the "business logic" has no print()/input() calls mixed
     into it except where an operation reports its own result.

4. How to run
   - Run this file directly in a Python console:  `python library_management_system.py`
   - It will first run a short DEMO using sample data (so a grader can see
     every requirement working with zero typing), and then drop into an
     interactive menu for manual testing.
   - Set RUN_DEMO = False below if you only want the interactive menu.
============================================================================
"""

from collections import Counter
from datetime import datetime

RUN_DEMO = True  # set to False to skip the automatic demo and go straight to the menu
AVAILABLE_STATUS = "Available"
ISSUED_STATUS = "Issued"


def normalize_text(value):
    """Return a trimmed string value for consistent IDs and names."""
    if value is None:
        return ""
    return str(value).strip()


def initialize_library():
    """Reset all in-memory data structures for a fresh run."""
    global books, members, borrow_log
    books.clear()
    members.clear()
    borrow_log.clear()


# ============================================================================
# 1. DATA STORES
# ============================================================================
books = {}        # book_id -> {title, author, genre, availability}
members = {}       # member_id -> {name, age, contact, borrowed_books: []}
borrow_log = []    # list of {book_id, member_id, action, timestamp}


# ============================================================================
# 2. BOOK MANAGEMENT
# ============================================================================
def add_book(book_id, title, author, genre):
    """Add a new book to the catalogue. Returns True/False + message."""
    book_id = normalize_text(book_id)
    title = normalize_text(title)
    author = normalize_text(author)
    genre = normalize_text(genre)

    if not all([book_id, title, author, genre]):
        return False, "Book ID, title, author, and genre must not be empty."
    if book_id in books:
        return False, f"Book ID '{book_id}' already exists."

    books[book_id] = {
        "title": title,
        "author": author,
        "genre": genre,
        "availability": AVAILABLE_STATUS,
    }
    return True, f"Book '{title}' added successfully."


def update_book_availability(book_id, status):
    """Internal helper: set a book's availability to 'Available' or 'Issued'."""
    if book_id not in books:
        return False, f"Book ID '{book_id}' not found."
    books[book_id]["availability"] = status
    return True, "Updated."


# ============================================================================
# 3. MEMBER MANAGEMENT
# ============================================================================
def add_member(member_id, name, age, contact):
    """Register a new library member."""
    member_id = normalize_text(member_id)
    name = normalize_text(name)
    contact = normalize_text(contact)

    if not all([member_id, name, contact]):
        return False, "Member ID, name, and contact info must not be empty."
    if member_id in members:
        return False, f"Member ID '{member_id}' already exists."

    members[member_id] = {
        "name": name,
        "age": age,
        "contact": contact,
        "borrowed_books": [],
    }
    return True, f"Member '{name}' registered successfully."


# ============================================================================
# 4. BORROW & RETURN SYSTEM
# ============================================================================
def issue_book(book_id, member_id):
    """Issue a book to a member, with validation."""
    book_id = normalize_text(book_id)
    member_id = normalize_text(member_id)

    if not book_id or not member_id:
        return False, "Book ID and Member ID must not be empty."
    if book_id not in books:
        return False, f"Book ID '{book_id}' does not exist."
    if member_id not in members:
        return False, f"Member ID '{member_id}' does not exist."
    if books[book_id]["availability"] == ISSUED_STATUS:
        return False, f"Book '{books[book_id]['title']}' is already issued to someone else."

    # Update state
    update_book_availability(book_id, ISSUED_STATUS)
    members[member_id]["borrowed_books"].append(book_id)
    borrow_log.append({
        "book_id": book_id,
        "member_id": member_id,
        "action": "Issued",
        "timestamp": datetime.now(),
    })
    return True, f"Book '{books[book_id]['title']}' issued to {members[member_id]['name']}."


def return_book(book_id, member_id):
    """Return a previously issued book, with validation."""
    book_id = normalize_text(book_id)
    member_id = normalize_text(member_id)

    if not book_id or not member_id:
        return False, "Book ID and Member ID must not be empty."
    if book_id not in books:
        return False, f"Book ID '{book_id}' does not exist."
    if member_id not in members:
        return False, f"Member ID '{member_id}' does not exist."
    if book_id not in members[member_id]["borrowed_books"]:
        return False, f"'{members[member_id]['name']}' is not currently holding this book."

    # Update state
    update_book_availability(book_id, AVAILABLE_STATUS)
    members[member_id]["borrowed_books"].remove(book_id)
    borrow_log.append({
        "book_id": book_id,
        "member_id": member_id,
        "action": "Returned",
        "timestamp": datetime.now(),
    })
    return True, f"Book '{books[book_id]['title']}' returned by {members[member_id]['name']}."


# ============================================================================
# 5. REPORTS & QUERIES
# ============================================================================
def available_books_by_genre(genre):
    """Return a list of available books in a given genre (case-insensitive)."""
    return [
        {"book_id": bid, **info}
        for bid, info in books.items()
        if info["genre"].lower() == genre.lower() and info["availability"] == AVAILABLE_STATUS
    ]


def members_who_borrowed():
    """Return members who currently have at least one book borrowed."""
    return [
        {"member_id": mid, "name": info["name"], "borrowed_books": info["borrowed_books"]}
        for mid, info in members.items()
        if info["borrowed_books"]
    ]


def search_book(keyword):
    """Search books by title or author (case-insensitive substring match)."""
    keyword = keyword.lower()
    return [
        {"book_id": bid, **info}
        for bid, info in books.items()
        if keyword in info["title"].lower() or keyword in info["author"].lower()
    ]


def most_popular_genre():
    """Return the genre with the highest number of 'Issued' transactions in the log."""
    issued_genres = [
        books[entry["book_id"]]["genre"]
        for entry in borrow_log
        if entry["action"] == "Issued" and entry["book_id"] in books
    ]
    if not issued_genres:
        return None, 0
    counts = Counter(issued_genres)
    genre, count = counts.most_common(1)[0]
    return genre, count


def library_summary():
    """A one-shot overview report combining several stats."""
    total_books = len(books)
    issued_books = sum(1 for b in books.values() if b["availability"] == ISSUED_STATUS)
    available_books = total_books - issued_books
    top_genre, top_count = most_popular_genre()
    return {
        "total_books": total_books,
        "available_books": available_books,
        "issued_books": issued_books,
        "total_members": len(members),
        "members_with_borrowed_books": len(members_who_borrowed()),
        "most_popular_genre": top_genre,
        "most_popular_genre_issue_count": top_count,
    }


# ============================================================================
# 6. DISPLAY HELPERS (printing only - no business logic)
# ============================================================================
def print_books(book_list, empty_msg="No books found."):
    if not book_list:
        print(empty_msg)
        return
    for b in book_list:
        print(f"  [{b['book_id']}] '{b['title']}' by {b['author']} "
              f"({b['genre']}) - {b['availability']}")


def print_members(member_list, empty_msg="No members found."):
    if not member_list:
        print(empty_msg)
        return
    for m in member_list:
        books_str = ", ".join(m["borrowed_books"]) if m["borrowed_books"] else "None"
        print(f"  [{m['member_id']}] {m['name']} - Borrowed: {books_str}")


# ============================================================================
# 7. DEMO (auto-runs so every requirement is visibly demonstrated)
# ============================================================================
def show_submission_summary():
    """Print a short summary suitable for presentation or submission."""
    print("\nSubmission summary:")
    print("- Stores books, members, and borrow transactions in structured data.")
    print("- Implements add, issue, return, search, and reporting functions.")
    print("- Includes validation rules and a simple interactive menu for testing.")


def run_demo():
    initialize_library()
    print("=" * 70)
    print("DEMO: CITY LIBRARY MANAGEMENT SYSTEM")
    print("=" * 70)

    # --- Add books ---
    add_book("B001", "The Hobbit", "J.R.R. Tolkien", "Fantasy")
    add_book("B002", "Dune", "Frank Herbert", "Sci-Fi")
    add_book("B003", "A Game of Thrones", "George R. R. Martin", "Fantasy")
    add_book("B004", "Foundation", "Isaac Asimov", "Sci-Fi")
    add_book("B005", "The Hobbit Companion", "J.R.R. Tolkien", "Fantasy")

    # --- Add members ---
    add_member("M001", "Aarav Shah", 28, "aarav@example.com")
    add_member("M002", "Priya Mehta", 34, "priya@example.com")

    # --- Issue books ---
    print("\n-- Issuing books --")
    for bid, mid in [("B001", "M001"), ("B002", "M002"), ("B003", "M001")]:
        ok, msg = issue_book(bid, mid)
        print(" ", msg)

    # --- Try an invalid issue (already issued) to show validation ---
    print("\n-- Attempting to issue an already-issued book (should fail) --")
    ok, msg = issue_book("B001", "M002")
    print(" ", msg)

    # --- Return a book ---
    print("\n-- Returning a book --")
    ok, msg = return_book("B002", "M002")
    print(" ", msg)

    # --- Reports ---
    print("\n-- Available Fantasy books --")
    print_books(available_books_by_genre("Fantasy"))

    print("\n-- Members who have borrowed books --")
    print_members(members_who_borrowed())

    print("\n-- Search for 'hobbit' (title/author) --")
    print_books(search_book("hobbit"))

    print("\n-- Library Summary --")
    for k, v in library_summary().items():
        print(f"  {k}: {v}")

    show_submission_summary()

    print("\n" + "=" * 70)
    print("END OF DEMO - entering interactive menu now")
    print("=" * 70 + "\n")


# ============================================================================
# 8. INTERACTIVE MENU (console interface)
# ============================================================================
def main_menu():
    menu = """
------------------------------------------
 CITY LIBRARY MANAGEMENT SYSTEM
------------------------------------------
 1. Add a new book
 2. Add a new member
 3. Issue a book
 4. Return a book
 5. Show available books by genre
 6. Show members who borrowed books
 7. Search book by title/author
 8. Show most popular genre
 9. Show library summary
 0. Exit
------------------------------------------
"""
    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            bid = input("Book ID: ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            genre = input("Genre: ").strip()
            ok, msg = add_book(bid, title, author, genre)
            print(msg)

        elif choice == "2":
            mid = input("Member ID: ").strip()
            name = input("Name: ").strip()
            age = input("Age: ").strip()
            contact = input("Contact Info: ").strip()
            ok, msg = add_member(mid, name, age, contact)
            print(msg)

        elif choice == "3":
            bid = input("Book ID to issue: ").strip()
            mid = input("Member ID: ").strip()
            ok, msg = issue_book(bid, mid)
            print(msg)

        elif choice == "4":
            bid = input("Book ID to return: ").strip()
            mid = input("Member ID: ").strip()
            ok, msg = return_book(bid, mid)
            print(msg)

        elif choice == "5":
            genre = input("Genre: ").strip()
            print_books(available_books_by_genre(genre))

        elif choice == "6":
            print_members(members_who_borrowed())

        elif choice == "7":
            keyword = input("Enter title/author keyword: ").strip()
            print_books(search_book(keyword))

        elif choice == "8":
            genre, count = most_popular_genre()
            if genre:
                print(f"Most popular genre: {genre} ({count} books issued)")
            else:
                print("No books have been issued yet.")

        elif choice == "9":
            for k, v in library_summary().items():
                print(f"  {k}: {v}")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


# ============================================================================
# 9. ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    initialize_library()
    if RUN_DEMO:
        run_demo()
    main_menu()
