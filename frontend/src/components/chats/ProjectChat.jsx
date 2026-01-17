import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useSessions } from '../../hooks/useSession';
import { useChat } from '../../hooks/useChat';
import { useSystemPrompt } from '../../hooks/useSystemPrompt';
import ChatSidebar from './ChatsSidebar';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatsMessages';
import ChatInput from './ChatInput';
import NewChatModal from './modals/NewChatModal';
import SystemPromptModal from './modals/SystemPromptModal';

export default function ProjectChat() {
    const { projectId } = useParams();
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [showNewChatModal, setShowNewChatModal] = useState(false);
    const [showSystemPromptModal, setShowSystemPromptModal] = useState(false);

    // Custom hooks for state management
    const {
        sessions,
        currentSession,
        setCurrentSession,
        loading: sessionsLoading,
        error,
        setError,
        createSession,
        deleteSession,
        renameSession
    } = useSessions(projectId);

    const {
        messages,
        input,
        setInput,
        sending,
        historyLoading,
        messagesEndRef,
        sendMessage
    } = useChat(currentSession);

    const {
        systemPrompt,
        setSystemPrompt,
        loading: systemPromptLoading,
        fetchSystemPrompt,
        saveSystemPrompt
    } = useSystemPrompt(projectId);

    // Handlers
    const handleSelectSession = async (session) => {
        setCurrentSession(session);
        if (window.innerWidth < 768) setSidebarOpen(false);
    };

    const handleCreateSession = async (title, model) => {
        try {
            const newSession = await createSession(title, model);
            handleSelectSession(newSession);
            setShowNewChatModal(false);
        } catch (err) {
            // Error handled in hook
        }
    };

    const handleOpenSystemPrompt = async () => {
        setShowSystemPromptModal(true);
        await fetchSystemPrompt();
    };

    const handleSaveSystemPrompt = async () => {
        const success = await saveSystemPrompt();
        if (success) {
            setShowSystemPromptModal(false);
        }
    };

    const handleSendMessage = async (message) => {
        if (currentSession) {
            await sendMessage(currentSession.id, message);
        }
    };

    return (
        <div className="flex h-screen bg-background text-foreground overflow-hidden">
            {/* Modals */}
            <NewChatModal
                isOpen={showNewChatModal}
                onClose={() => setShowNewChatModal(false)}
                onCreate={handleCreateSession}
                loading={sessionsLoading}
            />

            <SystemPromptModal
                isOpen={showSystemPromptModal}
                onClose={() => setShowSystemPromptModal(false)}
                systemPrompt={systemPrompt}
                setSystemPrompt={setSystemPrompt}
                onSave={handleSaveSystemPrompt}
                loading={systemPromptLoading}
            />

            {/* Sidebar */}
            <ChatSidebar
                isOpen={sidebarOpen}
                sessions={sessions}
                currentSession={currentSession}
                onSelectSession={handleSelectSession}
                onNewChat={() => setShowNewChatModal(true)}
                onDeleteSession={deleteSession}
                onRenameSession={renameSession}
                error={error}
                onClearError={() => setError(null)}
                loading={sessionsLoading}
            />

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col h-full relative">
                <ChatHeader
                    currentSession={currentSession}
                    onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
                    onOpenSystemPrompt={handleOpenSystemPrompt}
                />

                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-muted/20">
                    <ChatMessages
                        currentSession={currentSession}
                        messages={messages}
                        historyLoading={historyLoading}
                        messagesEndRef={messagesEndRef}
                    />
                </div>

                {currentSession && (
                    <ChatInput
                        input={input}
                        setInput={setInput}
                        onSend={handleSendMessage}
                        disabled={sending}
                    />
                )}
            </div>
        </div>
    );
}