"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { MOCK_ENDPOINTS } from "@/lib/mock-data";

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <div className="flex-1 border-t">
        <div className="container mx-auto max-w-7xl flex flex-col md:flex-row min-h-[calc(100vh-4rem)]">
          
          {/* Left Sidebar (Sticky) */}
          <aside className="w-full md:w-64 border-r bg-muted/20 md:block hidden animate-in slide-in-from-left-4 fade-in duration-500 pt-8 pb-12 px-4 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto">
            <nav className="space-y-8">
              <div className="space-y-2">
                <h4 className="font-semibold text-sm px-2">Getting Started</h4>
                <ul className="space-y-1">
                  <li>
                    <Link 
                      href="/docs/introduction"
                      className={`block w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors ${pathname === "/docs/introduction" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      Introduction
                    </Link>
                  </li>
                  <li>
                    <Link 
                      href="/docs/authentication"
                      className={`block w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors ${pathname === "/docs/authentication" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      Authentication
                    </Link>
                  </li>
                  <li>
                    <Link 
                      href="/docs/rate-limits"
                      className={`block w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors ${pathname === "/docs/rate-limits" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      Rate Limits
                    </Link>
                  </li>
                </ul>
              </div>

              <div className="space-y-2">
                <h4 className="font-semibold text-sm px-2">REST API Endpoints</h4>
                <ul className="space-y-1">
                  {MOCK_ENDPOINTS.map(endpoint => (
                    <li key={endpoint.path}>
                      <Link 
                        href={`/docs/${endpoint.slug}`}
                        className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors flex items-center space-x-2 ${pathname === `/docs/${endpoint.slug}` ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                      >
                        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                          endpoint.method === "GET" ? "bg-blue-100 text-blue-700" :
                          endpoint.method === "POST" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-700"
                        }`}>
                          {endpoint.method}
                        </span>
                        <span className="truncate">{endpoint.title}</span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            </nav>
          </aside>

          {/* Right Content Area */}
          <main className="flex-1 py-12 px-6 md:px-12 max-w-4xl mx-auto animate-in slide-in-from-bottom-8 fade-in duration-700 w-full">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}
