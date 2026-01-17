import { useState, useEffect, useRef } from 'react';
import client from '../api/client';

const baseURL = import.meta.env.VITE_BASE_URL;
export function useChat(currentSession) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [sending, setSending] = useState(false);
    const [historyLoading, setHistoryLoading] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        if (currentSession) {
            loadHistory(currentSession.id);
        } else {
            setMessages([]);
        }
        setSending(false);
    }, [currentSession]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const loadHistory = async (sessionId) => {
        setMessages([]);
        setHistoryLoading(true);
        try {
            const historyRes = await client.get(`/sessions/${sessionId}/history`);
            setMessages(historyRes.data);
        } catch (error) {
            console.error("Failed to load history:", error);
        } finally {
            setHistoryLoading(false);
        }
    };

    const sendMessage = async (sessionId, messageContent) => {
        if (!messageContent.trim() || sending) return;

        const userMsg = { role: 'user', content: messageContent };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setSending(true);

        setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${baseURL}/sessions/${sessionId}/chat/stream`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    message: userMsg.content
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') continue;

                        setMessages(prev => {
                            const updated = [...prev];
                            const lastIdx = updated.length - 1;
                            if (lastIdx >= 0 && updated[lastIdx].role === 'assistant') {
                                updated[lastIdx] = {
                                    ...updated[lastIdx],
                                    content: updated[lastIdx].content + data
                                };
                            }
                            return updated;
                        });
                    }
                }
            }
        } catch (error) {
            console.error("Failed to send message:", error);
            setMessages(prev => {
                const updated = [...prev];
                const lastIdx = updated.length - 1;
                if (lastIdx >= 0 && updated[lastIdx].role === 'assistant' && !updated[lastIdx].content) {
                    updated[lastIdx] = { role: 'system', content: 'Error sending message. Please try again.' };
                }
                return updated;
            });
        } finally {
            setSending(false);
        }
    };

    return {
        messages,
        input,
        setInput,
        sending,
        historyLoading,
        messagesEndRef,
        sendMessage
    };
}