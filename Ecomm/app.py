from chalice import Chalice
import psycopg2
app = Chalice(app_name='Ecomm')

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
    conn = psycopg2.connect(database="database",
                        host="host.docker.internal",
                        user="user",
                        password="pass",
                        port="4510")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders;")
    return {"hello": cursor.fetchall()}
