import { useEffect, useState } from 'react';
import { createRobo, executarRobo, getRobos } from '../services/api';
import StatusBadge from '../components/StatusBadge';

const executorOptions = ['python', 'playwright', 'selenium'];

function RobosPage() {
  const [robos, setRobos] = useState([]);
  const [form, setForm] = useState({ nome: '', descricao: '', tipo: 'python', script: '', status: 'draft' });
  const [message, setMessage] = useState('');

  useEffect(() => {
    getRobos().then(setRobos).catch(() => setRobos([]));
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      const created = await createRobo(form);
      setRobos((previous) => [created, ...previous]);
      setForm({ nome: '', descricao: '', tipo: 'python', script: '', status: 'draft' });
      setMessage(`Robô '${created.nome}' cadastrado para orquestração.`);
    } catch (error) {
      setMessage(error.message);
    }
  }

  async function handleExecutar(id) {
    try {
      const result = await executarRobo(id);
      setMessage(`Execução registrada. ID: ${result.id}`);
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <div className="header">
        <div>
          <h1>Robôs de automação</h1>
          <p>Cadastre e orquestre automações, mantendo o núcleo do sistema desacoplado do executor.</p>
        </div>
      </div>

      <section className="panel" style={{ marginBottom: '1rem' }}>
        <h3>Novo robô</h3>
        <form onSubmit={handleSubmit}>
          <input value={form.nome} onChange={(event) => setForm({ ...form, nome: event.target.value })} placeholder="Nome" required />
          <input value={form.descricao} onChange={(event) => setForm({ ...form, descricao: event.target.value })} placeholder="Descrição" />
          <select value={form.tipo} onChange={(event) => setForm({ ...form, tipo: event.target.value })}>
            {executorOptions.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
          <textarea value={form.script} onChange={(event) => setForm({ ...form, script: event.target.value })} placeholder="Script ou referência da automação" rows="4" />
          <input value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })} placeholder="Status" />
          <button type="submit">Salvar robô</button>
        </form>
        {message && <p>{message}</p>}
      </section>

      <section className="panel">
        <h3>Robôs cadastrados</h3>
        {robos.length ? (
          <ul>
            {robos.map((robo) => (
              <li key={robo.id} style={{ marginBottom: '0.8rem' }}>
                <strong>{robo.nome}</strong>
                <div>
                  <StatusBadge status={robo.status} />
                  <span style={{ marginLeft: '0.7rem' }}>{robo.tipo}</span>
                </div>
                <div style={{ marginTop: '0.4rem' }}>
                  <button type="button" onClick={() => handleExecutar(robo.id)}>Orquestrar</button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>Nenhum robô cadastrado ainda.</p>
        )}
      </section>
    </div>
  );
}

export default RobosPage;
