// middleware.ts
import { NextResponse } from "next/server";//helper class to create HTTP responses representing what i want to send forward to continue the request
import type { NextRequest } from "next/server"; //object representing incoming http request

// Protected routes
const protectedRoutes = ["/home", "/applied-jobs"];

export async function middleware(req: NextRequest) {
  const url = req.nextUrl.clone();
  const path = url.pathname;

  // Only check authentication for protected routes
  if (protectedRoutes.includes(path)) {
    const accessToken = req.cookies.get("access_token")?.value;

    // If no token, redirect to login
    if (!accessToken) {
      url.pathname = "/login";
      return NextResponse.redirect(url);
    }
    
    try {
      const res = await fetch("http://localhost:8000/auth/validate-token", {
        method: "POST",
        headers: {
          Cookie: `access_token=${accessToken}`,
        },
      });

      if (!res.ok) {
        url.pathname = "/login";
        return NextResponse.redirect(url);
      }
    } catch (err) {
      url.pathname = "/login";
      return NextResponse.redirect(url);
    }
  }

  // Not a protected route → continue
  return NextResponse.next();
}

// Apply middleware to all routes except Next.js internals
export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
