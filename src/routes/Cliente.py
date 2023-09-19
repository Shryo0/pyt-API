from flask import Blueprint, jsonify, request
import uuid
from models.entities.Cliente import Cliente
from models.ClienteModel import ClienteModel

main = Blueprint('cliente_blueprint', __name__)


@main.route('/')
def get_clientes():
    try:
        clientes = ClienteModel.get_clientes()
        return jsonify(clientes)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<id>')
def get_cliente(id):
    try:
        cliente = ClienteModel.get_cliente(id)
        if cliente != None:
            return jsonify(cliente)
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_cliente():
    try:
        nome = request.json['nome']
        telefone = request.json['telefone']
        cep = request.json['cep']
        complemento = request.json['complemento']
        numcpf = request.json['numcpf']
        cliente = Cliente(nome, telefone, cep, complemento, numcpf)
        
        # Adicionando um print para verificar os dados recebidos
        print(f'Dados recebidos: nome={nome}, telefone={telefone}, cep={cep}, complemento={complemento}, numcpf={numcpf}')

        affected_rows = ClienteModel.add_cliente(cliente)
        print('Cliente inserido com sucesso')
        
        if affected_rows == 1:
            return jsonify(cliente.id)
        else:
            print('Erro ao inserir o produto')
            return jsonify({'message': "error on insert"}), 500
    except Exception as ex:
        # Adicionando um print para verificar a exceção
        print(f'Erro: {ex}')
        return jsonify({'message': str(ex)}), 500

@main.route('/delete/<id>', methods=['DELETE'])
def delete_produto(id):
    try:
       cliente = Cliente(id)
       
       affected_rows = ClienteModel.delete_cliente(cliente)
       
       if affected_rows == 1:
           return jsonify(cliente.id)
       else:
           return jsonify({'message': "cliente nao encontrado"}), 404
       
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/update/<id>', methods=['PUT'])
def update_cliente(id):
    try:
 #       nome_prod = request.json["nome_prod"]
  #      descproduto = request.json["descproduto"]
   #     valorproduto = request.json["valorproduto"]
        cliente = Cliente(id, nome_prod, descproduto, valorproduto)            
       
        affected_rows = ProdutoModel.add_produto(produto)
       
        if affected_rows == 1:
           return jsonify(produto.id_produto)
        else:
            return jsonify({'message': "Error on insert"}), 500
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
