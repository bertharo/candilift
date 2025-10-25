'use client'

interface AnalysisResultsProps {
  result: any
}

export default function AnalysisResults({ result }: AnalysisResultsProps) {
  if (!result) return null

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
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
        <button className="btn-primary flex-1 flex items-center justify-center space-x-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>Download Report</span>
        </button>
        <button className="btn-secondary flex-1 flex items-center justify-center space-x-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          <span>Generate Resume</span>
        </button>
      </div>
    </div>
  )
}
