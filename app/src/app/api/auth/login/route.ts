import { NextRequest, NextResponse } from "next/server";
import { $SESSION_COOKIE, buildApiUrl } from "@/lib/constants";

export async function POST(req: NextRequest) {
    const body = await req.json();

    const response = await fetch(buildApiUrl("/auth/login"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({})); // swallow JSON parsing errors
        return NextResponse.json(
            { error: error.message || "Login failed" },
            { status: response.status }
        );
    }

    const { access_token: accessToken } = await response.json();

    const res = NextResponse.json({ message: "Logged in" });
    res.cookies.set($SESSION_COOKIE, accessToken, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        path: "/",
        maxAge: 60 * 60 * 24,
    });

    return res;
}
