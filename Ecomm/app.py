from chalice import Chalice

app = Chalice(app_name='Ecomm')

# AWS Lambda
@app.lambda_function()
def first_function(event, context):
    return {'hello': 'world'}

# AWS Gateway
@app.route("/order", methods=['POST'])
def receive_an_order():
    return {'hello': app.current_request.json_body}

# AWS Gateway
@app.route("/order", methods=['PATCH'])
def update_an_order():
    return {'hello': app.current_request.json_body}

@app.route("/order/{ID}", methods=['GET'] )
def get_order(ID):
    return ID

    
# https://43slci3gy8.execute-api.localhost.localstack.cloud:4566/api/order