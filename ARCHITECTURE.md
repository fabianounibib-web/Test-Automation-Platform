# Arquitetura da Plataforma de Automação de Testes

## 1. Visão geral
A plataforma é composta por um backend Flask responsável por gerenciar clientes, roteiros, casos de teste, execuções, logs e evidências, além de integrar com um motor RPA via fila de tarefas Celery/Redis.

O frontend será uma aplicação React com Vite para oferecer uma interface web moderna para cadastro, execução e acompanhamento de testes.

## 2. Objetivo do sistema
Permitir que times de QA e automação:
- cadastrem clientes e sistemas;
- façam upload de roteiros de automação;
- definam casos de teste com dados e expectativas;
- executem testes de forma assíncrona;
- acompanhem logs, evidências e status de execução.

## 3. Arquitetura proposta

### 3.1 Backend
- Framework: Flask
- ORM: SQLAlchemy
- Autenticação: JWT (planejado)
- Tarefas assíncronas: Celery + Redis
- Armazenamento: PostgreSQL
- Estrutura modular por domínio:
  - auth
  - clientes
  - roteiros
  - testes
  - execucoes
  - logs
  - evidencias
  - core
  - tasks
  - database

### 3.2 Frontend
- Framework: React + Vite
- Roteamento: React Router
- Estilo: CSS simples e escalável, com possibilidade de evolução para Tailwind ou MUI
- Comunicação: consumo de APIs REST via fetch/axios

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
```

backend/
  app/
    auth/
    clientes/
    roteiros/
    testes/
    execucoes/
    logs/
    evidencias/
    core/
    database/
    tasks/
```

## 5. Fluxo principal
1. O usuário autentica-se no frontend.
2. O frontend cria ou consulta clientes, roteiros e casos.
3. O backend armazena os dados no banco.
4. Ao executar um caso, o backend enfileira uma tarefa no Celery.
5. O worker executa o fluxo no motor RPA.
6. Resultados, logs e evidências são gravados no banco e disponibilizados via API.

## 6. Modelo de dados principal
- Cliente: nome, e-mail, responsável
- Roteiro: cliente associado, arquivo, status
- CasoTeste: roteiro associado, nome, objetivo, dados, resultado esperado, status
- Execucao: caso associado, início, fim, status, tempo, identificador do RPA
- Log: execução associada, nível, mensagem
- Evidencia: execução associada, arquivo, tipo

## 7. Regras de implementação
- Manter o backend e o frontend desacoplados.
- Utilizar rotas REST padronizadas.
- Expor resposta JSON consistente para o frontend.
- Tratar erros de execução com status e logs claros.
- Evitar lógica de negócio no frontend; usar o backend como fonte de verdade.

## 8. Próximos passos recomendados
- Implementar autenticação com JWT.
- Criar CRUD completo para clientes e roteiros.
- Integrar upload de arquivos e armazenamento persistente.
- Implementar telas de listagem e detalhes para casos e execuções.
- Criar camada de serviços no frontend para consumo das APIs.
- Adicionar testes automatizados para backend e frontend.
