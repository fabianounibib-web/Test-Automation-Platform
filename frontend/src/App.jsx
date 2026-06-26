import { Navigate, NavLink, Route, Routes } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
import DashboardPage from './pages/DashboardPage';
import ClientesPage from './pages/ClientesPage';
import RoteirosPage from './pages/RoteirosPage';
import CasosPage from './pages/CasosPage';
import ExecucoesPage from './pages/ExecucoesPage';
import LoginPage from './pages/LoginPage';

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/clientes', label: 'Clientes' },
  { to: '/roteiros', label: 'Roteiros' },
  { to: '/casos', label: 'Casos' },
  { to: '/execucoes', label: 'Execuções' }
];

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
}

function App() {
  const { user, logout } = useAuth();

  if (!user) {
    return <LoginPage />;
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
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/clientes" element={<ProtectedRoute><ClientesPage /></ProtectedRoute>} />
          <Route path="/roteiros" element={<ProtectedRoute><RoteirosPage /></ProtectedRoute>} />
          <Route path="/casos" element={<ProtectedRoute><CasosPage /></ProtectedRoute>} />
          <Route path="/execucoes" element={<ProtectedRoute><ExecucoesPage /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
