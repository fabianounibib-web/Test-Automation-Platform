import { Link } from 'react-router-dom';

const features = [
  {
    icon: '🧭',
    title: 'Roteiros organizados',
    description: 'Centralize cenários, passos e expectativas em um único fluxo para facilitar a revisão e o compartilhamento.'
  },
  {
    icon: '⚡',
    title: 'Execução com rastreio',
    description: 'Monitore cada execução, acompanhe status e consulte logs sem perder contexto do que foi validado.'
  },
  {
    icon: '📎',
    title: 'Evidências e histórico',
    description: 'Guarde prints, arquivos e resultados para construir um histórico confiável de validação e auditoria.'
  }
];

const steps = [
  'Cadastre clientes e defina o escopo de automação.',
  'Importe roteiros e transforme-os em casos de teste.',
  'Execute, acompanhe e compartilhe resultados com a equipe.'
];

function HomePage() {
  return (
    <div className="home-page">
      <header className="topbar">
        <Link to="/" className="brand">
          <span className="brand-mark">⚙</span>
          <span>FluxTest</span>
        </Link>
        <nav className="topnav">
          <a href="#recursos">Recursos</a>
          <a href="#como-funciona">Como funciona</a>
          <Link to="/login" className="text-link">Entrar</Link>
          <Link to="/register" className="button small primary">Começar</Link>
        </nav>
      </header>

      <section className="hero-section">
        <div className="hero-copy">
          <span className="eyebrow">Plataforma de automação de testes</span>
          <h1>Organize, execute e acompanhe seus testes em um único lugar.</h1>
          <p>
            A FluxTest ajuda times de QA, tecnologia e operação a estruturar roteiros, validar cenários e guardar evidências com mais agilidade e menos retrabalho.
          </p>
          <div className="hero-actions">
            <Link to="/register" className="button primary">Criar conta</Link>
            <Link to="/login" className="button secondary">Entrar</Link>
          </div>
          <div className="trust-row">
            <span>✅ Setup simples</span>
            <span>📈 Visão do ciclo completo</span>
            <span>🔐 Acesso seguro</span>
          </div>
        </div>

        <div className="hero-visual panel">
          <div className="visual-card">
            <img
              src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='560' height='420' viewBox='0 0 560 420'%3E%3Crect width='560' height='420' rx='28' fill='%23f8fbff'/%3E%3Crect x='44' y='48' width='472' height='324' rx='20' fill='%23ffffff' stroke='%23dbeafe' stroke-width='2'/%3E%3Crect x='70' y='84' width='200' height='16' rx='8' fill='%230f172a'/%3E%3Crect x='70' y='118' width='160' height='12' rx='6' fill='%236b7280'/%3E%3Crect x='70' y='158' width='220' height='92' rx='16' fill='%23eff6ff'/%3E%3Crect x='308' y='158' width='182' height='92' rx='16' fill='%23fef3c7'/%3E%3Crect x='70' y='276' width='420' height='64' rx='16' fill='%23f8fafc' stroke='%23e2e8f0'/%3E%3Ccircle cx='112' cy='308' r='12' fill='%232563eb'/%3E%3Ccircle cx='152' cy='308' r='12' fill='%231d4ed8'/%3E%3Ccircle cx='192' cy='308' r='12' fill='%233b82f6'/%3E%3Cpath d='M358 198h92' stroke='%23f59e0b' stroke-width='12' stroke-linecap='round'/%3E%3Cpath d='M358 220h62' stroke='%23f59e0b' stroke-width='12' stroke-linecap='round'/%3E%3C/svg%3E"
              alt="Dashboard de automação de testes"
            />
          </div>
        </div>
      </section>

      <section id="recursos" className="feature-section">
        <div className="section-heading">
          <span className="eyebrow">Recursos principais</span>
          <h2>Mais controle para cada etapa do ciclo de teste</h2>
        </div>
        <div className="cards">
          {features.map((feature) => (
            <article key={feature.title} className="card">
              <div className="icon-badge">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="como-funciona" className="process-section">
        <div className="section-heading">
          <span className="eyebrow">Como funciona</span>
          <h2>Do roteiro à execução, tudo acompanhado em tempo real</h2>
        </div>
        <div className="grid">
          {steps.map((step, index) => (
            <div key={step} className="panel step-card">
              <h3>0{index + 1}</h3>
              <p>{step}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="cta-section panel">
        <h2>Pronto para acelerar sua rotina de testes?</h2>
        <p>Crie sua conta e comece a organizar roteiros, acompanhar execuções e consolidar evidências em poucos minutos.</p>
        <Link to="/register" className="button primary">Começar agora</Link>
      </section>
    </div>
  );
}

export default HomePage;
