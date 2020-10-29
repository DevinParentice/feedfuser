from flask import Flask

app = Flask(__name__)

from main.routes import main

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)