'use client'

import { useState } from 'react'
import PolicyUpload from './PolicyUpload'
import ClaimForm from './ClaimForm'
import EvaluationResults from './EvaluationResults'
import { logger } from '@/config/api'

export interface PolicyMetadata {
  policy_id: string
  insurance_company: string
  policy_holder: string
  policy_number: string
  date_issued: string
  total_pages: number
}

export interface ClaimEvaluation {
  claim_id: string
  claim_status: 'valid' | 'invalid' | 'needs_review'
  evaluation: string
  email_draft?: string
  suggestions?: string[]
  policy_id: string
}

type AppStep = 'upload' | 'claim' | 'results'

export default function ClaimWiseApp() {
  const [currentStep, setCurrentStep] = useState<AppStep>('upload')
  const [policyMetadata, setPolicyMetadata] = useState<PolicyMetadata | null>(null)
  const [claimEvaluation, setClaimEvaluation] = useState<ClaimEvaluation | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isFormCollapsed, setIsFormCollapsed] = useState(true)
  const [isFormEditable, setIsFormEditable] = useState(false)
  const [claimFormData, setClaimFormData] = useState<{
    policy_holder_name: string
    incident_date: string
    incident_time: string
    location: string
    description: string
  } | null>(null)

  const handlePolicyUploaded = (metadata: PolicyMetadata) => {
    logger.success('Policy uploaded successfully', metadata)
    setPolicyMetadata(metadata)
    setCurrentStep('claim')
  }

  const handleClaimSubmitted = (evaluation: ClaimEvaluation, formData: typeof claimFormData) => {
    logger.success('Claim evaluated successfully', evaluation)
    setClaimEvaluation(evaluation)
    setClaimFormData(formData)
    setCurrentStep('results')
    setIsFormCollapsed(true)
    setIsFormEditable(false)
  }

  const handleStartOver = () => {
    setPolicyMetadata(null)
    setClaimEvaluation(null)
    setClaimFormData(null)
    setCurrentStep('upload')
    setIsFormCollapsed(true)
    setIsFormEditable(false)
  }

  const handleToggleForm = () => {
    setIsFormCollapsed(!isFormCollapsed)
  }

  const handleEditForm = () => {
    setIsFormEditable(true)
    setIsFormCollapsed(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            ClaimWise
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered insurance claim evaluation and professional email drafting
          </p>
        </header>

        {/* Progress Steps */}
        <div className="flex justify-center mb-12">
          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 ${
              currentStep === 'upload' ? 'text-blue-600' : 
              policyMetadata ? 'text-green-600' : 'text-gray-400'
            }`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                currentStep === 'upload' ? 'bg-blue-600 text-white' :
                policyMetadata ? 'bg-green-600 text-white' : 'bg-gray-300 text-gray-600'
              }`}>
                1
              </div>
              <span className="font-medium">Upload Policy</span>
            </div>
            
            <div className="w-8 h-0.5 bg-gray-300"></div>
            
            <div className={`flex items-center space-x-2 ${
              currentStep === 'claim' ? 'text-blue-600' : 
              claimEvaluation ? 'text-green-600' : 'text-gray-400'
            }`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                currentStep === 'claim' ? 'bg-blue-600 text-white' :
                claimEvaluation ? 'bg-green-600 text-white' : 'bg-gray-300 text-gray-600'
              }`}>
                2
              </div>
              <span className="font-medium">Describe Claim</span>
            </div>
            
            <div className="w-8 h-0.5 bg-gray-300"></div>
            
            <div className={`flex items-center space-x-2 ${
              currentStep === 'results' ? 'text-blue-600' : 'text-gray-400'
            }`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                currentStep === 'results' ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-600'
              }`}>
                3
              </div>
              <span className="font-medium">Get Evaluation</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          {currentStep === 'upload' && (
            <PolicyUpload 
              onPolicyUploaded={handlePolicyUploaded}
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
          )}
          
          {currentStep === 'claim' && policyMetadata && (
            <ClaimForm 
              policyMetadata={policyMetadata}
              onClaimSubmitted={handleClaimSubmitted}
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
          )}
          
          {currentStep === 'results' && claimEvaluation && policyMetadata && claimFormData && (
            <div className="space-y-6">
              {/* Collapsible Claim Form */}
              <ClaimForm 
                policyMetadata={policyMetadata}
                onClaimSubmitted={handleClaimSubmitted}
                isLoading={isLoading}
                setIsLoading={setIsLoading}
                isCollapsed={isFormCollapsed}
                isReadOnly={!isFormEditable}
                onToggleCollapse={handleToggleForm}
                onEdit={handleEditForm}
                initialFormData={claimFormData}
              />
              
              {/* Evaluation Results */}
              <EvaluationResults 
                evaluation={claimEvaluation}
                policyMetadata={policyMetadata}
                onStartOver={handleStartOver}
                onEditClaim={handleEditForm}
              />
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="text-center mt-16 text-gray-500">
          <p>Powered by AI • For informational purposes only</p>
        </footer>
      </div>
    </div>
  )
}