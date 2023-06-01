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

# 2 - Iniciando um banco de dados RDS para usar com o Chalice:

Ecolhemos o banco de dados Postgres por ser compatível com o Localstack e ter uma boa base de documentação de como utilizá-lo.

### Pré-requisitos:
<br>
Biblioteca psycopg2 local

`pip3 install psycopg2-binary`

<br>

Cliente postgress para o terminal\
`sudo apt install postgresql-client`

<br>

Para conectar-se com  banco usaremos a versão já complilada e adaptada da biblioteca psycopg2.
Para isso, no arquivo "requeriments.txt" escreva:\
`aws-psycopg2`

<br>

Para listar as instâncias de banco de dados RDS\
`awslocal rds describe-db-instances`

<br>

Devemos criar o banco de dados\
`awslocal rds create-db-instance --master-username user --master-user-password pass --db-instance-identifier mydb --engine postgres --db-name database --db-instance-class db.t3.small`

<br>

Agora você pode se conectar ao banco de dados PostgreSQL usando um cliente de banco de dados ou uma biblioteca de programação. Use o host localhost, a porta 4510, o nome de usuário postgres e a senha para se conectar ao banco de dados.
`psql -d database -U user -p 4510 -h localhost -W`\
A senha é `pass` e o usuário caso necessário é `user`

<br>

Se quiser sair do banco de dados use:
```sql
exit
```

<br>

... Agora, dentro do banco de dados...
Para exibir as tabelas que temos
```sql
\dt
```

<br>

Criar a tabela de pedidos
```sql
CREATE TABLE orders ( 
id SERIAL PRIMARY KEY,
status VARCHAR(20) NOT NULL,
user_id INTEGER NOT NULL,
items INTEGER[] NOT NULL
);
```

<br>

Criar a tabela de items
```sql
CREATE TABLE items ( 
id SERIAL PRIMARY KEY,
nome VARCHAR(20) NOT NULL
);
```

<br>

Para deletar uma tabela
```sql
DROP TABLE orders;
```

<br>

Para inserir itens na tabela items
```sql
INSERT INTO items (nome) VALUES ('x-salada'), ('misto'), ('hot-dog');
```

<br>

Para inserir itens na tabela pedidos
```sql
INSERT INTO orders (status, user_id, items) VALUES ('APROVADO', '1', ARRAY[1, 2]);
```

<br>

```sql
INSERT INTO orders (status, user_id, items) VALUES ('APROVADO', '2', ARRAY[2, 3]);
```


<br>

```sql
INSERT INTO orders (status, user_id, items) VALUES ('APROVADO', '3', ARRAY[1, 3]);
```

<br>

Para exibir todos os registros de uma tabela
```sql
SELECT * FROM livros;
```

<br>

Para exibir os registros de uma tabela, filtrando por um parâmetro específico
```sql
SELECT * FROM orders WHERE id=1;
```

<br>

Deletando linhas de uma tabela
```sql
DELETE from livros WHERE id=1;
```

<br>

Para fazer um update em uma linha da tabela
```sql
UPDATE livros SET disponivel=1 WHERE id=19;
```

# 3 - Como testar a API: 

### POST

`https://x2l6kzsp69.execute-api.localhost.localstack.cloud:4566/api/order/`

#### BODY:
```json
{
  "ID": "1",
  "items": [
    1,
    2
  ]
}
```

```json
{
  "ID": "2",
  "items": [
    1,
    3
  ]
}
```

```json
{
  "ID": "3",
  "items": [
    1,
    3,
    2
  ]
}
```

<br>

### GET
`https://x2l6kzsp69.execute-api.localhost.localstack.cloud:4566/api/order/2`

<br>

### UPDATE 
`https://2v3qgzz3sn.execute-api.localhost.localstack.cloud:4566/api/order`

#### BODY:
```json
{
  "ID": "2"
}
```
<br>

### DELETE
`https://n0q4zv02w2.execute-api.localhost.localstack.cloud:4566/api/order/2`

<br>
<br>


## Extra:

### Comandos amigos:

Para listar todas as funções lambdas\
`awslocal lambda list-functions | grep FunctionName`

Para passar algum parâmetro para uma funçao lambda específica\
`echo '{"ID":"1053"}' | chalice-local invoke -n get_order`

Para logar nos serviços pagos da Localsatck\
`export LOCALSTACK_API_KEY=sua_key`  Essa key você pega na sua página de usuário da localstak




