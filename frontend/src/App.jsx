import { NavLink, Route, Routes } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import ClientesPage from './pages/ClientesPage';
import RoteirosPage from './pages/RoteirosPage';
import CasosPage from './pages/CasosPage';
import ExecucoesPage from './pages/ExecucoesPage';

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/clientes', label: 'Clientes' },
  { to: '/roteiros', label: 'Roteiros' },
  { to: '/casos', label: 'Casos' },
  { to: '/execucoes', label: 'Execuções' }
];

function App() {
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
      </aside>

      <main className="main-panel">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/clientes" element={<ClientesPage />} />
          <Route path="/roteiros" element={<RoteirosPage />} />
          <Route path="/casos" element={<CasosPage />} />
          <Route path="/execucoes" element={<ExecucoesPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
