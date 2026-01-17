import React from 'react';
import ChatSkeleton from '@/components/ChatSkeleton';

export default function ChatMessages({
    currentSession,
    messages,
    historyLoading,
    messagesEndRef
}) {
    if (!currentSession) {
        return (
            <div className="h-full flex items-center justify-center text-muted-foreground">
                <p>Select or create a chat to begin</p>
            </div>
        );
    }

    if (historyLoading) {
        return <ChatSkeleton messageCount={4} />;
    }

    return (
    <>
        {messages
            .filter(msg => msg.role !== 'system')gi
            .map((msg, idx) => (
                <div
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                    <div
                        className={`
                            max-w-[80%] rounded-md px-3 py-2 text-sm whitespace-pre-wrap
                            ${msg.role === 'user'
                                ? 'bg-primary text-primary-foreground'
                                : 'bg-muted border border-border'} 
                        `}
                    >
                        {msg.content}
                    </div>
                </div>
            ))}
        <div ref={messagesEndRef} />
    </>
);
}