export default function RateLimitsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-extrabold tracking-tight">Rate Limits</h1>
      <p className="text-lg text-muted-foreground">
        API rate limits depend on your pricing tier. Free tier includes 100 requests per month.
      </p>
    </div>
  );
}
