'use client'

import { useState, useCallback } from 'react'
import { API_ENDPOINTS, logger } from '@/config/api'
import { PolicyMetadata } from './ClaimWiseApp'

interface PolicyUploadProps {
  onPolicyUploaded: (metadata: PolicyMetadata) => void
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

export default function PolicyUpload({ onPolicyUploaded, isLoading, setIsLoading }: PolicyUploadProps) {
  const [dragActive, setDragActive] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const uploadPolicy = async (file: File) => {
    setIsLoading(true)
    setError(null)
    
    try {
      logger.info('Uploading policy file', { filename: file.name, size: file.size })
      
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(API_ENDPOINTS.POLICIES.UPLOAD, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Upload failed' }))
        throw new Error(errorData.detail || `Upload failed: ${response.status}`)
      }

      const result = await response.json()
      logger.success('Policy uploaded successfully', result)
      onPolicyUploaded(result)
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to upload policy'
      logger.warn('Policy upload failed', errorMessage)
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (file.type === 'application/pdf') {
        uploadPolicy(file)
      } else {
        setError('Please upload a PDF file only')
      }
    }
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (file.type === 'application/pdf') {
        uploadPolicy(file)
      } else {
        setError('Please upload a PDF file only')
      }
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Upload Your Insurance Policy
        </h2>
        <p className="text-gray-600">
          Upload your insurance policy PDF to get started with claim evaluation
        </p>
      </div>

      {/* Upload Area */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
          dragActive 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
        } ${isLoading ? 'opacity-50 pointer-events-none' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          disabled={isLoading}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        
        {isLoading ? (
          <div className="flex flex-col items-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p className="text-lg font-medium text-gray-700">Processing your policy...</p>
            <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <svg className="w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p className="text-lg font-medium text-gray-700 mb-2">
              Drop your PDF here or click to browse
            </p>
            <p className="text-sm text-gray-500">
              Supports PDF files up to 10MB
            </p>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <p className="text-red-700 font-medium">{error}</p>
          </div>
        </div>
      )}

      {/* Tips */}
      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-3">Tips for best results:</h3>
        <ul className="text-blue-700 space-y-2 text-sm">
          <li>• Upload your complete insurance policy document</li>
          <li>• Ensure the PDF is clear and readable</li>
          <li>• Include all pages of your policy for comprehensive analysis</li>
        </ul>
      </div>
    </div>
  )
}