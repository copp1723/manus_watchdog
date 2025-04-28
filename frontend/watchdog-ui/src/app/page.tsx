'use client'
import { useState } from 'react'
import { Upload } from '@/components/Upload'
import { Chat } from '@/components/Chat'
import { InsightCard } from '@/components/InsightCard'
import { Header } from '@/components/Header'
import { Footer } from '@/components/Footer'

export default function Home() {
  const [uploadId, setUploadId] = useState<string | null>(null)
  const [fileName, setFileName] = useState<string | null>(null)
  const [insights, setInsights] = useState<any[]>([])
  const [chartUrl, setChartUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleUploadSuccess = (id: string, name: string) => {
    setUploadId(id)
    setFileName(name)
    // Trigger initial analysis
    handleAnalysis(id)
  }

  const handleAnalysis = async (id: string) => {
    setIsLoading(true)
    try {
      const response = await fetch(`/api/analyze/${id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ intent: 'general_analysis' }),
      })
      
      if (!response.ok) {
        throw new Error('Analysis failed')
      }
      
      const data = await response.json()
      setInsights(data.insights || [])
      setChartUrl(data.chart_url || null)
    } catch (error) {
      console.error('Error analyzing data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleQuestion = async (question: string) => {
    if (!uploadId) return
    
    setIsLoading(true)
    try {
      const response = await fetch(`/api/question/${uploadId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })
      
      if (!response.ok) {
        throw new Error('Question processing failed')
      }
      
      const data = await response.json()
      setInsights(data.insights || [])
      setChartUrl(data.chart_url || null)
    } catch (error) {
      console.error('Error processing question:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen flex-col">
      <Header />
      
      <div className="flex-1 container mx-auto px-4 py-8">
        {!uploadId ? (
          <div className="max-w-3xl mx-auto">
            <h1 className="text-3xl font-bold text-center mb-8">
              Upload your dealership data to get started
            </h1>
            <Upload onUploadSuccess={handleUploadSuccess} />
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-8 space-y-6">
              {insights.map((insight, index) => (
                <InsightCard 
                  key={index}
                  title={insight.title}
                  description={insight.description}
                  employee={insight.employee}
                  employeeTitle={insight.employeeTitle}
                  amount={insight.amount}
                  percentage={insight.percentage}
                  actionItems={insight.actionItems}
                />
              ))}
              
              {chartUrl && (
                <div className="bg-white rounded-lg shadow-md p-4 overflow-hidden">
                  <img 
                    src={chartUrl} 
                    alt="Data visualization" 
                    className="w-full h-auto"
                  />
                </div>
              )}
            </div>
            
            <div className="lg:col-span-4">
              <div className="bg-white rounded-lg shadow-md p-4 sticky top-4">
                <div className="mb-4">
                  <h2 className="font-medium text-lg">Current File</h2>
                  <p className="text-sm text-gray-600">{fileName}</p>
                </div>
                
                <Chat 
                  onSendQuestion={handleQuestion} 
                  isLoading={isLoading}
                  disabled={!uploadId}
                />
              </div>
            </div>
          </div>
        )}
      </div>
      
      <Footer />
    </main>
  )
}
