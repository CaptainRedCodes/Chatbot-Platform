import { useState, useEffect } from 'react';
import client from '../api/client';

export function useSessions(projectId) {
    const [sessions, setSessions] = useState([]);
    const [currentSession, setCurrentSession] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (projectId) {
            fetchSessions();
        }
    }, [projectId]);

    const fetchSessions = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await client.get('/sessions/', {
                params: { project_id: projectId }
            });
            setSessions(res.data);
        } catch (err) {
            console.error("Failed to fetch sessions:", err);
            setError(err.response?.data?.detail || 'Failed to fetch chat sessions');
        } finally {
            setLoading(false);
        }
    };

    const createSession = async (title, chatModel) => {
        setLoading(true);
        setError(null);
        try {
            const res = await client.post('/sessions/', {
                project_id: projectId,
                title: title || 'New Conversation',
                chat_model: chatModel
            });
            setSessions([res.data, ...sessions]);
            return res.data;
        } catch (err) {
            console.error("Failed to create session:", err);
            setError(err.response?.data?.detail || 'Failed to create new chat');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const deleteSession = async (sessionId) => {
        const previousSessions = sessions;
        setSessions(sessions.filter(s => s.id !== sessionId));

        if (currentSession?.id === sessionId) {
            setCurrentSession(null);
        }

        try {
            await client.delete(`/sessions/${sessionId}`);
        } catch (error) {
            console.error("Failed to delete session:", error);
            setError(error.response?.data?.detail || 'Failed to delete chat');
            setSessions(previousSessions);
            throw error;
        }
    };

    const renameSession = async (sessionId, newTitle) => {
        if (!newTitle.trim()) return;

        try {
            await client.patch(`/sessions/${sessionId}`, {
                title: newTitle.trim()
            });
            setSessions(sessions.map(s =>
                s.id === sessionId ? { ...s, title: newTitle.trim() } : s
            ));
            if (currentSession?.id === sessionId) {
                setCurrentSession({ ...currentSession, title: newTitle.trim() });
            }
        } catch (error) {
            console.error("Failed to rename session:", error);
            setError(error.response?.data?.detail || 'Failed to rename chat');
            throw error;
        }
    };

    return {
        sessions,
        currentSession,
        setCurrentSession,
        loading,
        error,
        setError,
        fetchSessions,
        createSession,
        deleteSession,
        renameSession
    };
}