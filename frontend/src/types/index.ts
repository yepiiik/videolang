export interface CaptionSnippet {
  id: string;
  timecode: string;
  seconds: number;
  text: string;
}

export interface Video {
  id: string;
  title: string;
  channelName: string;
  thumbnailUrl: string;
  views: string;
  publishedAt: string;
  captions: CaptionSnippet[];
  fullCaptionText?: string;
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
