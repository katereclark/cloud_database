import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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
    property = None
    print()
    print(f'Which part of the "{title}" entry would you like to edit?')
    print("1) Title")
    print("2) Author")
    print("3) Series name")
    print("4) Number in series")
    print("5) Checked out")
    print("6) Quit")
    property = input("> ")
    print()
    
    entry_ref = db.collection("books").document(title)

    while property != "6":
        if property == "1":
            title = input("What is the new title? ")
            entry_ref.update({"title": title})
            break
        elif property == "2":
            author = input("What is the new first and last names of the author? ")
            entry_ref.update({"author": author})
            break
        elif property == "3":
            series_name = input("What is the new series name? ")
            entry_ref.update({"series_name": series_name})
            break
        elif property == "4":
            num_in_series = input("What is the new number in the book series (1, 2, 3...)? ")
            entry_ref.update({"num_in_series": num_in_series})
            break
        elif property == "5":
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

# Adds a user to the users collection.
def set_user(db, username, librarian, patron):
    user = {"librarian" : librarian, "patron" : patron}
    db.collection("users").document(username).set(user)

# Deletes a user from the users collection.
def remove_user(db, username):
    db.collection("users").document(username).delete()

# Edites a user field for the specified username.
def edit_user(db, username):
    property = None
    print()
    print(f"Which part of the user's information would you like to edit?")
    print("1) Username")
    print("2) Librarian access")
    print("3) Patron access")
    print("4) Quit")
    property = input("> ")
    print()
    
    entry_ref = db.collection("users").document(username)

    while property != "4":
        if property == "1":
            print("Please delete the user and then create them again under the desired username.")
            break
        elif property == "2":
            librarian = input("Will this user have libarian access (yes or no)? ")
            if librarian == "no":
                librarian = False
            else:
                librarian = True
            entry_ref.update({"librarian": librarian})
            print(f'\n"{username}" has been successfully edited.')
            break
        elif property == "3":
            patron = input("Will this user have patron access (yes or no)? ")
            if patron == "no":
                patron = False
            else:
                patron = True
            entry_ref.update({"patron": patron})
            print(f'\n"{username}" has been successfully edited.')
            break
        else:
            break

# Only accessible to librarians.
def display_librarian_control_panel(db):
    choice = None
    while choice != "9":
        print()
        print("1) Add Book to Library")
        print("2) Remove Book from Library")
        print("3) Edit Book in Library")
        print("4) Display Books in Series")
        print("5) Display Books in Library")
        print("6) Add User")
        print("7) Remove User")
        print("8) Edit User")
        print("9) Quit")
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
        elif choice == "6":
            username = input("What is the username you wish to add? ")
            librarian = input("Will this user have libarian access (yes or no)? ")
            if librarian == "no":
                librarian = False
            else:
                librarian = True
            patron = input("Will this user have patron access (yes or no)? ")
            if patron == "no":
                patron = False
            else:
                patron = True
            set_user(db, username, librarian, patron)
            print(f'\n"{username}" has been added.')
        elif choice == "7":
            username = input("What is the username you wish to remove? ")
            remove_user(db, username)
            print(f'\n"{username}" has been removed.')
        elif choice == "8":
            username = input("What is the username you wish to edit? ")
            edit_user(db, username)
        else:
            break

# Only accessible to patrons.
def display_patron_control_panel(db):
    choice = None
    while choice != "3":
        print()
        print("1) Display Books in Series")
        print("2) Display Books in Library")
        print("3) Quit")
        choice = input("> ")
        print()

        if choice == "1":
            series_name = input("What is the name of the book series you wish to view? ")
            display_books_by_series(db, series_name)
        elif choice == "2":
            display_books(db)
        else:
            break

# Accessible to anyone who is not a librarian or patron.
def display_unauthorized_user_control_panel():
    print("Unauthorized User")
    choice = None
    while choice != "2":
        print("1) Try another username")
        print("2) Quit")
        choice = input("> ")
        print()

        if choice == "1":
            main(db)
        else:
            break

def main(db):
    user = input("Enter your username: ")
    person = db.collection("users").document(f"{user}").get()
    person = person.to_dict()

    if person["librarian"] == True and person["patron"] == True:
        display_librarian_control_panel(db)
    elif person["librarian"] == False and person["patron"] == True:
        display_patron_control_panel(db)
    else:
        display_unauthorized_user_control_panel()

if __name__ == "__main__":
    db = initialize_firestore()
    main(db)