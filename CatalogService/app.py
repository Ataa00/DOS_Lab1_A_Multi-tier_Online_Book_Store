from flask import Flask,Blueprint
from  .catalogService import catalogService 

app = Flask(__name__)

app.register_blueprint(catalogService)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=8787)