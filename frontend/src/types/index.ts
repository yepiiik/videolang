export interface CaptionSnippet {
  id?: string;
  timecode?: string;
  seconds?: number;
  start?: number;
  end?: number;
  text: string;
}

export interface Video {
  id?: string; // used by mock data
  video_id?: string; // from real backend
  title: string;
  channelName?: string;
  thumbnailUrl?: string;
  views?: string;
  publishedAt?: string;
  captions?: CaptionSnippet[];
  chunks_count?: number;
  chunks?: any[]; // Full chunks returned when indexing
  fullCaptionText?: string;
}

export interface SearchResult {
  video_id: string;
  title: string;
  score: number;
  timestamp_score: number;
  start: number;
  end: number;
  text: string;
}


export interface PricingTier {
  name: string;
  tag: string;
  description: string;
  price: string;
  period?: string;
  ctaText: string;
  ctaVariant: "default" | "outline" | "accent";
  features: string[];
}

export interface ApiEndpoint {
  method: "GET" | "POST" | "PUT" | "DELETE";
  path: string;
  title: string;
  slug: string;
  description: string;
  parameters: {
    name: string;
    type: string;
    required: boolean;
    description: string;
  }[];
  sampleRequest: {
    headers?: Record<string, string>;
    body?: any;
  };
  sampleResponse: any;
}
