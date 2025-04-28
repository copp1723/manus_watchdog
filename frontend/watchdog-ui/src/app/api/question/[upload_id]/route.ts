// This file contains API route handlers for the question endpoint
// It acts as a proxy between the frontend and the backend API

import { NextRequest, NextResponse } from 'next/server'

// Backend API URL
const API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000/v1'

// Question handler
export async function POST(
  request: NextRequest,
  { params }: { params: { upload_id: string } }
) {
  try {
    const uploadId = params.upload_id
    const body = await request.json()
    
    // Forward the request to the backend API
    const response = await fetch(`${API_URL}/question/${uploadId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
    
    // Get the response data
    const data = await response.json()
    
    // Return the response
    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('Error in question API route:', error)
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    )
  }
}
