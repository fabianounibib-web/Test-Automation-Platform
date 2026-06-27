import { useEffect, useState } from 'react';
import * as api from '../services/api';

function ConectoresPage() {
  const [sistemas, setSistemas] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [nome, setNome] = useState('');
  const [urlBase, setUrlBase] = useState('');
  const [tipo, setTipo] = useState('web');
  const [ambiente, setAmbiente] = useState('desenvolvimento');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSistemas();
  }, [page]);

  async function loadSistemas() {
    try {
      setLoading(true);
      const result = await api.getSistemas(page, 20);
      setSistemas(result.items || []);
      setTotal(result.total || 0);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      setError('');
      setSuccess('');
      await api.createSistema({
        nome,
        url_base: urlBase,
        tipo,
        ambiente
      });
      setNome('');
      setUrlBase('');
      setTipo('web');
      setAmbiente('desenvolvimento');
      setSuccess('Sistema criado com sucesso!');
      loadSistemas();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Deletar este sistema?')) return;
    try {
      await api.deleteSistema(id);
      loadSistemas();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <div className="header">
        <h1>Sistemas/Conectores</h1>
        <p>Gerenciamento de sistemas para automação de testes.</p>
      </div>

      <div className="grid">
        <section className="panel">
          <h3>Novo Sistema</h3>
          {error && <div className="alert error">{error}</div>}
          {success && <div className="alert success">{success}</div>}
          <form onSubmit={handleSubmit}>
            <input 
              type="text"
              placeholder="Nome do sistema" 
              value={nome} 
              onChange={(e) => setNome(e.target.value)}
              required
            />
            <input 
              type="url"
              placeholder="URL base" 
              value={urlBase} 
              onChange={(e) => setUrlBase(e.target.value)}
              required
            />
            <select 
              value={tipo} 
              onChange={(e) => setTipo(e.target.value)}
            >
              <option value="web">Web (MVP)</option>
              <option value="sap">SAP (Futuro)</option>
              <option value="desktop">Desktop (Futuro)</option>
              <option value="api">API (Futuro)</option>
              <option value="legacy">Legacy (Futuro)</option>
            </select>
            <select 
              value={ambiente} 
              onChange={(e) => setAmbiente(e.target.value)}
            >
              <option value="desenvolvimento">Desenvolvimento</option>
              <option value="homologacao">Homologação</option>
              <option value="producao_assistida">Produção Assistida</option>
            </select>
            <button type="submit">Criar Sistema</button>
          </form>
        </section>

        <section className="panel">
          <h3>Sistemas</h3>
          {loading ? (
            <div className="loading"><div className="spinner"></div></div>
          ) : sistemas.length > 0 ? (
            <>
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>URL</th>
                    <th>Tipo</th>
                    <th>Ambiente</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {sistemas.map(s => (
                    <tr key={s.id}>
                      <td>{s.nome}</td>
                      <td style={{ fontSize: '0.85rem' }}>{s.url_base?.substring(0, 30)}</td>
                      <td><span className="badge info">{s.tipo}</span></td>
                      <td>{s.ambiente}</td>
                      <td>
                        <button 
                          className="secondary danger"
                          onClick={() => handleDelete(s.id)}
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
            <p>Nenhum sistema criado ainda.</p>
          )}
        </section>
      </div>
    </div>
  );
}

export default ConectoresPage;
