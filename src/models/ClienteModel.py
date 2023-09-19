from database.db import get_connection
from .entities.Cliente import Cliente


class ClienteModel():

    @classmethod
    def get_clientes(cls):
        try:
            connection = get_connection()
            clientes = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nome, telefone, cep, complemento, numcpf FROM public.tb_cliente ORDER BY nome ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    cliente = Cliente(row[0], row[1], row[2], row[3])
                    clientes.append(cliente.to_JSON())

            connection.close()
            return clientes
        except Exception as ex:
            raise Exception(ex)



    @classmethod
    def get_cliente(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nome, telefone, cep, complemento, numcpf FROM public.tb_cliente WHERE id = %s", (id,))
                row = cursor.fetchone()

                cliente = None
                if row != None:
                    cliente = Cliente(row[0], row[1], row[2], row[3])
                    cliente = cliente.to_JSON()

                    connection.close()
                    return cliente
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_cliente(self, cliente):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO tb_cliente (nome, telefone, cep, complemento, numcpf)
                VALUES (%s, %s, %s, %s, %s)""", (cliente.nome, cliente.telefone, cliente.cep, cliente.complemento, cliente.numcpf))
                affected_rows = cursor.rowcount
                connection.commit()

                connection.close()
                return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_cliente(self, cliente):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tb_cliente WHERE id = %s", (cliente.id,))
                affected_rows = cursor.rowcount
                connection.commit()

                connection.close()
                return affected_rows
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_cliente(self, cliente):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE tb_cliente SET nome = %s, telefone = %s, cep = %s, complemento = %s, numcpf = %s 
                               WHERE id = %s""", (cliente.nome, cliente.telefone, cliente.cep, cliente.complemento, cliente.numcpf ,cliente.id))
                affected_rows = cursor.rowcount
                connection.commit()
                
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        
    