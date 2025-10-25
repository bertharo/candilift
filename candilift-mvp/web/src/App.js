import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Info, Loader2 } from 'lucide-react';
import FileUpload from './components/FileUpload';
import AnalysisResults from './components/AnalysisResults';
import { analyzeResume } from './services/api';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalysis = async (formData) => {
    setIsAnalyzing(true);
    setError(null);
    
    try {
      const result = await analyzeResume(formData);
      setAnalysisResult(result);
    } catch (err) {
      setError(err.message || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-primary-600 mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">ATS Resume Reviewer</h1>
                <p className="text-sm text-gray-600">Optimize your resume for ATS and recruiters</p>
              </div>
            </div>
            {analysisResult && (
              <button
                onClick={handleReset}
                className="btn-secondary"
              >
                New Analysis
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!analysisResult ? (
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Get Your Resume ATS-Ready
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Upload your resume and job description to receive personalized recommendations 
                for improving ATS compatibility, keyword optimization, and recruiter appeal.
              </p>
            </div>

            {/* Features */}
            <div className="grid md:grid-cols-3 gap-6">
              <div className="card text-center">
                <CheckCircle className="h-12 w-12 text-success-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">ATS Optimization</h3>
                <p className="text-gray-600">
                  Identify formatting issues and keyword gaps that prevent ATS parsing
                </p>
              </div>
              <div className="card text-center">
                <AlertCircle className="h-12 w-12 text-warning-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">Impact Analysis</h3>
                <p className="text-gray-600">
                  Analyze bullet points for measurable outcomes and strong action verbs
                </p>
              </div>
              <div className="card text-center">
                <Info className="h-12 w-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">Actionable Insights</h3>
                <p className="text-gray-600">
                  Receive prioritized recommendations with before/after examples
                </p>
              </div>
            </div>

            {/* Upload Section */}
            <div className="max-w-2xl mx-auto">
              {isAnalyzing ? (
                <div className="card text-center">
                  <Loader2 className="h-12 w-12 text-primary-600 mx-auto mb-4 animate-spin" />
                  <h3 className="text-lg font-semibold mb-2">Analyzing Your Resume</h3>
                  <p className="text-gray-600">
                    This may take a few moments. Please don't close this page.
                  </p>
                </div>
              ) : (
                <FileUpload onAnalysis={handleAnalysis} />
              )}
            </div>

            {/* Error Display */}
            {error && (
              <div className="max-w-2xl mx-auto">
                <div className="bg-error-50 border border-error-200 rounded-lg p-4">
                  <div className="flex">
                    <AlertCircle className="h-5 w-5 text-error-600 mr-3 mt-0.5" />
                    <div>
                      <h3 className="text-sm font-medium text-error-800">Analysis Failed</h3>
                      <p className="text-sm text-error-700 mt-1">{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          <AnalysisResults result={analysisResult} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>&copy; 2024 ATS Resume Reviewer. Built to help you land your dream job.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
