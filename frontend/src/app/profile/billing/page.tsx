"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Check, DollarSign, Bitcoin, Loader2 } from "lucide-react";
import { MOCK_PRICING } from "@/lib/mock-data";
import { getProfileData, schedulePlan, applyScheduledPlan, depositFunds } from "@/app/actions/profile.actions";
import { TransactionData } from "@/models/transaction.model";

export default function BillingPage() {
  const router = useRouter();

  // Billing State
  const [currentPlan, setCurrentPlan] = useState("Free");
  const [nextPlan, setNextPlan] = useState<string | null>(null);
  const [accountBalance, setAccountBalance] = useState(0);
  const [transactions, setTransactions] = useState<TransactionData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const [isChangePlanModalOpen, setIsChangePlanModalOpen] = useState(false);
  const [isApplyNowModalOpen, setIsApplyNowModalOpen] = useState(false);
  const [isAddFundsModalOpen, setIsAddFundsModalOpen] = useState(false);
  const [addFundsAmount, setAddFundsAmount] = useState<number>(20);
  const [selectedNewPlan, setSelectedNewPlan] = useState("Standard");
  const [paymentMethod, setPaymentMethod] = useState<"paypal" | "crypto">("paypal");
  const [isProcessingPayment, setIsProcessingPayment] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const data = await getProfileData();
      setCurrentPlan(data.user.currentPlan || "Free");
      setNextPlan(data.user.scheduledPlan || null);
      setAccountBalance(data.user.walletBalance || 0);
      setTransactions(data.transactions);
    } catch (error) {
      console.error("Failed to load billing data", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubscribe = async () => {
    setIsProcessingPayment(true);
    try {
      const price = MOCK_PRICING.find(p => p.name === selectedNewPlan)?.price || "$0";
      const method = paymentMethod === 'paypal' ? 'PayPal' : 'Crypto';
      await schedulePlan(selectedNewPlan, price, method);
      await loadData();
      setIsChangePlanModalOpen(false);
    } catch (error) {
      console.error("Failed to change plan", error);
    } finally {
      setIsProcessingPayment(false);
    }
  };

  const handleApplyNow = async () => {
    if (nextPlan) {
      try {
        await applyScheduledPlan();
        await loadData();
        setIsApplyNowModalOpen(false);
      } catch (error) {
        console.error("Failed to apply plan immediately", error);
      }
    }
  };

  const handleAddFunds = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessingPayment(true);
    try {
      const method = paymentMethod === "paypal" ? "PayPal" : "Cryptocurrency";
      await depositFunds(addFundsAmount, method);
      await loadData();
      setIsAddFundsModalOpen(false);
    } catch (error) {
      console.error("Failed to add funds", error);
    } finally {
      setIsProcessingPayment(false);
    }
  };

  return (
    <>
      <div className="flex flex-col space-y-8">
        <div className="flex flex-col space-y-2 mb-2">
          <h1 className="text-4xl font-extrabold tracking-tight">Billing & Plans</h1>
          <p className="text-lg text-muted-foreground">Manage your subscription and view your payment history.</p>
        </div>

        {/* Account Balance Card (Top, Full Width) */}
        <div className="bg-card border-2 border-primary/20 rounded-2xl p-6 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">Account Balance</p>
            <h2 className="text-4xl font-black mt-1 tracking-tighter">
              {isLoading ? <Loader2 className="w-8 h-8 animate-spin mt-1" /> : `$${accountBalance.toFixed(2)}`}
            </h2>
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
            {isLoading ? (
              <div className="flex-1 flex items-center justify-center p-8">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
              </div>
            ) : MOCK_PRICING.filter(p => p.name === currentPlan).map(plan => (
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
            {isLoading ? (
              <div className="flex-1 flex items-center justify-center p-8">
                <Loader2 className="w-8 h-8 animate-spin text-amber-500" />
              </div>
            ) : !nextPlan ? (
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
                  <div className="mt-auto space-y-3">
                    <div className="bg-amber-500/10 border border-amber-500/20 text-amber-600 p-4 rounded-lg text-sm font-medium text-center">
                      This plan will activate at the end of your current billing cycle.
                    </div>
                    <button
                      onClick={() => setIsApplyNowModalOpen(true)}
                      className="w-full inline-flex items-center justify-center rounded-md text-sm font-bold transition-colors h-12 px-8 focus-visible:outline-none border-2 border-primary text-primary hover:bg-primary/10 shadow-sm"
                    >
                      Apply Now
                    </button>
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
                {isLoading ? (
                  <tr>
                    <td colSpan={4} className="px-4 py-8 text-center text-muted-foreground">
                      <Loader2 className="w-5 h-5 animate-spin mx-auto" />
                    </td>
                  </tr>
                ) : transactions.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="px-4 py-8 text-center text-muted-foreground">No transactions found.</td>
                  </tr>
                ) : transactions.map(tx => (
                  <tr key={tx.id} className="hover:bg-muted/20 transition-colors">
                    <td className="px-4 py-3 whitespace-nowrap text-muted-foreground">{new Date(tx.date as string).toISOString().split('T')[0]}</td>
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
            </div>

            <div className="p-6 md:p-8 border-t bg-muted/10 rounded-b-2xl flex items-center justify-between sticky bottom-0 z-10">
              <div>
                <p className="text-sm font-semibold">Total due today:</p>
                <p className="text-2xl font-black">{MOCK_PRICING.find(p => p.name === selectedNewPlan)?.price}</p>
              </div>
              
              {selectedNewPlan === "Custom" ? (
                <button 
                  onClick={() => router.push("/contact")}
                  className="px-8 py-3 flex items-center justify-center font-bold text-accent-foreground bg-accent hover:bg-accent/90 transition-all shadow-md rounded-xl"
                >
                  Contact Sales
                </button>
              ) : (
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
              )}
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

      {/* Apply Now Warning Modal */}
      {isApplyNowModalOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-background/80 backdrop-blur-sm p-4">
          <div className="bg-card w-full max-w-md rounded-2xl border shadow-2xl animate-in zoom-in-95 duration-200 overflow-hidden">
            <div className="p-6 border-b bg-destructive/10">
              <h2 className="text-xl font-bold text-destructive flex items-center gap-2">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Warning
              </h2>
            </div>
            
            <div className="p-6">
              <p className="text-foreground text-lg mb-4">
                Are you sure you want to apply this plan immediately?
              </p>
              <p className="text-muted-foreground font-medium bg-muted p-4 rounded-lg">
                All resources and remaining limits of your current billing plan will be <strong className="text-destructive">lost immediately</strong>.
              </p>
            </div>

            <div className="p-6 bg-muted/20 border-t flex items-center justify-end gap-3">
              <button 
                onClick={() => setIsApplyNowModalOpen(false)}
                className="px-4 py-2 font-bold text-muted-foreground hover:text-foreground transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={handleApplyNow}
                className="px-6 py-2 bg-destructive text-destructive-foreground font-bold rounded-lg hover:bg-destructive/90 transition-colors shadow-sm"
              >
                Apply Immediately
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
