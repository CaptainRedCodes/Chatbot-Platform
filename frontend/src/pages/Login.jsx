import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import client from '../api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Loader2, Bot } from 'lucide-react';

export default function Login() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        try {
            const response = await client.post('/auth/login', {
                email: data.email,
                password: data.password,
            });
            if (response.data.token?.access_token) {
                localStorage.setItem('token', response.data.token.access_token);
                navigate('/');
            }
        } catch (err) {
            console.error(err);
            setError(
                err.response?.data?.detail || 'Something went wrong. Please try again.'
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-background px-4 py-12">
            <div className="w-full max-w-md border border-border rounded-md p-6 bg-card">
                <div className="text-center mb-6">
                    <div className="flex items-center justify-center gap-2 mb-4">
                        <Bot className="text-primary w-8 h-8" />
                        <span className="text-2xl font-bold">ChatPlatform</span>
                    </div>
                    <h1 className="text-xl font-bold">Welcome back</h1>
                    <p className="text-muted-foreground text-sm">Enter your email to sign in</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <Label htmlFor="email">Email</Label>
                        <Input
                            id="email"
                            name="email"
                            type="email"
                            placeholder="name@example.com"
                            required
                            disabled={loading}
                            className="mt-1"
                        />
                    </div>
                    <div>
                        <Label htmlFor="password">Password</Label>
                        <Input
                            id="password"
                            name="password"
                            type="password"
                            required
                            disabled={loading}
                            className="mt-1"
                        />
                    </div>

                    {error && (
                        <div className="p-3 text-sm text-red-600 bg-red-50 rounded border border-red-200">
                            {error}
                        </div>
                    )}

                    <Button className="w-full" type="submit" disabled={loading}>
                        {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                        Sign in
                    </Button>
                </form>

                <div className="text-center mt-4 text-sm text-muted-foreground">
                    Don't have an account?{' '}
                    <Link to="/register" className="text-primary font-medium">
                        Create one
                    </Link>
                </div>
            </div>
        </div>
    );
}
