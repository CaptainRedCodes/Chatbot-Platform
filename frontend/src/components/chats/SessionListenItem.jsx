import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MessageSquare, Edit2, Trash2, Check, X } from 'lucide-react';

export default function SessionListItem({
    session,
    isActive,
    onSelect,
    onDelete,
    onRename
}) {
    const [isEditing, setIsEditing] = useState(false);
    const [editTitle, setEditTitle] = useState(session.title || 'New Chat');

    const handleRename = async () => {
        if (!editTitle.trim()) {
            setIsEditing(false);
            return;
        }
        await onRename(session.id, editTitle);
        setIsEditing(false);
    };

    const handleDelete = (e) => {
        e.stopPropagation();
        if (window.confirm("Delete this chat? This cannot be undone.")) {
            onDelete(session.id);
        }
    };

    const startEditing = (e) => {
        e.stopPropagation();
        setIsEditing(true);
        setEditTitle(session.title || 'New Chat');
    };

    return (
        <div
            onClick={() => !isEditing && onSelect(session)}
            className={`
                flex items-center justify-between p-2 rounded cursor-pointer
                ${isActive ? 'bg-primary/10 border border-primary/30' : 'hover:bg-muted'}
            `}
        >
            <div className="flex items-center gap-2 flex-1 min-w-0">
                <MessageSquare className="w-4 h-4 flex-shrink-0 text-muted-foreground" />
                {isEditing ? (
                    <div className="flex items-center gap-1 flex-1" onClick={e => e.stopPropagation()}>
                        <Input
                            value={editTitle}
                            onChange={(e) => setEditTitle(e.target.value)}
                            className="h-7 text-sm"
                            autoFocus
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') handleRename();
                                if (e.key === 'Escape') setIsEditing(false);
                            }}
                        />
                        <Button variant="outline" size="sm" className="h-7 w-7 p-0" onClick={handleRename}>
                            <Check className="w-3 h-3" />
                        </Button>
                        <Button variant="outline" size="sm" className="h-7 w-7 p-0" onClick={() => setIsEditing(false)}>
                            <X className="w-3 h-3" />
                        </Button>
                    </div>
                ) : (
                    <span className="truncate text-sm">{session.title || "New Chat"}</span>
                )}
            </div>

            {!isEditing && (
                <div className="flex items-center gap-1 ml-2">
                    <Button variant="ghost" size="sm" className="h-7 w-7 p-0" onClick={startEditing}>
                        <Edit2 className="w-3 h-3" />
                    </Button>
                    <Button variant="ghost" size="sm" className="h-7 w-7 p-0 text-red-600" onClick={handleDelete}>
                        <Trash2 className="w-3 h-3" />
                    </Button>
                </div>
            )}
        </div>
    );
}