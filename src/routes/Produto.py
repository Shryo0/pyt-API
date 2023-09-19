from flask import Blueprint, jsonify, request

from models.entities.Produto import Produto

from models.ProdutoModel import ProdutoModel

main = Blueprint('produto_blueprint', __name__)


@main.route('/')
def get_produtos():
    try:
        produtos = ProdutoModel.get_produtos()
        return jsonify(produtos)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<id_produto>')
def get_produto(id_produto):
    try:
        produto = ProdutoModel.get_produto(id_produto)
        if produto != None:
            return jsonify(produto)
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/', methods=['POST'])
def add_produto():
    try:
        id_produto = ProdutoModel.get_next_sequence_produto()
        
        # Obtenha os dados do JSON da solicitação
        data = request.json

        # Extraia os dados necessários do JSON
        nome_prod = data.get('nome_prod')
        descproduto = data.get('descproduto')
        valorproduto = data.get('valorproduto')

        # Verifique se os campos obrigatórios estão presentes
        if nome_prod is None or descproduto is None or valorproduto is None:
            return jsonify({'message': 'Campos obrigatórios ausentes'}), 400

        # Crie um objeto Produto com os dados
        produto = Produto(id_produto, nome_prod, descproduto, valorproduto)

        affected_rows = ProdutoModel.add_produto(produto)
        
        if affected_rows == 1:
            return jsonify({'message': 'Produto inserido com sucesso'}), 201
        else:
            return jsonify({'message': 'Erro ao inserir o produto'}), 500
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<id_produto>', methods=['DELETE'])
def delete_produto(id_produto):
    try:
       produto = Produto(id_produto)
       
       affected_rows = ProdutoModel.delete_produto(produto)
       
       if affected_rows == 1:
           return "true"
       else:
           return jsonify({'message': "produto nao encontrado"}), 404
       
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/<id_produto>', methods=['PUT'])
def update_produto(id_produto):
    try:
        # Obtenha os dados do JSON da solicitação
        data = request.json

        # Extraia os dados necessários do JSON
        nome_prod = data.get('nome_prod')
        descproduto = data.get('descproduto')
        valorproduto = data.get('valorproduto')

        # Verifique se os campos obrigatórios estão presentes
        if nome_prod is None or descproduto is None or valorproduto is None:
            return jsonify({'message': 'Campos obrigatórios ausentes'}), 400

        # Crie um objeto Produto com os dados
        produto = Produto(id_produto, nome_prod, descproduto, valorproduto)

        affected_rows = ProdutoModel.update_produto(produto)

        if affected_rows == 1:
            return jsonify({'message': 'Produto atualizado com sucesso'}), 200
        else:
            return jsonify({'message': 'Produto não encontrado'}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

