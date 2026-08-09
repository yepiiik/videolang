export default function IntroductionPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-extrabold tracking-tight">Introduction</h1>
      <p className="text-lg text-muted-foreground">
        Welcome to the uSearch REST API documentation. Our API allows you to programmatically search through YouTube captions, fetch semantic matches, and export full transcripts in various formats.
      </p>
      <div className="bg-muted/50 border rounded-lg p-6 mt-8">
        <h3 className="font-semibold mb-2">Base URL</h3>
        <code className="text-sm bg-background px-2 py-1 rounded border">https://usearch.floredo.com/api/v1</code>
      </div>
    </div>
  );
}
