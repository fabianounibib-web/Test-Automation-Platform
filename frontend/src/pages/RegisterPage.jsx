import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { register as registerRequest } from '../services/api';

function RegisterPage() {
  const [form, setForm] = useState({ nome: '', email: '', senha: '', perfil: 'analista' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      await registerRequest(form);
      setError('');
      setSuccess('Usuário criado com sucesso. Você pode entrar agora.');
      setTimeout(() => navigate('/login'), 900);
    } catch (err) {
      setError(err.message || 'Não foi possível criar o usuário.');
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'grid', placeItems: 'center', background: '#f4f7fb' }}>
      <div className="panel" style={{ width: 'min(460px, 90vw)' }}>
        <h2>Criar conta</h2>
        <p>Cadastre um usuário para acessar a plataforma.</p>
        <form onSubmit={handleSubmit}>
          <input placeholder="Nome" value={form.nome} onChange={(e) => setForm({ ...form, nome: e.target.value })} />
          <input placeholder="E-mail" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input type="password" placeholder="Senha" value={form.senha} onChange={(e) => setForm({ ...form, senha: e.target.value })} />
          <input placeholder="Perfil" value={form.perfil} onChange={(e) => setForm({ ...form, perfil: e.target.value })} />
          <button type="submit">Cadastrar</button>
        </form>
        {error && <p style={{ color: '#dc2626' }}>{error}</p>}
        {success && <p style={{ color: '#16a34a' }}>{success}</p>}
        <p style={{ marginTop: '0.8rem' }}>
          Já possui conta? <Link to="/login">Entrar</Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
