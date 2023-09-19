from database.db import get_connection
from .entities.Produto import Produto
import json
from psycopg2.extras import Json

class ProdutoModel():

    @classmethod
    def get_produtos(cls):
        try:
            connection = get_connection()
            produtos = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_produto, nome_prod, descproduto, valorproduto FROM public.tb_produto ORDER BY nome_prod ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    produto = Produto(row[0], row[1], row[2], row[3])
                    produtos.append(produto.to_JSON())

            connection.close()
            return produtos
        except Exception as ex:
            raise Exception(ex)



    @classmethod
    def get_produto(self, id_produto):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_produto, nome_prod, descproduto, valorproduto FROM public.tb_produto WHERE id_produto = %s", (id_produto,))
                row = cursor.fetchone()

                produto = None
                if row != None:
                    produto = Produto(row[0], row[1], row[2], row[3])
                    produto = produto.to_JSON()

                    connection.close()
                    return produto
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_produto(self, produto):
        try:
            connection = get_connection()        

            with connection.cursor() as cursor:
                next_id = ProdutoModel.get_next_sequence_produto()
                # Converta os valores do JSON para os tipos de dados corretos
                nome_prod = str(produto.nome_prod)
                descproduto = str(produto.descproduto)
                valorproduto = float(produto.valorproduto)
                cursor.execute("""INSERT INTO tb_produto (id_produto, nome_prod, descproduto, valorproduto)
                        VALUES (%s, %s, %s, %s)""", (next_id, nome_prod, descproduto, valorproduto))

                affected_rows = cursor.rowcount
                connection.commit()

                connection.close()
                return affected_rows
        except Exception as ex:
            raise Exception(ex)





    @classmethod
    def delete_produto(self, produto):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tb_produto WHERE id_produto = %s", (produto.id_produto,))
                affected_rows = cursor.rowcount
                connection.commit()

                connection.close()
                return affected_rows
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_produto(cls, produto):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                     "UPDATE tb_produto SET nome_prod = %s, descproduto = %s, valorproduto = %s WHERE id_produto = %s",
                     (produto.nome_prod, produto.descproduto, produto.valorproduto, produto.id_produto))

            affected_rows = cursor.rowcount
            connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

        
    @classmethod
    def get_next_sequence_produto(cls):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT nextval('produto_id_produto_seq'::regclass)")
                row = cursor.fetchone()

                if row != None:
                    next_id = row[0]
                    connection.close()
                    return next_id
        except Exception as ex:
            raise Exception(ex)