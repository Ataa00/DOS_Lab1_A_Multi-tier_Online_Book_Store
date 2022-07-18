from queue import Empty
from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import sqlite3 

catalogService=Blueprint('catalogService',__name__)

#Data base Connection
def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn 

#Get all books from the DB.
def get_books():
    books = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM book")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            book = {}
            book["id"] = i["id"]
            book["title"] = i["title"]
            book["topic"] = i["topic"]
            book["quantity"] = i["quantity"]
            book["price"] = i["price"]
            books.append(book)
        conn.close()     

    except Exception as e:
        print(e)
        books = ["error to get books"]

    return books

#Get a specifice Book from its ID.
def get_book_by_id(id):
    book = {}
    try:
        conn = connect_to_db()
        
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT title,quantity,price FROM book WHERE id = ?",(id))
        row = cur.fetchone()
        # convert row object to dictionary
        print(row)
        if row is Empty:
            return {f"There is No book has id = {id}"}
        book["title"] = row["title"]
        book["quantity"] = row["quantity"]
        book["price"] = row["price"]
        conn.close()
    except Exception as e:
        print(e)
        book = {"error to get book"}
         
    return book

#Search for a book by its topic
def searchBookByTopic(topic):
    books = []
    print(topic)
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM book WHERE topic=?",[topic])
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            book = {}
            book["id"] = i["id"]
            book["title"] = i["title"]
            books.append(book)
        conn.close()
    except Exception as e:
        print(e)
        books = ["error to get books"]

    return books  

#To update Books price or quantity or both
def update_book(book):
    updated_book = {"status":"OK"}
    # try:
    #     conn = connect_to_db()
    #     cur = conn.cursor()
    #     cur.execute("UPDATE book SET quantity = ?, price =? WHERE id =?",  
    #                  (book["quantity"], book["price"], book["id"],))
    #     conn.commit()
    #     #return the user
    #     updated_book = get_book_by_id(book["id"])

    # except:
    #     conn.rollback()
    #     updated_book = {}
    # finally:
    #     conn.close()

    print(updated_book)

    return updated_book

@catalog.route("/CATALOG_WEBSERVICE_IP/info")
def books_api():
    return jsonify(get_books()) 

@catalog.route('/CATALOG_WEBSERVICE_IP/info/<id>', methods=['GET'])
def get_api(id):
    return jsonify(get_book_by_id(id)) 

@catalog.route("/CATALOG_WEBSERVICE_IP/search/<topic>", methods=['GET'])
def topic_api(topic):
    return jsonify(searchBookByTopic(topic)) 

@catalog.route('/CATALOG_WEBSERVICE_IP/info', methods=['PUT'])
def update_api():
    book = request.get_json()
    return jsonify(update_book(book))