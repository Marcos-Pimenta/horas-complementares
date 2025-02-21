# 📌 Projeto Horas Complementares

Este projeto é um sistema web desenvolvido para auxiliar no controle e gerenciamento de horas complementares. Ele permite que os usuários registrem, acompanhem e gerenciem suas atividades, garantindo um melhor controle das horas necessárias para sua formação acadêmica.

## 🚀 Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **Banco de Dados:** SQLite (arquivo `db/database.db`)
- **Gerenciamento de Dependências:** `requirements.txt`

## 📂 Estrutura do Projeto

```
📦 Horas-Complementares
├── 📂 venv (Ambiente virtual)
├── 📂 migrations (Gerenciamento do banco de dados)
├── 📂 static (Arquivos estáticos)
│   ├── styles.css
│   ├── script.js
│
├── 📂 templates (Páginas HTML)
│   ├── index.html
│   ├── relatorio.html
│   ├── profile.html
│
├── 📂 db (Banco de dados SQLite)
│   ├── database.db
│
├── .env (Configurações do ambiente)
├── app.py (Código principal da aplicação)
├── auth.py (Autenticação de usuários)
├── models.py (Modelos do banco de dados com SQLAlchemy)
├── requirements.txt (Dependências do projeto)
├── README.md (Este arquivo)
```

## 🛠️ Configuração e Instalação

Para rodar o projeto localmente, siga os passos abaixo:

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd Horas-Complementares
```

### 2️⃣ Criar e ativar o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3️⃣ Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Inicializar o banco de dados
O banco de dados SQLite é criado automaticamente ao iniciar o projeto. Caso necessário, exclua `database.db` para recriá-lo.

Se houver mudanças no modelo (`models.py`), utilize:
```bash
flask db migrate -m "Atualizando tabelas"
flask db upgrade
```

### 5️⃣ Executar o projeto
```bash
python app.py
```
Acesse no navegador: `http://127.0.0.1:5000/`

## 🔑 Usuários de Teste
O projeto já inclui os seguintes usuários de teste cadastrados no banco de dados:
| Usuário  | Senha  |
|----------|--------|
| Marcos   | 1234   |
| Marina   | 1234   |
| João     | 1234   |

## 📝 Estrutura do Banco de Dados
As tabelas **usuario** e **atividade** armazenam informações de usuários e atividades cadastradas, com relação baseada no `user_id`.

## 🛠️ Ferramentas para Visualização do Banco
Para inspecionar as tabelas e os dados armazenados, foi utilizado o **SQLite Explorer** no VS Code.

## 🔧 Comandos Úteis

### Ambiente Virtual
```bash
python -m venv venv  # Criar ambiente virtual
venv\Scripts\activate  # Ativar no Windows
source venv/bin/activate  # Ativar no Linux/Mac
deactivate  # Desativar
```

### Instalação de Dependências
```bash
pip install flask flask-sqlalchemy
pip freeze > requirements.txt  # Salvar dependências
```

### Gerenciamento do Banco de Dados
```bash
flask db migrate -m "Atualizando tabelas"
flask db upgrade
```

## 📜 Licença
Este projeto está sob a licença MIT. Sinta-se livre para modificar e compartilhar!

## 🤝 Contribuição
Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do projeto
2. Crie um branch (`git checkout -b minha-feature`)
3. Faça suas alterações e commit (`git commit -m 'Minha nova feature'`)
4. Envie um push para o branch (`git push origin minha-feature`)
5. Abra um Pull Request!


