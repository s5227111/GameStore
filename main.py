from flask import Flask
from auth.views import auth_bp

#Initialize Flask framework
app = Flask(__name__)
app.register_blueprint(auth_bp)


if __name__ == "__main__": 
    app.run(debug=True)

