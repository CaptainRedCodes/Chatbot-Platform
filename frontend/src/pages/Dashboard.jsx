import React, { useState, useEffect } from 'react';
import client from '../api/client';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Plus, Edit2, Trash2, X, Loader2, Bot, LogOut, MessageSquare } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentProject, setCurrentProject] = useState(null);
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        project_name: '',
        project_description: '',
        system_prompt: '',
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
        setFormData({ project_name: '', project_description: '', system_prompt: '' });
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
                const response = await client.patch(`/project/${currentProject.id}`, formData);
                setProjects(projects.map((p) => (p.id === currentProject.id ? response.data : p)));
            } else {
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
        <div className="min-h-screen bg-background">
            {/* Header */}
            <nav className="border-b border-border bg-background">
                <div className="container mx-auto px-4 h-14 flex items-center justify-between">
                    <div className="flex items-center gap-2 font-bold text-lg">
                        <Bot className="text-primary w-6 h-6" />
                        <span>ChatPlatform</span>
                    </div>
                    <Button onClick={handleLogout} variant="outline" size="sm">
                        <LogOut className="w-4 h-4 mr-2" /> Logout
                    </Button>
                </div>
            </nav>

            <main className="container mx-auto px-4 py-6">
                <div className="flex items-center justify-between mb-6">
                    <h1 className="text-2xl font-bold">Projects</h1>
                    <Button onClick={handleCreateClick}>
                        <Plus className="w-4 h-4 mr-2" /> Create Project
                    </Button>
                </div>

                {error && (
                    <div className="flex items-center justify-between p-3 mb-4 text-sm text-red-600 bg-red-50 rounded border border-red-200">
                        <span>{error}</span>
                        <button onClick={() => setError(null)}><X className="h-4 w-4" /></button>
                    </div>
                )}

                {loading ? (
                    <div className="flex justify-center py-12">
                        <Loader2 className="w-6 h-6 animate-spin text-primary" />
                    </div>
                ) : projects.length === 0 ? (
                    <div className="text-center py-12 text-muted-foreground">
                        <p>No projects yet. Create one to get started.</p>
                    </div>
                ) : (
                    <div className="border border-border rounded-md divide-y divide-border">
                        {projects.map((project) => (
                            <div key={project.id} className="flex items-center justify-between p-4">
                                <div className="flex-1 min-w-0">
                                    <h3 className="font-medium truncate">{project.project_name}</h3>
                                    <p className="text-sm text-muted-foreground truncate">
                                        {project.project_description || 'No description'}
                                    </p>
                                </div>
                                <div className="flex items-center gap-2 ml-4">
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => navigate(`/project/${project.id}/chat`)}
                                    >
                                        <MessageSquare className="w-4 h-4 mr-1" /> Chat
                                    </Button>
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => handleEditClick(project)}
                                    >
                                        <Edit2 className="w-4 h-4" />
                                    </Button>
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => handleDeleteClick(project.id)}
                                        className="text-red-600 hover:bg-red-50"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </Button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>

            {/* Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
                    <div className="w-full max-w-md bg-white border border-gray-200 rounded-lg shadow-xl p-6">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg font-bold">
                                {currentProject ? 'Edit Project' : 'Create Project'}
                            </h2>
                            <button onClick={() => setIsModalOpen(false)}>
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <Label htmlFor="project_name">Project Name</Label>
                                <Input
                                    id="project_name"
                                    value={formData.project_name}
                                    onChange={(e) => setFormData({ ...formData, project_name: e.target.value })}
                                    placeholder="My Bot"
                                    required
                                    className="mt-1"
                                />
                            </div>
                            <div>
                                <Label htmlFor="project_description">Description</Label>
                                <Input
                                    id="project_description"
                                    value={formData.project_description}
                                    onChange={(e) => setFormData({ ...formData, project_description: e.target.value })}
                                    placeholder="What does this bot do?"
                                    className="mt-1"
                                />
                            </div>
                            <div>
                                <Label htmlFor="system_prompt">System Prompt</Label>
                                <textarea
                                    id="system_prompt"
                                    className="mt-1 w-full min-h-[80px] rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    value={formData.system_prompt}
                                    onChange={(e) => setFormData({ ...formData, system_prompt: e.target.value })}
                                    placeholder="You are a helpful assistant."
                                    required
                                />
                            </div>

                            <div className="flex gap-2 pt-2">
                                <Button type="button" variant="outline" className="flex-1" onClick={() => setIsModalOpen(false)}>
                                    Cancel
                                </Button>
                                <Button type="submit" className="flex-1" disabled={formLoading}>
                                    {formLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                    {currentProject ? 'Save' : 'Create'}
                                </Button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
