import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { video_id, title } = body;

    if (!video_id || !title) {
      return NextResponse.json({ error: "Missing video_id or title parameter" }, { status: 400 });
    }

    const backendUrl = process.env.BACKEND_API_URL || "http://127.0.0.1:8000";
    const apiKey = process.env.BACKEND_API_KEY || "free_tier_api_key";

    const response = await fetch(`${backendUrl}/youtube/index/video`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": apiKey
      },
      body: JSON.stringify({ video_id, title })
    });

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json({ error: "Backend failed to process", details: errorText }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error("Index Video API error:", error);
    return NextResponse.json({ error: "Internal server error", details: error.message }, { status: 500 });
  }
}
