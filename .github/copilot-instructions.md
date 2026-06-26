# Instruções para implementação da Plataforma

## Objetivo
Implementar a primeira versão funcional da plataforma com foco em usabilidade, integração com o backend existente e evolução incremental.

## Etapas recomendadas

### 1. Preparar o frontend
- Criar a estrutura inicial com React + Vite.
- Definir layout base com sidebar, páginas principais e navegação.
- Organizar pastas por domínio: pages, services, components, hooks, contexts.

### 2. Integrar com a API backend
- Criar serviços para consumir os endpoints de:
  - autenticação
  - clientes
  - roteiros
  - casos de teste
  - execuções
  - logs e evidências
- Usar base URL configurável via variável de ambiente.

### 3. Implementar autenticação
- Criar fluxo de login e proteção de rotas.
- Armazenar token JWT de forma segura.
- Adicionar tratamento de erros e refresh de sessão quando necessário.

### 4. Implementar CRUD inicial
- Clientes: listagem, cadastro e edição.
- Roteiros: listagem, upload e status.
- Casos: cadastro, edição e execução.
- Execuções: histórico, detalhes e acompanhamento em tempo real.

### 5. Integrar execução assíncrona
- Ao clicar em executar, chamar o endpoint de execução do backend.
- Exibir feedback para o usuário enquanto a tarefa roda.
- Mostrar logs e evidências ao final da execução.

### 6. Qualidade e observabilidade
- Adicionar validação de formulário no frontend.
- Exibir mensagens de erro amigáveis.
- Registrar logs relevantes no backend e no frontend.
- Criar testes básicos para fluxos críticos.

## Diretrizes técnicas
- Manter o frontend desacoplado do backend.
- Priorizar componentes reutilizáveis.
- Usar nomes claros para rotas, serviços e estados.
- Documentar novas integrações no README e na arquitetura.
- Evitar duplicação de lógica de negócio.

## Entregas iniciais
1. Estrutura base do frontend.
2. Navegação principal.
3. Tela de dashboard.
4. Telas de clientes e roteiros com estrutura inicial.
5. Integração inicial com endpoints do backend.
