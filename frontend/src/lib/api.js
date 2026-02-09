export function getBackendUrl() {
	return import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
}

export async function callBackendAPI(endpoint, options = {}) {
	const token = localStorage.getItem('firebaseToken');
	const headers = {
		'Content-Type': 'application/json',
		...options.headers
	};

	if (token && !options.skipAuth) {
		headers['Authorization'] = `Bearer ${token}`;
	}

	const response = await fetch(`${getBackendUrl()}${endpoint}`, {
		...options,
		headers
	});

	if (!response.ok) {
		const error = await response.json();
		throw new Error(error.detail || 'API error');
	}

	return response.json();
}
