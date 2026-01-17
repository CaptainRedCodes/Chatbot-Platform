import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Plus, X } from 'lucide-react';
import SessionListItem from './SessionListenItem';

export default function ChatSidebar({
    isOpen,
    sessions,
    currentSession,
    onSelectSession,
    onNewChat,
    onDeleteSession,
    onRenameSession,
    error,
    onClearError,
    loading
}) {
    const navigate = useNavigate();

    return (
        <div
            className={`
                fixed inset-y-0 left-0 z-50 w-72 bg-card border-r border-border
                ${isOpen ? 'translate-x-0' : '-translate-x-full'}
                md:relative md:translate-x-0 flex flex-col
            `}
        >
            <div className="p-3 border-b border-border flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm" onClick={() => navigate('/')}>
                        <ArrowLeft className="w-4 h-4" />
                    </Button>
                    <span className="font-medium">Chats</span>
                </div>
                <Button onClick={onNewChat} size="sm">
                    <Plus className="w-4 h-4 mr-1" /> New
                </Button>
            </div>

            <div className="flex-1 overflow-y-auto p-2 space-y-1">
                {error && (
                    <div className="flex items-center justify-between p-2 text-xs text-red-600 bg-red-50 rounded border border-red-200 mb-2">
                        <span>{error}</span>
                        <button onClick={onClearError}><X className="h-3 w-3" /></button>
                    </div>
                )}
                {sessions.length === 0 && !loading && !error && (
                    <div className="text-center text-muted-foreground text-sm mt-8">
                        No chats yet. Start a new one!
                    </div>
                )}
                {sessions.map(session => (
                    <SessionListItem
                        key={session.id}
                        session={session}
                        isActive={currentSession?.id === session.id}
                        onSelect={onSelectSession}
                        onDelete={onDeleteSession}
                        onRename={onRenameSession}
                    />
                ))}
            </div>
        </div>
    );
}