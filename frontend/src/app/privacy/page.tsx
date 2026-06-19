export default function PrivacyPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background pt-20 pb-24">
      <div className="container mx-auto max-w-3xl px-6 md:px-8 animate-in slide-in-from-bottom-8 fade-in duration-700">
        <h1 className="text-4xl font-extrabold tracking-tight mb-4 text-foreground">
          Privacy Policy
        </h1>
        <p className="text-sm text-muted-foreground mb-8">Last updated: June 19, 2026</p>
        <div className="prose prose-zinc dark:prose-invert max-w-none prose-headings:font-bold prose-headings:tracking-tight prose-a:text-primary prose-p:leading-relaxed text-muted-foreground text-lg">
          <p>
            Your privacy is critically important to us. At uSearch, we follow a few fundamental principles:
          </p>
          <ul className="list-disc pl-6 space-y-2 mt-4 mb-8">
            <li>We don't ask you for personal information unless we truly need it.</li>
            <li>We don't share your personal information with anyone except to comply with the law, develop our products, or protect our rights.</li>
            <li>We don't store personal information on our servers unless required for the ongoing operation of our services.</li>
          </ul>
          <h2 className="text-2xl mt-12 mb-6 text-foreground">Information We Collect</h2>
          <p>
            <strong>Account Information:</strong> When you sign up, we require basic information such as your email address and a password.
          </p>
          <p className="mt-4">
            <strong>Usage Data:</strong> We collect aggregate statistics about the API queries being made to monitor performance and improve our search algorithms. The specific search terms are not linked to your personal identity unless explicitly stated.
          </p>
          <h2 className="text-2xl mt-12 mb-6 text-foreground">Security</h2>
          <p>
            The security of your Personal Information is important to us, but remember that no method of transmission over the Internet, or method of electronic storage is 100% secure. While we strive to use commercially acceptable means to protect your Personal Information, we cannot guarantee its absolute security.
          </p>
        </div>
      </div>
    </div>
  );
}