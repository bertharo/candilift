import React, { useState } from 'react';
import { 
  CheckCircle, 
  AlertCircle, 
  Info, 
  TrendingUp, 
  TrendingDown,
  Star,
  Target,
  FileText,
  Users,
  Calendar,
  ArrowRight,
  Copy,
  Download
} from 'lucide-react';

const AnalysisResults = ({ result }) => {
  const [activeTab, setActiveTab] = useState('overview');

  const getScoreColor = (score) => {
    if (score >= 85) return 'score-excellent';
    if (score >= 70) return 'score-good';
    if (score >= 55) return 'score-fair';
    return 'score-poor';
  };

  const getScoreIcon = (score) => {
    if (score >= 85) return <Star className="h-5 w-5" />;
    if (score >= 70) return <TrendingUp className="h-5 w-5" />;
    if (score >= 55) return <Info className="h-5 w-5" />;
    return <TrendingDown className="h-5 w-5" />;
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'text-error-600 bg-error-50 border-error-200';
      case 'major': return 'text-warning-600 bg-warning-50 border-warning-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'keyword': return <Target className="h-4 w-4" />;
      case 'formatting': return <FileText className="h-4 w-4" />;
      case 'impact': return <TrendingUp className="h-4 w-4" />;
      case 'structure': return <Users className="h-4 w-4" />;
      default: return <Info className="h-4 w-4" />;
    }
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: <Target className="h-4 w-4" /> },
    { id: 'keywords', label: 'Keywords', icon: <Target className="h-4 w-4" /> },
    { id: 'formatting', label: 'Formatting', icon: <FileText className="h-4 w-4" /> },
    { id: 'impact', label: 'Impact', icon: <TrendingUp className="h-4 w-4" /> },
    { id: 'recommendations', label: 'Recommendations', icon: <AlertCircle className="h-4 w-4" /> }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Analysis Results</h2>
            <p className="text-gray-600">Resume: {result.resume_filename}</p>
            <p className="text-sm text-gray-500">
              Analyzed on {new Date(result.analysis_timestamp).toLocaleDateString()}
            </p>
          </div>
          <div className="flex space-x-2">
            <button className="btn-secondary">
              <Download className="h-4 w-4 mr-2" />
              Export
            </button>
            <button className="btn-secondary">
              <Copy className="h-4 w-4 mr-2" />
              Copy Report
            </button>
          </div>
        </div>

        {/* Score Cards */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className={`card border-2 ${getScoreColor(result.ats_score)}`}>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-lg font-semibold">ATS Score</h3>
              {getScoreIcon(result.ats_score)}
            </div>
            <div className="text-3xl font-bold mb-2">{result.ats_score.toFixed(0)}/100</div>
            <p className="text-sm mb-2">
              Measures compatibility with Applicant Tracking Systems
            </p>
            {result.ats_platform && (
              <div className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">
                Simulated on: {result.ats_platform}
                {result.processing_time && ` • ${result.processing_time.toFixed(1)}s`}
              </div>
            )}
          </div>

          <div className={`card border-2 ${getScoreColor(result.recruiter_score)}`}>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-lg font-semibold">Recruiter Score</h3>
              {getScoreIcon(result.recruiter_score)}
            </div>
            <div className="text-3xl font-bold mb-2">{result.recruiter_score.toFixed(0)}/100</div>
            <p className="text-sm">
              Measures appeal to human recruiters and hiring managers
            </p>
          </div>
        </div>

        {/* ATS Platform Info */}
        {result.ats_platform && (
          <div className="card bg-blue-50 border-blue-200">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 text-sm font-bold">ATS</span>
                </div>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">
                  ATS Platform: {result.ats_platform}
                </h3>
                <p className="text-sm text-blue-700 mt-1">
                  Your resume was analyzed using {result.ats_platform} simulation with realistic parsing rules and scoring algorithms.
                </p>
                {result.ats_quirks && result.ats_quirks.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs font-medium text-blue-800 mb-1">Platform-specific insights:</p>
                    <ul className="text-xs text-blue-700 space-y-1">
                      {result.ats_quirks.map((quirk, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-blue-500 mr-1">•</span>
                          <span>{quirk}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="card">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.icon}
                <span className="ml-2">{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="mt-6">
          {activeTab === 'overview' && (
            <OverviewTab 
              result={result} 
              getScoreColor={getScoreColor}
              getSeverityColor={getSeverityColor}
            />
          )}
          {activeTab === 'keywords' && (
            <KeywordsTab result={result} />
          )}
          {activeTab === 'formatting' && (
            <FormattingTab result={result} />
          )}
          {activeTab === 'impact' && (
            <ImpactTab result={result} />
          )}
          {activeTab === 'recommendations' && (
            <RecommendationsTab 
              result={result} 
              getSeverityColor={getSeverityColor}
              getCategoryIcon={getCategoryIcon}
            />
          )}
        </div>
      </div>
    </div>
  );
};

// Overview Tab Component
const OverviewTab = ({ result, getScoreColor, getSeverityColor }) => {
  const criticalIssues = result.recommendations.filter(r => r.severity === 'critical').length;
  const majorIssues = result.recommendations.filter(r => r.severity === 'major').length;
  const totalIssues = result.recommendations.length;

  return (
    <div className="space-y-6">
      {/* Quick Stats */}
      <div className="grid md:grid-cols-3 gap-4">
        <div className="text-center p-4 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-gray-900">{result.keyword_analysis.coverage_score.toFixed(0)}%</div>
          <div className="text-sm text-gray-600">Keyword Coverage</div>
        </div>
        <div className="text-center p-4 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-gray-900">{result.formatting_analysis.ats_compatibility_score.toFixed(0)}%</div>
          <div className="text-sm text-gray-600">ATS Compatibility</div>
        </div>
        <div className="text-center p-4 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-gray-900">{result.impact_analysis.impact_score.toFixed(0)}%</div>
          <div className="text-sm text-gray-600">Impact Score</div>
        </div>
      </div>

      {/* Issues Summary */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="font-semibold mb-3">Issues Summary</h3>
        <div className="space-y-2">
          {criticalIssues > 0 && (
            <div className="flex items-center text-error-600">
              <AlertCircle className="h-4 w-4 mr-2" />
              <span>{criticalIssues} critical issues need immediate attention</span>
            </div>
          )}
          {majorIssues > 0 && (
            <div className="flex items-center text-warning-600">
              <AlertCircle className="h-4 w-4 mr-2" />
              <span>{majorIssues} major improvements recommended</span>
            </div>
          )}
          {totalIssues - criticalIssues - majorIssues > 0 && (
            <div className="flex items-center text-gray-600">
              <Info className="h-4 w-4 mr-2" />
              <span>{totalIssues - criticalIssues - majorIssues} minor optimizations available</span>
            </div>
          )}
        </div>
      </div>

      {/* Top Recommendations */}
      <div>
        <h3 className="font-semibold mb-3">Top Recommendations</h3>
        <div className="space-y-3">
          {result.recommendations.slice(0, 3).map((rec, index) => (
            <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className={`px-2 py-1 rounded text-xs font-medium ${getSeverityColor(rec.severity)}`}>
                {rec.severity.toUpperCase()}
              </div>
              <div className="flex-1">
                <h4 className="font-medium text-gray-900">{rec.title}</h4>
                <p className="text-sm text-gray-600">{rec.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Keywords Tab Component
const KeywordsTab = ({ result }) => {
  const { keyword_analysis } = result;

  return (
    <div className="space-y-6">
      {/* Coverage Score */}
      <div className="text-center">
        <div className="text-4xl font-bold text-primary-600 mb-2">
          {keyword_analysis.coverage_score.toFixed(0)}%
        </div>
        <p className="text-gray-600">Keyword Coverage Score</p>
      </div>

      {/* Missing Keywords */}
      {keyword_analysis.missing_keywords.length > 0 && (
        <div>
          <h3 className="font-semibold mb-3 text-error-600">
            Missing Keywords ({keyword_analysis.missing_keywords.length})
          </h3>
          <div className="flex flex-wrap gap-2">
            {keyword_analysis.missing_keywords.map((keyword, index) => (
              <span key={index} className="px-3 py-1 bg-error-100 text-error-800 rounded-full text-sm">
                {keyword}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Strong Keywords */}
      {keyword_analysis.strong_keywords.length > 0 && (
        <div>
          <h3 className="font-semibold mb-3 text-success-600">
            Strong Keywords ({keyword_analysis.strong_keywords.length})
          </h3>
          <div className="space-y-2">
            {keyword_analysis.strong_keywords.slice(0, 10).map((keyword, index) => (
              <div key={index} className="flex items-center justify-between p-2 bg-success-50 rounded">
                <span className="font-medium">{keyword.keyword}</span>
                <span className="text-sm text-success-600">
                  {keyword.location_in_resume} • Score: {keyword.importance_score.toFixed(1)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Weak Keywords */}
      {keyword_analysis.weak_keywords.length > 0 && (
        <div>
          <h3 className="font-semibold mb-3 text-warning-600">
            Weak Keywords ({keyword_analysis.weak_keywords.length})
          </h3>
          <div className="space-y-2">
            {keyword_analysis.weak_keywords.slice(0, 10).map((keyword, index) => (
              <div key={index} className="flex items-center justify-between p-2 bg-warning-50 rounded">
                <span className="font-medium">{keyword.keyword}</span>
                <span className="text-sm text-warning-600">
                  {keyword.location_in_resume} • Score: {keyword.importance_score.toFixed(1)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Formatting Tab Component
const FormattingTab = ({ result }) => {
  const { formatting_analysis } = result;

  return (
    <div className="space-y-6">
      {/* Scores */}
      <div className="grid md:grid-cols-2 gap-4">
        <div className="text-center p-4 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-gray-900">
            {formatting_analysis.ats_compatibility_score.toFixed(0)}%
          </div>
          <div className="text-sm text-gray-600">ATS Compatibility</div>
        </div>
        <div className="text-center p-4 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-gray-900">
            {formatting_analysis.structure_score.toFixed(0)}%
          </div>
          <div className="text-sm text-gray-600">Structure Score</div>
        </div>
      </div>

      {/* Formatting Issues */}
      {formatting_analysis.issues.length > 0 ? (
        <div>
          <h3 className="font-semibold mb-3">Formatting Issues</h3>
          <div className="space-y-3">
            {formatting_analysis.issues.map((issue, index) => (
              <div key={index} className="p-4 border rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium capitalize">
                    {issue.issue_type.replace('_', ' ')}
                  </h4>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    issue.severity === 'critical' 
                      ? 'text-error-600 bg-error-50 border-error-200'
                      : issue.severity === 'major'
                      ? 'text-warning-600 bg-warning-50 border-warning-200'
                      : 'text-gray-600 bg-gray-50 border-gray-200'
                  }`}>
                    {issue.severity.toUpperCase()}
                  </span>
                </div>
                <p className="text-gray-600 mb-2">{issue.description}</p>
                <p className="text-sm text-gray-500">
                  <strong>Suggestion:</strong> {issue.suggestion}
                </p>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center p-8 bg-success-50 rounded-lg">
          <CheckCircle className="h-12 w-12 text-success-600 mx-auto mb-4" />
          <h3 className="font-semibold text-success-800 mb-2">Great Formatting!</h3>
          <p className="text-success-600">No significant formatting issues found.</p>
        </div>
      )}
    </div>
  );
};

// Impact Tab Component
const ImpactTab = ({ result }) => {
  const { impact_analysis } = result;

  return (
    <div className="space-y-6">
      {/* Impact Score */}
      <div className="text-center">
        <div className="text-4xl font-bold text-primary-600 mb-2">
          {impact_analysis.impact_score.toFixed(0)}%
        </div>
        <p className="text-gray-600">Overall Impact Score</p>
      </div>

      {/* Strong Bullets */}
      {impact_analysis.strong_bullets.length > 0 && (
        <div>
          <h3 className="font-semibold mb-3 text-success-600">
            Strong Impact Statements ({impact_analysis.strong_bullets.length})
          </h3>
          <div className="space-y-3">
            {impact_analysis.strong_bullets.slice(0, 5).map((bullet, index) => (
              <div key={index} className="p-3 bg-success-50 border border-success-200 rounded-lg">
                <p className="text-gray-900 mb-2">"{bullet.text}"</p>
                <div className="flex items-center space-x-4 text-sm">
                  <span className="flex items-center text-success-600">
                    <CheckCircle className="h-4 w-4 mr-1" />
                    Score: {bullet.strength_score.toFixed(1)}
                  </span>
                  {bullet.has_metrics && (
                    <span className="flex items-center text-success-600">
                      <TrendingUp className="h-4 w-4 mr-1" />
                      Has Metrics
                    </span>
                  )}
                  {bullet.has_action_verb && (
                    <span className="flex items-center text-success-600">
                      <Target className="h-4 w-4 mr-1" />
                      Action Verb
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Weak Bullets */}
      {impact_analysis.weak_bullets.length > 0 && (
        <div>
          <h3 className="font-semibold mb-3 text-warning-600">
            Needs Improvement ({impact_analysis.weak_bullets.length})
          </h3>
          <div className="space-y-3">
            {impact_analysis.weak_bullets.slice(0, 5).map((bullet, index) => (
              <div key={index} className="p-3 bg-warning-50 border border-warning-200 rounded-lg">
                <p className="text-gray-900 mb-2">"{bullet.text}"</p>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-warning-600">
                    Score: {bullet.strength_score.toFixed(1)}
                  </span>
                  {bullet.suggestion && (
                    <span className="text-sm text-gray-600 italic">
                      {bullet.suggestion}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Generic Phrases */}
      {impact_analysis.generic_phrases_found.length > 0 && (
        <div>
          <h3 className="font-semibold mb-3 text-error-600">
            Generic Phrases Found
          </h3>
          <div className="flex flex-wrap gap-2">
            {impact_analysis.generic_phrases_found.map((phrase, index) => (
              <span key={index} className="px-3 py-1 bg-error-100 text-error-800 rounded-full text-sm">
                "{phrase}"
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Recommendations Tab Component
const RecommendationsTab = ({ result, getSeverityColor, getCategoryIcon }) => {
  return (
    <div className="space-y-6">
      <div className="space-y-4">
        {result.recommendations.map((rec, index) => (
          <div key={index} className="p-4 border rounded-lg">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-3">
                {getCategoryIcon(rec.category)}
                <h3 className="font-semibold text-gray-900">{rec.title}</h3>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 rounded text-xs font-medium ${getSeverityColor(rec.severity)}`}>
                  {rec.severity.toUpperCase()}
                </span>
                <span className="text-sm text-gray-500">
                  Priority: {rec.priority_score.toFixed(1)}
                </span>
              </div>
            </div>
            
            <p className="text-gray-600 mb-4">{rec.description}</p>
            
            {rec.before_example && rec.after_example && (
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-error-600 mb-2">Before:</h4>
                    <p className="text-sm text-gray-700 bg-error-50 p-3 rounded">
                      {rec.before_example}
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium text-success-600 mb-2">After:</h4>
                    <p className="text-sm text-gray-700 bg-success-50 p-3 rounded">
                      {rec.after_example}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AnalysisResults;
