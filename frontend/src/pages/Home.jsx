import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { ArrowRight, Bot, Shield, Zap } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Home() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };
    return (
        <div className="min-h-screen bg-background text-foreground flex flex-col">
            {/* Navigation */}
            <nav className="border-b border-border sticky top-0 z-50 bg-background">
                <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
                        <Bot className="text-primary w-6 h-6" />
                        <span>ChatPlatform</span>
                    </div>
                    <div className="hidden md:flex gap-8 text-sm font-medium text-muted-foreground">
                        <a href="#" className="hover:text-primary transition-colors">Features</a>
                        <a href="#" className="hover:text-primary transition-colors">Pricing</a>
                        <a href="#" className="hover:text-primary transition-colors">Documentation</a>
                    </div>
                    <div className="flex gap-4">
                        <Button onClick={handleLogout} variant="outline" size="sm" className="font-medium">Logout</Button>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="flex-1 container mx-auto px-4 py-24 lg:py-32 flex flex-col items-center text-center">
                <div className="inline-flex items-center rounded-full border border-border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 bg-secondary text-secondary-foreground mb-8">
                    v1.0 is now live
                </div>
                <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight mb-8 max-w-4xl text-foreground">
                    Build Smarter <span className="text-muted-foreground">Chatbots</span> Faster
                </h1>
                <p className="text-muted-foreground text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
                    The ultimate platform for deploying FastAPI-powered AI agents with a
                    beautiful React interface. Secure, scalable, and ready for production.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center w-full sm:w-auto">
                    <Button size="lg" className="gap-2 h-12 px-8 text-base bg-foreground text-background hover:bg-foreground/90">
                        Start Building <ArrowRight className="w-4 h-4" />
                    </Button>
                    <Button size="lg" variant="outline" className="h-12 px-8 text-base">
                        View Demo
                    </Button>
                </div>
            </section>

            {/* Features Grid */}
            <section className="py-24 border-t border-border">
                <div className="container mx-auto px-4">
                    <div className="grid md:grid-cols-3 gap-8">
                        <Card className="bg-background border-border shadow-none">
                            <CardHeader>
                                <Zap className="w-10 h-10 text-foreground mb-4" />
                                <CardTitle>Real-time Speed</CardTitle>
                                <CardDescription>
                                    Built on FastAPI and Vite for lightning-fast responses and development.
                                </CardDescription>
                            </CardHeader>
                        </Card>
                        <Card className="bg-background border-border shadow-none">
                            <CardHeader>
                                <Shield className="w-10 h-10 text-foreground mb-4" />
                                <CardTitle>Secure Auth</CardTitle>
                                <CardDescription>
                                    Ready-to-use OAuth and session management out of the box.
                                </CardDescription>
                            </CardHeader>
                        </Card>
                        <Card className="bg-background border-border shadow-none">
                            <CardHeader>
                                <Bot className="w-10 h-10 text-foreground mb-4" />
                                <CardTitle>AI Native</CardTitle>
                                <CardDescription>
                                    Designed specifically to handle complex LLM streaming and state.
                                </CardDescription>
                            </CardHeader>
                        </Card>
                    </div>
                </div>
            </section>
        </div>
    );
}
