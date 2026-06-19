"use client";

import { useState } from "react";
import { PricingCards } from "@/components/pricing/PricingCards";
import { FeatureMatrix } from "@/components/pricing/FeatureMatrix";

export default function PricingPage() {
  const [isAnnual, setIsAnnual] = useState(false);

  return (
    <div className="flex flex-col min-h-screen bg-background pt-20 pb-24">
      <div className="container mx-auto max-w-7xl px-4 md:px-8">
        {/* Pricing Header */}
        <div className="text-center mb-16 animate-in slide-in-from-top-4 fade-in duration-700">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            Simple, transparent pricing
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            Whether you're exploring the platform or scaling an enterprise product, we have a plan for you.
          </p>
          
          {/* Monthly/Annually Toggle */}
          <div className="flex items-center justify-center space-x-3">
            <span className={`text-sm font-medium transition-colors ${!isAnnual ? "text-foreground" : "text-muted-foreground"}`}>Monthly</span>
            <button 
              onClick={() => setIsAnnual(!isAnnual)}
              className="relative inline-flex h-6 w-11 items-center rounded-full bg-primary/20 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              aria-checked={isAnnual}
              role="switch"
            >
              <span 
                className={`inline-block h-5 w-5 transform rounded-full bg-primary transition-transform ${isAnnual ? "translate-x-5" : "translate-x-1"}`} 
              />
            </button>
            <span className={`text-sm font-medium transition-colors ${isAnnual ? "text-foreground" : "text-muted-foreground"}`}>
              Annually <span className="ml-1 inline-flex items-center rounded-full bg-green-100 px-2 py-0.5 text-xs font-semibold text-green-700 dark:bg-green-900/30 dark:text-green-400">Save 20%</span>
            </span>
          </div>
        </div>

        {/* Tier Grid */}
        <PricingCards isAnnual={isAnnual} />

        {/* Feature Comparison Matrix */}
        <FeatureMatrix />
      </div>
    </div>
  );
}