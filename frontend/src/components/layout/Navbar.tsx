import Image from "next/image";
import Link from "next/link";
import { Search } from "lucide-react";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background transition-all duration-300 ease-in-out">
      <div className="w-full flex h-16 items-center px-4 md:px-8 xl:px-12">
        <Link href="/" className="flex items-center space-x-2.5 transition-opacity hover:opacity-80">
          <Image src="/usearch.svg" alt="uSearch Logo" width={28} height={28} className="h-7 w-auto" priority />
          <span className="font-bold inline-block text-xl tracking-tight">uSearch</span>
        </Link>
        <div className="flex flex-1 items-center justify-end space-x-6">
          <nav className="hidden md:flex items-center space-x-6 text-sm font-medium text-muted-foreground">
            <Link href="/" className="transition-colors hover:text-foreground">
              Features
            </Link>
            <Link href="/pricing" className="transition-colors hover:text-foreground">
              Pricing
            </Link>
            <Link href="/docs" className="transition-colors hover:text-foreground">
              Docs
            </Link>
            <Link href="/about" className="transition-colors hover:text-foreground">
              About
            </Link>
            <Link href="/profile" className="transition-colors hover:text-foreground">
              Dashboard
            </Link>
          </nav>
          <div className="flex items-center space-x-4">
            <Link 
              href="/auth" 
              className="hidden sm:inline-flex items-center justify-center rounded-lg font-bold transition-colors bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 text-sm"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}
