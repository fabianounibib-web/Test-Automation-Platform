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
    const errorText = await response.text();
    throw new Error(errorText || 'Erro ao consultar a API');
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export async function getDashboard() {
  return request('/dashboard');
}

export async function getClientes() {
  return request('/clientes');
}

export async function createCliente(payload) {
  return request('/clientes', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export async function getRoteiros() {
  return request('/roteiros');
}

export async function uploadRoteiro(formData) {
  return fetch(`${API_BASE_URL}/roteiros/upload`, {
    method: 'POST',
    body: formData
  }).then(async (response) => {
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || 'Falha no upload');
    }

    return response.json();
  });
}

export async function getCasos() {
  return request('/casos');
}

export async function executarCaso(id) {
  return request(`/casos/${id}/executar`, {
    method: 'POST'
  });
}

export async function getExecucoes() {
  return request('/execucoes');
}

export async function getRobos() {
  return request('/robos');
}

export async function createRobo(payload) {
  return request('/robos', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export async function executarRobo(id) {
  return request(`/robos/${id}/executar`, {
    method: 'POST'
  });
}

export async function login(payload) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}

export async function register(payload) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}
