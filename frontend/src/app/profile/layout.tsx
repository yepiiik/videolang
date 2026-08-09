"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Key, Play, CreditCard, LogOut, Loader2 } from "lucide-react";
import { useAuthViewModel } from "@/viewmodels/useAuthViewModel";
import { useState } from "react";

export default function ProfileLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { signOut } = useAuthViewModel();
  const [isSigningOut, setIsSigningOut] = useState(false);

  const handleSignOut = async () => {
    setIsSigningOut(true);
    try {
      await signOut();
      router.push("/");
    } catch (error) {
      console.error("Failed to sign out", error);
      setIsSigningOut(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <div className="flex-1 border-t">
        <div className="container mx-auto max-w-7xl flex flex-col md:flex-row min-h-[calc(100vh-4rem)]">
          
          {/* Left Sidebar (Sticky) */}
          <aside className="w-full md:w-64 border-r bg-muted/20 md:block hidden animate-in slide-in-from-left-4 fade-in duration-500 pt-8 pb-12 px-4 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto">
            <nav className="space-y-8">
              <div className="space-y-2">
                <h4 className="font-semibold text-sm px-2">Dashboard</h4>
                <ul className="space-y-1">
                  <li>
                    <Link 
                      href="/profile/api-keys"
                      className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors flex items-center gap-2 ${pathname === "/profile/api-keys" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      <Key className="w-4 h-4" />
                      API Keys
                    </Link>
                  </li>
                  <li>
                    <Link 
                      href="/profile/playground"
                      className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors flex items-center gap-2 ${pathname === "/profile/playground" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      <Play className="w-4 h-4" />
                      API Playground
                    </Link>
                  </li>
                  <li>
                    <Link 
                      href="/profile/billing"
                      className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors flex items-center gap-2 ${pathname === "/profile/billing" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      <CreditCard className="w-4 h-4" />
                      Billing
                    </Link>
                  </li>
                </ul>
              </div>
            </nav>
            <div className="absolute bottom-12 w-[calc(100%-2rem)]">
              <button 
                onClick={handleSignOut}
                disabled={isSigningOut}
                className="w-full text-left px-2 py-2 text-sm rounded-md transition-colors flex items-center gap-2 text-muted-foreground hover:bg-destructive/10 hover:text-destructive font-medium disabled:opacity-50"
              >
                {isSigningOut ? <Loader2 className="w-4 h-4 animate-spin" /> : <LogOut className="w-4 h-4" />}
                Sign Out
              </button>
            </div>
          </aside>

          {/* Right Content Area */}
          <main className="flex-1 py-12 px-6 md:px-12 max-w-5xl mx-auto animate-in slide-in-from-bottom-8 fade-in duration-700 w-full">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}
