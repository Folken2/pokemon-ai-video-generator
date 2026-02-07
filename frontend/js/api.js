/**
 * API Client for Pokemon Documentary Pipeline
 */

const API_BASE = '/api';

const api = {
    // --- Projects ---
    async listProjects() {
        const resp = await fetch(`${API_BASE}/projects/`);
        return resp.json();
    },

    async createProject(pokemonName) {
        const resp = await fetch(`${API_BASE}/projects/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pokemon_name: pokemonName }),
        });
        return resp.json();
    },

    async getProject(pokemonName) {
        const resp = await fetch(`${API_BASE}/projects/${pokemonName}`);
        return resp.json();
    },

    async getArtifacts(pokemonName, stepName) {
        const resp = await fetch(`${API_BASE}/projects/${pokemonName}/artifacts/${stepName}`);
        return resp.json();
    },

    // --- Pipeline ---
    async runStep(pokemonName, stepName) {
        const resp = await fetch(`${API_BASE}/pipeline/${pokemonName}/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ step: stepName }),
        });
        return resp.json();
    },

    async approveStep(pokemonName, stepName, feedback = '', selectedOption = null) {
        const body = { step: stepName, feedback };
        if (selectedOption !== null) {
            body.selected_option = selectedOption;
        }
        const resp = await fetch(`${API_BASE}/pipeline/${pokemonName}/approve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        return resp.json();
    },

    async retryStep(pokemonName, stepName) {
        const resp = await fetch(`${API_BASE}/pipeline/${pokemonName}/retry`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ step: stepName }),
        });
        return resp.json();
    },

    async getPipelineStatus(pokemonName) {
        const resp = await fetch(`${API_BASE}/pipeline/${pokemonName}/status`);
        return resp.json();
    },

    async getStepDetail(pokemonName, stepName) {
        const resp = await fetch(`${API_BASE}/pipeline/${pokemonName}/step/${stepName}`);
        return resp.json();
    },

    // --- Health ---
    async checkHealth() {
        const resp = await fetch(`${API_BASE}/health`);
        return resp.json();
    },
};
