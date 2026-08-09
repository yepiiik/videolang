"use client";

import { useState } from "react";
import { Key, Copy, Trash2, Plus, Play, ChevronDown, CheckCircle2, CreditCard, Bitcoin, DollarSign, Check } from "lucide-react";
import { MOCK_ENDPOINTS, MOCK_PRICING } from "@/lib/mock-data";

interface ApiKey {
  id: string;
  key: string;
  name: string;
  createdAt: string;
  lastUsed: string | null;
}

export default function ProfilePage() {
  const [activeSection, setActiveSection] = useState<string>("API Keys");

  // API Key State
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([
    { id: "1", key: "sk_live_51Mxyz89AbcdEFgh1234", name: "Production Key", createdAt: "2026-06-10", lastUsed: "2026-06-18" },
    { id: "2", key: "sk_test_89AbcdEFgh12345678", name: "Development Key", createdAt: "2026-06-15", lastUsed: "Never" }
  ]);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Modal State
  const [isGenerateModalOpen, setIsGenerateModalOpen] = useState(false);
  const [newKeyName, setNewKeyName] = useState("");
  const [newGeneratedKey, setNewGeneratedKey] = useState<string | null>(null);

  // Delete Confirmation State
  const [keyToDelete, setKeyToDelete] = useState<ApiKey | null>(null);
  const [deleteConfirmationName, setDeleteConfirmationName] = useState("");

  // Playground State
  const [selectedEndpointIndex, setSelectedEndpointIndex] = useState(0);
  const selectedEndpoint = MOCK_ENDPOINTS[selectedEndpointIndex];
  
  const [playgroundParams, setPlaygroundParams] = useState<Record<string, string>>({});
  const [isSending, setIsSending] = useState(false);
  const [responseOutput, setResponseOutput] = useState<string | null>(null);

  // Billing State
  const [currentPlan, setCurrentPlan] = useState("Free");
  const [nextPlan, setNextPlan] = useState<string | null>(null);
  const [accountBalance, setAccountBalance] = useState(50);
  const [isChangePlanModalOpen, setIsChangePlanModalOpen] = useState(false);
  const [isAddFundsModalOpen, setIsAddFundsModalOpen] = useState(false);
  const [addFundsAmount, setAddFundsAmount] = useState<number>(20);
  const [selectedNewPlan, setSelectedNewPlan] = useState("Standard");
  const [transactions, setTransactions] = useState<any[]>([
    { id: "tx_1", date: "2026-06-10", amount: "$0", description: "Free Plan Registration", method: "-", status: "Completed" }
  ]);
  const [paymentMethod, setPaymentMethod] = useState<"paypal" | "crypto">("paypal");
  const [isProcessingPayment, setIsProcessingPayment] = useState(false);

  const handleOpenModal = () => {
    const generatedSecret = `sk_live_${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`;
    setNewGeneratedKey(generatedSecret);
    setNewKeyName("");
    setIsGenerateModalOpen(true);
  };

  const handleConfirmKey = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKeyName.trim() || !newGeneratedKey) return;

    const newId = Date.now().toString();
    const newKey = {
      id: newId,
      key: newGeneratedKey,
      name: newKeyName,
      createdAt: new Date().toISOString().split('T')[0],
      lastUsed: "Never"
    };
    
    setApiKeys([newKey, ...apiKeys]);
    setIsGenerateModalOpen(false);
    setNewGeneratedKey(null);
  };

  const confirmDeleteKey = (e: React.FormEvent) => {
    e.preventDefault();
    if (keyToDelete && deleteConfirmationName === keyToDelete.name) {
      setApiKeys(apiKeys.filter(k => k.id !== keyToDelete.id));
      setKeyToDelete(null);
      setDeleteConfirmationName("");
    }
  };

  const handleCopyKey = (id: string, key: string) => {
    navigator.clipboard.writeText(key);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSendRequest = () => {
    setIsSending(true);
    setResponseOutput(null);
    setTimeout(() => {
      setIsSending(false);
      setResponseOutput(JSON.stringify(selectedEndpoint.sampleResponse, null, 2));
    }, 600); // Simulate network latency
  };

  const handleSubscribe = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsProcessingPayment(true);
    setTimeout(() => {
      const planData = MOCK_PRICING.find(p => p.name === selectedNewPlan);
      setNextPlan(selectedNewPlan);
      setTransactions([{
        id: `tx_${Date.now()}`,
        date: new Date().toISOString().split('T')[0],
        amount: planData?.price || "$0",
        description: `Scheduled ${selectedNewPlan} Plan Subscription`,
        method: paymentMethod === "paypal" ? "PayPal" : "Cryptocurrency",
        status: "Pending"
      }, ...transactions]);
      setIsProcessingPayment(false);
      setIsChangePlanModalOpen(false);
    }, 1500);
  };

  const handleAddFunds = (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessingPayment(true);
    setTimeout(() => {
      setAccountBalance(prev => prev + addFundsAmount);
      setTransactions([{
        id: `tx_${Date.now()}`,
        date: new Date().toISOString().split('T')[0],
        amount: `+$${addFundsAmount}.00`,
        description: `Wallet Deposit`,
        method: paymentMethod === "paypal" ? "PayPal" : "Cryptocurrency",
        status: "Completed"
      }, ...transactions]);
      setIsProcessingPayment(false);
      setIsAddFundsModalOpen(false);
    }, 1500);
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
                    <button 
                      onClick={() => setActiveSection("API Keys")}
                      className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors flex items-center gap-2 ${activeSection === "API Keys" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      <Key className="w-4 h-4" />
                      API Keys
                    </button>
                  </li>
                  <li>
                    <button 
                      onClick={() => setActiveSection("Playground")}
                      className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors flex items-center gap-2 ${activeSection === "Playground" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      <Play className="w-4 h-4" />
                      API Playground
                    </button>
                  </li>
                  <li>
                    <button 
                      onClick={() => setActiveSection("Billing")}
                      className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors flex items-center gap-2 ${activeSection === "Billing" ? "bg-primary/10 text-primary font-medium" : "text-muted-foreground hover:bg-muted hover:text-foreground"}`}
                    >
                      <CreditCard className="w-4 h-4" />
                      Billing
                    </button>
                  </li>
                </ul>
              </div>
            </nav>
          </aside>

          {/* Right Content Area */}
          <main className="flex-1 py-12 px-6 md:px-12 max-w-5xl mx-auto animate-in slide-in-from-bottom-8 fade-in duration-700 w-full">
            
            {activeSection === "API Keys" && (
              <div className="flex flex-col space-y-6">
                <div className="flex flex-col space-y-2 mb-4">
                  <h1 className="text-4xl font-extrabold tracking-tight">API Keys</h1>
                  <p className="text-lg text-muted-foreground">Manage your secret keys for accessing the uSearch API.</p>
                </div>

                <div className="flex items-center justify-between border-b pb-4">
                  <h2 className="text-xl font-bold flex items-center gap-2">
                    Active Keys
                  </h2>
                  <button 
                    onClick={handleOpenModal}
                    className="flex items-center gap-2 bg-foreground text-background hover:bg-foreground/90 px-4 py-2 rounded-lg font-bold text-sm transition-colors"
                  >
                    <Plus className="w-4 h-4" />
                    Generate Key
                  </button>
                </div>

                <div className="bg-card border rounded-2xl overflow-hidden shadow-sm">
                  {apiKeys.length === 0 ? (
                    <div className="p-8 text-center text-muted-foreground font-medium">No API keys found. Generate one to get started.</div>
                  ) : (
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm text-left">
                        <thead className="bg-muted/50 text-muted-foreground text-xs uppercase font-semibold">
                          <tr>
                            <th className="px-6 py-4">Name</th>
                            <th className="px-6 py-4">Key</th>
                            <th className="px-6 py-4">Created</th>
                            <th className="px-6 py-4">Last Used</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-border">
                          {apiKeys.map(key => (
                            <tr key={key.id} className="hover:bg-muted/20 transition-colors">
                              <td className="px-6 py-4 font-semibold">{key.name}</td>
                              <td className="px-6 py-4 font-mono text-muted-foreground tracking-widest">
                                sk_live_••••••••••••{key.key.slice(-4)}
                              </td>
                              <td className="px-6 py-4 text-muted-foreground">{key.createdAt}</td>
                              <td className="px-6 py-4 text-muted-foreground">{key.lastUsed}</td>
                              <td className="px-6 py-4 text-right flex items-center justify-end gap-2">
                                <button 
                                  onClick={() => {
                                    setKeyToDelete(key);
                                    setDeleteConfirmationName("");
                                  }}
                                  className="p-2 text-muted-foreground hover:text-destructive transition-colors rounded-md hover:bg-muted"
                                  title="Delete Key"
                                >
                                  <Trash2 className="w-4 h-4" />
                                </button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeSection === "Playground" && (
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
            )}

            {activeSection === "Billing" && (
              <div className="flex flex-col space-y-8">
                <div className="flex flex-col space-y-2 mb-2">
                  <h1 className="text-4xl font-extrabold tracking-tight">Billing & Plans</h1>
                  <p className="text-lg text-muted-foreground">Manage your subscription and view your payment history.</p>
                </div>

                {/* Account Balance Card (Top, Full Width) */}
                <div className="bg-card border-2 border-primary/20 rounded-2xl p-6 shadow-sm flex items-center justify-between">
                  <div>
                    <p className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Account Balance</p>
                    <h2 className="text-4xl font-black mt-1 tracking-tighter">${accountBalance.toFixed(2)}</h2>
                  </div>
                  <button 
                    onClick={() => setIsAddFundsModalOpen(true)}
                    className="inline-flex items-center justify-center rounded-md text-sm font-bold transition-colors h-11 px-6 bg-foreground text-background hover:bg-foreground/90 shadow-md whitespace-nowrap"
                  >
                    Add Funds
                  </button>
                </div>

                {/* Plans Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Current Plan Card (Left) */}
                  <div className="bg-card border rounded-2xl p-6 shadow-sm flex flex-col">
                    <h3 className="text-xl font-bold border-b pb-4 mb-4">Current Plan</h3>
                    
                    {MOCK_PRICING.filter(p => p.name === currentPlan).map(plan => (
                      <div key={plan.name} className="flex flex-col flex-1">
                        <div className="mb-4">
                          <h4 className="text-2xl font-bold">{plan.name}</h4>
                          <p className="text-sm text-muted-foreground mt-1">{plan.description}</p>
                        </div>
                        <div className="mb-6">
                          <span className="text-4xl font-extrabold">{plan.price}</span>
                          {plan.period && <span className="text-muted-foreground ml-1">{plan.period}</span>}
                        </div>
                        <ul className="flex-1 space-y-3 mb-8">
                          {plan.features.map((feature, i) => (
                            <li key={i} className="flex items-start text-sm">
                              <Check className="h-4 w-4 text-primary mr-3 flex-shrink-0 mt-0.5" />
                              <span className="text-muted-foreground">{feature}</span>
                            </li>
                          ))}
                        </ul>
                        <button 
                          onClick={() => {
                            setSelectedNewPlan(nextPlan || currentPlan);
                            setIsChangePlanModalOpen(true);
                          }}
                          className="w-full inline-flex items-center justify-center rounded-md text-sm font-bold transition-colors h-12 px-8 focus-visible:outline-none bg-primary text-primary-foreground hover:bg-primary/90 shadow-md mt-auto"
                        >
                          Change Plan
                        </button>
                      </div>
                    ))}
                  </div>

                  {/* Scheduled Plan Card (Right) */}
                  <div className="bg-card border rounded-2xl p-6 shadow-sm flex flex-col">
                    <h3 className="text-xl font-bold border-b pb-4 mb-4 text-amber-500">Scheduled Plan</h3>
                    
                    {!nextPlan ? (
                      <div className="flex-1 flex flex-col items-center justify-center text-center p-6 border-2 border-dashed rounded-xl border-border bg-muted/20">
                        <p className="text-muted-foreground mb-4">No scheduled plan changes.</p>
                        <p className="text-sm text-muted-foreground">Your current plan will auto-renew at the end of the billing cycle.</p>
                      </div>
                    ) : (
                      MOCK_PRICING.filter(p => p.name === nextPlan).map(plan => (
                        <div key={plan.name} className="flex flex-col flex-1">
                          <div className="mb-4">
                            <h4 className="text-2xl font-bold">{plan.name}</h4>
                            <p className="text-sm text-muted-foreground mt-1">{plan.description}</p>
                          </div>
                          <div className="mb-6">
                            <span className="text-4xl font-extrabold">{plan.price}</span>
                            {plan.period && <span className="text-muted-foreground ml-1">{plan.period}</span>}
                          </div>
                          <ul className="flex-1 space-y-3 mb-8">
                            {plan.features.map((feature, i) => (
                              <li key={i} className="flex items-start text-sm">
                                <Check className="h-4 w-4 text-primary mr-3 flex-shrink-0 mt-0.5" />
                                <span className="text-muted-foreground">{feature}</span>
                              </li>
                            ))}
                          </ul>
                          <div className="mt-auto bg-amber-500/10 border border-amber-500/20 text-amber-600 p-4 rounded-lg text-sm font-medium text-center">
                            This plan will activate at the end of your current billing cycle.
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>

                {/* Transaction History (Bottom, Full Width) */}
                <div className="bg-card border rounded-2xl p-6 shadow-sm flex flex-col">
                  <h3 className="text-xl font-bold border-b pb-4 mb-4">Transaction History</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                      <thead className="bg-muted/50 text-muted-foreground text-[10px] uppercase font-bold tracking-wider">
                        <tr>
                          <th className="px-4 py-3 rounded-tl-lg">Date</th>
                          <th className="px-4 py-3">Amount</th>
                          <th className="px-4 py-3">Description</th>
                          <th className="px-4 py-3 rounded-tr-lg">Method</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-border">
                        {transactions.map(tx => (
                          <tr key={tx.id} className="hover:bg-muted/20 transition-colors">
                            <td className="px-4 py-3 whitespace-nowrap text-muted-foreground">{tx.date}</td>
                            <td className="px-4 py-3 font-semibold">{tx.amount}</td>
                            <td className="px-4 py-3 text-muted-foreground">{tx.description}</td>
                            <td className="px-4 py-3 text-muted-foreground">{tx.method}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}

          </main>
        </div>
      </div>

      {/* Generate Key Modal */}
      {isGenerateModalOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
          <div className="bg-card border w-full max-w-md rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="p-6">
              <h2 className="text-xl font-bold mb-2">Generate New Secret Key</h2>
              
              <form onSubmit={handleConfirmKey} className="space-y-4">
                <p className="text-sm text-muted-foreground">
                  Give your new API key a name and copy the secret key below.
                </p>

                <div className="space-y-2">
                  <label className="text-sm font-semibold">Key Name</label>
                  <input 
                    type="text" 
                    required 
                    autoFocus
                    value={newKeyName}
                    onChange={(e) => setNewKeyName(e.target.value)}
                    className="w-full px-4 py-3 bg-muted/50 border-2 border-transparent focus:border-primary focus:bg-background outline-none rounded-xl transition-all"
                    placeholder="e.g. Production Web App"
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-semibold">Secret Key</label>
                  <div className="flex items-center bg-muted border rounded-xl p-2 gap-2">
                    <code className="flex-1 px-2 font-mono text-sm text-foreground overflow-x-auto custom-scrollbar">
                      {newGeneratedKey}
                    </code>
                    <button 
                      type="button"
                      onClick={() => {
                        if (newGeneratedKey) {
                          navigator.clipboard.writeText(newGeneratedKey);
                          setCopiedId("modal-copy");
                          setTimeout(() => setCopiedId(null), 2000);
                        }
                      }}
                      className="p-2 bg-background hover:bg-muted-foreground/10 text-foreground border rounded-lg transition-colors shadow-sm shrink-0"
                    >
                      {copiedId === "modal-copy" ? <CheckCircle2 className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                <div className="bg-amber-500/10 border border-amber-500/20 text-amber-600 p-4 rounded-xl text-sm font-medium leading-relaxed mt-4">
                  Please save this secret key somewhere safe and accessible. For security reasons, <strong>you won't be able to view it again</strong> after confirming.
                </div>

                <div className="flex items-center justify-end gap-3 mt-6 pt-4 border-t">
                  <button 
                    type="button" 
                    onClick={() => setIsGenerateModalOpen(false)}
                    className="px-4 py-2 text-sm font-bold text-muted-foreground hover:text-foreground transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit"
                    className="px-6 py-2 bg-primary text-primary-foreground font-bold rounded-lg hover:bg-primary/90 transition-colors shadow-sm"
                  >
                    Save API Key
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {keyToDelete && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
          <div className="bg-card border w-full max-w-md rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="p-6">
              <div className="flex items-center gap-3 mb-2 text-destructive">
                <Trash2 className="w-6 h-6" />
                <h2 className="text-xl font-bold">Delete API Key</h2>
              </div>
              
              <form onSubmit={confirmDeleteKey} className="space-y-4">
                <p className="text-sm text-muted-foreground leading-relaxed">
                  This action cannot be undone. Any applications using this API key will immediately lose access.
                </p>
                <div className="bg-muted p-3 rounded-lg border">
                  <p className="text-sm font-medium">Key Name: <span className="font-bold text-foreground">{keyToDelete.name}</span></p>
                </div>

                <div className="space-y-2 pt-2">
                  <label className="text-sm font-semibold">
                    To verify, type <span className="font-bold text-foreground select-all">{keyToDelete.name}</span> below:
                  </label>
                  <input 
                    type="text" 
                    required 
                    autoFocus
                    value={deleteConfirmationName}
                    onChange={(e) => setDeleteConfirmationName(e.target.value)}
                    className="w-full px-4 py-3 bg-muted/50 border-2 border-transparent focus:border-destructive focus:bg-background outline-none rounded-xl transition-all"
                    placeholder={keyToDelete.name}
                  />
                </div>

                <div className="flex items-center justify-end gap-3 mt-6 pt-4 border-t">
                  <button 
                    type="button" 
                    onClick={() => {
                      setKeyToDelete(null);
                      setDeleteConfirmationName("");
                    }}
                    className="px-4 py-2 text-sm font-bold text-muted-foreground hover:text-foreground transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit"
                    disabled={deleteConfirmationName !== keyToDelete.name}
                    className="px-6 py-2 bg-destructive text-destructive-foreground font-bold rounded-lg hover:bg-destructive/90 transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Delete API Key
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Change Plan Modal */}
      {isChangePlanModalOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background/80 backdrop-blur-sm p-4 overflow-y-auto">
          <div className="bg-card border w-full max-w-5xl rounded-2xl shadow-2xl animate-in fade-in zoom-in-95 duration-200 my-8">
            <div className="p-6 md:p-8 border-b flex items-center justify-between sticky top-0 bg-card z-10 rounded-t-2xl">
              <div>
                <h2 className="text-2xl font-bold">Change Plan</h2>
                <p className="text-muted-foreground text-sm">Select a new subscription tier below.</p>
              </div>
              <button onClick={() => setIsChangePlanModalOpen(false)} className="text-muted-foreground font-bold hover:text-foreground">
                Cancel
              </button>
            </div>
            
            <div className="p-6 md:p-8 space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                {MOCK_PRICING.map((tier) => (
                  <button 
                    key={tier.name} 
                    onClick={() => setSelectedNewPlan(tier.name)}
                    className={`flex flex-col text-left rounded-2xl border bg-card p-6 shadow-sm transition-all hover:shadow-md ${selectedNewPlan === tier.name ? "border-primary ring-2 ring-primary bg-primary/5" : ""}`}
                  >
                    <div className="mb-4">
                      <h3 className="text-xl font-bold">{tier.name}</h3>
                      <p className="text-xs text-muted-foreground mt-1 min-h-[40px]">{tier.description}</p>
                    </div>
                    <div className="mb-6">
                      <span className="text-3xl font-extrabold">{tier.price}</span>
                      {tier.period && <span className="text-muted-foreground text-sm ml-1">{tier.period}</span>}
                    </div>
                    <ul className="flex-1 space-y-3">
                      {tier.features.map((feature, i) => (
                        <li key={i} className="flex items-start text-xs">
                          <Check className="h-4 w-4 text-primary mr-2 flex-shrink-0" />
                          <span className="text-muted-foreground">{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </button>
                ))}
              </div>

              <div className="bg-muted/30 p-6 rounded-2xl border space-y-4">
                <h3 className="font-bold text-lg">Payment Details</h3>
                <div className="grid grid-cols-2 gap-4 max-w-md">
                  <button
                    onClick={() => setPaymentMethod("paypal")}
                    className={`flex items-center justify-center gap-2 p-3 rounded-xl border-2 transition-all font-bold ${paymentMethod === "paypal" ? 'border-primary bg-primary/10 text-primary' : 'border-border hover:border-primary/50 text-muted-foreground bg-background'}`}
                  >
                    <DollarSign className="w-5 h-5" />
                    PayPal
                  </button>
                  <button
                    onClick={() => setPaymentMethod("crypto")}
                    className={`flex items-center justify-center gap-2 p-3 rounded-xl border-2 transition-all font-bold ${paymentMethod === "crypto" ? 'border-primary bg-primary/10 text-primary' : 'border-border hover:border-primary/50 text-muted-foreground bg-background'}`}
                  >
                    <Bitcoin className="w-5 h-5" />
                    Crypto
                  </button>
                </div>
              </div>
            </div>

            <div className="p-6 md:p-8 border-t bg-muted/10 rounded-b-2xl flex items-center justify-between sticky bottom-0 z-10">
              <div>
                <p className="text-sm font-semibold">Total due today:</p>
                <p className="text-2xl font-black">{MOCK_PRICING.find(p => p.name === selectedNewPlan)?.price}</p>
              </div>
              <button 
                onClick={handleSubscribe}
                disabled={isProcessingPayment || selectedNewPlan === currentPlan}
                className="px-8 py-3 flex items-center justify-center font-bold text-primary-foreground bg-primary hover:bg-primary/90 transition-all shadow-md rounded-xl disabled:opacity-50"
              >
                {isProcessingPayment ? (
                  <div className="flex items-center gap-2">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span>Processing...</span>
                  </div>
                ) : selectedNewPlan === currentPlan ? (
                  <span>Current Plan</span>
                ) : (
                  <span>Confirm & Pay</span>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Add Funds Modal */}
      {isAddFundsModalOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
          <div className="bg-card border w-full max-w-md rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="p-6">
              <h2 className="text-xl font-bold mb-2">Add Funds</h2>
              
              <form onSubmit={handleAddFunds} className="space-y-6">
                <p className="text-sm text-muted-foreground">
                  Deposit money into your account wallet to pay for usage automatically.
                </p>

                <div className="space-y-2">
                  <label className="text-sm font-semibold">Deposit Amount (USD)</label>
                  <div className="relative">
                    <DollarSign className="absolute left-4 top-3.5 h-5 w-5 text-muted-foreground" />
                    <input 
                      type="number" 
                      min="5"
                      step="5"
                      required 
                      autoFocus
                      value={addFundsAmount}
                      onChange={(e) => setAddFundsAmount(Number(e.target.value))}
                      className="w-full pl-12 pr-4 py-3 bg-muted/50 border-2 border-transparent focus:border-primary focus:bg-background outline-none rounded-xl transition-all text-lg font-bold"
                    />
                  </div>
                </div>

                <div className="space-y-3">
                  <label className="text-sm font-semibold">Payment Method</label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => setPaymentMethod("paypal")}
                      className={`flex items-center justify-center gap-2 p-3 rounded-xl border-2 transition-all font-bold ${paymentMethod === "paypal" ? 'border-primary bg-primary/10 text-primary' : 'border-border hover:border-primary/50 text-muted-foreground'}`}
                    >
                      <DollarSign className="w-4 h-4" />
                      PayPal
                    </button>
                    <button
                      type="button"
                      onClick={() => setPaymentMethod("crypto")}
                      className={`flex items-center justify-center gap-2 p-3 rounded-xl border-2 transition-all font-bold ${paymentMethod === "crypto" ? 'border-primary bg-primary/10 text-primary' : 'border-border hover:border-primary/50 text-muted-foreground'}`}
                    >
                      <Bitcoin className="w-4 h-4" />
                      Crypto
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-end gap-3 pt-4 border-t">
                  <button 
                    type="button" 
                    onClick={() => setIsAddFundsModalOpen(false)}
                    className="px-4 py-2 text-sm font-bold text-muted-foreground hover:text-foreground transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit"
                    disabled={isProcessingPayment}
                    className="px-6 py-2 bg-foreground text-background font-bold rounded-lg hover:bg-foreground/90 transition-colors shadow-sm disabled:opacity-50"
                  >
                    {isProcessingPayment ? "Processing..." : `Pay $${addFundsAmount}.00`}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
