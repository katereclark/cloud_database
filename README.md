# Overview

I built this database in order to improve my ability to add items to, remove items from, and edit items in a cloud database and to better understand how to secure the integrity of a database.

This software initiatlizes Firestore in the terminal using the appropriate key and credentials for where my cloud database is stored. The software asks the user to choose whether to add a book, remove a book, edit a field from an existing book, view the details of all books in a series, or to view the details of all books in the library. Any book or field that is added, removed, or modified is immediatly updated in the Firestore view of the database on Google.

My purpose for writing this cloud database software is to create and maintain a cloud database that imitates a library database and stores books and their individual properties.

{4-5 minute - software running, a walkthrough of the code, and a view of the cloud database.}
Here is a demo of my software: [Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

I am using the Firestore cloud database hosted by Google Firebase. It is a NoSQL database that uses a hierarchy of collections, documents, and fields. The database that I created imitates a library and has a books collection that contains book documents. Each of these book documents has the following fields: title, author, series name, number in the series, and whether the book is checked out or not.

# Development Environment

* Visual Studio Code
* Python 3.8.5 32-bit
* Git / GitHub
* firebase_admin module

# Useful Websites

* [Cloud Firestore Documentation](https://firebase.google.com/docs/firestore/quickstart)
* [Cloud Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started#auth-required)

# Future Work

* Use JavaScript to present the queries and data in a more asthetic way.
* Add a component that will create a notification if any of the data is changed.
* Create an index to order the data by author as well.