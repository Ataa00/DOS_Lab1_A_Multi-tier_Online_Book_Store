from flask import Flask,Blueprint
import catalogService 

app = Flask(__name__)

app.register_blueprint(catalogService.catalogService)

