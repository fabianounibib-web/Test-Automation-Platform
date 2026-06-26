import { useAuth } from '../contexts/AuthContext';

function ProfilePage() {
  const { user } = useAuth();

  return (
    <div>
      <div className="header">
        <div>
          <h1>Perfil</h1>
          <p>Informações do usuário autenticado.</p>
        </div>
      </div>

      <section className="panel">
        <h3>Dados da conta</h3>
        <p><strong>Nome:</strong> {user?.nome || 'Não informado'}</p>
        <p><strong>E-mail:</strong> {user?.email || 'Não informado'}</p>
        <p><strong>Perfil:</strong> {user?.perfil || 'Não informado'}</p>
      </section>
    </div>
  );
}

export default ProfilePage;
