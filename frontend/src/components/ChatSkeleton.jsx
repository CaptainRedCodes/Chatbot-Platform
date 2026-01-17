import React from 'react';
import { Bot, User } from 'lucide-react';


export default function ChatSkeleton({ messageCount = 4 }) {
    const skeletonMessages = Array.from({ length: messageCount }, (_, i) => ({
        id: i,
        isUser: i % 2 === 0, // Alternate: user, assistant, user, assistant
        width: ['75%', '60%', '85%', '50%'][i % 4]
    }));

    return (
        <div className="space-y-4 animate-pulse">
            {skeletonMessages.map((msg) => (
                <div
                    key={msg.id}
                    className={`flex gap-3 ${msg.isUser ? 'justify-end' : 'justify-start'}`}
                >
                    {/* Assistant avatar placeholder */}
                    {!msg.isUser && (
                        <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                            <Bot className="w-5 h-5 text-muted-foreground/50" />
                        </div>
                    )}

                    {/* Message bubble skeleton */}
                    <div
                        className={`
                            rounded-lg px-4 py-3 
                            ${msg.isUser
                                ? 'bg-muted/60 rounded-br-none'
                                : 'bg-muted/40 border border-border/50 rounded-bl-none'
                            }
                        `}
                        style={{ width: msg.width, maxWidth: '80%' }}
                    >
                        {/* Text line skeletons */}
                        <div className="space-y-2">
                            <div className="h-3 bg-muted-foreground/20 rounded w-full" />
                            <div className="h-3 bg-muted-foreground/20 rounded w-4/5" />
                            {msg.width === '85%' && (
                                <div className="h-3 bg-muted-foreground/20 rounded w-3/5" />
                            )}
                        </div>
                    </div>

                    {/* User avatar placeholder */}
                    {msg.isUser && (
                        <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
                            <User className="w-5 h-5 text-muted-foreground/50" />
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}
