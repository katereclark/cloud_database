import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def initialize_firestore():

    cred = credentials.Certificate(r"C:\Users\Kate\Documents\Folders\CSE 310\cloud_database\cosmere-database-firebase-adminsdk-ekqyh-164672a1d3.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db

def set_book(db, title, author, series_name, num_in_series, checked_out):
    book = {"title" : title, "author" : author, "series_name" : series_name, "num_in_series" : num_in_series, "checked_out" : checked_out}
    db.collection("books").document(title).set(book)

def remove_book(db, title):
    selection = db.collection("books").where("title", "==", title).stream()
    for selected in selection:
        selected.reference.delete()

def display_books(db):
    results = db.collection("books").stream()
    print()
    print("Books in Library:")
    print("{:<25}  {:<20}  {:<25}  {:<20}  {:<20}".format("Title", "Author", "Series Name", "Number in Series", "Checked Out"))
    for result in results:
        books = result.to_dict()
        print("{:<25}  {:<20}  {:<25}  {:<20}  {:<20}".format(books["title"], books["author"], books["series_name"], books["num_in_series"], books["checked_out"]))

def edit_book(db, title):
    component = None
    print()
    print(f'Which part of "{title}" would you like to edit?')
    print("1) Title")
    print("2) Author")
    print("3) Series name")
    print("4) Number in series")
    print("5) Checked out")
    print("6) Quit")
    component = input("> ")
    print()
    
    while component != "6":
        if component == "1":
            title = input("What is the new title? ")
        elif component == "2":
            author = input("What is the new first and last names of the author? ")
        elif component == "3":
            series_name = input("What is the new series name? ")
        elif component == "4":
            num_in_series = input("What is the new number in the book series (1, 2, 3...)? ")
        elif component == "5":
            checked_out = input("Is the book checked out (y/n)? ")

    # books[f"{component}"] = new_entry
    # db.collection("books").document(title)...


def main():
    db = initialize_firestore()
    choice = None
    while choice != "5":
        print()
        print("1) Add Book to Library")
        print("2) Remove Book from Library")
        print("3) Edit Book in Library")
        print("4) Display Books in Library")
        print("5) Quit")
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
            display_books(db)
        else:
            exit()

if __name__ == "__main__":
    main()