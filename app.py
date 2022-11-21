# implementar padrao de projeto onde vou colocar aqui todas as configuracoes do aplicativo

from flask import Flask
from auth.views import configure as config_auth
from auth.models import configure as config_db


def create_app():
    #Initialize Flask framework
    app = Flask(__name__)

# configurando visualizacoes
    config_auth(app)
    config_db(app)

    return app


# Executa quando utilizamos python3 app.py no terminal
if __name__ == "__main__": 
    app = create_app()
    app.run(debug=True)
