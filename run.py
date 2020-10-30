from flask import Flask

app = Flask(__name__)

from main.routes import main
from user.routes import user

app.register_blueprint(main)
app.register_blueprint(user)

if __name__ == '__main__':
    app.run(debug=True)