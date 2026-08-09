import { notFound } from "next/navigation";
import { MOCK_ENDPOINTS } from "@/lib/mock-data";

export default async function EndpointPage({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = await params;
  const endpoint = MOCK_ENDPOINTS.find(e => e.slug === resolvedParams.slug);

  if (!endpoint) {
    notFound();
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      <div>
        <div className="flex items-center space-x-3 mb-4">
          <h1 className="text-3xl font-extrabold tracking-tight">{endpoint.title}</h1>
          <span className={`text-xs font-bold px-2 py-1 rounded-md ${
              endpoint.method === "GET" ? "bg-blue-100 text-blue-700" :
              endpoint.method === "POST" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-700"
            }`}>
            {endpoint.method}
          </span>
        </div>
        <p className="text-lg text-muted-foreground">{endpoint.description}</p>
        <div className="mt-4 flex items-center space-x-2">
          <code className="text-sm bg-muted px-2 py-1 rounded font-mono border">
            {endpoint.path}
          </code>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-xl font-semibold border-b pb-2">Parameters</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-muted/40">
              <tr>
                <th className="px-4 py-3 font-medium border-b">Name</th>
                <th className="px-4 py-3 font-medium border-b">Type</th>
                <th className="px-4 py-3 font-medium border-b">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {endpoint.parameters.map((param, idx) => (
                <tr key={idx}>
                  <td className="px-4 py-3 font-mono font-medium text-foreground">
                    {param.name}
                    {param.required && <span className="text-red-500 ml-1" title="Required">*</span>}
                  </td>
                  <td className="px-4 py-3 font-mono text-muted-foreground text-xs">{param.type}</td>
                  <td className="px-4 py-3 text-muted-foreground">{param.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-xl font-semibold border-b pb-2">Example Request</h3>
        <div className="bg-zinc-950 text-zinc-50 rounded-lg overflow-hidden border border-zinc-800">
          <div className="bg-zinc-900 px-4 py-2 border-b border-zinc-800 text-xs font-mono text-zinc-400">
            cURL
          </div>
          <div className="p-4 overflow-x-auto">
            <pre className="text-sm font-mono leading-relaxed">
              <code>
                curl -X {endpoint.method} https://api.ucontext.com{endpoint.path} \{"\n"}
                {endpoint.sampleRequest.headers && Object.entries(endpoint.sampleRequest.headers).map(([k, v]) => `  -H "${k}: ${v}" \\\n`).join('')}
                {endpoint.sampleRequest.body && `  -d '${JSON.stringify(endpoint.sampleRequest.body, null, 2)}'`}
              </code>
            </pre>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-xl font-semibold border-b pb-2">Example Response</h3>
        <div className="bg-zinc-950 text-zinc-50 rounded-lg overflow-hidden border border-zinc-800">
          <div className="bg-zinc-900 px-4 py-2 border-b border-zinc-800 text-xs font-mono text-zinc-400">
            JSON
          </div>
          <div className="p-4 overflow-x-auto">
            <pre className="text-sm font-mono text-green-400">
              <code>
                {JSON.stringify(endpoint.sampleResponse, null, 2)}
              </code>
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
