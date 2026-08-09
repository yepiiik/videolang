"use client";

import { useState, useEffect } from "react";
import { Key, Copy, Trash2, Plus, CheckCircle2, Loader2 } from "lucide-react";
import { getProfileData, generateApiKey, removeApiKey } from "@/app/actions/profile.actions";

interface ApiKey {
  id: string;
  key: string;
  name: string;
  createdAt: string;
  lastUsedAt: string | null;
}

export default function ApiKeysPage() {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const [isGenerateModalOpen, setIsGenerateModalOpen] = useState(false);
  const [newKeyName, setNewKeyName] = useState("");
  const [newGeneratedKey, setNewGeneratedKey] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const [keyToDelete, setKeyToDelete] = useState<ApiKey | null>(null);
  const [deleteConfirmationName, setDeleteConfirmationName] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const data = await getProfileData();
      setApiKeys(data.apiKeys);
    } catch (error) {
      console.error("Failed to load API keys", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenModal = () => {
    setNewGeneratedKey(null);
    setNewKeyName("");
    setIsGenerateModalOpen(true);
  };

  const handleConfirmKey = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKeyName.trim()) return;

    setIsGenerating(true);
    try {
      const newKey = await generateApiKey(newKeyName);
      setNewGeneratedKey(newKey.key);
      setApiKeys([newKey, ...apiKeys]);
    } catch (error) {
      console.error("Failed to generate key", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const confirmDeleteKey = async (e: React.FormEvent) => {
    e.preventDefault();
    if (keyToDelete && deleteConfirmationName === keyToDelete.name) {
      setIsDeleting(true);
      try {
        await removeApiKey(keyToDelete.id);
        setApiKeys(apiKeys.filter(k => k.id !== keyToDelete.id));
        setKeyToDelete(null);
        setDeleteConfirmationName("");
      } catch (error) {
        console.error("Failed to delete key", error);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  const handleCopyKey = (id: string, key: string) => {
    navigator.clipboard.writeText(key);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <>
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
          {isLoading ? (
            <div className="p-8 text-center flex flex-col items-center gap-3 text-muted-foreground font-medium">
              <Loader2 className="w-6 h-6 animate-spin text-primary" />
              Loading API keys...
            </div>
          ) : apiKeys.length === 0 ? (
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
                      <td className="px-6 py-4 text-muted-foreground">{new Date(key.createdAt).toISOString().split('T')[0]}</td>
                      <td className="px-6 py-4 text-muted-foreground">{key.lastUsedAt ? new Date(key.lastUsedAt).toISOString().split('T')[0] : "Never"}</td>
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

      {/* Modals */}
      {isGenerateModalOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
          <div className="bg-card w-full max-w-md rounded-2xl border shadow-2xl animate-in zoom-in-95 duration-200 overflow-hidden">
            <div className="p-6 border-b">
              <h2 className="text-xl font-bold">Generate New API Key</h2>
            </div>
            {newGeneratedKey && newKeyName.trim() !== "" ? (
              <div className="p-6 space-y-6">
                <div className="p-4 bg-green-500/10 text-green-600 rounded-lg flex items-start gap-3 border border-green-500/20">
                  <CheckCircle2 className="w-5 h-5 mt-0.5 flex-shrink-0" />
                  <div className="space-y-1">
                    <p className="font-bold text-sm">Key generated successfully!</p>
                    <p className="text-xs">Please copy this key now. You won't be able to see it again after closing this window.</p>
                  </div>
                </div>
                <div className="flex flex-col space-y-2">
                  <label className="text-sm font-semibold">Your New Key</label>
                  <div className="flex gap-2">
                    <input 
                      type="text" 
                      readOnly 
                      value={newGeneratedKey} 
                      className="flex-1 bg-muted/50 border-2 border-border rounded-lg px-3 py-2 font-mono text-sm"
                    />
                    <button 
                      onClick={() => handleCopyKey("new", newGeneratedKey)}
                      className="p-2 bg-foreground text-background rounded-lg hover:bg-foreground/90 transition-colors"
                    >
                      {copiedId === "new" ? <CheckCircle2 className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                    </button>
                  </div>
                </div>
                <button 
                  onClick={() => {
                    setIsGenerateModalOpen(false);
                    setNewGeneratedKey(null);
                    setNewKeyName("");
                  }}
                  className="w-full py-2.5 bg-foreground text-background font-bold rounded-lg hover:bg-foreground/90 transition-colors shadow-sm"
                >
                  I've stored it safely
                </button>
              </div>
            ) : (
              <form onSubmit={handleConfirmKey} className="p-6 space-y-6">
                <div className="space-y-2">
                  <label htmlFor="keyName" className="text-sm font-semibold">Key Name</label>
                  <input 
                    id="keyName"
                    type="text" 
                    required 
                    value={newKeyName}
                    onChange={(e) => setNewKeyName(e.target.value)}
                    className="w-full px-4 py-2.5 bg-muted/50 border-2 border-transparent focus:border-primary focus:bg-background outline-none rounded-xl transition-all"
                    placeholder="e.g. Production Environment"
                  />
                  <p className="text-xs text-muted-foreground">Give your key a descriptive name to help identify it later.</p>
                </div>
                <div className="flex items-center justify-end gap-3 pt-4 border-t">
                  <button 
                    type="button" 
                    onClick={() => {
                      setIsGenerateModalOpen(false);
                      setNewGeneratedKey(null);
                      setNewKeyName("");
                    }}
                    className="px-4 py-2 text-sm font-bold text-muted-foreground hover:text-foreground transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit"
                    disabled={!newKeyName.trim() || isGenerating}
                    className="px-6 py-2 bg-foreground text-background font-bold rounded-lg hover:bg-foreground/90 transition-colors shadow-sm disabled:opacity-50 flex items-center gap-2"
                  >
                    {isGenerating ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                    Generate
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      {keyToDelete && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
          <div className="bg-card w-full max-w-md rounded-2xl border shadow-2xl animate-in zoom-in-95 duration-200 overflow-hidden">
            <div className="p-6 border-b">
              <h2 className="text-xl font-bold text-destructive">Delete API Key</h2>
            </div>
            <form onSubmit={confirmDeleteKey} className="p-6 space-y-6">
              <div className="p-4 bg-destructive/10 text-destructive rounded-lg text-sm border border-destructive/20 font-medium">
                This action cannot be undone. Any applications using this key will immediately lose access.
              </div>
              <div className="space-y-2">
                <label className="text-sm font-semibold text-muted-foreground">
                  Type <span className="text-foreground font-bold">{keyToDelete.name}</span> to confirm
                </label>
                <input 
                  type="text" 
                  required 
                  value={deleteConfirmationName}
                  onChange={(e) => setDeleteConfirmationName(e.target.value)}
                  className="w-full px-4 py-2.5 bg-muted/50 border-2 border-transparent focus:border-destructive focus:bg-background outline-none rounded-xl transition-all font-semibold"
                  placeholder={keyToDelete.name}
                />
              </div>
              <div className="flex items-center justify-end gap-3 pt-4 border-t">
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
                  disabled={deleteConfirmationName !== keyToDelete.name || isDeleting}
                  className="px-6 py-2 bg-destructive text-destructive-foreground font-bold rounded-lg hover:bg-destructive/90 transition-colors shadow-sm disabled:opacity-50 flex items-center gap-2"
                >
                  {isDeleting ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                  Delete Key
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
