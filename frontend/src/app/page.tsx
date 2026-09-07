"use client";

import { useState, useMemo, useEffect } from "react";
import { Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";

import { Search, Link as LinkIcon, CheckSquare, Square, Download, ChevronDown, Sparkles, Code2, ArrowRight, X, LayoutGrid, List as ListIcon } from "lucide-react";
import { Video, SearchResult } from "@/types";
import Link from "next/link";

type SearchType = "intelligent" | "regex";

function SearchPageContent() {
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

  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [expandedVideos, setExpandedVideos] = useState<Record<string, boolean>>({});
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [isProcessing, setIsProcessing] = useState(false);
  const [includeShorts, setIncludeShorts] = useState(false);

  const [loadedVideos, setLoadedVideos] = useState<Video[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  const updateUrl = (source: string, query: string, type: SearchType) => {
    const params = new URLSearchParams();
    if (source) params.set('source', source);
    if (query) params.set('q', query);
    if (type !== 'intelligent') params.set('type', type);
    
    const newUrl = params.toString() ? `/?${params.toString()}` : '/';
    if (window.location.search !== `?${params.toString()}` && window.location.search !== newUrl) {
      router.replace(newUrl, { scroll: false });
    }
  };

  const loadSource = async (url: string) => {
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
      }

      setHasLoaded(true); // Show grid immediately

      // 2. Process videos in blocks
      const BATCH_SIZE = 3;
      const MAX_VIDEOS = 15; // Limit to 15 to avoid massive usage during testing

      const videosToProcess = allVideos.slice(0, Math.min(allVideos.length, MAX_VIDEOS));

      for (let i = 0; i < videosToProcess.length; i += BATCH_SIZE) {
        const batch = videosToProcess.slice(i, i + BATCH_SIZE);

        // Process batch concurrently
        const promises = batch.map(async (v: any) => {
          try {
            const res = await fetch(`/api/youtube/index/video`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                video_id: v.video_id || v.id,
                title: v.title,
                description: v.description,
                published_at: v.published_at,
                thumbnail: v.thumbnail || v.thumbnailUrl
              })
            });
            const data = await res.json();
            if (data.status === "indexed" || data.status === "skipped") {
              setLoadedVideos(prev => {
                // Ensure no duplicates
                if (prev.some(pv => pv.video_id === data.video.video_id)) return prev;
                return [...prev, data.video];
              });
            }
          } catch (e) {
            console.error(`Failed to index ${v.title}`, e);
          }
        });

        await Promise.all(promises);

        // Add delay between batches
        if (i + BATCH_SIZE < videosToProcess.length) {
          await new Promise(r => setTimeout(r, 2000));
        }
      }

    } catch (err) {
      console.error(err);
      alert("Error loading source");
    } finally {
      setIsLoading(false);
    }
  };

  
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



  const clearSource = () => {
    setHasLoaded(false);
    setSourceUrl("");
    setSearchQuery("");
    setSelectedIds(new Set());
    setLoadedVideos([]);
    setSearchResults([]);
    setLastIntelligentQuery("");
  };

  const [isSearching, setIsSearching] = useState(false);
  const [lastIntelligentQuery, setLastIntelligentQuery] = useState("");

  const handleIntelligentSearch = async (query = searchQuery, type = searchType) => {
    if (!query.trim() || type !== 'intelligent') {
      setSearchResults([]);
      setLastIntelligentQuery("");
      return;
    }
    setIsSearching(true);
    setLastIntelligentQuery(query.trim());
    updateUrl(sourceUrl, query, type);
    try {
      const res = await fetch(`/api/youtube/search?query=${encodeURIComponent(query)}`);
      const data = await res.json();
      if (Array.isArray(data)) {
        setSearchResults(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  // Clear search results when switching back to intelligent search if query is empty
  useEffect(() => {
    if (searchType === 'intelligent' && !searchQuery.trim()) {
      setSearchResults([]);
      setLastIntelligentQuery("");
    }
  }, [searchType, searchQuery]);

  const filteredResults = useMemo(() => {
    if (!hasLoaded) return [];

    let results = [];
    
    const isRegexActive = searchType === 'regex' && !!searchQuery.trim();
    const isIntelligentActive = searchType === 'intelligent' && !!lastIntelligentQuery;

    // If no active search submitted, show all videos with all windows
    if (!isRegexActive && !isIntelligentActive) {
      results = loadedVideos.map(v => {
        const allWindows = (v.chunks || []).flatMap((c: any) => c.windows || []);
        const initialCaptions = allWindows.map((w: any, index: number) => {
          const minutes = Math.floor(w.start / 60);
          const seconds = Math.floor(w.start % 60);
          const timecode = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

          return {
            id: `window_${index}`,
            timecode: timecode,
            seconds: Math.floor(w.start),
            start: w.start,
            end: w.end,
            text: w.text
          };
        });

        return {
          ...v,
          id: v.video_id,
          thumbnailUrl: `https://img.youtube.com/vi/${v.video_id}/hqdefault.jpg`,
          captions: initialCaptions
        };
      });
    } else if (searchType === 'regex') {
      // Regex Search: filter local windows directly
      let regex: RegExp | null = null;
      try {
        regex = new RegExp(searchQuery, 'gi');
      } catch (e) {
        // Invalid regex, return empty or treat as normal string
        // Falling back to simple includes
        const q = searchQuery.toLowerCase();
        results = loadedVideos.map(v => {
          const allWindows = (v.chunks || []).flatMap((c: any) => c.windows || []);
          const filteredCaptions = allWindows.filter((w: any) => w.text.toLowerCase().includes(q)).map((w: any, index: number) => {
            const minutes = Math.floor(w.start / 60);
            const seconds = Math.floor(w.start % 60);
            const timecode = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
            return {
              id: `window_${index}`,
              timecode: timecode,
              seconds: Math.floor(w.start),
              start: w.start,
              end: w.end,
              text: w.text
            };
          });
          return {
            ...v,
            id: v.video_id,
            thumbnailUrl: `https://img.youtube.com/vi/${v.video_id}/hqdefault.jpg`,
            captions: filteredCaptions
          };
        }).filter(v => v.captions.length > 0);
      }

      if (regex) {
        results = loadedVideos.map(v => {
          const allWindows = (v.chunks || []).flatMap((c: any) => c.windows || []);
          const filteredCaptions = allWindows.filter((w: any) => regex.test(w.text)).map((w: any, index: number) => {
            const minutes = Math.floor(w.start / 60);
            const seconds = Math.floor(w.start % 60);
            const timecode = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
            return {
              id: `window_${index}`,
              timecode: timecode,
              seconds: Math.floor(w.start),
              start: w.start,
              end: w.end,
              text: w.text
            };
          });
          return {
            ...v,
            id: v.video_id,
            thumbnailUrl: `https://img.youtube.com/vi/${v.video_id}/hqdefault.jpg`,
            captions: filteredCaptions
          };
        }).filter(v => v.captions.length > 0);
      }
    } else {
      // Intelligent Search: use results from backend embedding search
      const videoMap = new Map();

      for (const r of searchResults) {
        if (!videoMap.has(r.video_id)) {
          const videoInfo = loadedVideos.find(v => v.video_id === r.video_id);
          if (videoInfo) {
            videoMap.set(r.video_id, {
              ...videoInfo,
              id: r.video_id,
              thumbnailUrl: `https://img.youtube.com/vi/${r.video_id}/hqdefault.jpg`,
              captions: []
            });
          }
        }

        const vid = videoMap.get(r.video_id);
        if (vid) {
          const minutes = Math.floor(r.start / 60);
          const seconds = Math.floor(r.start % 60);
          const timecode = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

          vid.captions.push({
            id: Math.random().toString(36).substring(7),
            timecode: timecode,
            seconds: Math.floor(r.start),
            text: r.text,
            end: r.end,
            score: r.timestamp_score
          });
        }
      }

      results = Array.from(videoMap.values()).filter(v => v.captions.length > 0);
    }

    // Filter out shorts if toggle is disabled
    if (!includeShorts) {
      results = results.filter(v => {
        // Check for #short or #shorts in title
        if (v.title.toLowerCase().includes('#short')) return false;

        // Check video duration based on the last chunk
        if (v.chunks && v.chunks.length > 0) {
          const lastChunk = v.chunks[v.chunks.length - 1];
          if (lastChunk.end <= 120) return false;
        } else if (v.captions && v.captions.length > 0) {
          const lastCaption = v.captions[v.captions.length - 1];
          if (lastCaption.end <= 120) return false;
        }
        return true;
      });
    }

    return results;
  }, [hasLoaded, loadedVideos, searchQuery, searchType, searchResults, includeShorts]);

  const toggleAll = () => {
    if (selectedIds.size === filteredResults.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(filteredResults.map(v => v.id)));
    }
  };

  const toggleVideo = (id: string) => {
    const newSet = new Set(selectedIds);
    if (newSet.has(id)) newSet.delete(id);
    else newSet.add(id);
    setSelectedIds(newSet);
  };

  const toggleExpand = (id: string) => {
    setExpandedVideos(prev => {
      // If we are collapsing the video, scroll back to its start
      if (prev[id]) {
        setTimeout(() => {
          document.getElementById(`video-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 10);
      }
      return { ...prev, [id]: !prev[id] };
    });
  };

  const handleExport = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setSelectedIds(new Set());
      alert(`Exported ${selectedIds.size} transcripts successfully!`);
    }, 1500);
  };

  const getBadgeClass = (score: number) => {
    const percent = Math.round(score * 100);
    if (percent > 40) return "bg-green-500/15 text-green-600 dark:text-green-400";
    if (percent > 20) return "bg-orange-500/15 text-orange-600 dark:text-orange-400";
    return "bg-red-500/15 text-red-600 dark:text-red-400";
  };

  const highlightText = (text: string, query: string, type: SearchType) => {
    if (!query) return text;
    try {
      const pattern = type === 'regex' ? query : query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(`(${pattern})`, 'gi');
      const parts = text.split(regex);
      return (
        <span>
          {parts.map((part, i) =>
            i % 2 !== 0 ? (
              <mark key={i} className="bg-primary/20 text-foreground font-semibold rounded-sm">{part}</mark>
            ) : part
          )}
        </span>
      );
    } catch (e) {
      return text; // Fallback to raw text if regex fails
    }
  };

  return (
    <div className="flex flex-col min-h-[calc(100vh-4rem)] bg-background text-foreground selection:bg-primary/20">

      {/* Dynamic Form Container */}
      <div
        className={`w-full flex flex-col items-center transition-all duration-700 ease-[cubic-bezier(0.2,0.8,0.2,1)] px-4 sm:px-6 z-40
        ${hasLoaded ? 'py-4 sticky top-[64px] bg-background/95 backdrop-blur-md border-b shadow-sm' : 'pt-[25vh] pb-16'}`}
      >
        <div className={`w-full transition-all duration-700 ${hasLoaded ? 'max-w-7xl flex flex-col xl:flex-row items-center gap-4' : 'max-w-3xl flex flex-col gap-6'}`}>

          {/* Initial Load Form */}
          {!hasLoaded ? (
            <form onSubmit={handleLoad} className="w-full flex flex-col gap-6">
              <div className="text-center space-y-2 mb-4">
                <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Extract Transcripts Instantly</h1>
                <p className="text-lg text-muted-foreground">Load any YouTube channel or playlist and export captions in bulk.</p>
              </div>

              <div className="flex bg-background border-2 border-border focus-within:border-primary focus-within:ring-4 focus-within:ring-primary/10 transition-all overflow-hidden rounded-2xl shadow-sm">
                <div className="relative border-r-2 border-border bg-muted/30 shrink-0">
                  <select
                    value={sourceType}
                    onChange={(e) => setSourceType(e.target.value)}
                    className="appearance-none bg-transparent font-semibold text-foreground focus:outline-none cursor-pointer py-4 pl-5 pr-10 text-lg"
                  >
                    <option value="channel">Channel</option>
                    <option value="playlist">Playlist</option>
                    <option value="category">Category</option>
                  </select>
                  <ChevronDown className="absolute right-4 top-4.5 w-5 h-5 opacity-50 pointer-events-none" />
                </div>
                <input
                  type="text"
                  value={sourceUrl}
                  onChange={(e) => setSourceUrl(e.target.value)}
                  placeholder="https://youtube.com/..."
                  className="flex-1 bg-transparent border-0 outline-none font-medium placeholder:text-muted-foreground/60 px-5 py-4 text-lg"
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex items-center justify-center font-bold text-primary-foreground bg-primary hover:bg-primary/90 transition-all shadow-md py-4 rounded-2xl text-lg disabled:opacity-50"
              >
                {isLoading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span>Analyzing Source...</span>
                  </div>
                ) : (
                  <>
                    Load Transcripts
                    <ArrowRight className="ml-2 w-5 h-5" />
                  </>
                )}
              </button>
            </form>
          ) : (
            /* Compact Header when Loaded */
            <div className="w-full flex flex-col lg:flex-row items-center gap-4 animate-in fade-in slide-in-from-top-2">

              {/* Loaded Source Badge */}
              <div className="flex items-center bg-muted/50 rounded-xl p-1.5 shrink-0 w-full lg:w-auto">
                <div className="flex items-center px-3 py-1.5 bg-background shadow-sm rounded-lg border">
                  <LinkIcon className="w-4 h-4 text-muted-foreground mr-2" />
                  <span className="text-sm font-semibold truncate max-w-[150px] sm:max-w-[200px]">{sourceUrl}</span>
                </div>
                <button onClick={clearSource} className="p-2 text-muted-foreground hover:text-destructive transition-colors ml-1">
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Advanced Filter Bar */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  if (searchType === 'intelligent') {
                    handleIntelligentSearch();
                  } else {
                    updateUrl(sourceUrl, searchQuery, searchType);
                  }
                }}
                className="flex flex-1 flex-col sm:flex-row bg-background border-2 border-border focus-within:border-primary focus-within:ring-4 focus-within:ring-primary/10 transition-all overflow-hidden rounded-xl shadow-sm w-full"
              >

                <div className="relative flex-1 flex items-center">
                  <Search className="absolute left-3 w-4 h-4 text-muted-foreground" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Filter loaded transcripts by keyword or regex..."
                    className="w-full bg-transparent border-0 outline-none font-medium placeholder:text-muted-foreground/60 pl-9 pr-12 py-2.5 text-sm"
                  />
                  {searchType === 'intelligent' && (
                    <button
                      type="submit"
                      disabled={isSearching}
                      className="absolute right-2 p-1.5 bg-primary/10 hover:bg-primary/20 text-primary rounded-md transition-colors disabled:opacity-50"
                    >
                      {isSearching ? (
                        <div className="w-4 h-4 border-2 border-primary/30 border-t-primary rounded-full animate-spin" />
                      ) : (
                        <ArrowRight className="w-4 h-4" />
                      )}
                    </button>
                  )}
                </div>

                <div className="flex border-t-2 sm:border-t-0 sm:border-l-2 border-border bg-muted/30 shrink-0 p-1">
                  <button
                    type="button"
                    onClick={() => setSearchType("intelligent")}
                    className={`flex items-center justify-center space-x-1.5 transition-all px-3 py-1.5 rounded-lg text-xs font-bold ${searchType === "intelligent" ? 'bg-background text-primary shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}
                  >
                    <Sparkles className="w-3 h-3" />
                    <span>Intelligent</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setSearchType("regex")}
                    className={`flex items-center justify-center space-x-1.5 transition-all px-3 py-1.5 rounded-lg text-xs font-bold ${searchType === "regex" ? 'bg-background text-primary shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}
                  >
                    <Code2 className="w-3 h-3" />
                    <span>Regex</span>
                  </button>
                </div>
              </form>

            </div>
          )}
        </div>
      </div>

      {/* Results Container */}
      {hasLoaded && (
        <div className="w-full px-4 sm:px-8 xl:px-12 py-8 flex-1 animate-in fade-in slide-in-from-top-4 duration-500">
          <div className="flex flex-col space-y-6 pb-24">

            {/* Grid Header */}
            <div className="flex items-center justify-between border-b pb-4">
              <div className="flex items-center space-x-6">
                <button onClick={toggleAll} className="flex items-center space-x-2 text-sm font-bold text-muted-foreground hover:text-foreground transition-colors">
                  {selectedIds.size === filteredResults.length && filteredResults.length > 0 ? <CheckSquare className="h-5 w-5 text-primary" /> : <Square className="h-5 w-5" />}
                  <span>Select All Filtered</span>
                </button>
                <h2 className="text-xl font-bold tracking-tight">Export Pipeline</h2>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex bg-muted/50 p-1 rounded-lg">
                  <button onClick={() => setViewMode("grid")} className={`p-1.5 rounded-md transition-all ${viewMode === "grid" ? "bg-background shadow-sm text-primary" : "text-muted-foreground hover:text-foreground"}`}>
                    <LayoutGrid className="w-4 h-4" />
                  </button>
                  <button onClick={() => setViewMode("list")} className={`p-1.5 rounded-md transition-all ${viewMode === "list" ? "bg-background shadow-sm text-primary" : "text-muted-foreground hover:text-foreground"}`}>
                    <ListIcon className="w-4 h-4" />
                  </button>
                </div>
                <button
                  onClick={() => setIncludeShorts(!includeShorts)}
                  className={`text-sm font-medium px-3 py-1.5 rounded-full transition-colors border ${includeShorts ? "bg-primary/10 text-primary border-primary/20" : "bg-transparent text-muted-foreground border-border hover:bg-muted"}`}
                >
                  {includeShorts ? "Shorts Included" : "Include Shorts"}
                </button>
                <div className="text-sm font-medium text-muted-foreground bg-muted px-3 py-1.5 rounded-full">
                  {filteredResults.length} videos match
                </div>
              </div>
            </div>

            {/* Video Grid / List */}
            {filteredResults.length > 0 || isLoading ? (
              viewMode === "grid" ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                  {filteredResults.map((video) => (
                    <div key={video.id} className={`flex flex-col bg-card border rounded-2xl overflow-hidden hover:shadow-lg transition-all group relative ${selectedIds.has(video.id) ? 'border-primary ring-2 ring-primary/20' : 'hover:border-primary/40'}`}>

                      {/* Checkbox Overlay */}
                      <button
                        onClick={() => toggleVideo(video.id)}
                        className="absolute top-2 left-2 z-10 bg-background/80 backdrop-blur rounded-md p-1 hover:bg-background transition-colors shadow-sm"
                      >
                        {selectedIds.has(video.id) ? <CheckSquare className="w-5 h-5 text-primary" /> : <Square className="w-5 h-5 text-muted-foreground" />}
                      </button>

                      <div
                        onClick={() => toggleVideo(video.id)}
                        className="relative aspect-video bg-muted border-b block shrink-0 cursor-pointer"
                      >
                        <img src={video.thumbnailUrl} alt={video.title} className="object-cover w-full h-full" />
                        <div className="absolute inset-0 bg-black/5 group-hover:bg-transparent transition-colors" />

                      </div>

                      <div className="p-4 flex flex-col flex-1 min-h-0">
                        <h3 className="font-bold text-[15px] leading-tight line-clamp-2 group-hover:text-primary transition-colors mb-2">
                          {video.title}
                        </h3>
                        <p className="text-[12px] text-muted-foreground font-medium mb-4">
                          {video.channelName}
                        </p>

                        {/* Scrollable Transcriptions with Timecodes */}
                        <div className="flex flex-col gap-2 mt-auto h-36 overflow-y-auto pr-2 custom-scrollbar">
                          {video.captions.map((cap) => (
                            <div key={cap.id} className="flex space-x-3 text-[13px] bg-muted/30 p-2 rounded-lg border border-transparent hover:border-border hover:bg-muted/50 transition-colors">
                              <a
                                href={`https://youtube.com/watch?v=${video.id}&t=${cap.seconds}s`}
                                target="_blank"
                                className="flex-shrink-0 text-primary font-semibold flex flex-col items-start pt-0.5 hover:underline"
                              >
                                <span>{cap.timecode}</span>
                                {cap.score !== undefined && (
                                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded mt-1 ${getBadgeClass(cap.score)}`}>
                                    {Math.round(cap.score * 100)}% Match
                                  </span>
                                )}
                              </a>
                              <p className="text-muted-foreground leading-relaxed">
                                {highlightText(cap.text, searchQuery, searchType)}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* Grid Loading Skeletons */}
                  {isLoading && (
                    <>
                      {[1, 2, 3].map((i) => (
                        <div key={`skeleton-${i}`} className="flex flex-col bg-card border rounded-2xl overflow-hidden animate-pulse">
                          <div className="aspect-video bg-muted/60" />
                          <div className="p-4 flex flex-col flex-1">
                            <div className="h-4 bg-muted rounded w-3/4 mb-2" />
                            <div className="h-3 bg-muted rounded w-1/2 mb-4" />
                            <div className="mt-auto h-32 bg-muted/20 rounded-lg" />
                          </div>
                        </div>
                      ))}
                    </>
                  )}
                </div>
              ) : (
                <div className="flex flex-col">
                  {filteredResults.map((video) => (
                    <div key={video.id} id={`video-${video.id}`} className="grid grid-cols-1 md:grid-cols-2 py-16 border-b border-border/50 relative group scroll-mt-[100px]">

                      {/* Left Column: Video Info (Sticky, hugging center) */}
                      <div className="flex flex-col w-full md:pr-6 lg:pr-12">
                        <div className={`w-full max-w-sm ml-auto sticky top-[180px] flex flex-col bg-card border rounded-2xl overflow-hidden transition-all shadow-sm ${selectedIds.has(video.id) ? 'border-primary ring-2 ring-primary/20' : 'hover:border-primary/40'}`}>
                          <div
                            onClick={() => toggleVideo(video.id)}
                            className="relative aspect-video bg-muted block shrink-0 cursor-pointer"
                          >
                            <img src={video.thumbnailUrl} alt={video.title} className="object-cover w-full h-full" />
                            <div className="absolute inset-0 bg-black/5 hover:bg-transparent transition-colors" />
                            <div className="absolute bottom-2 right-2 bg-black/80 text-white text-[11px] px-2 py-0.5 rounded-md font-medium tracking-wide">
                              12:45
                            </div>
                            {/* Checkbox Overlay */}
                            <button
                              onClick={(e) => { e.preventDefault(); e.stopPropagation(); toggleVideo(video.id); }}
                              className="absolute top-2 left-2 z-10 bg-background/80 backdrop-blur rounded-md p-1.5 hover:bg-background transition-colors shadow-sm"
                            >
                              {selectedIds.has(video.id) ? <CheckSquare className="w-5 h-5 text-primary" /> : <Square className="w-5 h-5 text-muted-foreground" />}
                            </button>
                          </div>
                          <div className="p-5 flex flex-col">
                            <h3 className="font-bold text-[15px] leading-snug line-clamp-2 hover:text-primary transition-colors mb-2">
                              {video.title}
                            </h3>
                            <p className="text-[13px] text-muted-foreground font-medium">
                              {video.channelName} • {video.views}
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* Right Column: Captions (Natural scroll, hugging center) */}
                      <div className="flex flex-col w-full md:pl-6 lg:pl-12 mt-8 md:mt-0">
                        <div className="w-full max-w-2xl mr-auto flex flex-col gap-3">

                          {/* Sticky Show Less Banner (Only visible when expanded) */}
                          {expandedVideos[video.id] && (
                            <div className="sticky top-[80px] sm:top-[180px] z-20 bg-background/95 backdrop-blur-sm p-3 rounded-xl border shadow-sm mb-2 flex items-center justify-between">
                              <span className="text-sm font-semibold text-muted-foreground">Showing all {video.captions.length} captions</span>
                              <button
                                onClick={() => toggleExpand(video.id)}
                                className="px-4 py-1.5 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 font-bold text-sm transition-all"
                              >
                                Show Less
                              </button>
                            </div>
                          )}

                          {(expandedVideos[video.id] ? video.captions : video.captions.slice(0, 10)).map((cap) => (
                            <div key={cap.id} className="flex space-x-4 text-[14px] bg-muted/10 p-4 rounded-xl border border-transparent hover:border-border hover:bg-muted/30 transition-colors">
                              <a
                                href={`https://youtube.com/watch?v=${video.id}&t=${cap.seconds}s`}
                                target="_blank"
                                className="flex-shrink-0 text-primary font-bold flex flex-col items-start pt-0.5 hover:underline"
                              >
                                <span>{cap.timecode}</span>
                                {cap.score !== undefined && (
                                  <span className={`text-[11px] font-bold px-2 py-0.5 rounded mt-1 ${getBadgeClass(cap.score)}`}>
                                    {Math.round(cap.score * 100)}% Match
                                  </span>
                                )}
                              </a>
                              <p className="text-muted-foreground leading-relaxed text-[14px]">
                                {highlightText(cap.text, searchQuery, searchType)}
                              </p>
                            </div>
                          ))}

                          {/* Bottom Toggle Button */}
                          {video.captions.length > 10 && (
                            <button
                              onClick={() => toggleExpand(video.id)}
                              className="mt-2 w-full py-3 rounded-xl border-2 border-border/50 hover:border-primary/30 bg-muted/10 hover:bg-muted/30 font-bold text-sm transition-all text-muted-foreground hover:text-foreground shadow-sm"
                            >
                              {expandedVideos[video.id] ? "Show Less" : `Show ${video.captions.length - 10} More`}
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* List Loading Skeletons */}
                  {isLoading && (
                    <>
                      {[1, 2].map((i) => (
                        <div key={`list-skeleton-${i}`} className="grid grid-cols-1 md:grid-cols-2 py-16 border-b border-border/50 animate-pulse">
                          <div className="flex flex-col w-full md:pr-6 lg:pr-12">
                            <div className="w-full max-w-sm ml-auto bg-card border rounded-2xl overflow-hidden">
                              <div className="aspect-video bg-muted/60" />
                              <div className="p-5 flex flex-col gap-2">
                                <div className="h-4 bg-muted rounded w-3/4" />
                                <div className="h-3 bg-muted rounded w-1/2" />
                              </div>
                            </div>
                          </div>
                          <div className="flex flex-col w-full md:pl-6 lg:pl-12 mt-8 md:mt-0 gap-3">
                            <div className="w-full max-w-2xl mr-auto h-16 bg-muted/20 rounded-xl" />
                            <div className="w-full max-w-2xl mr-auto h-16 bg-muted/20 rounded-xl" />
                            <div className="w-full max-w-2xl mr-auto h-16 bg-muted/20 rounded-xl" />
                          </div>
                        </div>
                      ))}
                    </>
                  )}
                </div>
              )
            ) : (
              <div className="py-32 flex flex-col items-center justify-center text-center space-y-3">
                <Search className="w-12 h-12 text-muted-foreground/50" />
                <h3 className="text-xl font-bold">No matches found</h3>
                <p className="text-muted-foreground max-w-sm">We couldn't find any captions matching "{searchQuery}" in the loaded source. Try a different keyword.</p>
              </div>
            )}

            {/* Sticky Action Footer */}
            <div className={`fixed bottom-0 left-0 right-0 p-4 bg-background/95 backdrop-blur-md border-t shadow-[0_-20px_40px_rgba(0,0,0,0.05)] transition-transform duration-500 ease-out flex justify-center z-50 ${selectedIds.size > 0 ? "translate-y-0" : "translate-y-full"}`}>
              <div className="w-full px-4 sm:px-8 xl:px-12 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="flex items-center space-x-3">
                  <span className="flex items-center justify-center bg-primary text-primary-foreground font-bold text-lg w-8 h-8 rounded-full">{selectedIds.size}</span>
                  <span className="text-muted-foreground font-medium text-[15px]">videos selected for export</span>
                </div>
                <div className="flex items-center space-x-3 w-full sm:w-auto">
                  <div className="relative flex-1 sm:flex-none">
                    <select className="w-full appearance-none rounded-xl border-2 border-muted bg-transparent pl-4 pr-10 py-2.5 text-[15px] font-semibold focus:outline-none focus:border-primary transition-colors cursor-pointer">
                      <option value="srt">.SRT File</option>
                      <option value="vtt">.VTT File</option>
                      <option value="txt">.TXT File</option>
                    </select>
                    <ChevronDown className="absolute right-4 top-3.5 h-4 w-4 opacity-50 pointer-events-none" />
                  </div>
                  <button
                    onClick={handleExport}
                    disabled={isProcessing}
                    className="flex-1 sm:flex-none inline-flex items-center justify-center rounded-xl font-bold text-[15px] transition-colors bg-foreground text-background hover:bg-foreground/90 py-2.5 px-8 disabled:opacity-50 shadow-md cursor-pointer"
                  >
                    {isProcessing ? "Processing..." : "Download"}
                    {!isProcessing && <Download className="ml-2 h-4 w-4" />}
                  </button>
                </div>
              </div>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}

export default function UnifiedPipelinePage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading...</div>}>
      <SearchPageContent />
    </Suspense>
  );
}
