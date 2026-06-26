import { useEffect, useState } from 'react';
import { executarCaso, getCasos } from '../services/api';
import StatusBadge from '../components/StatusBadge';

function CasosPage() {
  const [casos, setCasos] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    getCasos().then(setCasos).catch(() => setCasos([]));
  }, []);

  async function handleExecutar(id) {
    try {
      const result = await executarCaso(id);
      setMessage(`Execução iniciada com sucesso. Task: ${result.task_id}`);
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <div className="header">
        <div>
          <h1>Casos de teste</h1>
          <p>Estruturação e execução de cenários a partir dos roteiros importados.</p>
        </div>
      </div>

      <section className="panel">
        <h3>Casos disponíveis</h3>
        {casos.length ? (
          <ul>
            {casos.map((caso) => (
              <li key={caso.id || caso.nome} style={{ marginBottom: '0.7rem' }}>
                <strong>{caso.nome || 'Caso sem nome'}</strong>
                <div>
                  <StatusBadge status={caso.status} />
                  <button type="button" style={{ marginLeft: '0.7rem' }} onClick={() => handleExecutar(caso.id)}>
                    Executar
                  </button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>Nenhum caso de teste cadastrado ainda.</p>
        )}
        {message && <p>{message}</p>}
      </section>
    </div>
  );
}

export default CasosPage;
