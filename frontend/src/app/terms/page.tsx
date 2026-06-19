export default function TermsPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background pt-20 pb-24">
      <div className="container mx-auto max-w-3xl px-6 md:px-8 animate-in slide-in-from-bottom-8 fade-in duration-700">
        <h1 className="text-4xl font-extrabold tracking-tight mb-4 text-foreground">
          Terms of Service
        </h1>
        <p className="text-sm text-muted-foreground mb-8">Last updated: June 19, 2026</p>
        <div className="prose prose-zinc dark:prose-invert max-w-none prose-headings:font-bold prose-headings:tracking-tight prose-a:text-primary prose-p:leading-relaxed text-muted-foreground text-lg">
          <p>
            Please read these Terms of Service ("Terms") carefully before using the uSearch website and API services.
          </p>
          <h2 className="text-2xl mt-12 mb-6 text-foreground">1. Acceptance of Terms</h2>
          <p>
            By accessing or using our services, you agree to be bound by these Terms. If you disagree with any part of the terms, you may not access the service.
          </p>
          <h2 className="text-2xl mt-12 mb-6 text-foreground">2. API Usage and Rate Limiting</h2>
          <ul className="list-disc pl-6 space-y-2">
            <li>You must use the provided API keys securely and not expose them in public repositories.</li>
            <li>Rate limits apply based on your subscription tier. Bypassing rate limits is strictly prohibited.</li>
            <li>We reserve the right to throttle or suspend accounts that exhibit abusive behavior or excessive usage beyond their allocated quota.</li>
          </ul>
          <h2 className="text-2xl mt-12 mb-6 text-foreground">3. Data Usage</h2>
          <p>
            uSearch processes YouTube captions. You agree that your usage of our API to fetch this data complies with YouTube's Terms of Service and applicable copyright laws. We do not claim ownership over the generated caption data.
          </p>
        </div>
      </div>
    </div>
  );
}