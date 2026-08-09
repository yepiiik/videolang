"use client";

import { useState, useMemo } from "react";
import { Search, Link as LinkIcon, CheckSquare, Square, Download, ChevronDown, Sparkles, Code2, ArrowRight, X, LayoutGrid, List as ListIcon } from "lucide-react";
import { MOCK_VIDEOS } from "@/lib/mock-data";
import Link from "next/link";

type SearchType = "intelligent" | "regex";

export default function UnifiedPipelinePage() {
  const [sourceType, setSourceType] = useState("channel");
  const [sourceUrl, setSourceUrl] = useState("");
  
  const [hasLoaded, setHasLoaded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const [searchQuery, setSearchQuery] = useState("");
  const [searchType, setSearchType] = useState<SearchType>("intelligent");
  
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [expandedVideos, setExpandedVideos] = useState<Record<string, boolean>>({});
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [isProcessing, setIsProcessing] = useState(false);

  const handleLoad = (e: React.FormEvent) => {
    e.preventDefault();
    if (!sourceUrl.trim()) {
      alert("Please enter a valid YouTube channel, playlist, or video URL.");
      return;
    }
    
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      setHasLoaded(true);
    }, 800);
  };

  const clearSource = () => {
    setHasLoaded(false);
    setSourceUrl("");
    setSearchQuery("");
    setSelectedIds(new Set());
  };

  const filteredResults = useMemo(() => {
    if (!hasLoaded) return [];
    
    const q = searchQuery.toLowerCase().trim();
    
    return MOCK_VIDEOS.map(video => {
      if (!q) return video; // Return full video if no query
      
      // Filter captions matching query
      const filteredCaptions = video.captions.filter(c => c.text.toLowerCase().includes(q));
      
      return {
        ...video,
        captions: filteredCaptions
      };
    }).filter(video => video.captions.length > 0); // Only keep videos with matching captions
  }, [hasLoaded, searchQuery]);

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
              <div className="flex flex-1 flex-col sm:flex-row bg-background border-2 border-border focus-within:border-primary focus-within:ring-4 focus-within:ring-primary/10 transition-all overflow-hidden rounded-xl shadow-sm w-full">
                
                <div className="relative flex-1 flex items-center">
                  <Search className="absolute left-3 w-4 h-4 text-muted-foreground" />
                  <input 
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Filter loaded transcripts by keyword or regex..."
                    className="w-full bg-transparent border-0 outline-none font-medium placeholder:text-muted-foreground/60 pl-9 pr-4 py-2.5 text-sm"
                  />
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
              </div>

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
                <div className="hidden sm:flex bg-muted/50 p-1 rounded-lg">
                  <button onClick={() => setViewMode("grid")} className={`p-1.5 rounded-md transition-all ${viewMode === "grid" ? "bg-background shadow-sm text-primary" : "text-muted-foreground hover:text-foreground"}`}>
                    <LayoutGrid className="w-4 h-4" />
                  </button>
                  <button onClick={() => setViewMode("list")} className={`p-1.5 rounded-md transition-all ${viewMode === "list" ? "bg-background shadow-sm text-primary" : "text-muted-foreground hover:text-foreground"}`}>
                    <ListIcon className="w-4 h-4" />
                  </button>
                </div>
                <div className="text-sm font-medium text-muted-foreground bg-muted px-3 py-1 rounded-full">
                  {filteredResults.length} videos match
                </div>
              </div>
            </div>

            {/* Video Grid / List */}
            {filteredResults.length > 0 ? (
              viewMode === "grid" ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-6">
                  {filteredResults.map((video) => (
                  <div key={video.id} className={`flex flex-col bg-card border rounded-2xl overflow-hidden hover:shadow-lg transition-all group relative ${selectedIds.has(video.id) ? 'border-primary ring-2 ring-primary/20' : 'hover:border-primary/40'}`}>
                    
                    {/* Checkbox Overlay */}
                    <button 
                      onClick={() => toggleVideo(video.id)} 
                      className="absolute top-2 left-2 z-10 bg-background/80 backdrop-blur rounded-md p-1 hover:bg-background transition-colors shadow-sm"
                    >
                      {selectedIds.has(video.id) ? <CheckSquare className="w-5 h-5 text-primary" /> : <Square className="w-5 h-5 text-muted-foreground" />}
                    </button>

                    <Link href={`https://youtube.com/watch?v=${video.id}`} target="_blank" className="relative aspect-video bg-muted border-b block shrink-0">
                      <img src={video.thumbnailUrl} alt={video.title} className="object-cover w-full h-full" />
                      <div className="absolute inset-0 bg-black/5 group-hover:bg-transparent transition-colors" />
                      <div className="absolute bottom-2 right-2 bg-black/80 text-white text-[11px] px-2 py-0.5 rounded-md font-medium tracking-wide">
                        12:45
                      </div>
                    </Link>
                    
                    <div className="p-4 flex flex-col flex-1 min-h-0">
                      <h3 className="font-bold text-[15px] leading-tight line-clamp-2 group-hover:text-primary transition-colors mb-2">
                        {video.title}
                      </h3>
                      <p className="text-[12px] text-muted-foreground font-medium mb-4">
                        {video.channelName} • {video.views}
                      </p>
                      
                      {/* Scrollable Transcriptions with Timecodes */}
                      <div className="flex flex-col gap-2 mt-auto h-36 overflow-y-auto pr-2 custom-scrollbar">
                        {video.captions.map((cap) => (
                          <div key={cap.id} className="flex space-x-3 text-[13px] bg-muted/30 p-2 rounded-lg border border-transparent hover:border-border hover:bg-muted/50 transition-colors">
                            <a 
                              href={`https://youtube.com/watch?v=${video.id}&t=${cap.seconds}s`} 
                              target="_blank" 
                              className="flex-shrink-0 text-primary font-semibold flex items-start space-x-1 pt-0.5 hover:underline"
                            >
                              <span>{cap.timecode}</span>
                            </a>
                            <p className="text-muted-foreground leading-relaxed">
                              {/* Highlight matching text if search query exists */}
                              {searchQuery ? (
                                <span>
                                  {cap.text.split(new RegExp(`(${searchQuery})`, 'gi')).map((part, i) => 
                                    part.toLowerCase() === searchQuery.toLowerCase() ? (
                                      <mark key={i} className="bg-primary/20 text-foreground font-semibold rounded-sm">{part}</mark>
                                    ) : part
                                  )}
                                </span>
                              ) : (
                                cap.text
                              )}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              ) : (
                <div className="flex flex-col">
                  {filteredResults.map((video) => (
                    <div key={video.id} id={`video-${video.id}`} className="grid grid-cols-1 md:grid-cols-2 py-16 border-b border-border/50 relative group scroll-mt-[100px]">
                      
                      {/* Left Column: Video Info (Sticky, hugging center) */}
                      <div className="flex flex-col w-full md:pr-6 lg:pr-12">
                        <div className={`w-full max-w-sm ml-auto sticky top-[180px] flex flex-col bg-card border rounded-2xl overflow-hidden transition-all shadow-sm ${selectedIds.has(video.id) ? 'border-primary ring-2 ring-primary/20' : 'hover:border-primary/40'}`}>
                          <Link href={`https://youtube.com/watch?v=${video.id}`} target="_blank" className="relative aspect-video bg-muted block shrink-0">
                            <img src={video.thumbnailUrl} alt={video.title} className="object-cover w-full h-full" />
                            <div className="absolute inset-0 bg-black/5 hover:bg-transparent transition-colors" />
                            <div className="absolute bottom-2 right-2 bg-black/80 text-white text-[11px] px-2 py-0.5 rounded-md font-medium tracking-wide">
                              12:45
                            </div>
                            {/* Checkbox Overlay */}
                            <button 
                              onClick={(e) => { e.preventDefault(); toggleVideo(video.id); }} 
                              className="absolute top-2 left-2 z-10 bg-background/80 backdrop-blur rounded-md p-1.5 hover:bg-background transition-colors shadow-sm"
                            >
                              {selectedIds.has(video.id) ? <CheckSquare className="w-5 h-5 text-primary" /> : <Square className="w-5 h-5 text-muted-foreground" />}
                            </button>
                          </Link>
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
                                className="flex-shrink-0 text-primary font-bold flex items-start space-x-1 pt-0.5 hover:underline"
                              >
                                <span>{cap.timecode}</span>
                              </a>
                              <p className="text-muted-foreground leading-relaxed text-[14px]">
                                {searchQuery ? (
                                  <span>
                                    {cap.text.split(new RegExp(`(${searchQuery})`, 'gi')).map((part, i) => 
                                      part.toLowerCase() === searchQuery.toLowerCase() ? (
                                        <mark key={i} className="bg-primary/20 text-foreground font-semibold rounded-sm px-1">{part}</mark>
                                      ) : part
                                    )}
                                  </span>
                                ) : (
                                  cap.text
                                )}
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
