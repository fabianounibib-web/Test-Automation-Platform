# Instruções para continuidade do MVP (foco em RPA)

## Objetivo
Evoluir a plataforma do MVP inicial para um fluxo de automação real, com conectores inteligentes, execução assíncrona, logs e evidências. A prioridade é transformar os passos gravados em automações executáveis pelo motor RPA.

## Estado verificado do repositório
- Frontend React + Vite com páginas de autenticação, dashboard, clientes, roteiros, casos, conectores, execuções e perfil.
- Backend Flask modular com autenticação JWT, CRUD de domínio, endpoints de execuções e conectores.
- Modelo de dados com Conector, CasoTeste, Execucao, Log e Evidencia.
- Camada de executores com registry para Python, Playwright e Selenium.
- Fluxo de execução assíncrono com Celery + Redis e task placeholder.
- Validação de passos e descrição de fluxo para conectores.

## Prioridades de implementação

### 1. Motor de execução real
- Implementar a execução de conectores em navegador com Playwright, mantendo Selenium como fallback.
- Mapear as ações suportadas: `goto`, `fill`, `click`, `select`, `wait`, `assert` e `download`.
- Resolver valores de runtime a partir de dados do caso e referências seguras de credenciais.

### 2. Evidências e observabilidade
- Capturar screenshots, logs estruturados e arquivos gerados durante a execução.
- Persistir evidências e associá-las à execução correspondente.
- Expor o status detalhado no frontend para acompanhamento em tempo real.

### 3. Robustez operacional
- Adicionar timeouts, retries, tratamento de falhas e cancelamento.
- Classificar sucesso, erro e inconclusão a partir de assertions e artefatos gerados.
- Garantir que falhas de execução não interrompam o fluxo da API.

### 4. Qualidade e testes
- Cobrir o fluxo de execução com testes de integração e regressão.
- Manter os endpoints REST consistentes e respostas claras para o frontend.
- Evitar duplicação de lógica entre backend e frontend.

## Diretrizes técnicas
- Manter o frontend desacoplado do backend e consumir as APIs via camada de serviços.
- Priorizar componentes reutilizáveis e estados claros no frontend.
- Tratar cada integração como um conector versionado, não como um script isolado.
- Nunca armazenar segredos em texto aberto nos fluxos; usar referências seguras e valores de runtime.
- Documentar alterações de integração e regras de execução no README e na arquitetura.

## Entregas recomendadas para o próximo ciclo
1. Implementar um executor Playwright real para o fluxo de conectores.
2. Conectar os passos salvos ao motor de execução e registrar logs em tempo real.
3. Adicionar captura de evidências e persistência de artefatos.
4. Melhorar o tratamento de erro e a experiência de acompanhamento no frontend.
