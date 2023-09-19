from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
import json
from config import config
from flask import Flask
from flask_cors import CORS

# routes
from routes import Produto
from models import ProdutoModel

app = Flask(__name__)

CORS(app)  # Isso habilitará CORS para todas as rotas do aplicativo.
api = Api(app)

CORS(
    app,
    resources={
        r"/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)


if __name__ == '__main__':
    app.config.from_object(config['development'])

    # blueprints
    app.register_blueprint(Produto.main, url_prefix='/api/produtos')


# Define a sample resource
class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello, World!'})

# Define a resource to return a list of produtos
class Produtos(Resource):
    def get(self):
        produtos = ProdutoModel.get_produtos()
        produtos_list = [{'id_produto': produto.id_produto, 'nome_prod': produto.nome_prod, 'descproduto': produto.descproduto, 'valorproduto': produto.valorproduto} for produto in produtos]
        return jsonify(produtos_list)

class ProdutoPorID(Resource):
    def get(self, id_produto):
        produto = ProdutoModel.get_produto(id_produto)
        if produto:
            return jsonify({'id_produto': produto.id_produto, 'nome_prod': produto.nome_prod, 'descproduto': produto.descproduto, 'valorproduto': produto.valorproduto})
        else:
            return jsonify({'message': 'Produto não encontrado'}), 404

class CriarProduto(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome_prod', type=str, required=True, help='Nome do produto é obrigatório')
        parser.add_argument('descproduto', type=str, required=True, help='Descrição do produto é obrigatória')
        parser.add_argument('valorproduto', type=str, required=True, help='Valor do produto é obrigatório')
        
        args = parser.parse_args()
        novo_produto = ProdutoModel.add_produto(args['nome_prod'], args['descproduto'], args['valorproduto'])
        
        if novo_produto:
            return jsonify({'message': 'Produto criado com sucesso', 'id_produto': novo_produto.id_produto}), 201
        else:
            return jsonify({'message': 'Erro ao criar o produto'}), 500
        
class AtualizarProduto(Resource):
    def put(self, id_produto):
        parser = reqparse.RequestParser()
        parser.add_argument('nome_prod', type=str, required=True, help='Nome do produto é obrigatório')
        parser.add_argument('descproduto', type=str, required=True, help='Descrição do produto é obrigatória')
        parser.add_argument('valorproduto', type=str, required=True, help='Valor do produto é obrigatório')

        args = parser.parse_args()
        produto_atualizado = ProdutoModel.update_produto(id_produto, args['nome_prod'], args['descproduto'], args['valorproduto'])

        if produto_atualizado:
            return jsonify({'message': 'Produto atualizado com sucesso'}), 200
        else:
            return jsonify({'message': 'Produto não encontrado'}), 404

class ExcluirProduto(Resource):
    def delete(self, id_produto):
        if ProdutoModel.delete_produto(id_produto):
            return jsonify({'message': 'Produto excluído com sucesso'}), 200
        else:
            return jsonify({'message': 'Produto não encontrado'}), 404



# Add the resources to the API
api.add_resource(HelloWorld, '/')
api.add_resource(Produtos, '/produtos')  # Alterei o endpoint para '/produtos'
api.add_resource(ExcluirProduto, '/delete/<int:id_produto>')

# Configure Swagger UI
SWAGGER_URL = '/swagger1'
API_URL = '/swagger1.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger1.json')
def swagger():
    with open('swagger1.json', 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(debug=True)
