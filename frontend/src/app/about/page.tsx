export default function AboutPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background pt-20 pb-24">
      <div className="container mx-auto max-w-3xl px-6 md:px-8 animate-in slide-in-from-bottom-8 fade-in duration-700">
        <h1 className="text-4xl font-extrabold tracking-tight mb-8 text-foreground">
          About uSearch
        </h1>
        <div className="prose prose-zinc dark:prose-invert max-w-none prose-headings:font-bold prose-headings:tracking-tight prose-a:text-primary prose-p:leading-relaxed text-muted-foreground text-lg">
          <p>
            uSearch was built on a simple premise: video content shouldn't be a black box. 
            With millions of hours of educational, technical, and entertainment content uploaded every day, finding a specific moment or quote can feel like searching for a needle in a haystack.
          </p>
          <h2 className="text-2xl mt-12 mb-6 text-foreground">Our Mission</h2>
          <p>
            We aim to make spoken knowledge within videos as searchable and accessible as plain text on a webpage. 
            By leveraging advanced embeddings and fast regex searching, we enable researchers, content creators, and developers to instantly pinpoint the exact context they need.
          </p>
          <h2 className="text-2xl mt-12 mb-6 text-foreground">Why We Built This</h2>
          <p>
            Traditional video search only looks at titles, descriptions, and tags. We go deeper by indexing the actual spoken words. Whether you need to export full transcripts for an AI pipeline or just want to find out when a specific topic was mentioned in a 2-hour podcast, uSearch provides the tools to do it efficiently.
          </p>
        </div>
      </div>
    </div>
  );
}
