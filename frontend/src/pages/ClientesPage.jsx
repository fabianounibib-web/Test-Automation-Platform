import { useEffect, useState } from 'react';
import { createCliente, getClientes } from '../services/api';

function ClientesPage() {
  const [clientes, setClientes] = useState([]);
  const [form, setForm] = useState({ nome: '', email: '', responsavel: '' });
  const [message, setMessage] = useState('');

  useEffect(() => {
    getClientes().then(setClientes).catch(() => setClientes([]));
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      const created = await createCliente(form);
      setClientes((prev) => [...prev, created]);
      setForm({ nome: '', email: '', responsavel: '' });
      setMessage('Cliente cadastrado com sucesso.');
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <div className="header">
        <div>
          <h1>Clientes</h1>
          <p>Cadastro e gestão de clientes e responsáveis.</p>
        </div>
      </div>

      <div className="grid">
        <section className="panel">
          <h3>Novo cliente</h3>
          <form onSubmit={handleSubmit}>
            <input placeholder="Nome" value={form.nome} onChange={(e) => setForm({ ...form, nome: e.target.value })} />
            <input placeholder="E-mail" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            <input placeholder="Responsável" value={form.responsavel} onChange={(e) => setForm({ ...form, responsavel: e.target.value })} />
            <button type="submit">Salvar</button>
          </form>
          {message && <p>{message}</p>}
        </section>

        <section className="panel">
          <h3>Clientes cadastrados</h3>
          {clientes.length ? (
            <ul>
              {clientes.map((cliente) => (
                <li key={cliente.id || cliente.nome}>
                  <strong>{cliente.nome}</strong> — {cliente.email || 'Sem e-mail'}
                </li>
              ))}
            </ul>
          ) : (
            <p>Ainda não há clientes cadastrados.</p>
          )}
        </section>
      </div>
    </div>
  );
}

export default ClientesPage;
