## Desafio da Semana: 

Fazer um sistema de e-commerce com itens, clientes (com dados), pedidos e status.
- Usando AWS Lambda
- Usando API Gateway
- Pede-se um cuidado com a modelagem.

### Equipe:
Estamos nos aventurando pelo mundo do AWS_SAM por demanda do Labs42_jan23 em parceria com o Itaú. 
Projeto feito pela equipe: Welton (wleite), Gabriel (gissao-m) e Maria Clara (maclara-).

### Pré-requisito:

Abra o docker desktop...\

Já no VsCode inicialize o container:\
`localstack start -d`

# 1 - Iniciando um projeto com o Chalice: 

`chalice-local new-project`

Escolha o nome do projeto\
`[?] Enter the project name: Ecomm`

Escolha a opção "Lambda Functions only"\
`[?] Select your project type: Lambda Functions only : > Lambda Functions only `

### Entre na pasta do projeto Chalice: 

`cd Ecomm`

Para "compilar" o arquivo, na verdade registra as nossas funções nos serviços AWS\
`chalice-local deploy`

### Rode o comando invoke para executar uma função: 
Para ver o retorno da função no terminal:\
`chalice-local invoke -n first_function`

Você verá o retorno da função no terminal:\
`{"hello": "world"}`


Com essa função criada, faremos modificações nela para atender as nossas necessidades....

# 2 - Iniciando um banco de dados para usar com o Chalice:

Ecolhemos o banco de dados Postgres por ser compatível com o Localstack e ter uma boa base de documentação de como utilizá-lo.

Devemos criar o banco de dados
``

E, em seguida, definir uma senha:
``

awslocal rds create-db-instance \
  --db-instance-identifier db1-instance \
  --db-instance-class db.t2.micro \
  --engine postgres \
  --allocated-storage 10 \
  --master-username admin \
  --master-user-password adminpass

awslocal rds create-db-cluster \
  --db-cluster-identifier db1 \
  --engine aurora-postgresql \
  --database-name test \
  --master-username admin \
  --master-user-password adminpass \
  --db-instance-identifier db1-instance \
  --port 5432 \
  --engine-version 10.12

  docker run --name postgres-container -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

  Agora você pode se conectar ao banco de dados PostgreSQL usando um cliente de banco de dados ou uma biblioteca de programação. Use o host localhost, a porta 5432, o nome de usuário postgres e a senha mysecretpassword para se conectar ao banco de dados.

  psql -d postgres -U root -p 5432 -h localhost -W
  psql -h localhost -p 5432 -d postgres -U postgres

  # https://qr0vyeldur.execute-api.localhost.localstack.cloud:4566/api/order