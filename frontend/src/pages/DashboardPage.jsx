import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import * as api from '../services/api';

function DashboardPage() {
  const { user, token } = useAuth();
  const [stats, setStats] = useState({ clientes: 0, sistemas: 0, casos: 0, execucoes: 0 });
  const [recentExecutions, setRecentExecutions] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    async function loadData() {
      try {
        const [clientesData, sistemasData, casosData, execucoesData] = await Promise.all([
          api.getClientes(1, 1),
          api.getSistemas(1, 1),
          api.getCasos(1, 1),
          api.getExecucoes(1, 10)
        ]);

        setStats({
          clientes: clientesData.total || 0,
          sistemas: sistemasData.total || 0,
          casos: casosData.total || 0,
          execucoes: execucoesData.total || 0
        });

        setRecentExecutions(execucoesData.items || []);
      } catch (err) {
        setError(err.message || 'Erro ao carregar dashboard');
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [token]);

  return (
    <div>
      <div className="header">
        <div>
          <h1>Dashboard</h1>
          <p>Bem-vindo, {user?.nome || 'Usuário'}. Aqui está um resumo da sua plataforma.</p>
        </div>
      </div>

      {error && <div className="alert error">{error}</div>}

      {loading ? (
        <div className="loading">
          <div className="spinner"></div>
          <p>Carregando dados...</p>
        </div>
      ) : (
        <>
          <section className="cards">
            <div className="card">
              <h3>Clientes</h3>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1d4ed8' }}>
                {stats.clientes}
              </p>
              <small>Clientes cadastrados</small>
            </div>
            <div className="card">
              <h3>Sistemas</h3>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#7c3aed' }}>
                {stats.sistemas}
              </p>
              <small>Conectores/Sistemas</small>
            </div>
            <div className="card">
              <h3>Casos de Teste</h3>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#16a34a' }}>
                {stats.casos}
              </p>
              <small>Testes criados</small>
            </div>
            <div className="card">
              <h3>Execuções</h3>
              <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#db2777' }}>
                {stats.execucoes}
              </p>
              <small>Total de execuções</small>
            </div>
          </section>

          <section className="panel" style={{ marginTop: '1.5rem' }}>
            <h3>Últimas Execuções</h3>
            {recentExecutions.length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Caso de Teste</th>
                    <th>Status</th>
                    <th>Tempo (s)</th>
                    <th>Criado em</th>
                  </tr>
                </thead>
                <tbody>
                  {recentExecutions.map((exec) => (
                    <tr key={exec.id}>
                      <td>#{exec.id}</td>
                      <td>{exec.caso_teste_id || '-'}</td>
                      <td>
                        <span className={`badge ${exec.status === 'sucesso' ? 'success' : exec.status === 'erro' ? 'error' : 'info'}`}>
                          {exec.status}
                        </span>
                      </td>
                      <td>{exec.tempo || '-'}</td>
                      <td>{new Date(exec.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>Nenhuma execução registrada ainda.</p>
            )}
          </section>
        </>
      )}
    </div>
  );
}

export default DashboardPage;
