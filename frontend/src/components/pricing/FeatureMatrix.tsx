import { Check, Minus } from "lucide-react";

export function FeatureMatrix() {
  const features = [
    { name: "API calls per month", free: "100", standard: "5,000", payg: "Unlimited", custom: "Unlimited" },
    { name: "Regex Search", free: true, standard: true, payg: true, custom: true },
    { name: "Intelligent Embeddings Search", free: false, standard: true, payg: true, custom: true },
    { name: "Export Formats", free: ".srt only", standard: "All formats", payg: "All formats", custom: "All formats" },
    { name: "Playlist & Channel Search", free: false, standard: true, payg: true, custom: true },
    { name: "Webhooks", free: false, standard: false, payg: true, custom: true },
    { name: "Custom Rate Limits", free: false, standard: false, payg: true, custom: true },
    { name: "Support Level", free: "Community", standard: "Email", payg: "Priority", custom: "24/7 Phone" },
    { name: "Custom Embedding Models", free: false, standard: false, payg: false, custom: true },
    { name: "SLA Guarantee", free: false, standard: false, payg: false, custom: true },
  ];

  return (
    <div className="mt-24 animate-in slide-in-from-bottom-12 fade-in duration-700 delay-150 fill-mode-both">
      <div className="text-center mb-10">
        <h3 className="text-2xl font-bold">Compare plans</h3>
        <p className="text-muted-foreground mt-2">Find the perfect feature set for your needs.</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[800px]">
          <thead>
            <tr className="border-b">
              <th className="py-4 px-6 font-medium text-muted-foreground w-1/3">Features</th>
              <th className="py-4 px-6 font-semibold text-center w-1/6">Free</th>
              <th className="py-4 px-6 font-semibold text-center w-1/6 text-primary">Standard</th>
              <th className="py-4 px-6 font-semibold text-center w-1/6">Metered</th>
              <th className="py-4 px-6 font-semibold text-center w-1/6">Custom</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {features.map((feature, idx) => (
              <tr key={idx} className="hover:bg-muted/30 transition-colors">
                <td className="py-4 px-6 text-sm font-medium">{feature.name}</td>
                <td className="py-4 px-6 text-center">
                  {typeof feature.free === "boolean" ? (
                    feature.free ? <Check className="h-4 w-4 mx-auto text-primary" /> : <Minus className="h-4 w-4 mx-auto text-muted-foreground/40" />
                  ) : (
                    <span className="text-sm text-muted-foreground">{feature.free}</span>
                  )}
                </td>
                <td className="py-4 px-6 text-center">
                  {typeof feature.standard === "boolean" ? (
                    feature.standard ? <Check className="h-4 w-4 mx-auto text-primary" /> : <Minus className="h-4 w-4 mx-auto text-muted-foreground/40" />
                  ) : (
                    <span className="text-sm text-muted-foreground">{feature.standard}</span>
                  )}
                </td>
                <td className="py-4 px-6 text-center">
                  {typeof feature.payg === "boolean" ? (
                    feature.payg ? <Check className="h-4 w-4 mx-auto text-primary" /> : <Minus className="h-4 w-4 mx-auto text-muted-foreground/40" />
                  ) : (
                    <span className="text-sm text-muted-foreground">{feature.payg}</span>
                  )}
                </td>
                <td className="py-4 px-6 text-center">
                  {typeof feature.custom === "boolean" ? (
                    feature.custom ? <Check className="h-4 w-4 mx-auto text-primary" /> : <Minus className="h-4 w-4 mx-auto text-muted-foreground/40" />
                  ) : (
                    <span className="text-sm text-muted-foreground">{feature.custom}</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
