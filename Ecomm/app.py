from chalice import Chalice
import psycopg2
import boto3
import json

# Um aplicativo Chalice, cria automaticamente a configuração necessária no Amazon API Gateway para expor
# suas rotas de API para o mundo externo e rotear as solicitações HTTP recebidas para as funções Lambda correspondentes no backend.
# fazer uma query(consulta) SQL que substitua o ID pelo nome.

#
app = Chalice(app_name='Ecomm')

# SELECT orders.id, orders.status, users.nome, orders.items
# FROM orders
# JOIN users ON orders.user_id = users.id
# WHERE orders.id = 3;

# AWS Lambda


@app.lambda_function()
def get_order(event, context):
    id_user = event['ID']
#    nome_user=(f"SELECT * FROM users WHERE id={id_do_usuario};")
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    cursor.execute(f"SELECT orders.id, orders.status, users.nome, \
       ARRAY(SELECT items.nome FROM items WHERE items.id = ANY(orders.items)) as item_nomes\
        FROM orders JOIN users ON orders.user_id = users.id WHERE orders.id = {id_user};")  # comando que faz a consulta no banco
    return {"list orders": cursor.fetchone()}


@app.lambda_function()
def get_order_name(event, context):
    name_user = event['nome']
#    nome_user=(f"SELECT * FROM users WHERE id={id_do_usuario};")
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT orders.id, orders.status, users.nome,
                   ARRAY(SELECT items.nome FROM items WHERE items.id=ANY(orders.items)) as item_nomes
                   FROM orders JOIN users ON orders.user_id=users.id
                   WHERE users.nome='{name_user}';""")  # comando que faz a consulta no banco
    return {"list orders": cursor.fetchall()}
# echo '{"nome":"Igor"}' | chalice-local invoke -n get_order_name


# @app.lambda_function()
# def new_order(event, context): # itens, user
#     id_do_usuario=event['ID']
#     status="PROCESSANDO"
#     items_pedidos=event['items']
#     conn = psycopg2.connect(database="database",
#                         host="host.docker.internal",
#                         user="user",
#                         password="pass",
#                         port="4510")
#     cursor = conn.cursor()
#     cursor.execute(f"INSERT INTO orders (status, user_id, items) VALUES ('{status}', {id_do_usuario}, ARRAY{items_pedidos});") #comando que insere um novo pedido no banco
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"new order": "pedido cadastrado com sucesso"}

@app.lambda_function()
def new_order(event, context):  # itens, user
    id_do_usuario = event['nome']
    status = "PROCESSANDO"
    items_pedidos = event['items']
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    # cursor.execute(f"INSERT INTO orders (status, user_id, items) VALUES ('{status}', {id_do_usuario}, ARRAY{items_pedidos});") #comando que insere um novo pedido no banco
    cursor.execute(f"WITH user_info AS (SELECT id FROM users WHERE nome = '{id_do_usuario}'),\
    insert_user AS (INSERT INTO users (nome) SELECT '{id_do_usuario}'\
    WHERE NOT EXISTS (SELECT 1 FROM user_info) RETURNING id)\
    INSERT INTO orders (status, user_id, items) SELECT '{status}',\
    COALESCE((SELECT id FROM user_info), (SELECT id FROM insert_user)), ARRAY{items_pedidos};")
    conn.commit()
    cursor.close()
    conn.close()
    return {"new order": "pedido cadastrado com sucesso"}
# echo '{"ID":"5","items":[1, 3]}' | chalice-local invoke -n new_order


@app.lambda_function()
def update_status(event, context):
    id_do_usuario = event['ID']
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    # comando que atualiza o status de um pedido para aprovado
    cursor.execute(
        f"UPDATE orders SET status='APROVADO' WHERE id={id_do_usuario};")
    conn.commit()
    cursor.close()
    conn.close()
    return {"Update Status": "pagamento aprovado"}
# UPDATE orders SET status='APROVADO' WHERE id=1;


@app.lambda_function()
def delete_order(event, context):
    id_do_pedido = event['ID']
    conn = psycopg2.connect(database="database",
                            host="host.docker.internal",
                            user="user",
                            password="pass",
                            port="4510")
    cursor = conn.cursor()
    # comando que atualiza o status de um pedido para aprovado
    cursor.execute(f"DELETE from orders WHERE id={id_do_pedido};")
    conn.commit()
    cursor.close()
    conn.close()
    return {"Deleted order": "pedido cancelado"}
# DELETE from orders WHERE id=1;


# INSERT INTO orders (status, user_id, items) VALUES ('APROVADO', '1', ARRAY[1, 2]);
# {"new order": [2, "PROCESSANDO", 2, [3, 2]]}
# {
# status: "PROCESSANDO"\,
# items:
#    [
#      id: 1,
#      id: 2
#    ]
# }

# ------------------------------------------------------------------

# AWS Gateway


@app.route("/order", methods=['PATCH'])
def update_an_order():
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))
    payload = app.current_request.json_body
    # transformamos um Json válido em uma string, já que Payload só
    json_payload = json.dumps(payload)
    # trabalha com strings
    result = client.invoke(FunctionName='Ecomm-dev-update_status',
                           Payload=json_payload)
    return json.load(result['Payload'])
# echo '{"ID":"5"}' | chalice-local invoke -n update_status
# https://mmwdi1i8c3.execute-api.localhost.localstack.cloud:4566/api/order


@app.route("/order/user/{nome}", methods=['GET'])
def get_order_name_api(nome):
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))

    # convertemos e recebemos o id passado por parâmetro
    payload = {"nome": nome}
    # transformamos um Json válido em uma string, já que Payload só
    json_payload = json.dumps(payload)
    # trabalha com strings

    # faz a mesma função que a linha do terminal: echo '{"nome":"Igor"}' | chalice-local invoke -n get_order
    # o client.invoke é: chalice-local invoke -n get_order_name
    # o payload é: echo '{"nome":"Igor"}'.
    result = client.invoke(FunctionName='Ecomm-dev-get_order_name',
                           Payload=json_payload)
    return json.load(result['Payload'])

# "/order/1"
# "/order/user/Igor"

# query params
# query string

# "/order?nome=Igor"


@app.route("/order/{var}", methods=['GET'])
def get_order_api(var):
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))

    if (var.isdigit()):
        # convertemos e recebemos o id passado por parâmetro
        payload = {"ID": var}
        # transformamos um Json válido em uma string, já que Payload só
        json_payload = json.dumps(payload)
        # trabalha com strings

        # faz a mesma função que a linha do terminal: echo '{"ID":"2"}' | chalice-local invoke -n get_order
        # o client.invoke é: chalice-local invoke -n get_order
        # o payload é: echo '{"ID":"2"}'.
        result = client.invoke(FunctionName='Ecomm-dev-get_order',
                               Payload=json_payload)
        return json.load(result['Payload'])
    else:
        payload = {"nome": var}
        # transformamos um Json válido em uma string, já que Payload só
        json_payload = json.dumps(payload)
        # trabalha com strings

        # faz a mesma função que a linha do terminal: echo '{"nome":"Igor"}' | chalice-local invoke -n get_order
        # o client.invoke é: chalice-local invoke -n get_order_name
        # o payload é: echo '{"nome":"Igor"}'.
        result = client.invoke(FunctionName='Ecomm-dev-get_order_name',
                               Payload=json_payload)
        return json.load(result['Payload'])


# @app.route("/order/{ID}", methods=['GET'])
# def get_order_api(ID):
#     client = boto3.client('lambda', endpoint_url=(
#         "http://host.docker.internal:4566"))

#     payload = {"ID": ID}  # convertemos e recebemos o id passado por parâmetro
#     # transformamos um Json válido em uma string, já que Payload só
#     json_payload = json.dumps(payload)
#     # trabalha com strings

#     # faz a mesma função que a linha do terminal: echo '{"ID":"2"}' | chalice-local invoke -n get_order
#     # o client.invoke é: chalice-local invoke -n get_order
#     # o payload é: echo '{"ID":"2"}'.
#     result = client.invoke(FunctionName='Ecomm-dev-get_order',
#                            Payload=json_payload)
#     return json.load(result['Payload'])


@app.route("/order", methods=['POST'])  # {"ID":"4","items":[1, 1]}
def receive_an_order():
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))

    # payload = {"ID": app.current_request.json_body[ID], "items": "[2,2]"}
    payload = app.current_request.json_body
    # transformamos um Json válido em uma string, já que Payload só
    json_payload = json.dumps(payload)
    # trabalha com strings
    # app.current_request.json_body => STRING ou JSON(dicionário)
    result = client.invoke(FunctionName='Ecomm-dev-new_order',
                           Payload=json_payload)
    return json.load(result['Payload'])
# https://e0f0uaiay3.execute-api.localhost.localstack.cloud:4566/api/order


@app.route("/order/{ID}", methods=['DELETE'])
def delete_order_api(ID):
    client = boto3.client('lambda', endpoint_url=(
        "http://host.docker.internal:4566"))

    payload = {"ID": ID}  # convertemos e recebemos o id passado por parâmetro
    # transformamos um Json válido em uma string, já que Payload só
    json_payload = json.dumps(payload)
    # trabalha com strings

    # faz a mesma função que a linha do terminal: echo '{"ID":"2"}' | chalice-local invoke -n get_order
    # o client.invoke é: chalice-local invoke -n get_order
    # o payload é: echo '{"ID":"2"}'.
    result = client.invoke(FunctionName='Ecomm-dev-delete_order',
                           Payload=json_payload)
    return json.load(result['Payload'])
# https://n0q4zv02w2.execute-api.localhost.localstack.cloud:4566/api/order/2


# https://cuwgd8cwng.execute-api.us-east-1.amazonaws.com/api/
# https://erksxun64s.execute-api.localhost.localstack.cloud:4566/api/order/2


# COMO TESTAR


# POST
# https://x2l6kzsp69.execute-api.localhost.localstack.cloud:4566/api/order/

# BODY:

# {
#   "ID": "1",
#   "items": [
#     1,
#     3
#   ]
# }


# BODY:
# {
#   "ID": "2",
#   "items": [
#     1,
#     2
#   ]
# }


# GET
#  https://x2l6kzsp69.execute-api.localhost.localstack.cloud:4566/api/order/2


# UPDATE
#  https://2v3qgzz3sn.execute-api.localhost.localstack.cloud:4566/api/order

# BODY:
# {
#   "ID": "2"
# }


# DELETE
#  https://n0q4zv02w2.execute-api.localhost.localstack.cloud:4566/api/order/2
