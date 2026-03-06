// API Client with automatic token inclusion
const API_BASE_URL = "http://localhost:5000";

export const apiClient = {
  async request(endpoint, options = {}) {
    const token = localStorage.getItem("authToken");
    
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "API request failed");
      }

      return data;
    } catch (error) {
      console.error(`API Error: ${endpoint}`, error);
      throw error;
    }
  },

  get(endpoint, options = {}) {
    return this.request(endpoint, { method: "GET", ...options });
  },

  post(endpoint, body = {}, options = {}) {
    return this.request(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
      ...options,
    });
  },

  put(endpoint, body = {}, options = {}) {
    return this.request(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
      ...options,
    });
  },

  delete(endpoint, options = {}) {
    return this.request(endpoint, { method: "DELETE", ...options });
  },
};
