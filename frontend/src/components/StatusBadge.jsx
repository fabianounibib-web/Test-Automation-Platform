function StatusBadge({ status }) {
  const normalized = (status || 'unknown').toLowerCase();
  const colors = {
    success: '#16a34a',
    failed: '#dc2626',
    running: '#2563eb',
    error: '#ea580c',
    pending: '#64748b'
  };

  return (
    <span
      style={{
        background: colors[normalized] || '#64748b',
        color: 'white',
        padding: '0.25rem 0.6rem',
        borderRadius: '999px',
        fontSize: '0.8rem',
        display: 'inline-block'
      }}
    >
      {status || 'Desconhecido'}
    </span>
  );
}

export default StatusBadge;
