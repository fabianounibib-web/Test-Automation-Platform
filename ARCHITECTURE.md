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
## 9. Como o robô sabe interagir com sistemas externos
O robô não deve tentar adivinhar sozinho os caminhos, labels, campos e botões de um portal externo. A plataforma precisa ensiná-lo a operar cada sistema por meio de conectores configuráveis. O conector é o artefato que descreve como acessar um sistema, autenticar-se, navegar até uma área funcional e executar uma ação, como baixar um histórico de pagamentos.

### 9.1 Estratégias possíveis
A plataforma pode suportar quatro estratégias de automação, com níveis diferentes de flexibilidade e robustez:

1. **Robô programado**: um desenvolvedor cria uma automação específica em Playwright, Selenium ou ferramenta equivalente. A plataforma apenas agenda, executa e registra evidências desse robô. É a opção mais robusta para fluxos críticos, mas exige manutenção técnica.
2. **Mapeamento visual**: o usuário cadastra o sistema e, em um assistente, aponta visualmente quais elementos representam usuário, senha, botão de login, aba de faturas e botão de download. A plataforma salva seletores e metadados reutilizáveis.
3. **Gravação de fluxo**: o usuário clica em "Gravar Automação", executa o processo manualmente uma vez, e a plataforma registra uma sequência de ações reproduzível.
4. **IA assistida**: modelos de linguagem e visão podem ajudar a identificar campos e botões a partir da página, mas devem atuar como camada auxiliar com validação, não como única fonte de decisão para processos críticos.

### 9.2 Abordagem recomendada para produto
Para esta plataforma, a recomendação é combinar **mapeamento visual** e **gravação de fluxo**. O usuário de negócio cadastra um sistema, abre um navegador controlado pela plataforma, realiza o processo uma vez e salva o resultado como um conector inteligente.

Exemplo de cadastro:

```text
Nome: Portal Financeiro
URL: https://xpto.com
Credenciais: usuário e senha armazenados de forma segura
Processo: baixar histórico de pagamentos
```

Durante a gravação, a plataforma transforma as interações em passos estruturados:

```json
[
  {
    "action": "goto",
    "url": "https://xpto.com"
  },
  {
    "action": "fill",
    "target": "usuario",
    "selector": "#usuario",
    "value": "${usuario}"
  },
  {
    "action": "fill",
    "target": "senha",
    "selector": "#senha",
    "value": "${senha}"
  },
  {
    "action": "click",
    "target": "entrar",
    "selector": "#entrar"
  },
  {
    "action": "click",
    "target": "faturas",
    "selector": "#menu_faturas"
  },
  {
    "action": "click",
    "target": "historico_pagamentos",
    "selector": "#historico"
  },
  {
    "action": "download",
    "target": "arquivo_historico",
    "selector": "#download"
  }
]
```

Assim, o motor de execução não precisa conhecer previamente o site `xpto.com`; ele interpreta o fluxo salvo no conector e executa os passos com os dados seguros do cliente.

### 9.3 Modelo conceitual do conector
Um conector inteligente deve conter, no mínimo:

- identificação do sistema: nome, URL base, cliente e ambiente;
- credenciais referenciadas por variáveis seguras, nunca salvas em texto aberto no fluxo;
- lista ordenada de ações: `goto`, `fill`, `click`, `select`, `wait`, `assert`, `download`;
- seletores principais e alternativas de localização;
- regras de espera e timeout;
- critérios de sucesso, como arquivo baixado, mensagem exibida ou registro encontrado;
- política de evidências, como screenshots, logs e arquivos coletados;
- versão do conector para permitir manutenção controlada.

### 9.4 Resolução inteligente de elementos
Como portais externos mudam com o tempo, a plataforma deve evitar depender de um único seletor frágil. Cada elemento mapeado deve guardar múltiplas pistas de identificação:

- seletor CSS preferencial;
- ID e atributo `name`;
- texto visível;
- label associada;
- papel acessível, como botão, link ou campo;
- XPath como último recurso;
- posição relativa ou contexto visual, apenas como fallback.

Na execução, o motor tenta localizar o elemento em ordem de confiabilidade. Se o seletor principal falhar, ele tenta as alternativas antes de marcar a execução como erro. Quando a alternativa funcionar, a plataforma pode sugerir atualização do conector.

### 9.5 Fluxo operacional sugerido
1. O usuário cadastra o sistema externo.
2. O usuário escolhe criar um conector por gravação ou importar um robô programado.
3. A plataforma abre uma sessão de navegador instrumentada.
4. O usuário executa o processo uma vez.
5. A plataforma salva os passos, seletores, variáveis e critérios de sucesso.
6. Um validador executa o fluxo em modo teste.
7. Após aprovação, o conector fica disponível para roteiros e casos de teste.
8. Em cada execução, a plataforma registra logs, evidências e arquivos baixados.

### 9.6 Implicação arquitetural
A plataforma não deve vender apenas "robôs" isolados. Ela deve tratar cada integração como um **conector inteligente versionado**, capaz de ser gravado, validado, executado, monitorado e mantido. Essa decisão preserva a robustez de automações programadas, reduz a barreira para usuários não técnicos e mantém a arquitetura preparada para incorporar IA de forma segura no futuro.

