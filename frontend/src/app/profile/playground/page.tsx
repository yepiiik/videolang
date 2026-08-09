"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { MOCK_ENDPOINTS } from "@/lib/mock-data";

export default function PlaygroundPage() {
  const [selectedEndpointIndex, setSelectedEndpointIndex] = useState(0);
  const selectedEndpoint = MOCK_ENDPOINTS[selectedEndpointIndex];
  
  const [playgroundParams, setPlaygroundParams] = useState<Record<string, string>>({});
  const [isSending, setIsSending] = useState(false);
  const [responseOutput, setResponseOutput] = useState<string | null>(null);

  const handleSendRequest = () => {
    setIsSending(true);
    setResponseOutput(null);
    setTimeout(() => {
      setIsSending(false);
      setResponseOutput(JSON.stringify(selectedEndpoint.sampleResponse, null, 2));
    }, 600); // Simulate network latency
  };

  return (
    <div className="flex flex-col space-y-6">
      <div className="flex flex-col space-y-2 mb-4">
        <h1 className="text-4xl font-extrabold tracking-tight">API Playground</h1>
        <p className="text-lg text-muted-foreground">Test uSearch endpoints interactively in your browser.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-4">
        {/* Request Builder */}
        <div className="flex flex-col space-y-6">
          <div className="bg-card border rounded-2xl shadow-sm p-6 space-y-6">
            
            {/* Endpoint Selector */}
            <div className="space-y-2">
              <label className="text-sm font-semibold">Select Endpoint</label>
              <div className="relative">
                <select 
                  value={selectedEndpointIndex}
                  onChange={(e) => {
                    setSelectedEndpointIndex(Number(e.target.value));
                    setPlaygroundParams({});
                    setResponseOutput(null);
                  }}
                  className="w-full appearance-none bg-muted/30 border-2 border-border focus:border-primary outline-none rounded-xl px-4 py-3 font-semibold cursor-pointer transition-colors"
                >
                  {MOCK_ENDPOINTS.map((ep, idx) => (
                    <option key={idx} value={idx}>{ep.method} {ep.path} - {ep.title}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-4 top-4 h-4 w-4 pointer-events-none opacity-50" />
              </div>
              <p className="text-xs text-muted-foreground mt-1 px-1">{selectedEndpoint.description}</p>
            </div>

            {/* Dynamic Parameters */}
            {selectedEndpoint.parameters.length > 0 && (
              <div className="space-y-4 pt-4 border-t">
                <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Parameters</h3>
                {selectedEndpoint.parameters.map((param) => (
                  <div key={param.name} className="space-y-1.5">
                    <label className="text-sm font-semibold flex items-center gap-2">
                      {param.name} 
                      {param.required && <span className="text-destructive text-[10px] uppercase font-bold bg-destructive/10 px-1.5 py-0.5 rounded-sm">Required</span>}
                    </label>
                    <input 
                      type="text" 
                      placeholder={param.type}
                      value={playgroundParams[param.name] || ""}
                      onChange={(e) => setPlaygroundParams({...playgroundParams, [param.name]: e.target.value})}
                      className="w-full bg-background border-2 border-border focus:border-primary outline-none rounded-lg px-3 py-2 text-sm transition-colors"
                    />
                    <p className="text-xs text-muted-foreground">{param.description}</p>
                  </div>
                ))}
              </div>
            )}

            <button 
              onClick={handleSendRequest}
              disabled={isSending}
              className="w-full flex items-center justify-center font-bold text-primary-foreground bg-primary hover:bg-primary/90 transition-all shadow-md py-3 rounded-xl disabled:opacity-50 mt-4"
            >
              {isSending ? (
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Sending...</span>
                </div>
              ) : (
                <span>Send Request</span>
              )}
            </button>
          </div>
        </div>

        {/* Response Viewer */}
        <div className="flex flex-col h-[500px]">
          <div className="bg-[#0D0D0D] border border-border rounded-2xl shadow-sm flex flex-col h-full overflow-hidden">
            <div className="flex items-center justify-between px-4 py-3 border-b border-white/10 bg-white/5">
              <span className="text-xs font-mono text-muted-foreground font-semibold">Response</span>
              <div className="flex gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-red-500/20 border border-red-500/50" />
                <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/20 border border-yellow-500/50" />
                <div className="w-2.5 h-2.5 rounded-full bg-green-500/20 border border-green-500/50" />
              </div>
            </div>
            <div className="p-4 overflow-auto flex-1 custom-scrollbar">
              {responseOutput ? (
                <pre className="text-sm font-mono text-green-400">
                  <code>{responseOutput}</code>
                </pre>
              ) : (
                <div className="h-full flex items-center justify-center text-muted-foreground/30 font-mono text-sm">
                  Waiting for request...
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
