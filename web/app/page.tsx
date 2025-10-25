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
      // Use your Render backend URL
      const API_BASE_URL = process.env.NODE_ENV === 'production' 
        ? 'https://rats-h0z1.onrender.com' 
        : 'http://localhost:8000'
      
      const response = await fetch(`${API_BASE_URL}/analyze`, {
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
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-600/5 via-purple-600/5 to-pink-600/5"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-24">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-indigo-100 text-indigo-800 text-sm font-medium mb-8">
              <span className="w-2 h-2 bg-indigo-600 rounded-full mr-2 animate-pulse"></span>
              AI-Powered Resume Analysis
            </div>
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Optimize your resume for
              <span className="block bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                better success
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              Get AI-powered analysis, gap identification, and tailored recommendations to make your resume stand out to recruiters and ATS systems.
            </p>

            {/* Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 mb-16 max-w-2xl mx-auto">
              <div className="text-center">
                <div className="text-3xl font-bold text-indigo-600 mb-2">95%</div>
                <div className="text-sm text-gray-600">ATS Compatibility</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">7x</div>
                <div className="text-sm text-gray-600">Faster Analysis</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-pink-600 mb-2">24/7</div>
                <div className="text-sm text-gray-600">Available</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <FileUpload 
          onAnalysis={handleAnalysis} 
          isLoading={isLoading}
        />
        
        {analysisResult && (
          <AnalysisResults result={analysisResult} />
        )}
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900 mb-2">CandiLift</div>
            <p className="text-gray-600 mb-4">Built with ❤️ for better candidate success</p>
            <div className="flex justify-center space-x-6 text-sm text-gray-500">
              <a href="#" className="hover:text-gray-900">Privacy</a>
              <a href="#" className="hover:text-gray-900">Terms</a>
              <a href="#" className="hover:text-gray-900">Support</a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
