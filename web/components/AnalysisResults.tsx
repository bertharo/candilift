'use client'

import { useState } from 'react'

interface AnalysisResultsProps {
  result: any
  onDownloadReport?: () => void
  onGenerateResume?: () => void
}

export default function AnalysisResults({ result, onDownloadReport, onGenerateResume }: AnalysisResultsProps) {
  const [isDownloadingReport, setIsDownloadingReport] = useState(false)
  const [isGeneratingResume, setIsGeneratingResume] = useState(false)

  if (!result) return null

  const handleDownloadReport = async () => {
    if (onDownloadReport) {
      setIsDownloadingReport(true)
      try {
        await onDownloadReport()
      } finally {
        setIsDownloadingReport(false)
      }
    }
  }

  const handleGenerateResume = async () => {
    if (onGenerateResume) {
      setIsGeneratingResume(true)
      try {
        await onGenerateResume()
      } finally {
        setIsGeneratingResume(false)
      }
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50'
    if (score >= 60) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  const getScoreIcon = (score: number) => {
    if (score >= 80) return '🎯'
    if (score >= 60) return '⚠️'
    return '🔴'
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-3">Analysis Complete</h2>
        <p className="text-lg text-gray-600">Here's how your resume performs</p>
      </div>

      {/* Overall Scores */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">ATS Score</h3>
                <p className="text-sm text-gray-600">System compatibility</p>
              </div>
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(result.ats_score || 0)}`}>
              {result.ats_score || 'N/A'}%
            </div>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${result.ats_score || 0}%` }}
            ></div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Recruiter Score</h3>
                <p className="text-sm text-gray-600">Human appeal</p>
              </div>
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(result.recruiter_score || 0)}`}>
              {result.recruiter_score || 'N/A'}%
            </div>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-green-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${result.recruiter_score || 0}%` }}
            ></div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Likelihood Score</h3>
                <p className="text-sm text-gray-600">Chance of hearing back</p>
              </div>
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(result.likelihood_score || 0)}`}>
              {result.likelihood_score || 'N/A'}%
            </div>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-purple-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${result.likelihood_score || 0}%` }}
            ></div>
          </div>
          {result.likelihood_explanation && (
            <div className="mt-3 p-3 bg-purple-50 rounded-lg">
              <p className="text-sm text-purple-700 mb-2">{result.likelihood_explanation}</p>
              
              {/* Domain Fit Assessment */}
              {result.domain_fit && (
                <div className="mb-3 p-2 bg-white rounded border border-purple-200">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-xs font-medium text-purple-600">Domain Fit:</span>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      result.domain_fit.fit_level === 'good' ? 'bg-green-100 text-green-700' :
                      result.domain_fit.fit_level === 'moderate' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {result.domain_fit.fit_level === 'good' ? '✓ Good' :
                       result.domain_fit.fit_level === 'moderate' ? '⚠ Moderate' :
                       '✗ Poor'}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600">{result.domain_fit.description}</p>
                </div>
              )}
              
              {/* Improvement Suggestions */}
              {result.likelihood_improvements && result.likelihood_improvements.length > 0 && (
                <div className="space-y-2">
                  <p className="text-xs font-medium text-purple-600 mb-2">Quick Wins to Improve Your Chances:</p>
                  {result.likelihood_improvements.slice(0, 3).map((improvement: any, index: number) => (
                    <div key={index} className="text-xs bg-white p-2 rounded border border-purple-200">
                      <div className="font-medium text-gray-800 mb-1">{improvement.category}</div>
                      <div className="text-gray-600 mb-1">{improvement.suggestion}</div>
                      <div className="text-purple-600">{improvement.impact}</div>
                    </div>
                  ))}
                </div>
              )}
              
              <div className="text-xs text-purple-600 bg-purple-100 p-2 rounded mt-2">
                <strong>Reality Check:</strong> Most job postings receive 100-500+ applications. Only 2-5% typically get any response.
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Score Breakdown */}
      {result.score_drivers && (
        <div className="card p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-6">Score Breakdown</h3>
          <div className="space-y-4">
            {result.score_drivers.map((driver: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-lg">{getScoreIcon(driver.score)}</span>
                    <h4 className="font-medium text-gray-900">{driver.component}</h4>
                  </div>
                  <p className="text-sm text-gray-600">{driver.explanation}</p>
                </div>
                <div className="ml-4">
                  <div className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(driver.score)}`}>
                    {driver.score}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {result.recommendations && (
        <div className="card p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-6">Recommendations</h3>
          <div className="space-y-4">
            {result.recommendations.map((rec: any, index: number) => (
              <div key={index} className="border border-yellow-200 bg-yellow-50 rounded-lg p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                      <svg className="w-4 h-4 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <h4 className="font-medium text-yellow-800">{rec.category}</h4>
                  </div>
                  <div className="px-2 py-1 bg-yellow-200 text-yellow-800 text-xs font-medium rounded-full">
                    +{rec.estimated_lift}% improvement
                  </div>
                </div>
                <p className="text-sm text-yellow-700 mb-3">{rec.description}</p>
                {rec.example && (
                  <div className="bg-white p-3 rounded border border-yellow-200">
                    <p className="text-xs text-gray-600 mb-1 font-medium">Example:</p>
                    <p className="text-sm text-gray-800">{rec.example}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Gap Analysis */}
      {result.gap_analysis && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Missing Skills</h3>
            </div>
            <div className="space-y-2">
              {result.gap_analysis.missing_skills?.map((skill: string, index: number) => (
                <div key={index} className="flex items-center space-x-2 text-sm text-red-600">
                  <span className="w-1.5 h-1.5 bg-red-400 rounded-full"></span>
                  <span>{skill}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Present Skills</h3>
            </div>
            <div className="space-y-2">
              {result.gap_analysis.present_skills?.map((skill: string, index: number) => (
                <div key={index} className="flex items-center space-x-2 text-sm text-green-600">
                  <span className="w-1.5 h-1.5 bg-green-400 rounded-full"></span>
                  <span>{skill}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 pt-6">
        <button 
          onClick={handleDownloadReport}
          disabled={isDownloadingReport}
          className="btn-primary flex-1 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isDownloadingReport ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Generating Report...</span>
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>Download Report</span>
            </>
          )}
        </button>
        <button 
          onClick={handleGenerateResume}
          disabled={isGeneratingResume}
          className="btn-secondary flex-1 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isGeneratingResume ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Generating Resume...</span>
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              <span>Generate Resume</span>
            </>
          )}
        </button>
      </div>
    </div>
  )
}
