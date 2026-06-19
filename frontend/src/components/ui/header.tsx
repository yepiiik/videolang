import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import { Input } from '@/components/ui/input'
import { Hamburger } from '@/components/ui/hamburger'

const Header = ({ onMenuClicked, isMenuOpen }: { onMenuClicked: () => void, isMenuOpen: boolean }) => {
    

  return (
    <header className='sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200'>
        <div className='flex justify-between items-center h-16 px-8'>
            <div className='flex items-center gap-4'>
                <Hamburger isOpen={isMenuOpen} onClick={onMenuClicked} />
                <Link href="/" className="flex items-center gap-2 group">
                    <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground font-bold group-hover:rotate-6 transition-transform">U</div>
                    <h1 className="text-xl font-bold tracking-tight hidden sm:block">uSearch</h1>
                </Link>
            </div>
            <div className='hidden md:flex flex-1 max-w-md mx-8'>
                <div className="relative w-full">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input placeholder="Quick search..." className="pl-10 h-9 bg-muted/50 border-none" />
                </div>
            </div>
            <div className='flex items-center gap-4'>
                <Link href="/signin" className="text-sm font-medium hover:text-primary transition-colors">
                    Sign In
                </Link>
                <Link href="/signin">
                    <Button size="sm" className="hidden sm:flex">Get Started</Button>
                </Link>
            </div>
        </div>
    </header>
  )
}

import { Search } from 'lucide-react'
import { Button } from './button'

export default Header