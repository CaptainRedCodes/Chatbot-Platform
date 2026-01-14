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
import { Plus, Edit2, Trash2, X, Loader2, Bot, LogOut } from 'lucide-react';
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
    });
    const [formLoading, setFormLoading] = useState(false);

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
        setFormData({ project_name: '', project_description: '' });
        setIsModalOpen(true);
    };

    const handleEditClick = (project) => {
        setCurrentProject(project);
        setFormData({
            project_name: project.project_name,
            project_description: project.project_description,
        });
        setIsModalOpen(true);
    };

    const handleDeleteClick = async (projectId) => {
        if (!window.confirm('Are you sure you want to delete this project?')) return;
        try {
            await client.delete(`/projects/${projectId}`);
            setProjects(projects.filter((p) => p.id !== projectId));
        } catch (error) {
            console.error('Failed to delete project:', error);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormLoading(true);
        try {
            if (currentProject) {
                // Update
                const response = await client.patch(`/projects/${currentProject.id}`, formData);
                setProjects(projects.map((p) => (p.id === currentProject.id ? response.data : p)));
            } else {
                // Create
                const response = await client.post('/projects/', formData);
                setProjects([response.data, ...projects]);
            }
            setIsModalOpen(false);
        } catch (error) {
            console.error('Failed to save project:', error);
            // Handle error (show toast/alert)
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
                                <CardFooter className="flex justify-end gap-2 pt-2">
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
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                )}
            </main>

            {/* Modal Overlay */}
            {isModalOpen && (
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
            )}
        </div>
    );
}
