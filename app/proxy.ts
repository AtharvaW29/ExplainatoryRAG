import { NextRequest, NextResponse } from "next/server";
import { $SESSION_COOKIE } from "@/lib/constants";

const PROTECTED_PREFIXES = ["/dashboard"];

export default function proxy(req: NextRequest) {
    const token  = req.cookies.get($SESSION_COOKIE)?.value;
    const isProtected = PROTECTED_PREFIXES.some((prefix) =>
        req.nextUrl.pathname.startsWith(prefix)
    );
    if (isProtected && !token) {
        return NextResponse.redirect(new URL("/login", req.url));
    }
    return NextResponse.next();
}

export const config = {
    matcher: ["/dashboard/:path*"],
};
