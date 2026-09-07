import { NextResponse } from "next/server";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const query = searchParams.get("query");

    if (!query) {
      return NextResponse.json({ error: "Missing query parameter" }, { status: 400 });
    }

    const backendUrl = process.env.BACKEND_API_URL || "http://127.0.0.1:8000";
    const apiKey = process.env.BACKEND_API_KEY || "free_tier_api_key";

    const response = await fetch(`${backendUrl}/youtube/channel/videos?query=${encodeURIComponent(query)}`, {
      headers: {
        "X-API-Key": apiKey
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json({ error: "Backend failed to process", details: errorText }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error("Channel Videos API error:", error);
    return NextResponse.json({ error: "Internal server error", details: error.message }, { status: 500 });
  }
}
