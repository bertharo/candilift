'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

interface FileUploadProps {
  onAnalysis: (formData: FormData) => Promise<void>
  isLoading: boolean
}

export default function FileUpload({ onAnalysis, isLoading }: FileUploadProps) {
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [jobUrl, setJobUrl] = useState('')
  const [atsPlatform, setAtsPlatform] = useState('generic')
  const [activeTab, setActiveTab] = useState<'description' | 'url'>('description')

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      setResumeFile(file)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    multiple: false,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!resumeFile) {
      alert('Please upload a resume file')
      return
    }

    if (!jobDescription && !jobUrl) {
      alert('Please provide either a job description or job URL')
      return
    }

    const formData = new FormData()
    formData.append('resume_file', resumeFile)
    
    if (jobDescription) {
      formData.append('job_description', jobDescription)
    }
    
    if (jobUrl) {
      formData.append('job_url', jobUrl)
    }
    
    formData.append('ats_platform', atsPlatform)

    await onAnalysis(formData)
  }

  return (
    <div className="card-elevated p-8 mb-8">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-3">Get Started</h2>
        <p className="text-lg text-gray-600">Upload your resume and job details for AI-powered analysis</p>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Resume Upload Section */}
        <div className="space-y-4">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Resume File
          </label>
          <div
            {...getRootProps()}
            className={`relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200 ${
              isDragActive 
                ? 'border-indigo-400 bg-indigo-50 scale-[1.02]' 
                : resumeFile 
                  ? 'border-green-400 bg-green-50' 
                  : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
            }`}
          >
            <input {...getInputProps()} />
            <div className="space-y-4">
              {resumeFile ? (
                <div className="space-y-2">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                    <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div className="text-green-700 font-medium">{resumeFile.name}</div>
                  <p className="text-sm text-green-600">Click to change file</p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto">
                    <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-lg font-medium text-gray-900 mb-2">
                      {isDragActive ? 'Drop your resume here' : 'Upload your resume'}
                    </p>
                    <p className="text-sm text-gray-600">Supports PDF and DOCX files up to 10MB</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Job Details Section */}
        <div className="space-y-6">
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Job Details
          </label>
          
          {/* Tab Navigation */}
          <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
            <button
              type="button"
              onClick={() => setActiveTab('description')}
              className={`flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all duration-200 ${
                activeTab === 'description'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Job Description
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('url')}
              className={`flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all duration-200 ${
                activeTab === 'url'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Job URL
            </button>
          </div>

          {/* Tab Content */}
          {activeTab === 'description' ? (
            <div className="space-y-4">
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                className="w-full h-40 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              />
              <p className="text-sm text-gray-500">Copy and paste the complete job description for best results</p>
            </div>
          ) : (
            <div className="space-y-4">
              <input
                type="url"
                value={jobUrl}
                onChange={(e) => setJobUrl(e.target.value)}
                placeholder="https://example.com/job-posting"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
              <p className="text-sm text-gray-500">We'll automatically extract the job details from the URL</p>
            </div>
          )}
        </div>

        {/* ATS Platform Selection */}
        <div className="space-y-4">
          <label className="block text-sm font-semibold text-gray-900">
            Target ATS Platform
          </label>
          <select
            value={atsPlatform}
            onChange={(e) => setAtsPlatform(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white"
          >
            <option value="generic">Generic ATS</option>
            <option value="workday">Workday</option>
            <option value="greenhouse">Greenhouse</option>
            <option value="lever">Lever</option>
            <option value="bamboohr">BambooHR</option>
            <option value="icims">iCIMS</option>
          </select>
          <p className="text-sm text-gray-500">Select the ATS platform you're targeting for optimized recommendations</p>
        </div>

        {/* Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={isLoading || !resumeFile || (!jobDescription && !jobUrl)}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span>Analyze Resume</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  )
}
