from queue import Empty
from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import requests
import json

ClientService=Blueprint('ClientService',__name__)

cache = {}
catalog1 = "http://catalog:5000"
oreder1 = "http://order:5000"

catalog2 = "http://catalog2:5000"
oreder2 = "http://order2:5000"

#load balancing alg round-robin
robin = False

#forward to catalog server-info
def get_books():
   
    global robin
    robin = not robin
    if robin:
        ip = catalog1+"/CATALOG_WEBSERVICE_IP/info"
        print(ip)
        query =  requests.get(ip)
    else:
        ip = catalog2+"/CATALOG_WEBSERVICE_IP/info"
        print(ip)
        query =  requests.get(ip)

    queryResponse = json.loads(query.text)
    return queryResponse

def get_book_by_id(id):
    global robin
    robin = not robin
    if(id not in cache):
        if robin:
            ip = catalog1+"/CATALOG_WEBSERVICE_IP/info/"
            print(ip)
        else:
            ip = catalog2+"/CATALOG_WEBSERVICE_IP/info/"
        print(ip)
        ip = ip + str(id)
        query = requests.get(ip).text
        cache[id] = json.loads(query)
    print(cache)
    return cache[id]

    
def searchBookByTopic(topic):
    print(topic)
    global robin
    robin = not robin
    if (topic not in cache):
        if robin:
            ip = catalog1+"/CATALOG_WEBSERVICE_IP/search/"
            print(ip)
        else:
            ip = catalog2+"/CATALOG_WEBSERVICE_IP/search/"
        print(ip)
        ip = ip + topic
        cache[topic] = json.loads(requests.get(ip).text)
    return cache[topic]

def purchase(id):
    global robin
    robin = not robin
    
    if robin:
        ip = oreder1+"/ORDER_WEBSERVICE_IP/purchase/"
        print(ip)
        ip = ip + str(id)
    else:
        ip = oreder2+"/ORDER_WEBSERVICE_IP/purchase/"
        print(ip)
        ip = ip + str(id)
    if (id in cache):
        cache.pop(id)    
    respose = requests.get(ip).text
    return json.loads(respose)
    
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