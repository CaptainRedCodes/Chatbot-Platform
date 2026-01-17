import React from 'react';
import { Button } from '@/components/ui/button';
import { X, Loader2 } from 'lucide-react';

export default function SystemPromptModal({
    isOpen,
    onClose,
    systemPrompt,
    setSystemPrompt,
    onSave,
    loading
}) {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
            <div className="w-full max-w-md bg-white border border-gray-200 rounded-lg shadow-xl p-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold">System Prompt</h3>
                    <button onClick={onClose}>
                        <X className="w-4 h-4" />
                    </button>
                </div>

                <div className="space-y-3">
                    <p className="text-sm text-muted-foreground">
                        This prompt defines the AI's behavior for all chats in this project.
                    </p>
                    {loading && !systemPrompt ? (
                        <div className="flex justify-center py-6">
                            <Loader2 className="w-5 h-5 animate-spin text-primary" />
                        </div>
                    ) : (
                        <textarea
                            className="w-full min-h-[120px] rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50"
                            value={systemPrompt}
                            onChange={(e) => setSystemPrompt(e.target.value)}
                            placeholder="You are a helpful AI assistant..."
                            disabled={loading}
                        />
                    )}
                </div>

                <div className="flex gap-2 mt-5">
                    <Button variant="outline" className="flex-1" onClick={onClose}>
                        Cancel
                    </Button>
                    <Button className="flex-1" onClick={onSave} disabled={loading}>
                        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Save'}
                    </Button>
                </div>
            </div>
        </div>
    );
}