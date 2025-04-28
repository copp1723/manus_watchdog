// This file contains middleware configuration for the Next.js application
// It handles CORS and other request preprocessing

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Middleware function that runs before any request is processed
export function middleware(request: NextRequest) {
  // Get response
  const response = NextResponse.next()
  
  // Add CORS headers
  response.headers.set('Access-Control-Allow-Origin', '*')
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  
  return response
}

// Configure middleware to run on API routes
export const config = {
  matcher: '/api/:path*',
}
