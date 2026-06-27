import { useEffect, useState } from 'react';
import StatusBadge from '../components/StatusBadge';
import { createConector, executarConector, getConectores } from '../services/api';

const exemploFluxo = JSON.stringify([
  { action: 'goto', url: 'https://xpto.com' },
  { action: 'fill', target: 'usuario', selector: '#usuario', value: '${usuario}' },
  { action: 'fill', target: 'senha', selector: '#senha', value: '${senha}' },
  { action: 'click', target: 'entrar', selector: '#entrar' },
  { action: 'click', target: 'faturas', selector: '#menu_faturas' },
  { action: 'download', target: 'historico_pagamentos', selector: '#download' }
], null, 2);

function ConectoresPage() {
  const [conectores, setConectores] = useState([]);
  const [form, setForm] = useState({
    nome: '',
    descricao: '',
    url_base: '',
    ambiente: 'produção',
    status: 'draft',
    versao: '1.0.0',
    steps: exemploFluxo
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    getConectores().then(setConectores).catch(() => setConectores([]));
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      const created = await createConector({
        ...form,
        credenciais_ref: {
          usuario: `vault://${form.nome || 'conector'}/usuario`,
          senha: `vault://${form.nome || 'conector'}/senha`
        },
        steps: JSON.parse(form.steps)
      });
      setConectores((previous) => [created, ...previous]);
      setForm({ nome: '', descricao: '', url_base: '', ambiente: 'produção', status: 'draft', versao: '1.0.0', steps: exemploFluxo });
      setMessage(`Conector '${created.nome}' cadastrado.`);
    } catch (error) {
      setMessage(error.message);
    }
  }

  async function handleExecutar(id) {
    try {
      const result = await executarConector(id, { variaveis: { usuario: 'demo', senha: 'demo' } });
      setMessage(`Execução do conector registrada. ID: ${result.id}. Passos: ${result.steps_executed}.`);
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <div className="header">
        <div>
          <h1>Conectores inteligentes</h1>
          <p>Ensine a plataforma a acessar portais externos por fluxos gravados, seletores e variáveis seguras.</p>
        </div>
      </div>

      <section className="panel" style={{ marginBottom: '1rem' }}>
        <h3>Novo conector</h3>
        <form onSubmit={handleSubmit}>
          <input value={form.nome} onChange={(event) => setForm({ ...form, nome: event.target.value })} placeholder="Nome do portal" required />
          <input value={form.url_base} onChange={(event) => setForm({ ...form, url_base: event.target.value })} placeholder="URL base" required />
          <input value={form.descricao} onChange={(event) => setForm({ ...form, descricao: event.target.value })} placeholder="Descrição do processo" />
          <input value={form.ambiente} onChange={(event) => setForm({ ...form, ambiente: event.target.value })} placeholder="Ambiente" />
          <input value={form.versao} onChange={(event) => setForm({ ...form, versao: event.target.value })} placeholder="Versão" />
          <textarea value={form.steps} onChange={(event) => setForm({ ...form, steps: event.target.value })} rows="12" aria-label="Fluxo JSON do conector" />
          <button type="submit">Salvar conector</button>
        </form>
        {message && <p>{message}</p>}
      </section>

      <section className="panel">
        <h3>Conectores cadastrados</h3>
        {conectores.length ? (
          <ul>
            {conectores.map((conector) => (
              <li key={conector.id} style={{ marginBottom: '0.8rem' }}>
                <strong>{conector.nome}</strong>
                <div>
                  <StatusBadge status={conector.status} />
                  <span style={{ marginLeft: '0.7rem' }}>{conector.url_base}</span>
                  <span style={{ marginLeft: '0.7rem' }}>v{conector.versao}</span>
                </div>
                <div style={{ marginTop: '0.4rem' }}>
                  <button type="button" onClick={() => handleExecutar(conector.id)}>Executar fluxo</button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>Nenhum conector cadastrado ainda.</p>
        )}
      </section>
    </div>
  );
}

export default ConectoresPage;
