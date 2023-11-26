import base64
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
from settings import HEADERS_API, ENDPOINT_PRODUTO
from mod_login.login import validaSessao

bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

''' rotas dos formulários '''
@bp_produto.route('/', methods=['GET', 'POST'])
@validaSessao
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=HEADERS_API)
        result = response.json()
                        
        if (response.status_code != 200):
            raise Exception(result[0])
        return render_template('formListaProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/form-produto/', methods=['GET'])
@validaSessao
def formProduto():
    return render_template('formProduto.html')

@bp_produto.route("/form-edit-produto", methods=['POST'])
@validaSessao
def formEditProduto():
    try:
        id_produto = request.form['id']
        response = requests.get(ENDPOINT_PRODUTO + id_produto, headers=HEADERS_API)
        print(response.json)
        result = response.json()
        print(result)
        if (response.status_code != 200):
            raise Exception(result[0])
        print("Testee")
        
        # renderiza o form passando os dados retornados
        return render_template('formProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])


@bp_produto.route('/insert', methods=['POST'])
@validaSessao
def insert():
    print("Caindo produto")
    try:
        # dados enviados via FORM
        id_produto = 0
        nome = request.form['nome']
        descricao = request.form['descricao']
        #foto = request.form['foto']
        valor_unitario = request.form['valor_unitario']
        # converte a foto em base64
        print("fOTOO")
        print(request.files['foto'])
        print("Pos foto 1")
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        print("Pos foto")

        # monta o JSON para envio a API
        payload = {'id_produto': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario}
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_PRODUTO, headers=HEADERS_API, json=payload)
        result = response.json()
        print(result)
        return redirect(url_for('produto.formListaProduto', msg=result[0]))
    except Exception as e:
        print(e.args[0])
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/edit', methods=['POST'])
@validaSessao
def edit():
    try:
        # dados enviados via FORM
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        foto =  "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        valor_unitario = request.form['valor_unitario']
        
        payload = {'id_produto': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario}
        
        response = requests.put(ENDPOINT_PRODUTO + id_produto, headers=HEADERS_API, json=payload)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        
        return redirect(url_for('produto.formListaProduto', msg=result[0]))
    
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])
    
@bp_produto.route('/delete', methods=['POST'])
@validaSessao
def delete():
    try:
      # dados enviados via FORM
      id_produto = request.form['id_produto']
      
      # executa o verbo DELETE da API e armazena seu retorno
      response = requests.delete(ENDPOINT_PRODUTO + id_produto, headers=HEADERS_API)
      result = response.json()
      
      if (response.status_code != 200 or result[1] != 200):
        raise Exception(result[0])
      
      # return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
      return jsonify(erro=False, msg=result[0])
    except Exception as e:
      # return render_template('formListaFuncionario.html', msgErro=e.args[0])
      return jsonify(erro=True, msgErro=e.args[0])