import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { register as registerRequest } from '../services/api';

function RegisterPage() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await registerRequest(nome, email, senha);
      setSuccess('Usuário criado com sucesso. Você pode entrar agora.');
      setTimeout(() => navigate('/login'), 1500);
    } catch (err) {
      setError(err.message || 'Não foi possível criar o usuário.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'grid', placeItems: 'center', background: '#f4f7fb' }}>
      <div className="panel" style={{ width: 'min(460px, 90vw)' }}>
        <h2>Criar conta</h2>
        <p>Cadastre um usuário para acessar a plataforma.</p>
        {error && <div className="alert error">{error}</div>}
        {success && <div className="alert success">{success}</div>}
        <form onSubmit={handleSubmit}>
          <input 
            type="text"
            placeholder="Nome" 
            value={nome} 
            onChange={(e) => setNome(e.target.value)}
            required
            disabled={loading}
          />
          <input 
            type="email"
            placeholder="E-mail" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
          <input 
            type="password" 
            placeholder="Senha" 
            value={senha} 
            onChange={(e) => setSenha(e.target.value)}
            required
            disabled={loading}
          />
          <button type="submit" disabled={loading || success !== ''}>
            {loading ? 'Criando conta...' : 'Cadastrar'}
          </button>
        </form>
        <p style={{ marginTop: '0.8rem' }}>
          Já possui conta? <Link to="/login">Entrar</Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
