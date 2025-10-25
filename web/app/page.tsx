'use client'

import { useState } from 'react'
import FileUpload from '../components/FileUpload'
import AnalysisResults from '../components/AnalysisResults'

export default function Home() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleAnalysis = async (formData: FormData) => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      setAnalysisResult(result)
    } catch (error) {
      console.error('Analysis failed:', error)
      alert('Analysis failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">CandiLift</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload your resume and job description to get AI-powered analysis and optimization recommendations
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <FileUpload 
            onAnalysis={handleAnalysis} 
            isLoading={isLoading}
          />
          
          {analysisResult && (
            <AnalysisResults result={analysisResult} />
          )}
        </div>
      </div>
    </main>
  )
}
