const API_BASE_URL = 'http://localhost:5000/api';

class ApiClient {
    constructor() {
        this.token = localStorage.getItem('access_token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('access_token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('access_token');
    }

    isLoggedIn() {
        return !!this.token;
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.getHeaders(),
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, config);

            if (response.status === 401) {
                this.clearToken();
                // Optionally redirect or notify
            }

            const data = await response.json();

            if (!response.ok) {
                return { success: false, error: data.detail || 'Error' };
            }

            return { success: true, data: data };
        } catch (error) {
            console.error('API Request Failed:', error);
            return { success: false, error: error.message };
        }
    }

    // Specific methods as used in index.html

    async submitQuiz(data) {
        return this.request('/quiz/submit', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async getHistory() {
        return this.request('/quiz/history', {
            method: 'GET'
        });
    }

    async login(email, password) {
        const res = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        if (res.success && res.data.token) {
            this.setToken(res.data.token);
        }
        return res;
    }

    async register(name, email, password) {
        const res = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password })
        });
        if (res.success && res.data.token) {
            this.setToken(res.data.token);
        }
        return res;
    }

    async getMe() {
        return this.request('/auth/me', { method: 'GET' });
    }

    async getLeaderboard() {
        return this.request('/stats/leaderboard', { method: 'GET' });
    }
}

// Expose as global API object to match index.html expectation
const API = new ApiClient();

// Keep generic api for auth.js if needed or update auth.js to use API
const api = API; 
