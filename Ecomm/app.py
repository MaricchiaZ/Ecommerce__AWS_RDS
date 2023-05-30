from chalice import Chalice
import psycopg2
app = Chalice(app_name='Ecomm')

# host = "localhost"
# port = 4510
# dbname = "database"
# user = "user"
# password = "pass"

conn = psycopg2.connect(database="database",
                        host="localhost",
                        user="user",
                        password="pass",
                        port="4510")

# hostname = 'localhost'
# username = 'user'
# password = 'pass'
# database = 'database'
# port = '4510'

# AWS Lambda
@app.lambda_function()
def first_function(event, context):
    return {'hello': 'world'}


# AWS Gateway
@app.route("/order", methods=['POST'])
def receive_an_order():
    return {'hello': app.current_request.json_body}


@app.route("/order", methods=['PATCH'])
def update_an_order():
    return {'hello': app.current_request.json_body}


@app.route("/order/{ID}", methods=['GET'])
def get_order(ID):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders;")
    return {"hello": cursor.fetchall()}
    # return {'hello': 'world'}

# A partir daqui, você pode esperar a criação da instância do RDS ser concluída e, em seguida, poderá se conectar a ela usando um cliente PostgreSQL, como o psql ou qualquer outro cliente compatível.


# Sim, você pode usar a biblioteca psycopg2 no Chalice para se conectar ao seu banco de dados RDS.
# No entanto, o erro que você está enfrentando ocorre porque o Chalice não fornece suporte direto
# para a instalação de dependências como a psycopg2.

# O Chalice usa um diretório chamado "vendor" para incluir as dependências necessárias no pacote de
# implantação do Chalice. Para usar a biblioteca psycopg2, você precisará instalar e "vendê-la"
# manualmente dentro do diretório "vendor" do seu projeto Chalice.

# Aqui estão os passos que você pode seguir para fazer isso:

# Crie um diretório chamado "vendor" no diretório raiz do seu projeto Chalice, caso ainda não exista.

# Instale a biblioteca psycopg2 no seu ambiente local usando o pip. Certifique-se de estar usando a
# mesma versão do Python que está sendo usado pelo Chalice.

# Após a instalação do psycopg2, você encontrará um diretório chamado "psycopg2" no diretório
# "site-packages" do seu ambiente Python. Copie o diretório "psycopg2" para o diretório "vendor"
# do seu projeto Chalice.

# Agora, dentro do diretório "vendor", você terá um diretório "psycopg2" contendo os arquivos da biblioteca.

# No seu código do Chalice, você pode importar e usar a biblioteca psycopg2 normalmente.

# Certifique-se de adicionar o diretório "vendor" ao controle de versão do seu projeto, para que as
# dependências sejam incluídas corretamente ao implantar o projeto em outro ambiente.

# Lembre-se de que a biblioteca psycopg2 depende de algumas bibliotecas C subjacentes,
# como o PostgreSQL. Portanto, ao implantar seu projeto Chalice em um ambiente diferente,
# certifique-se de que todas as bibliotecas necessárias estejam disponíveis nesse ambiente.

# Obtendo os resultados
# results = cursor.fetchall()

# # Iterando sobre os resultados
# for row in results:
#     print(row)

# # Fechando o cursor e a conexão
# cursor.close()
# conn.close()

# https://43slci3gy8.execute-api.localhost.localstack.cloud:4566/api/order
