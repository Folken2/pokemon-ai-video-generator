/**
 * API Client for AI Documentary Pipeline
 */

const API_BASE = '/api';

function authHeaders(extra = {}) {
    const h = { ...extra };
    if (window.__API_KEY__) h['X-API-Key'] = window.__API_KEY__;
    return h;
}

const api = {
    // --- Projects ---
    async listProjects() {
        const resp = await fetch(`${API_BASE}/projects/`, { headers: authHeaders() });
        return resp.json();
    },

    async createProject(subjectName, theme = 'pokemon') {
        const resp = await fetch(`${API_BASE}/projects/`, {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ subject_name: subjectName, theme }),
        });
        return resp.json();
    },

    async getProject(subjectName) {
        const resp = await fetch(`${API_BASE}/projects/${subjectName}`, { headers: authHeaders() });
        return resp.json();
    },

    async getArtifacts(subjectName, stepName) {
        const resp = await fetch(`${API_BASE}/projects/${subjectName}/artifacts/${stepName}`, { headers: authHeaders() });
        return resp.json();
    },

    // --- Pipeline ---
    async runStep(subjectName, stepName) {
        const resp = await fetch(`${API_BASE}/pipeline/${subjectName}/run`, {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ step: stepName }),
        });
        return resp.json();
    },

    async approveStep(subjectName, stepName, feedback = '', selectedOption = null) {
        const body = { step: stepName, feedback };
        if (selectedOption !== null) {
            body.selected_option = selectedOption;
        }
        const resp = await fetch(`${API_BASE}/pipeline/${subjectName}/approve`, {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify(body),
        });
        return resp.json();
    },

    async retryStep(subjectName, stepName) {
        const resp = await fetch(`${API_BASE}/pipeline/${subjectName}/retry`, {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ step: stepName }),
        });
        return resp.json();
    },

    async getPipelineStatus(subjectName) {
        const resp = await fetch(`${API_BASE}/pipeline/${subjectName}/status`, { headers: authHeaders() });
        return resp.json();
    },

    async getStepDetail(subjectName, stepName) {
        const resp = await fetch(`${API_BASE}/pipeline/${subjectName}/step/${stepName}`, { headers: authHeaders() });
        return resp.json();
    },

    async regenerateAsset(subjectName, filename, feedback) {
        const resp = await fetch(`${API_BASE}/pipeline/${subjectName}/regenerate-asset`, {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ step: 'asset_generation', asset_filename: filename, feedback }),
        });
        return resp.json();
    },

    async listThemes() {
        const resp = await fetch(`${API_BASE}/projects/themes`, { headers: authHeaders() });
        return resp.json();
    },

    async listSubjects(theme, query = '') {
        const params = query ? `?q=${encodeURIComponent(query)}` : '';
        const resp = await fetch(`${API_BASE}/projects/subjects/${theme}${params}`, { headers: authHeaders() });
        return resp.json();
    },

    // --- Health ---
    async checkHealth() {
        const resp = await fetch(`${API_BASE}/health`, { headers: authHeaders() });
        return resp.json();
    },
};
