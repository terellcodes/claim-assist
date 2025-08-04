'use client'

import { useState } from 'react'
import { API_ENDPOINTS, logger } from '@/config/api'
import { PolicyMetadata, ClaimEvaluation } from './ClaimWiseApp'

interface ClaimFormProps {
  policyMetadata: PolicyMetadata
  onClaimSubmitted: (evaluation: ClaimEvaluation) => void
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

export default function ClaimForm({ policyMetadata, onClaimSubmitted, isLoading, setIsLoading }: ClaimFormProps) {
  const [formData, setFormData] = useState({
    policy_holder_name: policyMetadata.policy_holder !== 'Not specified' ? policyMetadata.policy_holder : '',
    incident_date: '',
    incident_time: '',
    location: '',
    description: ''
  })
  const [error, setError] = useState<string | null>(null)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      logger.info('Submitting claim for evaluation', formData)

      const claimRequest = {
        policy_id: policyMetadata.policy_id,
        ...formData
      }

      const response = await fetch(API_ENDPOINTS.CLAIMS.SUBMIT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(claimRequest),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Claim submission failed' }))
        throw new Error(errorData.detail || `Submission failed: ${response.status}`)
      }

      const result = await response.json()
      logger.success('Claim evaluated successfully', result)
      onClaimSubmitted(result)
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit claim'
      logger.warn('Claim submission failed', errorMessage)
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const isFormValid = formData.policy_holder_name && formData.incident_date && 
                      formData.location && formData.description.trim().length > 50

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Describe Your Claim
        </h2>
        <p className="text-gray-600">
          Provide details about your incident for AI-powered evaluation
        </p>
      </div>

      {/* Policy Info */}
      <div className="bg-green-50 rounded-lg p-4 mb-8">
        <div className="flex items-center mb-2">
          <svg className="w-5 h-5 text-green-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          <span className="font-medium text-green-800">Policy Loaded Successfully</span>
        </div>
        <div className="text-sm text-green-700">
          <p><strong>Insurance Company:</strong> {policyMetadata.insurance_company}</p>
          <p><strong>Policy ID:</strong> {policyMetadata.policy_id}</p>
          {policyMetadata.policy_number !== 'Not specified' && (
            <p><strong>Policy Number:</strong> {policyMetadata.policy_number}</p>
          )}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Policy Holder Name */}
        <div>
          <label htmlFor="policy_holder_name" className="block text-sm font-medium text-gray-700 mb-2">
            Policy Holder Name *
          </label>
          <input
            type="text"
            id="policy_holder_name"
            name="policy_holder_name"
            value={formData.policy_holder_name}
            onChange={handleInputChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-500"
            placeholder="Enter the policy holder's full name"
          />
        </div>

        {/* Incident Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="incident_date" className="block text-sm font-medium text-gray-700 mb-2">
              Incident Date *
            </label>
            <input
              type="date"
              id="incident_date"
              name="incident_date"
              value={formData.incident_date}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-500"
            />
          </div>

          <div>
            <label htmlFor="incident_time" className="block text-sm font-medium text-gray-700 mb-2">
              Incident Time (optional)
            </label>
            <input
              type="time"
              id="incident_time"
              name="incident_time"
              value={formData.incident_time}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-500"
            />
          </div>
        </div>

        {/* Location */}
        <div>
          <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
            Location of Incident *
          </label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-500"
            placeholder="e.g., 123 Main St, City, State, ZIP"
          />
        </div>

        {/* Description */}
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
            Detailed Description of the Incident *
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            required
            rows={6}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-500"
            placeholder="Describe what happened in detail. Include information about the cause, extent of damage, any immediate actions taken, evidence available (photos, witnesses), and any other relevant details that might help evaluate your claim."
          />
          <p className="text-sm text-gray-500 mt-1">
            {formData.description.length} characters 
            {formData.description.length < 50 && (
              <span className="text-orange-600"> (minimum 50 characters for best results)</span>
            )}
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <p className="text-red-700 font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={!isFormValid || isLoading}
            className={`w-full py-3 px-4 rounded-md font-medium text-white transition-colors ${
              isFormValid && !isLoading
                ? 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
                : 'bg-gray-400 cursor-not-allowed'
            }`}
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Evaluating Claim...
              </div>
            ) : (
              'Submit Claim for Evaluation'
            )}
          </button>
        </div>
      </form>

      {/* Tips */}
      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-3">Tips for accurate evaluation:</h3>
        <ul className="text-blue-700 space-y-2 text-sm">
          <li>• Be as specific as possible about what caused the damage</li>
          <li>• Include exact dates and times when known</li>
          <li>• Mention any photos, receipts, or other evidence you have</li>
          <li>• Describe the full extent of damage or loss</li>
        </ul>
      </div>
    </div>
  )
}