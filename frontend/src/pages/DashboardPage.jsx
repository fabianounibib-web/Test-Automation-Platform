import { useEffect, useState } from 'react';
import { getDashboard } from '../services/api';

function DashboardPage() {
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    getDashboard()
      .then(setMetrics)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <div className="header">
        <div>
          <h1>Dashboard</h1>
          <p>Visão geral das execuções, testes e indicadores do ambiente.</p>
        </div>
      </div>

      {error && <p style={{ color: '#dc2626' }}>{error}</p>}

      <section className="cards">
        <div className="card">
          <h3>Total de testes</h3>
          <p>{metrics?.total_testes ?? 0}</p>
        </div>
        <div className="card">
          <h3>Robôs cadastrados</h3>
          <p>{metrics?.total_robos ?? 0}</p>
        </div>
        <div className="card">
          <h3>Execuções em fila</h3>
          <p>{metrics?.fila_execucao ?? 0}</p>
        </div>
        <div className="card">
          <h3>Tempo médio</h3>
          <p>{metrics?.tempo_medio ?? 0}s</p>
        </div>
      </section>

      <section className="panel" style={{ marginTop: '1rem' }}>
        <h3>Últimas execuções</h3>
        {metrics?.ultimas_execucoes?.length ? (
          <ul>
            {metrics.ultimas_execucoes.map((item) => (
              <li key={item.id || item.nome}>{item.nome || item.id}</li>
            ))}
          </ul>
        ) : (
          <p>Nenhuma execução registrada ainda.</p>
        )}
      </section>
    </div>
  );
}

export default DashboardPage;
