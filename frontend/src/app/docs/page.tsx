"use client";

import { useState } from "react";
import { MOCK_ENDPOINTS } from "@/lib/mock-data";

export default function DocsPage() {
  const [activeSection, setActiveSection] = useState<string>("Introduction");

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
                    <button 
                      onClick={() => setActiveSection("Introduction")}
                      className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors ${activeSection === "Introduction" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      Introduction
                    </button>
                  </li>
                  <li>
                    <button 
                      onClick={() => setActiveSection("Authentication")}
                      className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors ${activeSection === "Authentication" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      Authentication
                    </button>
                  </li>
                  <li>
                    <button 
                      onClick={() => setActiveSection("Rate Limits")}
                      className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors ${activeSection === "Rate Limits" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      Rate Limits
                    </button>
                  </li>
                </ul>
              </div>

              <div className="space-y-2">
                <h4 className="font-semibold text-sm px-2">REST API Endpoints</h4>
                <ul className="space-y-1">
                  {MOCK_ENDPOINTS.map(endpoint => (
                    <li key={endpoint.path}>
                      <button 
                        onClick={() => setActiveSection(endpoint.title)}
                        className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors flex items-center space-x-2 ${activeSection === endpoint.title ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                      >
                        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                          endpoint.method === "GET" ? "bg-blue-100 text-blue-700" :
                          endpoint.method === "POST" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-700"
                        }`}>
                          {endpoint.method}
                        </span>
                        <span className="truncate">{endpoint.title}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            </nav>
          </aside>

          {/* Right Content Area */}
          <main className="flex-1 py-12 px-6 md:px-12 max-w-4xl mx-auto animate-in slide-in-from-bottom-8 fade-in duration-700 w-full">
            {activeSection === "Introduction" && (
              <div className="space-y-6">
                <h1 className="text-4xl font-extrabold tracking-tight">Introduction</h1>
                <p className="text-lg text-muted-foreground">
                  Welcome to the uSearch REST API documentation. Our API allows you to programmatically search through YouTube captions, fetch semantic matches, and export full transcripts in various formats.
                </p>
                <div className="bg-muted/50 border rounded-lg p-6 mt-8">
                  <h3 className="font-semibold mb-2">Base URL</h3>
                  <code className="text-sm bg-background px-2 py-1 rounded border">https://api.ucontext.com/v1</code>
                </div>
              </div>
            )}

            {activeSection === "Authentication" && (
              <div className="space-y-6">
                <h1 className="text-4xl font-extrabold tracking-tight">Authentication</h1>
                <p className="text-lg text-muted-foreground">
                  Authenticate your API requests by including your secret API key in the Authorization header.
                </p>
                <div className="bg-zinc-950 text-zinc-50 rounded-lg p-4 mt-6 overflow-x-auto">
                  <pre className="text-sm"><code>Authorization: Bearer YOUR_API_KEY</code></pre>
                </div>
              </div>
            )}

            {activeSection === "Rate Limits" && (
              <div className="space-y-6">
                <h1 className="text-4xl font-extrabold tracking-tight">Rate Limits</h1>
                <p className="text-lg text-muted-foreground">
                  API rate limits depend on your pricing tier. Free tier includes 100 requests per month.
                </p>
              </div>
            )}

            {MOCK_ENDPOINTS.map(endpoint => {
              if (activeSection !== endpoint.title) return null;
              return (
                <div key={endpoint.path} className="space-y-8 animate-in fade-in duration-300">
                  <div>
                    <div className="flex items-center space-x-3 mb-4">
                      <h1 className="text-3xl font-extrabold tracking-tight">{endpoint.title}</h1>
                      <span className={`text-xs font-bold px-2 py-1 rounded-md ${
                          endpoint.method === "GET" ? "bg-blue-100 text-blue-700" :
                          endpoint.method === "POST" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-700"
                        }`}>
                        {endpoint.method}
                      </span>
                    </div>
                    <p className="text-lg text-muted-foreground">{endpoint.description}</p>
                    <div className="mt-4 flex items-center space-x-2">
                      <code className="text-sm bg-muted px-2 py-1 rounded font-mono border">
                        {endpoint.path}
                      </code>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="text-xl font-semibold border-b pb-2">Parameters</h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm text-left">
                        <thead className="bg-muted/40">
                          <tr>
                            <th className="px-4 py-3 font-medium border-b">Name</th>
                            <th className="px-4 py-3 font-medium border-b">Type</th>
                            <th className="px-4 py-3 font-medium border-b">Description</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y">
                          {endpoint.parameters.map((param, idx) => (
                            <tr key={idx}>
                              <td className="px-4 py-3 font-mono font-medium text-foreground">
                                {param.name}
                                {param.required && <span className="text-red-500 ml-1" title="Required">*</span>}
                              </td>
                              <td className="px-4 py-3 font-mono text-muted-foreground text-xs">{param.type}</td>
                              <td className="px-4 py-3 text-muted-foreground">{param.description}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="text-xl font-semibold border-b pb-2">Example Request</h3>
                    <div className="bg-zinc-950 text-zinc-50 rounded-lg overflow-hidden border border-zinc-800">
                      <div className="bg-zinc-900 px-4 py-2 border-b border-zinc-800 text-xs font-mono text-zinc-400">
                        cURL
                      </div>
                      <div className="p-4 overflow-x-auto">
                        <pre className="text-sm font-mono leading-relaxed">
                          <code>
                            curl -X {endpoint.method} https://api.ucontext.com{endpoint.path} \{'\n'}
                            {endpoint.sampleRequest.headers && Object.entries(endpoint.sampleRequest.headers).map(([k, v]) => `  -H "${k}: ${v}" \\\n`).join('')}
                            {endpoint.sampleRequest.body && `  -d '${JSON.stringify(endpoint.sampleRequest.body, null, 2)}'`}
                          </code>
                        </pre>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="text-xl font-semibold border-b pb-2">Example Response</h3>
                    <div className="bg-zinc-950 text-zinc-50 rounded-lg overflow-hidden border border-zinc-800">
                      <div className="bg-zinc-900 px-4 py-2 border-b border-zinc-800 text-xs font-mono text-zinc-400">
                        JSON
                      </div>
                      <div className="p-4 overflow-x-auto">
                        <pre className="text-sm font-mono text-green-400">
                          <code>
                            {JSON.stringify(endpoint.sampleResponse, null, 2)}
                          </code>
                        </pre>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </main>
        </div>
      </div>
    </div>
  );
}
