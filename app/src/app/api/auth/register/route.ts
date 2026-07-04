import { NextResponse, NextRequest } from "next/server";
import { $API_URL } from "@/lib/constants";

export async function POST(req: NextRequest) {
    const body = await req.json();

    const fastApiRes = await fetch(`${$API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    const data = await fastApiRes.json();
    return NextResponse.json(data, { status: fastApiRes.status });
}
