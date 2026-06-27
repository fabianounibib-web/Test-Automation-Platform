import { useEffect, useState } from 'react';
import * as api from '../services/api';

function ExecucoesPage() {
  const [execucoes, setExecucoes] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [selectedExecution, setSelectedExecution] = useState(null);
  const [logs, setLogs] = useState([]);
  const [evidencias, setEvidencias] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [pollingInterval, setPollingInterval] = useState(null);

  useEffect(() => {
    loadExecucoes();
  }, [page]);

  // Polling: atualiza a execução selecionada a cada 3 segundos
  useEffect(() => {
    if (!selectedId) return;

    const poll = async () => {
      try {
        const exec = await api.getExecucao(selectedId);
        setSelectedExecution(exec);
        
        // Se ainda está executando, continua o polling
        if (exec.status === 'executando' || exec.status === 'iniciando') {
          return; // continua o interval
        } else {
          // Se terminou, carrega logs e evidências
          loadLogsAndEvidencias(selectedId);
        }
      } catch (err) {
        console.error('Erro ao fazer polling:', err);
      }
    };

    const interval = setInterval(poll, 3000);
    setPollingInterval(interval);
    poll(); // Primeira chamada imediata

    return () => clearInterval(interval);
  }, [selectedId]);

  async function loadExecucoes() {
    try {
      setLoading(true);
      const result = await api.getExecucoes(page, 20);
      setExecucoes(result.items || []);
      setTotal(result.total || 0);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadLogsAndEvidencias(execId) {
    try {
      const [logsData, evidenciasData] = await Promise.all([
        api.getExecucaoLogs(execId, 1, 50),
        api.getExecucaoEvidencias(execId, 1, 50)
      ]);
      setLogs(logsData.items || []);
      setEvidencias(evidenciasData.items || []);
    } catch (err) {
      console.error('Erro ao carregar logs/evidências:', err);
    }
  }

  async function handleSelectExecution(exec) {
    setSelectedId(exec.id);
    setSelectedExecution(exec);
    setLogs([]);
    setEvidencias([]);
    loadLogsAndEvidencias(exec.id);
  }

  async function handleCancel() {
    if (!selectedId) return;
    if (!window.confirm('Cancelar esta execução?')) return;

    try {
      await api.cancelExecution(selectedId);
      loadExecucoes();
      setSelectedId(null);
      setSelectedExecution(null);
    } catch (err) {
      setError(err.message);
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'sucesso':
        return 'success';
      case 'erro':
        return 'error';
      case 'executando':
      case 'iniciando':
        return 'warning';
      default:
        return 'info';
    }
  };

  return (
    <div>
      <div className="header">
        <h1>Execuções</h1>
        <p>Acompanhe status, logs e evidências das automações em tempo real.</p>
      </div>

      {error && <div className="alert error">{error}</div>}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1rem' }}>
        <section className="panel">
          <h3>Lista de Execuções</h3>
          {loading && !execucoes.length ? (
            <div className="loading"><div className="spinner"></div></div>
          ) : execucoes.length > 0 ? (
            <>
              {execucoes.map(exec => (
                <div
                  key={exec.id}
                  onClick={() => handleSelectExecution(exec)}
                  style={{
                    padding: '0.8rem',
                    marginBottom: '0.5rem',
                    border: selectedId === exec.id ? '2px solid #1d4ed8' : '1px solid #e5e7eb',
                    borderRadius: '0.5rem',
                    cursor: 'pointer',
                    backgroundColor: selectedId === exec.id ? '#f0f9ff' : '#f9fafb'
                  }}
                >
                  <strong>#{exec.id}</strong>
                  <span className={`badge ${getStatusColor(exec.status)}`} style={{ marginLeft: '0.5rem' }}>
                    {exec.status}
                  </span>
                  {exec.tempo && <div style={{ fontSize: '0.85rem', color: '#6b7280' }}>Tempo: {exec.tempo}s</div>}
                </div>
              ))}
              <div className="pagination">
                <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Anterior</button>
                <span>Página {page}</span>
                <button disabled={page >= Math.ceil(total / 20)} onClick={() => setPage(p => p + 1)}>Próxima →</button>
              </div>
            </>
          ) : (
            <p>Nenhuma execução ainda.</p>
          )}
        </section>

        <section className="panel">
          <h3>Detalhes da Execução</h3>
          {selectedExecution ? (
            <>
              <div style={{ marginBottom: '1rem' }}>
                <p><strong>ID:</strong> {selectedExecution.id}</p>
                <p><strong>Status:</strong> <span className={`badge ${getStatusColor(selectedExecution.status)}`}>{selectedExecution.status}</span></p>
                <p><strong>Tempo:</strong> {selectedExecution.tempo ? `${selectedExecution.tempo}s` : 'Em andamento...'}</p>
                {selectedExecution.status === 'executando' || selectedExecution.status === 'iniciando' ? (
                  <>
                    <p style={{ color: '#7c3aed', fontSize: '0.9rem' }}>⏳ Atualizando automaticamente a cada 3 segundos...</p>
                    <button className="danger" onClick={handleCancel} style={{ marginTop: '0.5rem' }}>Cancelar Execução</button>
                  </>
                ) : null}
              </div>

              <h4 style={{ marginTop: '1rem', borderTop: '1px solid #e5e7eb', paddingTop: '1rem' }}>Logs ({logs.length})</h4>
              {logs.length > 0 ? (
                <div style={{ backgroundColor: '#f3f4f6', padding: '0.8rem', borderRadius: '0.5rem', maxHeight: '200px', overflow: 'auto', fontSize: '0.85rem' }}>
                  {logs.map((log, idx) => (
                    <div key={idx} style={{ marginBottom: '0.4rem', color: log.nivel === 'ERROR' ? '#dc2626' : '#666' }}>
                      <strong>[{log.nivel}]</strong> {log.mensagem}
                    </div>
                  ))}
                </div>
              ) : (
                <p style={{ fontSize: '0.9rem' }}>Sem logs ainda.</p>
              )}

              <h4 style={{ marginTop: '1rem' }}>Evidências ({evidencias.length})</h4>
              {evidencias.length > 0 ? (
                <ul>
                  {evidencias.map((ev, idx) => (
                    <li key={idx} style={{ fontSize: '0.9rem', marginBottom: '0.4rem' }}>
                      <strong>{ev.tipo}:</strong> {ev.arquivo}
                    </li>
                  ))}
                </ul>
              ) : (
                <p style={{ fontSize: '0.9rem' }}>Sem evidências ainda.</p>
              )}
            </>
          ) : (
            <p>Selecione uma execução para ver detalhes.</p>
          )}
        </section>
      </div>
    </div>
  );
}

export default ExecucoesPage;
