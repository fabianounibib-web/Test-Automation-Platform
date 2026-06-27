import { useEffect, useState } from 'react';
import * as api from '../services/api';

function ClientesPage() {
  const [clientes, setClientes] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [responsavel, setResponsavel] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadClientes();
  }, [page]);

  async function loadClientes() {
    try {
      setLoading(true);
      const result = await api.getClientes(page, 20);
      setClientes(result.items || []);
      setTotal(result.total || 0);
      setError('');
    } catch (err) {
      setError(err.message || 'Erro ao carregar clientes');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      setError('');
      setSuccess('');
      await api.createCliente({ nome, email, responsavel });
      setNome('');
      setEmail('');
      setResponsavel('');
      setSuccess('Cliente cadastrado com sucesso!');
      loadClientes();
    } catch (err) {
      setError(err.message || 'Erro ao criar cliente');
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Tem certeza que deseja deletar este cliente?')) return;
    try {
      await api.deleteCliente(id);
      loadClientes();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <div className="header">
        <div>
          <h1>Clientes</h1>
          <p>Cadastro e gestão de clientes.</p>
        </div>
      </div>

      <div className="grid">
        <section className="panel">
          <h3>Novo Cliente</h3>
          {error && <div className="alert error">{error}</div>}
          {success && <div className="alert success">{success}</div>}
          <form onSubmit={handleSubmit}>
            <input 
              type="text"
              placeholder="Nome" 
              value={nome} 
              onChange={(e) => setNome(e.target.value)}
              required 
            />
            <input 
              type="email"
              placeholder="E-mail" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)}
              required 
            />
            <input 
              type="text"
              placeholder="Responsável" 
              value={responsavel} 
              onChange={(e) => setResponsavel(e.target.value)}
            />
            <button type="submit">Salvar Cliente</button>
          </form>
        </section>

        <section className="panel">
          <h3>Clientes Cadastrados</h3>
          {loading ? (
            <div className="loading"><div className="spinner"></div></div>
          ) : clientes.length > 0 ? (
            <>
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>E-mail</th>
                    <th>Responsável</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {clientes.map((cliente) => (
                    <tr key={cliente.id}>
                      <td>{cliente.nome}</td>
                      <td>{cliente.email}</td>
                      <td>{cliente.responsavel || '-'}</td>
                      <td>
                        <button 
                          className="secondary" 
                          onClick={() => handleDelete(cliente.id)}
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
                <button 
                  disabled={page === 1}
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                >
                  ← Anterior
                </button>
                <span style={{ padding: '0.4rem 0.8rem' }}>
                  Página {page} de {Math.ceil(total / 20)}
                </span>
                <button 
                  disabled={page >= Math.ceil(total / 20)}
                  onClick={() => setPage(p => p + 1)}
                >
                  Próxima →
                </button>
              </div>
            </>
          ) : (
            <p>Nenhum cliente cadastrado ainda.</p>
          )}
        </section>
      </div>
    </div>
  );
}

export default ClientesPage;
