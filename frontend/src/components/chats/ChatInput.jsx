import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send } from 'lucide-react';

export default function ChatInput({
    input,
    setInput,
    onSend,
    disabled
}) {
    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim() || disabled) return;
        onSend(input);
    };

    return (
        <div className="p-4 bg-background border-t border-border">
            <form onSubmit={handleSubmit} className="flex gap-2 max-w-3xl mx-auto">
                <Input
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    placeholder="Type a message..."
                    className="flex-1"
                    disabled={disabled}
                    autoFocus
                />
                <Button type="submit" disabled={!input.trim() || disabled}>
                    <Send className="w-4 h-4" />
                </Button>
            </form>
        </div>
    );
}