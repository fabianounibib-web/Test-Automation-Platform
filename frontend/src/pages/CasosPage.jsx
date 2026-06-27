import { useEffect, useState } from 'react';
import * as api from '../services/api';
import { useNavigate } from 'react-router-dom';

function CasosPage() {
  const navigate = useNavigate();
  const [casos, setCasos] = useState([]);
  const [roteiros, setRoteiros] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [nome, setNome] = useState('');
  const [objetivo, setObjetivo] = useState('');
  const [resultadoEsperado, setResultadoEsperado] = useState('');
  const [roteiromId, setRoteiroId] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCasos();
    loadRoteiros();
  }, [page]);

  async function loadCasos() {
    try {
      setLoading(true);
      const result = await api.getCasos(page, 20);
      setCasos(result.items || []);
      setTotal(result.total || 0);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadRoteiros() {
    try {
      const result = await api.getRoteiros(1, 100);
      setRoteiros(result.items || []);
    } catch (err) {
      console.error('Erro ao carregar roteiros:', err);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      setError('');
      setSuccess('');
      await api.createCaso({
        nome,
        objetivo,
        resultado_esperado: resultadoEsperado,
        roteiro_id: parseInt(roteiromId),
        dados: {}
      });
      setNome('');
      setObjetivo('');
      setResultadoEsperado('');
      setRoteiroId('');
      setSuccess('Caso de teste criado com sucesso!');
      loadCasos();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleExecute(id) {
    try {
      const result = await api.executeCaso(id);
      navigate(`/execucoes`);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Deletar este caso?')) return;
    try {
      await api.deleteCaso(id);
      loadCasos();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <div className="header">
        <h1>Casos de Teste</h1>
        <p>Estruturação e execução de cenários.</p>
      </div>

      <div className="grid">
        <section className="panel">
          <h3>Novo Caso</h3>
          {error && <div className="alert error">{error}</div>}
          {success && <div className="alert success">{success}</div>}
          <form onSubmit={handleSubmit}>
            <input 
              type="text"
              placeholder="Nome do caso" 
              value={nome} 
              onChange={(e) => setNome(e.target.value)}
              required
            />
            <textarea 
              placeholder="Objetivo" 
              value={objetivo} 
              onChange={(e) => setObjetivo(e.target.value)}
              rows="2"
              required
            />
            <textarea 
              placeholder="Resultado esperado" 
              value={resultadoEsperado} 
              onChange={(e) => setResultadoEsperado(e.target.value)}
              rows="2"
              required
            />
            <select 
              value={roteiromId} 
              onChange={(e) => setRoteiroId(e.target.value)}
              required
            >
              <option value="">Selecione um roteiro</option>
              {roteiros.map(r => (
                <option key={r.id} value={r.id}>{r.arquivo}</option>
              ))}
            </select>
            <button type="submit">Criar Caso</button>
          </form>
        </section>

        <section className="panel">
          <h3>Casos de Teste</h3>
          {loading ? (
            <div className="loading"><div className="spinner"></div></div>
          ) : casos.length > 0 ? (
            <>
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Objetivo</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {casos.map(caso => (
                    <tr key={caso.id}>
                      <td>{caso.nome}</td>
                      <td>{caso.objetivo?.substring(0, 40)}...</td>
                      <td><span className="badge info">{caso.status}</span></td>
                      <td style={{ display: 'flex', gap: '0.3rem' }}>
                        <button 
                          className="secondary"
                          onClick={() => handleExecute(caso.id)}
                          style={{ padding: '0.3rem 0.6rem', fontSize: '0.85rem' }}
                        >
                          Executar
                        </button>
                        <button 
                          className="secondary danger"
                          onClick={() => handleDelete(caso.id)}
                          style={{ padding: '0.3rem 0.6rem', fontSize: '0.85rem' }}
                        >
                          Deletar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="pagination">
                <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Anterior</button>
                <span>Página {page} de {Math.ceil(total / 20)}</span>
                <button disabled={page >= Math.ceil(total / 20)} onClick={() => setPage(p => p + 1)}>Próxima →</button>
              </div>
            </>
          ) : (
            <p>Nenhum caso criado ainda.</p>
          )}
        </section>
      </div>
    </div>
  );
}

export default CasosPage;
