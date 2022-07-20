from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import sqlite3
import requests
import json

order=Blueprint('order',__name__)

def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn 

def purchase(id):
    query = requests.get("http://192.168.1.204:8787/CATALOG_WEBSERVICE_IP/info")
    
    id = int(id)
    
    books = json.loads(query.text)

    flag = False
    for book in books:
        if book["id"] == id:
            flag = True

    if flag:
        request = {
            "id":id
        }
        Update = requests.put("http://192.168.1.204:8787/CATALOG_WEBSERVICE_IP/update", json=request)
        response = json.loads(Update.text)
        if response["status"] == "OK":
            return "Done"
        else:
            return "There is no enough books in the storage."
    else:
        return "There is no book with this ID"

@order.route('/ORDER_WEBSERVICE_IP/purchase/<id>')
def home_page(id):
    return purchase(id)