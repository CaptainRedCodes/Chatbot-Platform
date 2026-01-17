import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Home, AlertTriangle } from 'lucide-react';

export default function NotFound() {
    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center px-4">
            <div className="text-center">
                <div className="flex justify-center mb-6">
                    <div className="rounded-full bg-destructive/10 p-6">
                        <AlertTriangle className="w-16 h-16 text-destructive" />
                    </div>
                </div>
                <h1 className="text-6xl font-bold text-foreground mb-2">404</h1>
                <h2 className="text-2xl font-semibold text-foreground mb-4">Page Not Found</h2>
                <p className="text-muted-foreground mb-8 max-w-md">
                    The page you're looking for doesn't exist or has been moved.
                </p>
                <Link to="/">
                    <Button className="gap-2">
                        <Home className="w-4 h-4" />
                        Back to Home
                    </Button>
                </Link>
            </div>
        </div>
    );
}
