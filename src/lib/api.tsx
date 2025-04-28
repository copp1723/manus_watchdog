'use client'
import { createContext, useContext, useState, ReactNode } from 'react'

interface ApiContextType {
  baseUrl: string
  isLoading: boolean
  error: string | null
  setIsLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

const ApiContext = createContext<ApiContextType | undefined>(undefined)

export function ApiProvider({ children }: { children: ReactNode }) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // In production, this would be configured based on environment
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  
  return (
    <ApiContext.Provider value={{ 
      baseUrl, 
      isLoading, 
      error, 
      setIsLoading, 
      setError 
    }}>
      {children}
    </ApiContext.Provider>
  )
}

export function useApi() {
  const context = useContext(ApiContext)
  if (context === undefined) {
    throw new Error('useApi must be used within an ApiProvider')
  }
  return context
}

export async function uploadFile(file: File): Promise<{ upload_id: string, filename: string }> {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await fetch('/api/upload', {
    method: 'POST',
    body: formData,
  })
  
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Upload failed')
  }
  
  return await response.json()
}

export async function analyzeData(uploadId: string, intent: string = 'general_analysis') {
  const response = await fetch(`/api/analyze/${uploadId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ intent }),
  })
  
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Analysis failed')
  }
  
  return await response.json()
}

export async function askQuestion(uploadId: string, question: string) {
  const response = await fetch(`/api/question/${uploadId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question }),
  })
  
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Question processing failed')
  }
  
  return await response.json()
}
