# Arquitetura da Plataforma de Automação de Testes

## 1. Visão geral
A plataforma é composta por um backend Flask responsável por gerenciar clientes, roteiros, casos de teste, execuções, logs e evidências, além de integrar um motor RPA via fila de tarefas Celery/Redis. O frontend é uma SPA React com Vite para oferecer uma interface web para cadastro, execução e acompanhamento de testes.

## 2. Objetivo do sistema
Permitir que times de QA e automação:
- cadastrem clientes e sistemas;
- criem conectores inteligentes para sites e sistemas externos;
- definam casos de teste com dados e expectativas;
- executem testes de forma assíncrona;
- acompanhem logs, evidências e status de execução.

## 3. Arquitetura atual do MVP

### 3.1 Frontend
- Framework: React + Vite
- Roteamento: React Router
- Estilo: CSS simples e escalável
- Comunicação: consumo de APIs REST via camada de serviços
- Responsabilidade: capturar ações do usuário, exibir status e acompanhar execuções

### 3.2 Backend
- Framework: Flask
- ORM: SQLAlchemy
- Autenticação: JWT
- Tarefas assíncronas: Celery + Redis
- Armazenamento: SQLite em desenvolvimento, com possibilidade de PostgreSQL em produção
- Estrutura modular por domínio:
  - auth
  - clientes
  - conectores
  - roteiros
  - testes
  - execucoes
  - logs
  - evidencias
  - core
  - tasks
  - database

### 3.3 Motor RPA
A camada de automação é composta por um registry de executores com abstração para:
- Python
- Playwright
- Selenium

Hoje, a execução é ainda um fluxo preparado para integração. O objetivo do próximo ciclo é implementar um executor real baseado em Playwright para interpretar os passos salvos no conector e produzir logs/evidências.

## 4. Estrutura de pastas

```text
frontend/
  src/
    pages/
    services/
    components/
    hooks/
    contexts/
    App.jsx
    main.jsx
    main.css

backend/
  app/
    auth/
    clientes/
    conectores/
    roteiros/
    testes/
    execucoes/
    logs/
    evidencias/
    core/
    database/
    tasks/
```

## 5. Fluxo principal de execução
1. O usuário autentica-se no frontend.
2. O frontend cria ou consulta clientes, conectores, roteiros e casos.
3. O backend armazena o modelo de execução e os passos do conector.
4. Ao executar um caso, o backend cria uma execução e enfileira uma tarefa no Celery.
5. O worker carrega o conector, resolve valores de runtime e executa os passos no navegador.
6. Logs, screenshots e artefatos são gravados e disponibilizados via API.

## 6. Modelo de dados principal
- Cliente: nome, e-mail e responsável
- Conector: nome, URL base, ambiente, versão, status, credenciais de referência e passos
- Roteiro: cliente associado, arquivo e status
- CasoTeste: roteiro associado, nome, objetivo, dados, resultado esperado e status
- Execucao: caso associado, início, fim, status, tempo e identificador do worker
- Log: execução associada, nível e mensagem
- Evidencia: execução associada, arquivo e tipo

## 7. Regras de implementação
- Manter backend e frontend desacoplados.
- Utilizar rotas REST padronizadas.
- Expor respostas JSON consistentes para o frontend.
- Tratar erros de execução com status claro e logs estruturados.
- Evitar lógica de negócio no frontend; usar o backend como fonte de verdade.
- Tratar cada integração como um conector versionado, não como um script improvisado.

## 8. Padrão de execução RPA
O motor de automação não deve adivinhar os caminhos de um portal externo. Ele deve receber um conector com passos estruturados e executá-los de forma determinística.

### 8.1 Ações suportadas
- `goto`: navegação para uma URL
- `fill`: preenchimento de campo
- `click`: clique em elemento
- `select`: seleção de opção
- `wait`: espera por condição ou elemento
- `assert`: verificação de resultado
- `download`: disparo de download

### 8.2 Requisitos para um conector robusto
- identificação do sistema: nome, URL base, ambiente e cliente;
- referências seguras para credenciais, nunca em texto aberto no fluxo;
- lista ordenada de ações com seletores e alternativas;
- regras de espera e timeout;
- critérios de sucesso baseados em assertions ou artefatos;
- política de evidências com screenshots e arquivos coletados.

## 9. Fluxo operacional recomendado para o próximo ciclo
1. O usuário cadastra um sistema externo.
2. A plataforma salva um conector com passos e seletores.
3. O usuário associa esse conector a um caso de teste.
4. O backend cria uma execução assíncrona.
5. O worker executa o fluxo em navegador e registra logs/evidências.
6. O frontend mostra o acompanhamento e os resultados finais.

## 10. Implicação arquitetural
A plataforma não deve ser vista apenas como um painel de automações. Ela precisa evoluir para um orquestrador de conectores inteligentes, versionados, executáveis, observáveis e fáceis de manter. Essa abordagem preserva a robustez de automações programadas, reduz a barreira para usuários não técnicos e prepara o produto para incorporar IA com segurança no futuro.
