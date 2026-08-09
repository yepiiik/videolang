import React from 'react'
import Link from 'next/link'
import { Home, MessageSquare, CreditCard, Search, Video, User, Shield, FileText } from "lucide-react";

interface SidebarProps {
  isOpened: boolean;
  onClose: () => void;
}

const Sidebar = ({ isOpened, onClose }: SidebarProps) => {
    const navItems = [
        { name: 'Home', href: '/', icon: Home },
        { name: 'Search', href: '/search', icon: Search },
        { name: 'Video Library', href: '/video', icon: Video },
        { name: 'Forum', href: '/forum', icon: MessageSquare },
        { name: 'Pricing', href: '/pricing', icon: CreditCard },
        { name: 'Profile', href: '/profile', icon: User },
    ];

    const legalItems = [
        { name: 'Privacy Policy', href: '/privacy', icon: Shield },
        { name: 'Terms of Service', href: '/terms', icon: FileText },
    ];

    return (
        <aside className={`fixed top-16 left-0 h-[calc(100vh-4rem)] w-64 border-r border-gray-200 bg-white flex flex-col p-6 ${isOpened ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out z-40 shadow-xl overflow-y-auto`}>
            <div className="flex items-center gap-2 mb-8 px-2">
                <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground font-bold">U</div>
                <span className="text-xl font-bold tracking-tight">uSearch</span>
            </div>
            
            <nav className="flex-1">
                <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground mb-4 px-2">Main Navigation</p>
                <ul className="space-y-1">
                    {navItems.map((item) => (
                        <li key={item.name}>
                            <Link 
                                href={item.href} 
                                onClick={onClose}
                                className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-muted-foreground hover:text-primary hover:bg-primary/5 transition-all"
                            >
                                <item.icon className="h-4 w-4" />
                                {item.name}
                            </Link>
                        </li>
                    ))}
                </ul>

                <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground mt-8 mb-4 px-2">Legal & Support</p>
                <ul className="space-y-1">
                    {legalItems.map((item) => (
                        <li key={item.name}>
                            <Link 
                                href={item.href} 
                                onClick={onClose}
                                className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-muted-foreground hover:text-primary hover:bg-primary/5 transition-all"
                            >
                                <item.icon className="h-4 w-4" />
                                {item.name}
                            </Link>
                        </li>
                    ))}
                </ul>
            </nav>

            <div className="mt-auto pt-6 border-t border-gray-100">
                <div className="bg-muted/50 p-4 rounded-xl flex flex-col gap-2">
                    <p className="text-xs font-bold text-foreground">Need help?</p>
                    <p className="text-[10px] text-muted-foreground leading-tight">Check our community forum or contact support.</p>
                    <Button variant="link" className="h-auto p-0 text-[10px] justify-start" onClick={onClose}>
                        <Link href="/forum">Visit Forum</Link>
                    </Button>
                </div>
            </div>
        </aside>
    )
}

import { Button } from './button'

export default Sidebar