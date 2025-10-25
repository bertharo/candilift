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
    <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">Upload Your Resume & Job Description</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Resume Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Resume File (PDF or DOCX)
          </label>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
              isDragActive ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getInputProps()} />
            {resumeFile ? (
              <div className="text-green-600">
                <p className="font-medium">✓ {resumeFile.name}</p>
                <p className="text-sm text-gray-500">Click to change file</p>
              </div>
            ) : (
              <div>
                <p className="text-gray-600">
                  {isDragActive ? 'Drop the file here' : 'Drag & drop your resume here, or click to select'}
                </p>
                <p className="text-sm text-gray-500 mt-2">Supports PDF and DOCX files</p>
              </div>
            )}
          </div>
        </div>

        {/* Job Description Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Job Description
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
            className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Job URL Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Or Job Posting URL
          </label>
          <input
            type="url"
            value={jobUrl}
            onChange={(e) => setJobUrl(e.target.value)}
            placeholder="https://example.com/job-posting"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* ATS Platform Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            ATS Platform
          </label>
          <select
            value={atsPlatform}
            onChange={(e) => setAtsPlatform(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="generic">Generic ATS</option>
            <option value="workday">Workday</option>
            <option value="greenhouse">Greenhouse</option>
            <option value="lever">Lever</option>
            <option value="bamboohr">BambooHR</option>
            <option value="icims">iCIMS</option>
          </select>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading || !resumeFile || (!jobDescription && !jobUrl)}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-md font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Analyzing...' : 'Analyze Resume'}
        </button>
      </form>
    </div>
  )
}
