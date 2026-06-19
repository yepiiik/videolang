import React from 'react'
import Link from 'next/link'
import { Globe, Send, Briefcase, Video } from "lucide-react";

// Note: Brand icons (Github, Twitter, etc.) are missing in lucide-react v1.14.0.
// Using generic icons (Globe, Send, Briefcase, Video) as alternatives.

const Footer = () => {
  return (
    <footer className='bg-white border-t border-gray-200'>
        <div className='px-8 py-12'>
            <div className='grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8'>
                <div className='col-span-2 lg:col-span-2'>
                    <Link href="/" className="text-xl font-bold tracking-tight">
                        uSearch
                    </Link>
                    <p className='mt-4 text-sm text-muted-foreground max-w-xs'>
                        Intelligent search engine for the YouTube era. Index transcripts, find concepts, and unlock the knowledge hidden in hours of video.
                    </p>
                    <div className='flex gap-4 mt-6'>
                        <Send className='h-5 w-5 text-muted-foreground hover:text-primary cursor-pointer' />
                        <Globe className='h-5 w-5 text-muted-foreground hover:text-primary cursor-pointer' />
                        <Briefcase className='h-5 w-5 text-muted-foreground hover:text-primary cursor-pointer' />
                        <Video className='h-5 w-5 text-muted-foreground hover:text-primary cursor-pointer' />
                    </div>
                </div>
                
                <div>
                    <h3 className='font-bold text-sm uppercase tracking-wider mb-4'>Product</h3>
                    <ul className='space-y-2 text-sm text-muted-foreground'>
                        <li><Link href="/search" className="hover:text-primary">Search Engine</Link></li>
                        <li><Link href="/pricing" className="hover:text-primary">Pricing Plans</Link></li>
                        <li><Link href="/forum" className="hover:text-primary">Community Forum</Link></li>
                        <li><Link href="#" className="hover:text-primary">API Documentation</Link></li>
                    </ul>
                </div>

                <div>
                    <h3 className='font-bold text-sm uppercase tracking-wider mb-4'>Company</h3>
                    <ul className='space-y-2 text-sm text-muted-foreground'>
                        <li><Link href="#" className="hover:text-primary">About Us</Link></li>
                        <li><Link href="#" className="hover:text-primary">Careers</Link></li>
                        <li><Link href="#" className="hover:text-primary">Blog</Link></li>
                        <li><Link href="#" className="hover:text-primary">Contact</Link></li>
                    </ul>
                </div>

                <div>
                    <h3 className='font-bold text-sm uppercase tracking-wider mb-4'>Legal</h3>
                    <ul className='space-y-2 text-sm text-muted-foreground'>
                        <li><Link href="/privacy" className="hover:text-primary">Privacy Policy</Link></li>
                        <li><Link href="/terms" className="hover:text-primary">Terms of Service</Link></li>
                        <li><Link href="#" className="hover:text-primary">Cookie Policy</Link></li>
                    </ul>
                </div>
            </div>
            
            <div className='mt-12 pt-8 border-t border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-muted-foreground'>
                <p>&copy; {new Date().getFullYear()} uSearch. All rights reserved.</p>
                <div className='flex gap-6'>
                    <span>System Status: <span className='text-green-500 font-bold'>Operational</span></span>
                    <span>v1.2.0-beta</span>
                </div>
            </div>
        </div>
    </footer>
  )
}

export default Footer