\
<img src="https://img.shields.io/badge/python-3.9.6-blue"/>
<img src="https://img.shields.io/badge/fastapi-0.93.0-orange"/>
<img src="https://img.shields.io/badge/SQLAlchemy-2.0.5-blueviolet"/>
<img src="https://img.shields.io/badge/coverage-96.65%25-darkgreen"/>

# API de CRUD de Produtos
Esta é uma API que permite criar, ler, atualizar e excluir produtos de uma tabela utilizando as tecnologias Python, FastAPI, SQLAlchemy, Alembic e Pydantic.

## Configuração do ambiente
Para executar esta aplicação, você precisará de:

- Docker
- Docker Compose
- Python 3.9 ou superior

## Instalação
Siga os passos abaixo para instalar e configurar a aplicação:

1. Clone o repositório do GitHub:
```commandline
git clone git@github.com:melqui-sa-menezes/mb-challenge.git
```
2. Crie um arquivo .env com as variáveis de ambiente necessárias:
```commandline
cp .env.example .env
```
3. Execute o comando make build para buildar a aplicação e aplicar as migrações do banco de dados:
```commandline
make build
```

## Uso
Para executar a aplicação, execute o seguinte comando:
```commandline
make run
```
Isso iniciará a aplicação e todos os seus contêineres.
Você pode então acessar a API na seguinte URL: http://localhost:8000/docs

#### A API oferece as seguintes rotas:

- GET /product: lista todos os produtos cadastrados.
- GET /product/{product_id}: exibe as informações de um produto específico.
- POST /product: cria um novo produto.
- PATCH /product/{product_id}: atualiza as informações de um produto existente.
- DELETE /product/{product_id}: exclui um produto existente.

### Parar a aplicação
Para parar todos os contêineres da aplicação, execute o seguinte comando:
```commandline
make stop
```
Caso queira parar e remover os containers, execute o seguinte comando:
```commandline
make down
```
### Rodando os testes
Para execução dos testes unitários e de integração, execute o seguinte comando:
```commandline
make test
```

## Migrações do Banco de Dados

### Gerando migrações
Para gerar uma nova migração do banco de dados, execute o seguinte comando:
```commandline
make migration msg="<descrição da migração>"
```
Isso criará um novo arquivo de migração na pasta migrations.

### Aplicando migrações
Para aplicar as migrações do banco de dados, execute o seguinte comando:
```commandline
make migrate
```
Isso aplicará todas as migrações pendentes no banco de dados.

## Observações
Este projeto foi desenvolvido como parte de um desafio do Mercado Bitcoin. 
Sinta-se à vontade para fazer fork deste repositório e adaptá-lo às suas necessidades. 
Se tiver algum problema ou encontrar algum bug, por favor abra uma issue no repositório.
