from flask import Blueprint, render_template, request, redirect, url_for, session
from settings import HEADERS_API, ENDPOINT_LOGIN
import requests
import jwt
from funcoes import Funcoes
from functools import wraps

bp_login = Blueprint('login', __name__, url_prefix='/', template_folder='templates')

@bp_login.route("/", methods=['GET', 'POST'])
def login():
    return render_template("formLogin.html")

@bp_login.route('/login', methods=['POST'])
def validaLogin():
    try:
        session.clear()
        cpf = request.form['cpf']
        senha = Funcoes.cifraSenha(request.form['senha'])
        
        payload = {'cpf': cpf, 'senha':senha}
        response = requests.post(ENDPOINT_LOGIN, headers=HEADERS_API, json=payload)
        print(response.status_code)
        result = response.json()
        
        if (result[1] != 200):
            raise Exception(result[0])
        
        token = jwt.decode(result[0]['access_token'],
            "EmainesSecretKey",
            algorithms=["HS256"])
        
        #print(result)
        if (cpf == token['cpf']):
            session['login'] = token['nome']
            session['grupo'] = changeToGroupName(token['grupo'])
        # abre a aplicação na tela home
            return redirect(url_for('index.formIndex'))
        else:
            raise Exception("Falha de Login! Verifique seus dados e tente novamente!")

    except Exception as e:
        print(e)
        return redirect(url_for('login.login', msgErro=e.args[0]))

@bp_login.route("/logoff", methods=['GET'])
def logoff():
    session.pop('login', None)
    session.clear()
    
    return redirect(url_for('login.login'))

# valida se o usuário esta ativo na sessão
def validaSessao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('login.login', msgErro='Usuário não logado!'))
        else:
            return f(*args, **kwargs)
    return decorated_function


def changeToGroupName(grupo):
    if grupo == 1:
        return 'Atendente'
    elif grupo == 2:
        return 'Caixa'
    elif grupo == 3:
        return 'Administrador'