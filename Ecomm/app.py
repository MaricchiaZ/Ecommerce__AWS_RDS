from chalice import Chalice
import psycopg2
import boto3
import json

# Um aplicativo Chalice, cria automaticamente a configuração necessária no Amazon API Gateway para expor 
# suas rotas de API para o mundo externo e rotear as solicitações HTTP recebidas para as funções Lambda correspondentes no backend.

app = Chalice(app_name='Ecomm')

# AWS Lambda
@app.lambda_function()
def get_order(event, context):
    id_do_usuario=event['ID']
    conn = psycopg2.connect(database="database",
                        host="host.docker.internal",
                        user="user",
                        password="pass",
                        port="4510")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE id={id_do_usuario};") #comando que faz a consulta no banco
    return {"list orders": cursor.fetchone()}
# echo '{"ID":"1053"}' | chalice-local invoke -n first_function


@app.lambda_function()
def new_order(event, context): # itens, user
    id_do_usuario=event['ID']
    status="PROCESSANDO"
    items_pedidos=event['items']
    conn = psycopg2.connect(database="database",
                        host="host.docker.internal",
                        user="user",
                        password="pass",
                        port="4510")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO orders (status, user_id, items) VALUES ('{status}', {id_do_usuario}, ARRAY{items_pedidos});") #comando que insere um novo pedido no banco
    conn.commit()
    cursor.close()
    conn.close()
    return {"new order": "pedido cadastrado com sucesso"}
# echo '{"ID":"5","items":[1, 3]}' | chalice-local invoke -n new_order


@app.lambda_function()
def update_status(event, context):
    id_do_usuario=event['ID']
    conn = psycopg2.connect(database="database",
                        host="host.docker.internal",
                        user="user",
                        password="pass",
                        port="4510")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE orders SET status='APROVADO' WHERE id={id_do_usuario};") #comando que atualiza o status de um pedido para aprovado
    conn.commit()
    cursor.close()
    conn.close()
    return {"Update Status": "pagamento aprovado"}
# UPDATE orders SET status='APROVADO' WHERE id=1;


@app.lambda_function()
def delete_order(event, context):
    id_do_pedido=event['ID']
    conn = psycopg2.connect(database="database",
                        host="host.docker.internal",
                        user="user",
                        password="pass",
                        port="4510")
    cursor = conn.cursor()
    cursor.execute(f"DELETE from orders WHERE id={id_do_pedido};") #comando que atualiza o status de um pedido para aprovado
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
    client = boto3.client('lambda', endpoint_url=("http://host.docker.internal:4566"))
    payload = app.current_request.json_body
    json_payload = json.dumps(payload)  # transformamos um Json válido em uma string, já que Payload só 
    # trabalha com strings
    result = client.invoke(FunctionName='Ecomm-dev-update_status',
                           Payload=json_payload)
    return json.load(result['Payload'])
# echo '{"ID":"5"}' | chalice-local invoke -n update_status
# https://2v3qgzz3sn.execute-api.localhost.localstack.cloud:4566/api/order



@app.route("/order/{ID}", methods=['GET'])
def get_order_api(ID):
    client = boto3.client('lambda', endpoint_url=("http://host.docker.internal:4566"))

    payload = {"ID": ID} #convertemos e recebemos o id passado por parâmetro
    json_payload = json.dumps(payload) # transformamos um Json válido em uma string, já que Payload só 
    # trabalha com strings

    # faz a mesma função que a linha do terminal: echo '{"ID":"2"}' | chalice-local invoke -n get_order
    #o client.invoke é: chalice-local invoke -n get_order
    #o payload é: echo '{"ID":"2"}'.
    result = client.invoke(FunctionName='Ecomm-dev-get_order',
                           Payload=json_payload)
    return json.load(result['Payload'])


@app.route("/order", methods=['POST']) # {"ID":"4","items":[1, 1]}
def receive_an_order():
    client = boto3.client('lambda', endpoint_url=("http://host.docker.internal:4566"))

    #payload = {"ID": app.current_request.json_body[ID], "items": "[2,2]"}
    payload = app.current_request.json_body
    json_payload = json.dumps(payload)  # transformamos um Json válido em uma string, já que Payload só 
    # trabalha com strings
    # app.current_request.json_body => STRING ou JSON(dicionário)
    result = client.invoke(FunctionName='Ecomm-dev-new_order',
                           Payload=json_payload)
    return json.load(result['Payload'])
# https://x2l6kzsp69.execute-api.localhost.localstack.cloud:4566/api/order



@app.route("/order/{ID}", methods=['DELETE'])
def delete_order_api(ID):
    client = boto3.client('lambda', endpoint_url=("http://host.docker.internal:4566"))

    payload = {"ID": ID} #convertemos e recebemos o id passado por parâmetro
    json_payload = json.dumps(payload) # transformamos um Json válido em uma string, já que Payload só 
    # trabalha com strings

    # faz a mesma função que a linha do terminal: echo '{"ID":"2"}' | chalice-local invoke -n get_order
    #o client.invoke é: chalice-local invoke -n get_order
    #o payload é: echo '{"ID":"2"}'.
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