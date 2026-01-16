import React, { useState, useEffect } from 'react';
import client from '../api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import { Plus, Edit2, Trash2, X, Loader2, Bot, LogOut, MessageSquare, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentProject, setCurrentProject] = useState(null); // For edit
    const navigate = useNavigate();

    // Form state
    const [formData, setFormData] = useState({
        project_name: '',
        project_description: '',
        system_prompt: 'You are a helpful AI assistant.',
    });
    const [formLoading, setFormLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchProjects();
    }, []);

    const fetchProjects = async () => {
        setLoading(true);
        try {
            const response = await client.get('/project/');
            setProjects(response.data);
        } catch (error) {
            console.error('Failed to fetch projects:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateClick = () => {
        setCurrentProject(null);
        setFormData({ project_name: '', project_description: '', system_prompt: 'You are a helpful AI assistant.' });
        setIsModalOpen(true);
    };

    const handleEditClick = (project) => {
        setCurrentProject(project);
        setFormData({
            project_name: project.project_name,
            project_description: project.project_description,
            system_prompt: project.system_prompt || '',
        });
        setIsModalOpen(true);
    };

    const handleDeleteClick = async (projectId) => {
        if (!window.confirm('Are you sure you want to delete this project?')) return;
        setError(null);
        try {
            await client.delete(`/project/${projectId}`);
            setProjects(projects.filter((p) => p.id !== projectId));
        } catch (err) {
            console.error('Failed to delete project:', err);
            setError(err.response?.data?.detail || 'Failed to delete project');
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormLoading(true);
        setError(null);
        try {
            if (currentProject) {
                // Update
                const response = await client.patch(`/project/${currentProject.id}`, formData);
                setProjects(projects.map((p) => (p.id === currentProject.id ? response.data : p)));
            } else {
                // Create
                const response = await client.post('/project/', formData);
                setProjects([response.data, ...projects]);
            }
            setIsModalOpen(false);
        } catch (err) {
            console.error('Failed to save project:', err);
            setError(err.response?.data?.detail || 'Failed to save project');
        } finally {
            setFormLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background text-foreground flex flex-col">
            {/* Header */}
            <nav className="border-b border-border bg-background sticky top-0 z-50">
                <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
                        <Bot className="text-primary w-6 h-6" />
                        <span>ChatPlatform</span>
                    </div>
                    <div className="flex gap-4">
                        <Button onClick={handleLogout} variant="ghost" size="sm" className="gap-2">
                            <LogOut className="w-4 h-4" /> Logout
                        </Button>
                    </div>
                </div>
            </nav>

            <main className="flex-1 container mx-auto px-4 py-8">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Projects</h1>
                        <p className="text-muted-foreground mt-1">Manage your AI chatbots and agents.</p>
                    </div>
                    <Button onClick={handleCreateClick} className="gap-2">
                        <Plus className="w-4 h-4" /> Create Project
                    </Button>
                </div>

                {error && (
                    <div className="flex items-center gap-x-2 rounded-md bg-destructive/15 p-3 text-sm text-destructive mb-4">
                        <AlertCircle className="h-4 w-4 flex-shrink-0" />
                        <p>{error}</p>
                        <Button variant="ghost" size="sm" className="ml-auto h-6 w-6 p-0" onClick={() => setError(null)}>
                            <X className="h-4 w-4" />
                        </Button>
                    </div>
                )}

                {loading ? (
                    <div className="flex justify-center py-12">
                        <Loader2 className="w-8 h-8 animate-spin text-primary" />
                    </div>
                ) : projects.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-12 text-center border rounded-lg bg-card/50 border-dashed">
                        <div className="rounded-full bg-muted p-4 mb-4">
                            <Bot className="w-8 h-8 text-muted-foreground" />
                        </div>
                        <h3 className="text-lg font-medium">No projects yet</h3>
                        <p className="text-muted-foreground max-w-sm mt-2 mb-6">
                            Create your first project to start building your AI agent.
                        </p>
                        <Button onClick={handleCreateClick}>Create Project</Button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {projects.map((project) => (
                            <Card key={project.id} className="flex flex-col">
                                <CardHeader>
                                    <CardTitle className="truncate">{project.project_name}</CardTitle>
                                    <CardDescription className="line-clamp-2">
                                        {project.project_description || 'No description provided.'}
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="flex-1">
                                    <div className="text-xs text-muted-foreground">
                                        Created: {new Date(project.created_at).toLocaleDateString()}
                                    </div>
                                </CardContent>
                                <CardFooter className="flex justify-between gap-2 pt-2">
                                    <Button
                                        variant="secondary"
                                        size="sm"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            navigate(`/project/${project.id}/chat`);
                                        }}
                                        className="gap-2"
                                    >
                                        <MessageSquare className="w-4 h-4" /> Chat
                                    </Button>
                                    <div className="flex gap-2">
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => handleEditClick(project)}
                                            className="h-8 w-8 p-0"
                                        >
                                            <Edit2 className="w-4 h-4" />
                                        </Button>
                                        <Button
                                            variant="destructive"
                                            size="sm"
                                            onClick={() => handleDeleteClick(project.id)}
                                            className="h-8 w-8 p-0"
                                        >
                                            <Trash2 className="w-4 h-4" />
                                        </Button>
                                    </div>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                )
                }
            </main >

            {/* Modal Overlay */}
            {
                isModalOpen && (
                    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
                        <Card className="w-full max-w-md shadow-lg animate-in fade-in zoom-in-95 duration-200">
                            <CardHeader className="relative">
                                <CardTitle>{currentProject ? 'Edit Project' : 'Create Project'}</CardTitle>
                                <CardDescription>
                                    {currentProject ? 'Update your project details.' : 'Add a new project to your workspace.'}
                                </CardDescription>
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    className="absolute right-4 top-4 h-8 w-8 p-0"
                                    onClick={() => setIsModalOpen(false)}
                                >
                                    <X className="w-4 h-4" />
                                </Button>
                            </CardHeader>
                            <form onSubmit={handleSubmit}>
                                <CardContent className="space-y-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="project_name">Project Name</Label>
                                        <Input
                                            id="project_name"
                                            value={formData.project_name}
                                            onChange={(e) =>
                                                setFormData({ ...formData, project_name: e.target.value })
                                            }
                                            placeholder="My Awesome Bot"
                                            required
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="project_description">Description</Label>
                                        <Input
                                            id="project_description"
                                            value={formData.project_description}
                                            onChange={(e) =>
                                                setFormData({ ...formData, project_description: e.target.value })
                                            }
                                            placeholder="What does this bot do?"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="system_prompt">System Prompt (Persona)</Label>
                                        <textarea
                                            id="system_prompt"
                                            className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                            value={formData.system_prompt}
                                            onChange={(e) =>
                                                setFormData({ ...formData, system_prompt: e.target.value })
                                            }
                                            placeholder="You are a helpful assistant who..."
                                            required
                                        />
                                    </div>
                                </CardContent>
                                <CardFooter className="flex justify-end gap-2">
                                    <Button
                                        type="button"
                                        variant="ghost"
                                        onClick={() => setIsModalOpen(false)}
                                        disabled={formLoading}
                                    >
                                        Cancel
                                    </Button>
                                    <Button type="submit" disabled={formLoading}>
                                        {formLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                        {currentProject ? 'Save Changes' : 'Create Project'}
                                    </Button>
                                </CardFooter>
                            </form>
                        </Card>
                    </div>
                )
            }
        </div >
    );
}
