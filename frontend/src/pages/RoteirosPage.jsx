import { useEffect, useState } from 'react';
import { getRoteiros, uploadRoteiro } from '../services/api';

function RoteirosPage() {
  const [roteiros, setRoteiros] = useState([]);
  const [message, setMessage] = useState('');
  const [file, setFile] = useState(null);

  useEffect(() => {
    getRoteiros().then(setRoteiros).catch(() => setRoteiros([]));
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!file) {
      setMessage('Selecione um arquivo para upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const result = await uploadRoteiro(formData);
      setRoteiros((prev) => [...prev, result]);
      setMessage('Roteiro enviado com sucesso.');
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <div className="header">
        <div>
          <h1>Roteiros</h1>
          <p>Importação e acompanhamento de roteiros enviados pelos clientes.</p>
        </div>
      </div>

      <div className="grid">
        <section className="panel">
          <h3>Upload de roteiro</h3>
          <form onSubmit={handleSubmit}>
            <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
            <button type="submit">Enviar</button>
          </form>
          {message && <p>{message}</p>}
        </section>

        <section className="panel">
          <h3>Roteiros recentes</h3>
          {roteiros.length ? (
            <ul>
              {roteiros.map((roteiro) => (
                <li key={roteiro.id || roteiro.arquivo}>{roteiro.arquivo || 'Roteiro sem nome'}</li>
              ))}
            </ul>
          ) : (
            <p>Ainda não há roteiros importados.</p>
          )}
        </section>
      </div>
    </div>
  );
}

export default RoteirosPage;
