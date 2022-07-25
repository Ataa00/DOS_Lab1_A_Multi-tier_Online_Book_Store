from queue import Empty
from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import sqlite3 
import requests
import json

ClientService=Blueprint('ClientService',__name__)

def get_books():
    query = requests.get(f"http://127.0.0.1:8787/CATALOG_WEBSERVICE_IP/info")
    
    queryResponse = json.loads(query.text)
    
    return queryResponse

def get_book_by_id(id):
    query = requests.get(f"http://127.0.0.1:8787/CATALOG_WEBSERVICE_IP/info/{id}")
    
    queryResponse = json.loads(query.text)
    
    return queryResponse

def searchBookByTopic(topic):
    print(topic)
    
    query = requests.get(f"http://127.0.0.1:8787/CATALOG_WEBSERVICE_IP/search/{topic}")
    
    queryResponse = json.loads(query.text)
    
    return queryResponse

def purchase(id):
    query = requests.get(f"http://127.0.0.1:8788/ORDER_WEBSERVICE_IP/purchase/{id}")
    print(query.text)
    queryResponse = json.loads(query.text)
    
    return queryResponse


@ClientService.route("/Bazar/info")
def books_api():
    return jsonify(get_books()) 

@ClientService.route('/Bazar/info/<id>', methods=['GET'])
def get_api(id):
    return jsonify(get_book_by_id(id)) 

@ClientService.route("/Bazar/search/<topic>", methods=['GET'])
def topic_api(topic):
    return jsonify(searchBookByTopic(topic)) 

@ClientService.route('/Bazar/purchase/<id>')
def home_page(id):
    return purchase(id)