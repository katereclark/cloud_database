import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def initialize_firestore():

    # Setup Google Cloud Key
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cosmere-database-firebase-adminsdk-ekqyh-164672a1d3.json"

    # Use the application default credentials
    cred = credentials.Certificate(r"C:\Users\Kate\Documents\Folders\CSE 310\cloud_database\cosmere-database-firebase-adminsdk-ekqyh-164672a1d3.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db

def set_book(db, title, author, num_in_series, checked_out):
    book = {"title" : title, "author" : author, "num_in_series" : num_in_series, "checked_out" : checked_out}
    db.collection("books").document(title).set(book)

def remove_book(db, title):
    db.collection("books").document(title).delete()

def display_books(db):
    results = db.collection("books").stream()
    print()
    print("Books in Library:")
    print("{:<25}  {:<20}  {:<20}  {:<20}".format("Title", "Author", "Number in Series", "Is Checked Out"))
    for result in results:
        books = result.to_dict()
        print("{:<25}  {:<20}  {:<20}  {:<20}".format(books["title"], books["author"], books["num_in_series"], books["checked_out"]))

def main():
    db = initialize_firestore()
    choice = None
    while choice != "5":
        print()
        print("1) Add Book to Library")
        print("2) Edit Book in Library")
        print("3) Remove Book from Library")
        print("4) Display Books in Library")
        print("5) Quit")
        choice = input("> ")
        print()
        if choice == "1" or "2":
            title = input("What is the book title? ")
            author = input("What is the first and last name of the author? ")
            num_in_series = input("What number in the book series is it (1, 2, 3...)? ")
            checked_out = input("Is the book checked out (y/n)? ")
            set_book(db, title, author, num_in_series, checked_out)
            print(f'\n"{title}" has been added to library.')
        elif choice == "3":
            title = "What is the title of the book you wish to remove? "
            remove_book(db, title)
            print(f'\n"{title}" has been removed from library.')
        elif choice == "4":
            display_books(db)
        else:
            exit()

if __name__ == "__main__":
    main()