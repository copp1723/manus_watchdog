'use client'
import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { SendIcon, Loader2 } from 'lucide-react'

interface ChatProps {
  onSendQuestion: (question: string) => void
  isLoading: boolean
  disabled?: boolean
}

export function Chat({ onSendQuestion, isLoading, disabled = false }: ChatProps) {
  const [question, setQuestion] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!question.trim() || isLoading || disabled) return
    
    onSendQuestion(question)
    setQuestion('')
    
    // Focus the input after sending
    setTimeout(() => {
      inputRef.current?.focus()
    }, 0)
  }

  return (
    <div className="space-y-4">
      <h2 className="font-medium text-lg">Ask a Question</h2>
      
      <p className="text-sm text-gray-600">
        Ask any question about your dealership data to get insights.
      </p>
      
      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <Input
          ref={inputRef}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g., Who is my top sales rep?"
          disabled={isLoading || disabled}
          className="flex-1"
        />
        
        <Button 
          type="submit" 
          size="icon"
          disabled={!question.trim() || isLoading || disabled}
        >
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <SendIcon className="h-4 w-4" />
          )}
        </Button>
      </form>
      
      <div className="text-xs text-gray-500">
        Try questions like:
        <ul className="mt-1 space-y-1">
          <li>• What was my total profit last month?</li>
          <li>• Who is my top performing sales rep?</li>
          <li>• Which lead source is most profitable?</li>
          <li>• What's my best selling vehicle?</li>
        </ul>
      </div>
    </div>
  )
}
