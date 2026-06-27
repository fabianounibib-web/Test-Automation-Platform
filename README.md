# Test-Automation-Platform

A Test Automation Platform é uma aplicação web para gerenciar clientes, roteiros de teste, casos de teste, execuções e evidências em um fluxo simples e centralizado. A plataforma foi pensada para apoiar times de QA e automação na organização de cenários, acompanhamento de execução e rastreio de resultados.

## Visão geral

A aplicação possui um backend em Flask e um frontend em React com Vite. Ela permite:

- cadastrar e listar clientes;
- importar roteiros de teste;
- gerar casos de teste a partir de arquivos enviados;
- executar casos de teste;
- acompanhar execuções, logs e evidências;
- autenticar usuários com JWT.

## Arquitetura

- Backend: Flask + SQLAlchemy + Flask-JWT-Extended + Celery + Redis
- Frontend: React + Vite + React Router
- Banco de dados: PostgreSQL (em Docker) ou SQLite para execução local simples
- Containerização: Docker Compose

## Estrutura do projeto

- backend/: API e lógica de negócios
- frontend/: interface web
- storage/: diretório para uploads, logs e evidências
- docker-compose.yml: orquestração do ambiente completo

## Requisitos

- Docker e Docker Compose
- Node.js 20+
- Python 3.12+
- pip

## Como executar localmente

### Usando Docker Compose

1. Na raiz do projeto, execute:
   ```bash
   docker compose up --build
   ```
2. Acesse:
   - frontend: http://localhost:3000
   - backend: http://localhost:5000
   - nginx: http://localhost/

### Executando apenas o backend localmente

1. Entre na pasta backend:
   ```bash
   cd backend
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python run.py
   ```

### Executando o frontend localmente

1. Entre na pasta frontend:
   ```bash
   cd frontend
   ```
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

## Fluxo de uso

1. Acesse a interface e crie uma conta ou faça login.
2. Cadastre um cliente.
3. Acesse a página de roteiros e faça o upload de um arquivo de roteiro.
4. O sistema salva o arquivo e cria automaticamente um caso de teste associado.
5. Na página de casos, execute o caso e acompanhe o resultado.
6. Consulte logs e evidências nas páginas correspondentes.

## Como construir o arquivo de roteiro para upload

O upload de roteiro é feito através da tela de roteiros ou da API. O arquivo enviado é salvo no diretório de uploads e, em seguida, é convertido em um caso de teste inicial pelo backend.

### Formato recomendado

O arquivo pode ser um texto simples com estrutura organizada em blocos. Um formato simples e legível é:

```text
Nome do roteiro
================
Cliente: Empresa Exemplo
Objetivo: Validar o fluxo de login do sistema

Cenário 1
---------
Passo 1: Acessar a tela inicial
Passo 2: Informar usuário e senha
Passo 3: Clicar em Entrar
Resultado esperado: O usuário é autenticado com sucesso

Cenário 2
---------
Passo 1: Acessar a tela de recuperação de senha
Passo 2: Informar e-mail válido
Passo 3: Enviar solicitação
Resultado esperado: O sistema exibe mensagem de sucesso
```

### Regras práticas para montar o roteiro

- Use títulos claros para cada cenário.
- Liste os passos em ordem cronológica.
- Defina o resultado esperado para cada cenário.
- Mantenha o conteúdo simples e objetivo, pois ele servirá como base para a geração do caso de teste.
- O arquivo pode ter extensão .txt, .md ou outro formato de texto simples.

### Exemplo de roteiro mínimo

```text
Roteiro de Login
================
Objetivo: Validar login com credenciais válidas

Cenário: Login com sucesso
Passo 1: Abrir a aplicação
Passo 2: Informar usuário válido
Passo 3: Informar senha válida
Passo 4: Clicar em Entrar
Resultado esperado: O sistema redireciona para a área principal
```


## Conectores inteligentes

A plataforma não espera que o robô "adivinhe" como navegar em um sistema externo. Cada portal deve ser representado por um conector inteligente, que ensina ao motor de automação quais campos preencher, quais botões clicar, quais telas acessar e quais evidências coletar.

O caminho recomendado para o produto é combinar:

- **Mapeamento visual**: o usuário aponta, em um assistente, os campos de usuário, senha, login, faturas e download.
- **Gravação de fluxo**: o usuário executa o processo manualmente uma vez enquanto a plataforma registra os passos.
- **Execução interpretada**: o backend salva a sequência de ações e o motor RPA reproduz o fluxo quando um caso de teste solicitar aquele processo.

Exemplo simplificado de fluxo salvo:

```json
[
  { "action": "goto", "url": "https://xpto.com" },
  { "action": "fill", "selector": "#usuario", "value": "${usuario}" },
  { "action": "fill", "selector": "#senha", "value": "${senha}" },
  { "action": "click", "selector": "#entrar" },
  { "action": "click", "selector": "#menu_faturas" },
  { "action": "download", "selector": "#download" }
]
```

Quando o portal muda, o conector deve usar uma camada de resolução inteligente de elementos, tentando localizar os componentes por CSS, ID, `name`, texto visível, label, papel acessível e XPath como fallback. Mais detalhes estão descritos em `ARCHITECTURE.md`.

## Autenticação

A API usa JWT para proteger os endpoints. O token é retornado no login e deve ser enviado no cabeçalho de autorização nas requisições subsequentes.

## Testes

Para validar o backend, execute:

```bash
cd backend
pytest
```

## Observações

- O projeto está em evolução inicial e o foco atual é oferecer um fluxo funcional de cadastro, gestão e execução de testes.
- Os arquivos de evidência, logs e uploads ficam salvos em diretórios sob a pasta storage.
