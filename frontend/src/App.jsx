import { Navigate, NavLink, Route, Routes } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
import DashboardPage from './pages/DashboardPage';
import ClientesPage from './pages/ClientesPage';
import RoteirosPage from './pages/RoteirosPage';
import CasosPage from './pages/CasosPage';
import ExecucoesPage from './pages/ExecucoesPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import HomePage from './pages/HomePage';
import RobosPage from './pages/RobosPage';
import ConectoresPage from './pages/ConectoresPage';

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/clientes', label: 'Clientes' },
  { to: '/roteiros', label: 'Roteiros' },
  { to: '/casos', label: 'Casos' },
  { to: '/robos', label: 'Robôs' },
  { to: '/conectores', label: 'Conectores' },
  { to: '/execucoes', label: 'Execuções' },
  { to: '/perfil', label: 'Perfil' }
];

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
}

function App() {
  const { user, logout } = useAuth();

  if (!user) {
    return (
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    );
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h2>Test Automation Platform</h2>
        <nav>
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.to === '/'}>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <button type="button" onClick={logout} style={{ marginTop: '1rem' }}>
          Sair
        </button>
      </aside>

      <main className="main-panel">
        <Routes>
          <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/clientes" element={<ProtectedRoute><ClientesPage /></ProtectedRoute>} />
          <Route path="/roteiros" element={<ProtectedRoute><RoteirosPage /></ProtectedRoute>} />
          <Route path="/casos" element={<ProtectedRoute><CasosPage /></ProtectedRoute>} />
          <Route path="/robos" element={<ProtectedRoute><RobosPage /></ProtectedRoute>} />
          <Route path="/conectores" element={<ProtectedRoute><ConectoresPage /></ProtectedRoute>} />
          <Route path="/execucoes" element={<ProtectedRoute><ExecucoesPage /></ProtectedRoute>} />
          <Route path="/perfil" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
