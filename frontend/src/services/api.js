const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

function getAuthToken() {
  return localStorage.getItem('auth-token') || '';
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      Authorization: getAuthToken() ? `Bearer ${getAuthToken()}` : '',
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    let errorMessage = 'Erro ao consultar a API';
    try {
      const error = await response.json();
      errorMessage = error.error || error.message || errorMessage;
    } catch (e) {
      // If response is not JSON, use default error message
    }
    throw new Error(errorMessage);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

// ============ Authentication ============

export async function login(email, senha) {
  const result = await request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, senha })
  });
  return result.data;
}

export async function register(nome, email, senha) {
  const result = await request('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ nome, email, senha })
  });
  return result.data;
}

export async function getCurrentUser() {
  const result = await request('/auth/me');
  return result.data;
}

export async function refreshToken() {
  const result = await request('/auth/refresh', { method: 'POST' });
  return result.data;
}

// ============ Clientes ============

export async function getClientes(page = 1, per_page = 20) {
  const result = await request(`/clientes?page=${page}&per_page=${per_page}`);
  return result.data;
}

export async function getCliente(id) {
  const result = await request(`/clientes/${id}`);
  return result.data;
}

export async function createCliente(payload) {
  const result = await request('/clientes', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
  return result.data;
}

export async function updateCliente(id, payload) {
  const result = await request(`/clientes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  });
  return result.data;
}

export async function deleteCliente(id) {
  await request(`/clientes/${id}`, { method: 'DELETE' });
}

// ============ Sistemas / Conectores ============

export async function getSistemas(page = 1, per_page = 20) {
  const result = await request(`/conectores?page=${page}&per_page=${per_page}`);
  return result.data;
}

export async function getSistema(id) {
  const result = await request(`/conectores/${id}`);
  return result.data;
}

export async function createSistema(payload) {
  const result = await request('/conectores', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
  return result.data;
}

export async function updateSistema(id, payload) {
  const result = await request(`/conectores/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  });
  return result.data;
}

export async function deleteSistema(id) {
  await request(`/conectores/${id}`, { method: 'DELETE' });
}

export async function getSistemaSteps(id) {
  const result = await request(`/conectores/${id}/steps`);
  return result.data;
}

export async function saveSistemaSteps(id, steps) {
  const result = await request(`/conectores/${id}/steps`, {
    method: 'POST',
    body: JSON.stringify({ steps })
  });
  return result.data;
}

// ============ Casos de Teste ============

export async function getCasos(page = 1, per_page = 20, filters = {}) {
  const params = new URLSearchParams({ page, per_page, ...filters });
  const result = await request(`/casos?${params}`);
  return result.data;
}

export async function getCaso(id) {
  const result = await request(`/casos/${id}`);
  return result.data;
}

export async function createCaso(payload) {
  const result = await request('/casos', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
  return result.data;
}

export async function updateCaso(id, payload) {
  const result = await request(`/casos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  });
  return result.data;
}

export async function deleteCaso(id) {
  await request(`/casos/${id}`, { method: 'DELETE' });
}

// ============ Roteiros ============

export async function getRoteiros(page = 1, per_page = 20, filters = {}) {
  const params = new URLSearchParams({ page, per_page, ...filters });
  const result = await request(`/roteiros?${params}`);
  return result.data;
}

export async function getRoteiro(id) {
  const result = await request(`/roteiros/${id}`);
  return result.data;
}

export async function uploadRoteiro(file, clienteId) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('cliente_id', clienteId);

  const response = await fetch(`${API_BASE_URL}/roteiros/upload`, {
    method: 'POST',
    headers: {
      Authorization: getAuthToken() ? `Bearer ${getAuthToken()}` : ''
    },
    body: formData
  });

  if (!response.ok) {
    throw new Error('Erro ao fazer upload do roteiro');
  }

  const data = await response.json();
  return data.data;
}

export async function deleteRoteiro(id) {
  await request(`/roteiros/${id}`, { method: 'DELETE' });
}

// ============ Execuções ============

export async function getExecucoes(page = 1, per_page = 20, filters = {}) {
  const params = new URLSearchParams({ page, per_page, ...filters });
  const result = await request(`/execucoes?${params}`);
  return result.data;
}

export async function getExecucao(id) {
  const result = await request(`/execucoes/${id}`);
  return result.data;
}

export async function executeCaso(casoId) {
  const result = await request(`/execucoes/casos/${casoId}/execute`, {
    method: 'POST'
  });
  return result.data;
}

export async function getExecucaoLogs(execucaoId, page = 1, per_page = 50, filters = {}) {
  const params = new URLSearchParams({ page, per_page, ...filters });
  const result = await request(`/execucoes/${execucaoId}/logs?${params}`);
  return result.data;
}

export async function getExecucaoEvidencias(execucaoId, page = 1, per_page = 50, filters = {}) {
  const params = new URLSearchParams({ page, per_page, ...filters });
  const result = await request(`/execucoes/${execucaoId}/evidencias?${params}`);
  return result.data;
}

export async function cancelExecution(execucaoId) {
  const result = await request(`/execucoes/${execucaoId}/cancel`, {
    method: 'POST'
  });
  return result.data;
}

// ============ Dashboard ============

export async function getDashboard() {
  const result = await request('/dashboard');
  return result.data;
}
