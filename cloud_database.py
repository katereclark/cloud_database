import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Sets up the firestore cloud database to be ready for use.
def initialize_firestore():

    cred = credentials.Certificate(r"C:\Users\Kate\Documents\Folders\CSE 310\cloud_database\cosmere-database-firebase-adminsdk-ekqyh-164672a1d3.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db

# Adds a book to the books collection.
def set_book(db, title, author, series_name, num_in_series, checked_out):
    book = {"title" : title, "author" : author, "series_name" : series_name, "num_in_series" : num_in_series, "checked_out" : checked_out}
    db.collection("books").document(title).set(book)

# Deletes a book where the title matches the title entered by the user.
def remove_book(db, title):
    selection = db.collection("books").where("title", "==", title).stream()
    for selected in selection:
        selected.reference.delete()

# Selects and displays all books and orders them by series name and book position in series.
def display_books(db):
    results = db.collection("books").order_by("series_name").order_by("num_in_series").stream()
    print()
    print("Books in Library:")
    print("{:<25}  {:<20}  {:<25}  {:<20}  {:<20}".format("Title", "Author", "Series Name", "Number in Series", "Checked Out"))
    for result in results:
        books = result.to_dict()
        print("{:<25}  {:<20}  {:<25}  {:<20}  {:<20}".format(books["title"], books["author"], books["series_name"], books["num_in_series"], books["checked_out"]))

# Selects a property of the user-specified book and modifies that property.
def edit_book(db, title):
    component = None
    print()
    print(f'Which part of the "{title}" entry would you like to edit?')
    print("1) Title")
    print("2) Author")
    print("3) Series name")
    print("4) Number in series")
    print("5) Checked out")
    print("6) Quit")
    component = input("> ")
    print()
    
    entry_ref = db.collection("books").document(title)

    while component != "6":
        if component == "1":
            title = input("What is the new title? ")
            entry_ref.update({"title": title})
            break
        elif component == "2":
            author = input("What is the new first and last names of the author? ")
            entry_ref.update({"author": author})
            break
        elif component == "3":
            series_name = input("What is the new series name? ")
            entry_ref.update({"series_name": series_name})
            break
        elif component == "4":
            num_in_series = input("What is the new number in the book series (1, 2, 3...)? ")
            entry_ref.update({"num_in_series": num_in_series})
            break
        elif component == "5":
            checked_out = input("Is the book checked out (y/n)? ")
            entry_ref.update({"checked_out": checked_out})
            break
        else:
            break

# Selects and displays all books where the series matches the entered series name.
def display_books_by_series(db, series_name):
    results = db.collection("books").where("series_name", "==", series_name).order_by("num_in_series").stream()
    print(f'Books in the "{series_name}" series: ')
    print("{:<25}  {:<20}  {:<25}  {:<20}  {:<20}".format("Title", "Author", "Series Name", "Number in Series", "Checked Out"))
    for result in results:
        books = result.to_dict()
        print("{:<25}  {:<20}  {:<25}  {:<20}  {:<20}".format(books["title"], books["author"], books["series_name"], books["num_in_series"], books["checked_out"]))

# def on_snapshot(doc_snapshot, changes, read_time):
#     # documents_list = []
#     # for doc in doc_snapshot:
#     #     documents_list.append(doc.id)
#     # print(f"Data changes made to: {documents_list}")

#     print("Current book status: ")
#     for change in changes:
#         if change.type.name == 'ADDED':
#             print(f'New book: {change.document.id}')
#         if change.type.name == 'MODIFIED':
#             print(f'Modified book: {change.document.id}')
#         elif change.type.name == 'REMOVED':
#             print(f'Removed book: {change.document.id}')

def main():
    db = initialize_firestore()

    choice = None
    while choice != "7":
        print()
        print("1) Add Book to Library")
        print("2) Remove Book from Library")
        print("3) Edit Book in Library")
        print("4) Display Books in Series")
        print("5) Display Books in Library")
        print("6) Display Book Changes")
        print("7) Quit")
        choice = input("> ")
        print()

        if choice == "1":
            title = input("What is the book title? ")
            author = input("What is the first and last name of the author? ")
            series_name = input("What is the name of the book series? ")
            num_in_series = input("What number in the book series is it (1, 2, 3...)? ")
            checked_out = input("Is the book checked out (y/n)? ")
            set_book(db, title, author, series_name, num_in_series, checked_out)
            print(f'\n"{title}" has been added to library.')
        elif choice == "2":
            title = input("What is the title of the book you wish to remove? ")
            remove_book(db, title)
            print(f'\n"{title}" has been removed from library.')
        elif choice == "3":
            title = input("What is the title of the book entry you wish to edit? ")
            edit_book(db, title)
            print(f'\n"{title}" has been successfully edited.')
        elif choice == "4":
            series_name = input("What is the name of the book series you wish to view? ")
            display_books_by_series(db, series_name)
        elif choice == "5":
            display_books(db)
        # elif choice == "6":
        #     col_query = db.collection("books")
        #     query_watch = col_query.on_snapshot(on_snapshot)
        #     continue
        else:
            break

if __name__ == "__main__":
    main()