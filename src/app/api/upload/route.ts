// This file contains API route handlers for the Next.js frontend
// It acts as a proxy between the frontend and the backend API

import { NextRequest, NextResponse } from 'next/server'

// Backend API URL
const API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000/v1'

// Upload file handler
export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    
    // Forward the request to the backend API
    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      body: formData,
    })
    
    // Get the response data
    const data = await response.json()
    
    // Return the response
    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('Error in upload API route:', error)
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    )
  }
}
