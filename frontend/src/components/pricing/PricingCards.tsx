import { Check } from "lucide-react";
import { MOCK_PRICING } from "@/lib/mock-data";

export function PricingCards({ isAnnual }: { isAnnual: boolean }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-in slide-in-from-bottom-8 fade-in duration-700">
      {MOCK_PRICING.map((tier) => (
        <div 
          key={tier.name} 
          className={`flex flex-col rounded-2xl border bg-card p-6 shadow-sm transition-all hover:shadow-md ${tier.name === "Standard" ? "border-primary ring-1 ring-primary" : ""}`}
        >
          {/* Header */}
          <div className="mb-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xl font-bold">{tier.name}</h3>
              {tier.name === "Standard" && (
                <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-primary/10 text-primary border-transparent">
                  Popular
                </span>
              )}
            </div>
            <p className="text-sm text-muted-foreground min-h-[40px]">{tier.description}</p>
          </div>

          {/* Price */}
          <div className="mb-6">
            <span className="text-4xl font-extrabold">{tier.price}</span>
            {tier.period && (
              <span className="text-muted-foreground ml-1">{tier.period}</span>
            )}
            {/* Show annual text if toggled, just as an example */}
            {isAnnual && tier.period && tier.name !== "Metered" && (
              <p className="text-xs text-muted-foreground mt-1">Billed annually</p>
            )}
          </div>

          {/* Features List */}
          <ul className="flex-1 space-y-3 mb-8">
            {tier.features.map((feature, i) => (
              <li key={i} className="flex items-start text-sm">
                <Check className="h-4 w-4 text-primary mr-3 flex-shrink-0 mt-0.5" />
                <span className="text-muted-foreground">{feature}</span>
              </li>
            ))}
          </ul>

          {/* CTA Button */}
          <button
            className={`w-full inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors h-11 px-8 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
              ${tier.ctaVariant === "default" ? "bg-primary text-primary-foreground hover:bg-primary/90 shadow" : ""}
              ${tier.ctaVariant === "outline" ? "border border-input bg-background hover:bg-muted hover:text-foreground shadow-sm" : ""}
              ${tier.ctaVariant === "accent" ? "bg-foreground text-background hover:bg-foreground/90 shadow" : ""}
            `}
          >
            {tier.ctaText}
          </button>
        </div>
      ))}
    </div>
  );
}
