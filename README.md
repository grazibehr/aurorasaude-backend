### `Pós-Graduação em Desenvolvimento FullStack @PUC-RIO – MVP` 

# 🌌 Aurora Saúde – Backend

API desenvolvida em **Python + Flask** para o MVP **Aurora Saúde**, um app de controle doméstico de sintomas e doenças.  
O backend fornece endpoints REST para autenticação de usuário, cadastro de sintomas e registros de saúde de usuários.

---

## Funcionalidades

-  Autenticação de usuários com **JWT (Bearer Token)**
-  Registro de sintomas por usuário (com nível de dor, notas, data etc.)
-  Integração com frontend (Aurora Saúde Web)
-  Documentação automática via **Swagger UI**

---

## Tecnologias

- **Linguagem:** Python 3.12
- **Framework Web:** Flask + flask-openapi3
- **Banco de Dados:** SQLite3
- **Validações:** Pydantic
- **Autenticação:** JWT
- **Outros:** dotenv, CORS, Werkzeug

---
## Estrutura do Projeto

```bash
backend/
│── modules/             
│   ├── auth/             # Autenticação e JWT
│   ├── sintomas/         # Sintomas gerais
│   └── usuario/sintomas/ # Sintomas do usuário
│
│── sql/                  # Scripts de criação do banco
│── data_base.py          
│── app.py                
│── requirements.txt     
│── README.md   
```   
---

## Como rodar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/grazibehr/aurorasaude-backend.git

cd aurorasaude-backend
```
---

### 2. Criar ambiente virtual
```bash
python -m venv venv

.\venv\Scripts\activate   # Windows

source venv/bin/activate  # Linux
```
---

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```
---

### 4. Configurar variáveis de ambiente
```bash
Crie um arquivo `.env` na raiz baseado em:

SECRET_KEY=exemplo
```
---

### 5. Rodar o servidor
```bash
  flask run
```
---

### 6. Documentação da API - Swagger

Após iniciar o servidor, acesse a documentação:

👉 [http://127.0.0.1:5000/openapi/swagger](http://127.0.0.1:5000/openapi/swagger)

 Para acessar as rotas que exigem autenticação, é necessário informar o token de acesso recebido ao realizar login (/auth/login).
 ```bash
 1 - No Swagger, clique no botão Authorize (canto superior direito).
 2 - No campo de autenticação, insira o token recebido.
 3 - Clique em Authorize e depois em Close.

A partir desse momento, todas as requisições protegidas no Swagger já estarão autenticadas.
 ```
---

## 👩‍💻 Autoria

Desenvolvido por [@grazielabehrens](https://github.com/grazibehr)              
Desenvolvedora FullStack • Graduada em Ciência da Computação  
Pós-graduanda em Desenvolvimento FullStack – PUC-Rio
LinkedIn: [linkedin.com/in/grazielabehrens](https://www.linkedin.com/in/grazielabehrens/) 
