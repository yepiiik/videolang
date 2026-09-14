import re

with open('c:/Users/user/prod/py/videolang/frontend/src/app/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add AlertCircle to imports
if 'AlertCircle' not in content:
    content = content.replace('Search, Link as LinkIcon, CheckSquare, Square, Download, ChevronDown, Sparkles, Code2, ArrowRight, X, LayoutGrid, List as ListIcon', 'Search, Link as LinkIcon, CheckSquare, Square, Download, ChevronDown, Sparkles, Code2, ArrowRight, X, LayoutGrid, List as ListIcon, AlertCircle')

# Add error state
if 'const [error, setError]' not in content:
    content = content.replace('const [isLoading, setIsLoading] = useState(false);', 'const [isLoading, setIsLoading] = useState(false);\n  const [error, setError] = useState<string | null>(null);')

# Update loadSource
loadSource_old = '''  const loadSource = async (url: string) => {
    if (!url.trim()) return;
    setIsLoading(true);
    updateUrl(url, searchQuery, searchType);
    setLoadedVideos([]);
    try {
      // 1. Fetch channel videos list
      const videosRes = await fetch(`/api/youtube/channel/videos?query=${encodeURIComponent(url)}`);
      const videosData = await videosRes.json();

      if (videosData.error) {
        alert("Failed to load videos: " + videosData.error);
        setIsLoading(false);
        return;
      }

      const allVideos = Array.isArray(videosData) ? videosData : (videosData.videos || []);
      if (allVideos.length === 0) {
        alert("No videos found in channel.");
        setIsLoading(false);
        return;
      }'''

loadSource_new = '''  const loadSource = async (url: string) => {
    if (!url.trim()) return;
    setError(null);
    setIsLoading(true);
    updateUrl(url, searchQuery, searchType);
    setLoadedVideos([]);
    try {
      // 1. Fetch channel videos list
      const videosRes = await fetch(`/api/youtube/channel/videos?query=${encodeURIComponent(url)}`);
      const videosData = await videosRes.json();

      if (videosData.error) {
        setError("Failed to load videos: " + videosData.error);
        setIsLoading(false);
        return;
      }

      const allVideos = Array.isArray(videosData) ? videosData : (videosData.videos || []);
      if (allVideos.length === 0) {
        setError("No videos found in channel.");
        setIsLoading(false);
        return;
      }'''

content = content.replace(loadSource_old, loadSource_new)

# Update handleLoad
handleLoad_old = '''  const handleLoad = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sourceUrl.trim()) {
      alert("Please enter a valid YouTube channel, playlist, or video URL.");
      return;
    }
    await loadSource(sourceUrl);
  };'''

handleLoad_new = '''  const handleLoad = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sourceUrl.trim()) {
      setError("Please enter a valid YouTube channel, playlist, or video URL.");
      return;
    }
    await loadSource(sourceUrl);
  };'''

content = content.replace(handleLoad_old, handleLoad_new)

# Render error message
error_jsx = '''
              {error && (
                <div className="w-full flex items-center p-4 mb-4 text-red-600 border border-red-200 rounded-2xl bg-red-50/50 dark:bg-red-950/20 dark:border-red-900/50 dark:text-red-400 animate-in fade-in zoom-in-95 duration-300">
                  <AlertCircle className="w-5 h-5 mr-3 shrink-0" />
                  <p className="text-sm font-medium">{error}</p>
                </div>
              )}
'''

if 'AlertCircle' not in content[content.find('<form onSubmit={handleLoad}'):content.find('<div className="flex bg-background border-2')]:
    content = content.replace(
        '<div className="flex bg-background border-2 border-border focus-within:border-primary',
        error_jsx.lstrip() + '              <div className="flex bg-background border-2 border-border focus-within:border-primary'
    )

with open('c:/Users/user/prod/py/videolang/frontend/src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
