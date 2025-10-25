'use client'

interface AnalysisResultsProps {
  result: any
}

export default function AnalysisResults({ result }: AnalysisResultsProps) {
  if (!result) return null

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6">Analysis Results</h2>
      
      {/* Overall Scores */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-blue-900 mb-2">ATS Score</h3>
          <div className="text-3xl font-bold text-blue-600">
            {result.ats_score || 'N/A'}%
          </div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-green-900 mb-2">Recruiter Score</h3>
          <div className="text-3xl font-bold text-green-600">
            {result.recruiter_score || 'N/A'}%
          </div>
        </div>
      </div>

      {/* Score Drivers */}
      {result.score_drivers && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Score Breakdown</h3>
          <div className="space-y-4">
            {result.score_drivers.map((driver: any, index: number) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-medium text-gray-900">{driver.component}</h4>
                  <span className="text-sm font-medium text-gray-600">{driver.score}%</span>
                </div>
                <p className="text-sm text-gray-600">{driver.explanation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {result.recommendations && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Recommendations</h3>
          <div className="space-y-3">
            {result.recommendations.map((rec: any, index: number) => (
              <div key={index} className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-medium text-yellow-800">{rec.category}</h4>
                  <span className="text-sm font-medium text-yellow-600">
                    +{rec.estimated_lift}% improvement
                  </span>
                </div>
                <p className="text-sm text-yellow-700 mb-2">{rec.description}</p>
                {rec.example && (
                  <div className="bg-white p-3 rounded border">
                    <p className="text-xs text-gray-600 mb-1">Example:</p>
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
        <div>
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Gap Analysis</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Missing Skills</h4>
              <ul className="space-y-1">
                {result.gap_analysis.missing_skills?.map((skill: string, index: number) => (
                  <li key={index} className="text-sm text-red-600">• {skill}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Present Skills</h4>
              <ul className="space-y-1">
                {result.gap_analysis.present_skills?.map((skill: string, index: number) => (
                  <li key={index} className="text-sm text-green-600">• {skill}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
