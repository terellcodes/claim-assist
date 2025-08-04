'use client'

import { useState } from 'react'
import { PolicyMetadata, ClaimEvaluation } from './ClaimWiseApp'

interface EvaluationResultsProps {
  evaluation: ClaimEvaluation
  policyMetadata: PolicyMetadata | null
  onStartOver: () => void
}

export default function EvaluationResults({ evaluation, policyMetadata, onStartOver }: EvaluationResultsProps) {
  const [copiedEmail, setCopiedEmail] = useState(false)
  const [copiedEvaluation, setCopiedEvaluation] = useState(false)

  const copyToClipboard = async (text: string, type: 'email' | 'evaluation') => {
    try {
      await navigator.clipboard.writeText(text)
      if (type === 'email') {
        setCopiedEmail(true)
        setTimeout(() => setCopiedEmail(false), 2000)
      } else {
        setCopiedEvaluation(true)
        setTimeout(() => setCopiedEvaluation(false), 2000)
      }
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'valid':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'invalid':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'needs_review':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'valid':
        return (
          <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        )
      case 'invalid':
        return (
          <svg className="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        )
      case 'needs_review':
        return (
          <svg className="w-5 h-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        )
      default:
        return null
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Claim Evaluation Results
          </h2>
          <p className="text-gray-600">
            AI-powered analysis of your insurance claim
          </p>
        </div>

        {/* Status Badge */}
        <div className={`inline-flex items-center px-4 py-2 rounded-full border ${getStatusColor(evaluation.claim_status)} mb-6`}>
          {getStatusIcon(evaluation.claim_status)}
          <span className="ml-2 font-medium capitalize">
            {evaluation.claim_status === 'needs_review' ? 'Needs Review' : evaluation.claim_status}
          </span>
        </div>

        {/* Policy Information */}
        {policyMetadata && (
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-gray-800 mb-2">Policy Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
              <p><strong>Insurance Company:</strong> {policyMetadata.insurance_company}</p>
              <p><strong>Policy ID:</strong> {policyMetadata.policy_id}</p>
              {policyMetadata.policy_number !== 'Not specified' && (
                <p><strong>Policy Number:</strong> {policyMetadata.policy_number}</p>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Evaluation Details */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold text-gray-900">
            Detailed Evaluation
          </h3>
          <button
            onClick={() => copyToClipboard(evaluation.evaluation, 'evaluation')}
            className="flex items-center px-3 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-md transition-colors"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            {copiedEvaluation ? 'Copied!' : 'Copy'}
          </button>
        </div>
        <div className="prose max-w-none">
          <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
            {evaluation.evaluation}
          </div>
        </div>
      </div>

      {/* Email Draft */}
      {evaluation.email_draft && (
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-gray-900">
              Professional Email Draft
            </h3>
            <button
              onClick={() => copyToClipboard(evaluation.email_draft!, 'email')}
              className="flex items-center px-3 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-md transition-colors"
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              {copiedEmail ? 'Copied!' : 'Copy Email'}
            </button>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="whitespace-pre-wrap text-gray-700 leading-relaxed font-mono text-sm">
              {evaluation.email_draft}
            </div>
          </div>
          <p className="text-sm text-gray-500 mt-2">
            This email draft is ready to send to your insurance company. Review and modify as needed.
          </p>
        </div>
      )}

      {/* Suggestions */}
      {evaluation.suggestions && evaluation.suggestions.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Recommendations
          </h3>
          <ul className="space-y-3">
            {evaluation.suggestions.map((suggestion, index) => (
              <li key={index} className="flex items-start">
                <svg className="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span className="text-gray-700">{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Actions */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={onStartOver}
            className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            Evaluate Another Claim
          </button>
          
          {evaluation.claim_status === 'valid' && evaluation.email_draft && (
            <button
              onClick={() => copyToClipboard(evaluation.email_draft!, 'email')}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              {copiedEmail ? 'Email Copied!' : 'Copy Email to Send'}
            </button>
          )}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <div className="flex items-start">
          <svg className="w-5 h-5 text-yellow-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <div>
            <h4 className="font-semibold text-yellow-800 mb-2">Important Disclaimer</h4>
            <p className="text-yellow-700 text-sm">
              This evaluation is generated by AI and is for informational purposes only. It does not constitute legal advice or a guarantee of claim approval. Always consult with your insurance company and consider seeking professional legal advice for complex claims.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}