import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { X, Loader2 } from 'lucide-react';
import { MODEL_OPTIONS, DEFAULT_MODEL } from '../../../constants/model';

export default function NewChatModal({ isOpen, onClose, onCreate, loading }) {
    const [chatTitle, setChatTitle] = useState('New Conversation');
    const [selectedModel, setSelectedModel] = useState(DEFAULT_MODEL);

    const handleCreate = async () => {
        await onCreate(chatTitle, selectedModel);
        setChatTitle('New Conversation');
        setSelectedModel(DEFAULT_MODEL);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-4">
            <div className="w-full max-w-sm bg-card border border-border rounded-md p-5">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold">New Chat</h3>
                    <button onClick={onClose}>
                        <X className="w-4 h-4" />
                    </button>
                </div>

                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-1">Chat Name</label>
                        <Input
                            value={chatTitle}
                            onChange={(e) => setChatTitle(e.target.value)}
                            placeholder="Enter chat name..."
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium mb-1">AI Model</label>
                        <select
                            value={selectedModel}
                            onChange={(e) => setSelectedModel(e.target.value)}
                            className="w-full h-9 rounded-md border border-input bg-background px-3 text-sm"
                        >
                            {MODEL_OPTIONS.map(model => (
                                <option key={model.value} value={model.value}>
                                    {model.label}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="flex gap-2 mt-5">
                    <Button variant="outline" className="flex-1" onClick={onClose}>
                        Cancel
                    </Button>
                    <Button className="flex-1" onClick={handleCreate} disabled={loading}>
                        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Create'}
                    </Button>
                </div>
            </div>
        </div>
    );
}