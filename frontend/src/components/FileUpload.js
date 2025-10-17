import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, AlertCircle } from 'lucide-react';

const FileUpload = ({ onAnalysis }) => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [jobDescriptionFile, setJobDescriptionFile] = useState(null);
  const [errors, setErrors] = useState({});

  const onDropResume = useCallback((acceptedFiles, rejectedFiles) => {
    setErrors(prev => ({ ...prev, resume: null }));
    
    if (rejectedFiles.length > 0) {
      setErrors(prev => ({ ...prev, resume: 'Please upload a PDF or DOCX file' }));
      return;
    }
    
    setResumeFile(acceptedFiles[0]);
  }, []);

  const onDropJobDescription = useCallback((acceptedFiles, rejectedFiles) => {
    setErrors(prev => ({ ...prev, jobDescription: null }));
    
    if (rejectedFiles.length > 0) {
      setErrors(prev => ({ ...prev, jobDescription: 'Please upload a PDF, DOCX, or TXT file' }));
      return;
    }
    
    setJobDescriptionFile(acceptedFiles[0]);
    setJobDescription(''); // Clear text input when file is uploaded
  }, []);

  const { getRootProps: getResumeRootProps, getInputProps: getResumeInputProps, isDragActive: isResumeDragActive } = useDropzone({
    onDrop: onDropResume,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1
  });

  const { getRootProps: getJobRootProps, getInputProps: getJobInputProps, isDragActive: isJobDragActive } = useDropzone({
    onDrop: onDropJobDescription,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: 1
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    const newErrors = {};
    if (!resumeFile) {
      newErrors.resume = 'Please upload your resume';
    }
    if (!jobDescription.trim() && !jobDescriptionFile) {
      newErrors.jobDescription = 'Please provide a job description';
    }
    
    setErrors(newErrors);
    
    if (Object.keys(newErrors).length > 0) {
      return;
    }

    // Create form data
    const formData = new FormData();
    formData.append('resume_file', resumeFile);
    
    if (jobDescriptionFile) {
      formData.append('job_description_file', jobDescriptionFile);
    } else {
      formData.append('job_description', jobDescription);
    }

    onAnalysis(formData);
  };

  const removeResumeFile = () => {
    setResumeFile(null);
    setErrors(prev => ({ ...prev, resume: null }));
  };

  const removeJobDescriptionFile = () => {
    setJobDescriptionFile(null);
    setErrors(prev => ({ ...prev, jobDescription: null }));
  };

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-6">Upload Your Resume & Job Description</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Resume Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Resume File *
          </label>
          {resumeFile ? (
            <div className="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center">
                <FileText className="h-5 w-5 text-green-600 mr-3" />
                <span className="text-sm font-medium text-green-800">{resumeFile.name}</span>
              </div>
              <button
                type="button"
                onClick={removeResumeFile}
                className="text-green-600 hover:text-green-800"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <div
              {...getResumeRootProps()}
              className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
                isResumeDragActive
                  ? 'border-primary-400 bg-primary-50'
                  : errors.resume
                  ? 'border-error-300 bg-error-50'
                  : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
              }`}
            >
              <input {...getResumeInputProps()} />
              <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-600">
                {isResumeDragActive
                  ? 'Drop your resume here...'
                  : 'Drag & drop your resume here, or click to select'}
              </p>
              <p className="text-xs text-gray-500 mt-1">PDF or DOCX files only</p>
            </div>
          )}
          {errors.resume && (
            <p className="mt-2 text-sm text-error-600 flex items-center">
              <AlertCircle className="h-4 w-4 mr-1" />
              {errors.resume}
            </p>
          )}
        </div>

        {/* Job Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Job Description *
          </label>
          
          {/* Text Input */}
          <div className="mb-3">
            <textarea
              value={jobDescription}
              onChange={(e) => {
                setJobDescription(e.target.value);
                setJobDescriptionFile(null); // Clear file when typing
                setErrors(prev => ({ ...prev, jobDescription: null }));
              }}
              placeholder="Paste the job description here..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              rows={6}
              disabled={!!jobDescriptionFile}
            />
          </div>

          {/* OR Divider */}
          <div className="relative mb-3">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">OR</span>
            </div>
          </div>

          {/* File Upload */}
          {jobDescriptionFile ? (
            <div className="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center">
                <FileText className="h-5 w-5 text-green-600 mr-3" />
                <span className="text-sm font-medium text-green-800">{jobDescriptionFile.name}</span>
              </div>
              <button
                type="button"
                onClick={removeJobDescriptionFile}
                className="text-green-600 hover:text-green-800"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <div
              {...getJobRootProps()}
              className={`border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-colors ${
                isJobDragActive
                  ? 'border-primary-400 bg-primary-50'
                  : errors.jobDescription
                  ? 'border-error-300 bg-error-50'
                  : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
              }`}
            >
              <input {...getJobInputProps()} />
              <Upload className="h-6 w-6 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-600">
                {isJobDragActive
                  ? 'Drop job description file here...'
                  : 'Upload job description file'}
              </p>
              <p className="text-xs text-gray-500">PDF, DOCX, or TXT files</p>
            </div>
          )}
          
          {errors.jobDescription && (
            <p className="mt-2 text-sm text-error-600 flex items-center">
              <AlertCircle className="h-4 w-4 mr-1" />
              {errors.jobDescription}
            </p>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full btn-primary"
          disabled={!resumeFile || (!jobDescription.trim() && !jobDescriptionFile)}
        >
          Analyze Resume
        </button>
      </form>
    </div>
  );
};

export default FileUpload;
