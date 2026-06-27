import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

export function useApi(apiFunc, deps = []) {
  const { token } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    async function loadData() {
      try {
        setLoading(true);
        const result = await apiFunc();
        setData(result);
        setError('');
      } catch (err) {
        setError(err.message || 'Erro ao carregar dados');
        setData(null);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [token, ...deps]);

  return { data, error, loading };
}
