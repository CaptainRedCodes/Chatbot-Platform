import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import client from '../api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import {
    MessageSquare, Send, Plus, Trash2, ArrowLeft, Bot, User, Menu, Loader2, AlertCircle, X
} from 'lucide-react';

export default function ProjectChat() {
    const { projectId } = useParams();
    const navigate = useNavigate();

    const [sessions, setSessions] = useState([]);
    const [currentSession, setCurrentSession] = useState(null);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false); // Creating session / loading history
    const [sending, setSending] = useState(false); // Sending message
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [error, setError] = useState(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        fetchSessions();
    }, [projectId]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const fetchSessions = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await client.get('/sessions/', {
                params: { project_id: projectId } // Pass project_id filter
            });
            setSessions(res.data);
        } catch (err) {
            console.error("Failed to fetch sessions:", err);
            setError(err.response?.data?.detail || 'Failed to fetch chat sessions');
        } finally {
            setLoading(false);
        }
    };

    const handleCreateSession = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await client.post('/sessions/', {
                project_id: projectId,
                title: 'New Conversation'
            });
            setSessions([res.data, ...sessions]);
            handleSelectSession(res.data);
        } catch (err) {
            console.error("Failed to create session:", err);
            setError(err.response?.data?.detail || 'Failed to create new chat');
        } finally {
            setLoading(false);
        }
    };

    const handleSelectSession = async (session) => {
        setCurrentSession(session);
        setMessages([]); // Clear previous
        setLoading(true);

        // On mobile, close sidebar
        if (window.innerWidth < 768) setSidebarOpen(false);

        try {
            const res = await client.get(`/sessions/${session.id}/history`);
            // Map history to UI format if needed. 
            // DB returns { role: 'user'|'assistant', content: '...', ... }
            // Our UI expects that.
            setMessages(res.data);
        } catch (error) {
            console.error("Failed to load history:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteSession = async (e, sessionId) => {
        e.stopPropagation();
        if (!window.confirm("Delete this chat?")) return;

        try {
            await client.delete(`/sessions/${sessionId}`);
            setSessions(sessions.filter(s => s.id !== sessionId));
            if (currentSession?.id === sessionId) {
                setCurrentSession(null);
                setMessages([]);
            }
        } catch (error) {
            console.error("Failed to delete session:", error);
        }
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim() || !currentSession || sending) return;

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setSending(true);

        try {
            const res = await client.post(`/sessions/${currentSession.id}/chat`, {
                message: userMsg.content
            });

            const botMsg = { role: 'assistant', content: res.data.response };
            setMessages(prev => [...prev, botMsg]);
        } catch (error) {
            console.error("Failed to send message:", error);
            setMessages(prev => [...prev, { role: 'system', content: 'Error sending message.' }]);
        } finally {
            setSending(false);
        }
    };

    return (
        <div className="flex h-screen bg-background text-foreground overflow-hidden">
            {/* Sidebar */}
            <div
                className={`
                    fixed inset-y-0 left-0 z-50 w-80 bg-card border-r border-border transform transition-transform duration-300 ease-in-out
                    ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
                    md:relative md:translate-x-0 flex flex-col
                `}
            >
                <div className="p-4 border-b border-border flex items-center justify-between bg-card text-card-foreground">
                    <div className="flex items-center gap-2 font-semibold">
                        <Button variant="ghost" size="icon" onClick={() => navigate('/')}>
                            <ArrowLeft className="w-5 h-5" />
                        </Button>
                        <span>Chats</span>
                    </div>
                    <Button onClick={handleCreateSession} size="sm" className="gap-2">
                        <Plus className="w-4 h-4" /> New
                    </Button>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-2">
                    {error && (
                        <div className="flex items-center gap-x-2 rounded-md bg-destructive/15 p-3 text-sm text-destructive mb-2">
                            <AlertCircle className="h-4 w-4 flex-shrink-0" />
                            <p className="flex-1 text-xs">{error}</p>
                            <Button variant="ghost" size="sm" className="h-5 w-5 p-0" onClick={() => setError(null)}>
                                <X className="h-3 w-3" />
                            </Button>
                        </div>
                    )}
                    {sessions.length === 0 && !loading && !error && (
                        <div className="text-center text-muted-foreground text-sm mt-8">
                            No chats yet. Start a new one!
                        </div>
                    )}
                    {sessions.map(session => (
                        <div
                            key={session.id}
                            onClick={() => handleSelectSession(session)}
                            className={`
                                group flex items-center justify-between p-3 rounded-md cursor-pointer transition-colors
                                ${currentSession?.id === session.id
                                    ? 'bg-primary/10 text-primary border border-primary/20'
                                    : 'hover:bg-muted text-muted-foreground hover:text-foreground'}
                            `}
                        >
                            <div className="flex items-center gap-3 truncate">
                                <MessageSquare className="w-4 h-4" />
                                <div className="flex flex-col text-left truncate">
                                    <span className="font-medium truncate w-40">
                                        {session.title || "New Chat"}
                                    </span>
                                    <span className="text-xs opacity-70">
                                        {new Date(session.created_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>
                            <Button
                                variant="ghost"
                                size="icon"
                                className="opacity-0 group-hover:opacity-100 h-8 w-8 text-destructive hover:bg-destructive/10"
                                onClick={(e) => handleDeleteSession(e, session.id)}
                            >
                                <Trash2 className="w-4 h-4" />
                            </Button>
                        </div>
                    ))}
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col h-full relative">
                {/* Header */}
                <div className="h-16 border-b border-border flex items-center px-4 justify-between bg-background/80 backdrop-blur-sm z-10">
                    <div className="flex items-center gap-2">
                        <Button
                            variant="ghost"
                            size="icon"
                            className="md:hidden"
                            onClick={() => setSidebarOpen(!sidebarOpen)}
                        >
                            <Menu className="w-5 h-5" />
                        </Button>
                        <h2 className="font-semibold text-lg">
                            {currentSession ? (currentSession.title || "Chat") : "Select a conversation"}
                        </h2>
                    </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-muted/20">
                    {!currentSession ? (
                        <div className="h-full flex flex-col items-center justify-center text-muted-foreground opacity-50">
                            <Bot className="w-16 h-16 mb-4" />
                            <p className="text-lg">Select or create a chat to begin</p>
                        </div>
                    ) : (
                        <>
                            {messages.map((msg, idx) => (
                                <div
                                    key={idx}
                                    className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    {msg.role === 'assistant' && (
                                        <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center border border-primary/20">
                                            <Bot className="w-5 h-5 text-primary" />
                                        </div>
                                    )}

                                    <div
                                        className={`
                                            max-w-[80%] rounded-lg px-4 py-2 text-sm shadow-sm whitespace-pre-wrap
                                            ${msg.role === 'user'
                                                ? 'bg-primary text-primary-foreground rounded-br-none'
                                                : 'bg-card border border-border rounded-bl-none'}
                                        `}
                                    >
                                        {msg.content}
                                    </div>

                                    {msg.role === 'user' && (
                                        <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                                            <User className="w-5 h-5 text-muted-foreground" />
                                        </div>
                                    )}
                                </div>
                            ))}
                            {sending && (
                                <div className="flex gap-3">
                                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center border border-primary/20">
                                        <Loader2 className="w-5 h-5 text-primary animate-spin" />
                                    </div>
                                    <div className="bg-card border border-border rounded-lg px-4 py-2 text-sm text-muted-foreground rounded-bl-none">
                                        Thinking...
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </>
                    )}
                </div>

                {/* Input */}
                {currentSession && (
                    <div className="p-4 bg-background border-t border-border">
                        <form onSubmit={handleSendMessage} className="flex gap-2 max-w-3xl mx-auto">
                            <Input
                                value={input}
                                onChange={e => setInput(e.target.value)}
                                placeholder="Type a message..."
                                className="flex-1"
                                disabled={sending}
                                autoFocus
                            />
                            <Button type="submit" disabled={!input.trim() || sending}>
                                <Send className="w-4 h-4" />
                            </Button>
                        </form>
                    </div>
                )}
            </div>
        </div>
    );
}
