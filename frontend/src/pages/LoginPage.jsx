import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login as loginRequest } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

function LoginPage() {
  const [form, setForm] = useState({ email: '', senha: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      const result = await loginRequest(form);
      login(result.user, result.access_token);
      navigate('/');
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'grid', placeItems: 'center', background: '#f4f7fb' }}>
      <div className="panel" style={{ width: 'min(420px, 90vw)' }}>
        <h2>Entrar na plataforma</h2>
        <p>Autentique-se para acessar os módulos de execução e rastreio.</p>
        <form onSubmit={handleSubmit}>
          <input placeholder="E-mail" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input type="password" placeholder="Senha" value={form.senha} onChange={(e) => setForm({ ...form, senha: e.target.value })} />
          <button type="submit">Entrar</button>
        </form>
        {error && <p style={{ color: '#dc2626' }}>{error}</p>}
      </div>
    </div>
  );
}

export default LoginPage;
