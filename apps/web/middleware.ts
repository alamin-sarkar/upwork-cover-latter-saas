import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { sessionCookieNames } from "./src/lib/auth";

const protectedRoutes = ["/dashboard", "/generator", "/history", "/knowledge", "/settings"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSession =
    request.cookies.has(sessionCookieNames.access) ||
    request.cookies.has(sessionCookieNames.refresh);

  const isProtected = protectedRoutes.some((route) => pathname.startsWith(route));

  if (isProtected && !hasSession) {
    return NextResponse.redirect(new URL("/auth", request.url));
  }

  if (pathname === "/auth" && hasSession) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/auth", "/dashboard/:path*", "/generator/:path*", "/history/:path*", "/knowledge/:path*", "/settings/:path*"],
};
