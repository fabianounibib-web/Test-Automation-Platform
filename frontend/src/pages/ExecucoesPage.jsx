import { useEffect, useState } from 'react';
import { getExecucoes } from '../services/api';
import StatusBadge from '../components/StatusBadge';

function ExecucoesPage() {
  const [execucoes, setExecucoes] = useState([]);

  useEffect(() => {
    getExecucoes().then(setExecucoes).catch(() => setExecucoes([]));
  }, []);

  return (
    <div>
      <div className="header">
        <div>
          <h1>Execuções</h1>
          <p>Acompanhe o histórico, status e detalhes das execuções.</p>
        </div>
      </div>

      <section className="panel">
        <h3>Histórico</h3>
        {execucoes.length ? (
          <ul>
            {execucoes.map((execucao) => (
              <li key={execucao.id} style={{ marginBottom: '0.9rem' }}>
                <strong>Execução #{execucao.id}</strong>
                <div>
                  <StatusBadge status={execucao.status} />
                  {execucao.tempo ? <span style={{ marginLeft: '0.7rem' }}>Tempo: {execucao.tempo}s</span> : null}
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>Nenhuma execução registrada.</p>
        )}
      </section>
    </div>
  );
}

export default ExecucoesPage;
