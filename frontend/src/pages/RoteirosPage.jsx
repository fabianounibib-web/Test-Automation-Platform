import { useEffect, useState } from 'react';
import * as api from '../services/api';

function RoteirosPage() {
  const [roteiros, setRoteiros] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [file, setFile] = useState(null);
  const [clienteId, setClienteId] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadRoteiros();
    loadClientes();
  }, [page]);

  async function loadRoteiros() {
    try {
      setLoading(true);
      const result = await api.getRoteiros(page, 20);
      setRoteiros(result.items || []);
      setTotal(result.total || 0);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadClientes() {
    try {
      const result = await api.getClientes(1, 100);
      setClientes(result.items || []);
    } catch (err) {
      console.error('Erro ao carregar clientes:', err);
    }
  }

  async function handleUpload(e) {
    e.preventDefault();
    if (!file || !clienteId) {
      setError('Selecione um arquivo e um cliente');
      return;
    }

    try {
      setError('');
      setSuccess('');
      setLoading(true);
      await api.uploadRoteiro(file, clienteId);
      setFile(null);
      setClienteId('');
      setSuccess('Roteiro enviado com sucesso!');
      loadRoteiros();
    } catch (err) {
      setError(err.message || 'Erro ao fazer upload');
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Deletar este roteiro?')) return;
    try {
      await api.deleteRoteiro(id);
      loadRoteiros();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <div className="header">
        <h1>Roteiros de Teste</h1>
        <p>Upload e gestão de cenários de automação.</p>
      </div>

      <div className="grid">
        <section className="panel">
          <h3>Upload Roteiro</h3>
          {error && <div className="alert error">{error}</div>}
          {success && <div className="alert success">{success}</div>}
          <form onSubmit={handleUpload}>
            <select 
              value={clienteId} 
              onChange={(e) => setClienteId(e.target.value)}
              required
              disabled={loading}
            >
              <option value="">Selecione um cliente</option>
              {clientes.map(c => (
                <option key={c.id} value={c.id}>{c.nome}</option>
              ))}
            </select>
            <input 
              type="file"
              accept=".xls,.xlsx,.csv,.json"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              required
              disabled={loading}
            />
            <button type="submit" disabled={loading || !file || !clienteId}>
              {loading ? 'Enviando...' : 'Upload'}
            </button>
          </form>
        </section>

        <section className="panel">
          <h3>Roteiros</h3>
          {loading ? (
            <div className="loading"><div className="spinner"></div></div>
          ) : roteiros.length > 0 ? (
            <>
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Arquivo</th>
                    <th>Status</th>
                    <th>Criado</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {roteiros.map(r => (
                    <tr key={r.id}>
                      <td>#{r.id}</td>
                      <td>{r.arquivo}</td>
                      <td><span className="badge info">{r.status || 'ativo'}</span></td>
                      <td>{new Date(r.created_at).toLocaleDateString()}</td>
                      <td>
                        <button 
                          className="secondary danger"
                          onClick={() => handleDelete(r.id)}
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
            <p>Nenhum roteiro enviado ainda.</p>
          )}
        </section>
      </div>
    </div>
  );
}

export default RoteirosPage;
