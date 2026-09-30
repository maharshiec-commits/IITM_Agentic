# Graded Mini Project: Part A: City Library
# Management System

import csv
import os
import random
import string
from datetime import datetime

BOOK_FILE = "book.csv"
MEMBER_FILE = "member.csv"
BORROW_LOG_FILE = "borrow_log.csv"


def generate_id(length=6):
    """Generate a random alphanumeric ID of the given length."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def load_books(file_name=BOOK_FILE):
    """Load books from a CSV file into a dictionary."""
    if not os.path.exists(file_name):
        return {}

    books = {}
    with open(file_name, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            book_id = (row.get("Book ID") or row.get("bookId") or row.get("book_id") or "").strip()
            if not book_id:
                continue
            books[book_id] = {
                "Title": (row.get("Title") or row.get("title") or "").strip(),
                "Author": (row.get("Author") or row.get("author") or "").strip(),
                "Genre": (row.get("Genre") or row.get("genre") or "").strip(),
                "Availability": (row.get("Availability") or row.get("availability") or "Available").strip().capitalize(),
            }
    return books


def load_members(file_name=MEMBER_FILE):
    """Load members from a CSV file into a dictionary."""
    if not os.path.exists(file_name):
        return {}

    members = {}
    with open(file_name, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            member_id = (row.get("Member ID") or row.get("memberId") or row.get("member_id") or "").strip()
            if not member_id:
                continue
            borrowed_books_value = row.get("Borrowed Books") or row.get("borrowedBooks") or ""
            if isinstance(borrowed_books_value, str):
                borrowed_books = [item.strip() for item in borrowed_books_value.split(",") if item.strip()]
            else:
                borrowed_books = []
            members[member_id] = {
                "Name": (row.get("Name") or row.get("name") or "").strip(),
                "Age": (row.get("Age") or row.get("age") or "").strip(),
                "Contact Info": (row.get("Contact Info") or row.get("contactinfo") or "").strip(),
                "Borrowed Books": borrowed_books,
            }
    return members


def load_borrow_log(file_name=BORROW_LOG_FILE):
    """Load borrow-return transactions from a CSV file."""
    if not os.path.exists(file_name):
        return []

    with open(file_name, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def save_books(books, file_name=BOOK_FILE):
    """Save book records back to the CSV file."""
    with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Book ID", "Title", "Author", "Genre", "Availability"])
        writer.writeheader()
        for book_id, details in books.items():
            writer.writerow({
                "Book ID": book_id,
                "Title": details.get("Title", ""),
                "Author": details.get("Author", ""),
                "Genre": details.get("Genre", ""),
                "Availability": details.get("Availability", "Available"),
            })


def save_members(members, file_name=MEMBER_FILE):
    """Save member records back to the CSV file."""
    with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Member ID", "Name", "Age", "Contact Info", "Borrowed Books"])
        writer.writeheader()
        for member_id, details in members.items():
            writer.writerow({
                "Member ID": member_id,
                "Name": details.get("Name", ""),
                "Age": details.get("Age", ""),
                "Contact Info": details.get("Contact Info", ""),
                "Borrowed Books": ",".join(details.get("Borrowed Books", [])),
            })


def save_borrow_log(borrow_log, file_name=BORROW_LOG_FILE):
    """Save borrow-return transactions to a CSV file."""
    with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Transaction ID", "Book ID", "Member ID", "Action", "Timestamp"])
        writer.writeheader()
        writer.writerows(borrow_log)


def save_records(books, members, borrow_log, book_file=BOOK_FILE, member_file=MEMBER_FILE, borrow_log_file=BORROW_LOG_FILE):
    """Persist all library data to CSV files."""
    save_books(books, book_file)
    save_members(members, member_file)
    save_borrow_log(borrow_log, borrow_log_file)
    print("Records saved successfully.")


def add_book(books, title, author, genre, book_file=BOOK_FILE):
    """Add a new book and save it to the CSV file."""
    book_id = generate_id()
    books[book_id] = {
        "Title": title,
        "Author": author,
        "Genre": genre,
        "Availability": "Available",
    }
    save_books(books, book_file)
    print(f"Book '{title}' added with ID: {book_id}")
    return book_id


def add_member(members, name, age, contact_info, member_file=MEMBER_FILE):
    """Add a new member and save it to the CSV file."""
    member_id = generate_id()
    members[member_id] = {
        "Name": name,
        "Age": age,
        "Contact Info": contact_info,
        "Borrowed Books": [],
    }
    save_members(members, member_file)
    print(f"Member '{name}' added with ID: {member_id}")
    return member_id


def add_borrow_log_entry(borrow_log, book_id, member_id, action, log_file=BORROW_LOG_FILE):
    """Append a transaction to the borrow log."""
    borrow_log.append({
        "Transaction ID": generate_id(8),
        "Book ID": book_id,
        "Member ID": member_id,
        "Action": action,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    save_borrow_log(borrow_log, log_file)


def borrow_book(books, members, borrow_log, book_id, member_id, book_file=BOOK_FILE, member_file=MEMBER_FILE, log_file=BORROW_LOG_FILE):
    """Allow a member to borrow a book if it is available."""
    if book_id not in books:
        print(f"Book ID {book_id} not found.")
        return False
    if member_id not in members:
        print(f"Member ID {member_id} not found.")
        return False

    if books[book_id]["Availability"] != "Available":
        print(f"Book ID {book_id} is currently not available.")
        return False

    if book_id in members[member_id].get("Borrowed Books", []):
        print(f"Member ID {member_id} already has Book ID {book_id}.")
        return False

    books[book_id]["Availability"] = "Issued"
    members[member_id]["Borrowed Books"].append(book_id)
    save_books(books, book_file)
    save_members(members, member_file)
    add_borrow_log_entry(borrow_log, book_id, member_id, "Borrow", log_file)
    print(f"Book ID {book_id} issued to Member ID {member_id}.")
    return True


def return_book(books, members, borrow_log, book_id, member_id, book_file=BOOK_FILE, member_file=MEMBER_FILE, log_file=BORROW_LOG_FILE):
    """Allow a member to return a borrowed book."""
    if book_id not in books:
        print(f"Book ID {book_id} not found.")
        return False
    if member_id not in members:
        print(f"Member ID {member_id} not found.")
        return False

    borrowed_books = members[member_id].get("Borrowed Books", [])
    if book_id not in borrowed_books:
        print(f"Member ID {member_id} did not borrow Book ID {book_id}.")
        return False

    books[book_id]["Availability"] = "Available"
    members[member_id]["Borrowed Books"] = [item for item in borrowed_books if item != book_id]
    save_books(books, book_file)
    save_members(members, member_file)
    add_borrow_log_entry(borrow_log, book_id, member_id, "Return", log_file)
    print(f"Book ID {book_id} returned by Member ID {member_id}.")
    return True


def show_available_books_by_genre(books, genre):
    """Show all available books in a specific genre."""
    matching_books = [
        (book_id, details)
        for book_id, details in books.items()
        if details.get("Genre", "").lower() == genre.lower() and details.get("Availability") == "Available"
    ]
    if matching_books:
        print(f"Available books in genre '{genre}':")
        for book_id, details in matching_books:
            print(f"ID: {book_id}, Title: {details['Title']}, Author: {details['Author']}")
    else:
        print(f"No available books found in genre '{genre}'.")


def list_members_with_borrowed_books(members):
    """List all members who are currently borrowing books."""
    members_with_books = {member_id: details for member_id, details in members.items() if details.get("Borrowed Books")}
    if members_with_books:
        print("Members who have borrowed books:")
        for member_id, details in members_with_books.items():
            print(f"ID: {member_id}, Name: {details['Name']}, Borrowed Books: {details['Borrowed Books']}")
    else:
        print("No members have borrowed books.")


def search_book(books, search_term):
    """Search books by title or author."""
    search_term = search_term.lower()
    found_books = [
        (book_id, details)
        for book_id, details in books.items()
        if search_term in details.get("Title", "").lower() or search_term in details.get("Author", "").lower()
    ]
    if found_books:
        print(f"Books matching '{search_term}':")
        for book_id, details in found_books:
            print(f"ID: {book_id}, Title: {details['Title']}, Author: {details['Author']}, Genre: {details['Genre']}, Availability: {details['Availability']}")
    else:
        print(f"No books found matching '{search_term}'.")


def most_popular_genre(books):
    """Show the most popular genre based on issued books."""
    genre_count = {}
    for details in books.values():
        if details.get("Availability") == "Issued":
            genre = details.get("Genre", "Unknown")
            genre_count[genre] = genre_count.get(genre, 0) + 1

    if genre_count:
        most_popular = max(genre_count, key=genre_count.get)
        print(f"The most popular genre is '{most_popular}' with {genre_count[most_popular]} issued books.")
    else:
        print("No books have been issued yet.")


def load_records(book_file=BOOK_FILE, member_file=MEMBER_FILE, borrow_log_file=BORROW_LOG_FILE):
    """Load all records from CSV files."""
    books = load_books(book_file)
    members = load_members(member_file)
    borrow_log = load_borrow_log(borrow_log_file)
    return books, members, borrow_log


def main():
    """Run the interactive library management system."""
    books, members, borrow_log = load_records()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Show Available Books by Genre")
        print("6. List Members with Borrowed Books")
        print("7. Search Book by Title/Author")
        print("8. Most Popular Genre")
        print("9. Save Records")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            genre = input("Enter book genre: ").strip()
            add_book(books, title, author, genre)
        elif choice == "2":
            name = input("Enter member name: ").strip()
            age = input("Enter member age: ").strip()
            contact_info = input("Enter member contact info: ").strip()
            add_member(members, name, age, contact_info)
        elif choice == "3":
            book_id = input("Enter book ID to borrow: ").strip()
            member_id = input("Enter member ID: ").strip()
            borrow_book(books, members, borrow_log, book_id, member_id)
        elif choice == "4":
            book_id = input("Enter book ID to return: ").strip()
            member_id = input("Enter member ID: ").strip()
            return_book(books, members, borrow_log, book_id, member_id)
        elif choice == "5":
            genre = input("Enter genre to search for available books: ").strip()
            show_available_books_by_genre(books, genre)
        elif choice == "6":
            list_members_with_borrowed_books(members)
        elif choice == "7":
            search_term = input("Enter title or author to search for a book: ").strip()
            search_book(books, search_term)
        elif choice == "8":
            most_popular_genre(books)
        elif choice == "9":
            save_records(books, members, borrow_log)
        elif choice == "0":
            save_records(books, members, borrow_log)
            print("Exiting the system.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
