export default function AuthenticationPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-extrabold tracking-tight">Authentication</h1>
      <p className="text-lg text-muted-foreground">
        Authenticate your API requests by including your secret API key in the Authorization header.
      </p>
      <div className="bg-zinc-950 text-zinc-50 rounded-lg p-4 mt-6 overflow-x-auto">
        <pre className="text-sm"><code>Authorization: Bearer YOUR_API_KEY</code></pre>
      </div>
    </div>
  );
}
