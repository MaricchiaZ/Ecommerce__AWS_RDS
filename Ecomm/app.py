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
    #cursor.execute(f"SELECT * FROM orders WHERE id={id_do_usuario};") #comando que faz a consulta no banco
    # cursor.execute(f"INSERT INTO orders (status, user_id, items) VALUES ({status}, {id_do_usuario}, ARRAY[{items_pedidos}]);") #comando que faz a consulta no banco
    # cursor.execute(f"INSERT INTO orders (status, user_id, items) VALUES ({status}, {id_do_usuario}, ARRAY[1, 2]);") #comando que faz a consulta no banco
    cursor.execute("INSERT INTO orders (status, user_id, items) VALUES ('APROVADO', '6', ARRAY[1, 2]);") #comando que faz a consulta no banco
    conn.commit()
    cursor.close()
    conn.close()
    # return {"new order": cursor.fetchone()}
    return {"new order": event}

# {{"ID":"5"},{"items":"1","3"}}

# {"ID":"5","items":[1, 3]}

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

# # AWS Gateway
# @app.route("/order", methods=['POST'])
# def receive_an_order():
#     return {'hello': app.current_request.json_body}


# @app.route("/order", methods=['PATCH'])
# def update_an_order():
#     return {'hello': app.current_request.json_body}

# ------------------------------------------------------------------

# @app.route("/order/{ID}", methods=['GET'])
# def get_order_api(ID):
#     client = boto3.client('lambda', endpoint_url=("http://host.docker.internal:4566"))

#     payload = {"ID": ID} #convertemos recebemos o id passado por parâmetro
#     json_payload = json.dumps(payload) # transformamos um Json válido em uma string, já que Payload só 
#     # trabalha com strinhs

#     # faz a mesma função que a linha do terminal: echo '{"ID":"2"}' | chalice-local invoke -n get_order
#     #o client.invoke é: chalice-local invoke -n get_order
#     #o payload é: echo '{"ID":"2"}'.
#     result = client.invoke(FunctionName='Ecomm-dev-get_order',
#                            Payload=json_payload)
#     return json.load(result['Payload'])


# response = client.invoke(
#     FunctionName='string',
#     InvocationType='Event'|'RequestResponse'|'DryRun',
#     LogType='None'|'Tail',
#     ClientContext='string',
#     Payload=b'bytes'|file,
#     Qualifier='string'
# )


# https://cuwgd8cwng.execute-api.us-east-1.amazonaws.com/api/
# https://erksxun64s.execute-api.localhost.localstack.cloud:4566/api/order/2
