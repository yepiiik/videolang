import re

with open('c:/Users/user/prod/py/videolang/frontend/src/app/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Rename UnifiedPipelinePage to SearchPageContent
content = content.replace('export default function UnifiedPipelinePage() {', 'function SearchPageContent() {')

# 2. Add suspense and hooks imports
imports = 'import { Suspense } from "react";\nimport { useRouter, useSearchParams } from "next/navigation";\n'
content = content.replace('import { useState, useMemo, useEffect } from "react";', 'import { useState, useMemo, useEffect } from "react";\n' + imports)

# 3. Add the wrapper component at the bottom
wrapper = '''
export default function UnifiedPipelinePage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading...</div>}>
      <SearchPageContent />
    </Suspense>
  );
}
'''
content = content + wrapper

# 4. Inject useSearchParams inside SearchPageContent
hooks = '''
  const router = useRouter();
  const searchParams = useSearchParams();

  const initialSourceUrl = searchParams.get('source') || "";
  const initialSearchQuery = searchParams.get('q') || "";
  const initialSearchType = (searchParams.get('type') as SearchType) || "intelligent";

  const [sourceType, setSourceType] = useState("channel");
  const [sourceUrl, setSourceUrl] = useState(initialSourceUrl);
  const [hasLoaded, setHasLoaded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState(initialSearchQuery);
  const [searchType, setSearchType] = useState<SearchType>(initialSearchType);
  const [initialLoadTriggered, setInitialLoadTriggered] = useState(false);
'''

start_state = '''  const [sourceType, setSourceType] = useState("channel");
  const [sourceUrl, setSourceUrl] = useState("");

  const [hasLoaded, setHasLoaded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const [searchQuery, setSearchQuery] = useState("");
  const [searchType, setSearchType] = useState<SearchType>("intelligent");'''

content = content.replace(start_state, hooks.strip())

# 5. Extract loadSource logic
handle_load_old = '''  const handleLoad = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sourceUrl.trim()) {
      alert("Please enter a valid YouTube channel, playlist, or video URL.");
      return;
    }

    setIsLoading(true);'''

handle_load_new = '''  const loadSource = async (url: string) => {
    if (!url.trim()) return;
    setIsLoading(true);'''

content = content.replace(handle_load_old, handle_load_new)

# Inside loadSource, replace `encodeURIComponent(sourceUrl)` with `encodeURIComponent(url)`
loadSource_part = content[content.find('const loadSource = async'):]
end_of_loadSource = loadSource_part.find('const clearSource = () =>')
loadSource_body = loadSource_part[:end_of_loadSource]
new_loadSource_body = loadSource_body.replace('encodeURIComponent(sourceUrl)', 'encodeURIComponent(url)')

content = content.replace(loadSource_body, new_loadSource_body)

# Now add back the handleLoad and the effects
effects = '''
  const handleLoad = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sourceUrl.trim()) {
      alert("Please enter a valid YouTube channel, playlist, or video URL.");
      return;
    }
    await loadSource(sourceUrl);
  };

  useEffect(() => {
    if (initialSourceUrl && !initialLoadTriggered) {
      setInitialLoadTriggered(true);
      loadSource(initialSourceUrl);
    }
  }, [initialSourceUrl, initialLoadTriggered]);

  const [initialSearchTriggered, setInitialSearchTriggered] = useState(false);
  useEffect(() => {
    if (hasLoaded && initialSearchQuery && !initialSearchTriggered) {
      setInitialSearchTriggered(true);
      if (initialSearchType === 'intelligent') {
        handleIntelligentSearch(initialSearchQuery, initialSearchType);
      }
    }
  }, [hasLoaded, initialSearchQuery, initialSearchType, initialSearchTriggered]);

  useEffect(() => {
    const params = new URLSearchParams();
    if (sourceUrl) params.set('source', sourceUrl);
    if (searchQuery) params.set('q', searchQuery);
    if (searchType !== 'intelligent') params.set('type', searchType);
    
    const newUrl = params.toString() ? `/?${params.toString()}` : '/';
    if (window.location.search !== `?${params.toString()}` && window.location.search !== newUrl) {
      router.replace(newUrl, { scroll: false });
    }
  }, [sourceUrl, searchQuery, searchType, router]);
'''

content = content.replace('const clearSource = () =>', effects + '\n  const clearSource = () =>')

# In handleIntelligentSearch, remove the filter using loadedVideos, and add arguments
handle_search_old = '''  const handleIntelligentSearch = async () => {
    if (!searchQuery.trim() || searchType !== 'intelligent') {
      setSearchResults([]);
      setLastIntelligentQuery("");
      return;
    }
    setIsSearching(true);
    setLastIntelligentQuery(searchQuery.trim());
    try {
      const res = await fetch(`/api/youtube/search?query=${encodeURIComponent(searchQuery)}`);
      const data = await res.json();
      if (Array.isArray(data)) {
        // filter data to only include videos from loadedVideos
        const loadedIds = new Set(loadedVideos.map(v => v.video_id));
        setSearchResults(data.filter(r => loadedIds.has(r.video_id)));
      }
    } catch (err) {'''

handle_search_new = '''  const handleIntelligentSearch = async (query = searchQuery, type = searchType) => {
    if (!query.trim() || type !== 'intelligent') {
      setSearchResults([]);
      setLastIntelligentQuery("");
      return;
    }
    setIsSearching(true);
    setLastIntelligentQuery(query.trim());
    try {
      const res = await fetch(`/api/youtube/search?query=${encodeURIComponent(query)}`);
      const data = await res.json();
      if (Array.isArray(data)) {
        setSearchResults(data);
      }
    } catch (err) {'''

content = content.replace(handle_search_old, handle_search_new)

with open('c:/Users/user/prod/py/videolang/frontend/src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Refactored page.tsx')
