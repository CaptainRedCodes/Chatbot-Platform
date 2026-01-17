import { useState } from 'react';
import client from '../api/client';

export function useSystemPrompt(projectId) {
    const [systemPrompt, setSystemPrompt] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchSystemPrompt = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await client.get(`/project/${projectId}`);
            setSystemPrompt(res.data.system_prompt || '');
        } catch (err) {
            console.error("Failed to fetch project:", err);
            setError('Failed to load system prompt');
        } finally {
            setLoading(false);
        }
    };

    const saveSystemPrompt = async () => {
        setLoading(true);
        setError(null);
        try {
            await client.patch(`/project/${projectId}`, { system_prompt: systemPrompt });
            return true;
        } catch (err) {
            console.error("Failed to save system prompt:", err);
            setError(err.response?.data?.detail || 'Failed to save system prompt');
            return false;
        } finally {
            setLoading(false);
        }
    };

    return {
        systemPrompt,
        setSystemPrompt,
        loading,
        error,
        fetchSystemPrompt,
        saveSystemPrompt
    };
}