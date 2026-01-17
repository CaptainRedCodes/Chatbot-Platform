import React from 'react';
import { Button } from '@/components/ui/button';
import { Menu } from 'lucide-react';

export default function ChatHeader({
    currentSession,
    onToggleSidebar,
    onOpenSystemPrompt
}) {
    return (
        <div className="h-14 border-b border-border flex items-center px-4 justify-between bg-background">
            <div className="flex items-center gap-3">
                <Button
                    variant="outline"
                    size="sm"
                    className="md:hidden"
                    onClick={onToggleSidebar}
                >
                    <Menu className="w-4 h-4" />
                </Button>
                <h2 className="font-medium">
                    {currentSession ? (currentSession.title || "Chat") : "Select a conversation"}
                </h2>
                {currentSession?.chat_model && (
                    <span className="text-xs px-2 py-0.5 rounded bg-muted text-muted-foreground">
                        {currentSession.chat_model}
                    </span>
                )}
            </div>
            <Button
                variant="outline"
                size="sm"
                onClick={onOpenSystemPrompt}
            >
                System Prompt
            </Button>
        </div>
    );
}