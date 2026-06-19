import Image from "next/image";
import Link from "next/link";
import { Search } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t py-12 bg-muted/40">
      <div className="w-full px-4 md:px-8 xl:px-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-8">
        <div className="flex flex-col space-y-4">
          <Link href="/" className="flex items-center space-x-2.5 transition-opacity hover:opacity-80">
            <Image src="/usearch.svg" alt="uSearch Logo" width={24} height={24} className="h-6 w-auto" />
            <span className="font-bold inline-block text-lg tracking-tight">uSearch</span>
          </Link>
          <p className="text-sm text-muted-foreground max-w-xs">
            Intelligent YouTube caption search and export tool. Find exactly what was said, instantly.
          </p>
        </div>
        
        <div className="flex gap-12 sm:gap-24">
          <div className="flex flex-col space-y-3">
            <h4 className="font-semibold text-sm">Product</h4>
            <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Features</Link>
            <Link href="/pricing" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Pricing</Link>
            <Link href="/docs" className="text-sm text-muted-foreground hover:text-foreground transition-colors">API Docs</Link>
          </div>
          <div className="flex flex-col space-y-3">
            <h4 className="font-semibold text-sm">Company</h4>
            <Link href="/about" className="text-sm text-muted-foreground hover:text-foreground transition-colors">About</Link>
            <Link href="/terms" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Terms</Link>
            <Link href="/privacy" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Privacy</Link>
          </div>
        </div>
      </div>
      <div className="w-full px-4 md:px-8 xl:px-12 mt-12 pt-8 border-t flex flex-col sm:flex-row items-center justify-between gap-4">
        <p className="text-sm text-muted-foreground">
          &copy; {new Date().getFullYear()} uSearch Inc. All rights reserved.
        </p>
        <div className="flex space-x-4">
          <a href="#" className="text-muted-foreground hover:text-foreground transition-colors text-sm">Twitter</a>
          <a href="#" className="text-muted-foreground hover:text-foreground transition-colors text-sm">GitHub</a>
        </div>
      </div>
    </footer>
  );
}
