from flask import Flask,Blueprint
from view.order import order

app = Flask(__name__)


app.register_blueprint(order)

if __name__ == '__main__':
    app.run(debug=True)

