'use client'

import { useState } from 'react'

export interface StrategyOption {
  value: string
  label: string
  description: string
  badge?: string
  icon?: string
}

interface RetrievalStrategySelectorProps {
  selectedStrategy: string
  onStrategyChange: (strategy: string) => void
  disabled?: boolean
}

const STRATEGY_OPTIONS: StrategyOption[] = [
  {
    value: "basic",
    label: "Basic Retrieval",
    description: "Fast and efficient for most claims. Uses simple vector search.",
    icon: "⚡"
  },
  {
    value: "advanced_flashrank", 
    label: "Advanced AI Reranking",
    description: "More accurate context selection using AI reranking. Works offline.",
    badge: "Recommended",
    icon: "🎯"
  },
  {
    value: "advanced_cohere",
    label: "Premium Accuracy", 
    description: "Highest accuracy with Cohere reranking. Requires API access.",
    badge: "Premium",
    icon: "⭐"
  }
]

export default function RetrievalStrategySelector({ 
  selectedStrategy, 
  onStrategyChange, 
  disabled = false 
}: RetrievalStrategySelectorProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const selectedOption = STRATEGY_OPTIONS.find(option => option.value === selectedStrategy) || STRATEGY_OPTIONS[0]

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium text-gray-900">
            Retrieval Strategy
          </h3>
          <p className="text-sm text-gray-600">
            Choose how the AI searches your policy for relevant information
          </p>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium"
          disabled={disabled}
        >
          {isExpanded ? 'Hide Options' : 'Show Options'}
        </button>
      </div>

      {/* Current Selection Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <span className="text-2xl">{selectedOption.icon}</span>
          <div className="flex-1">
            <div className="flex items-center space-x-2">
              <h4 className="font-medium text-blue-900">{selectedOption.label}</h4>
              {selectedOption.badge && (
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                  selectedOption.badge === 'Recommended' 
                    ? 'bg-green-100 text-green-800'
                    : 'bg-purple-100 text-purple-800'
                }`}>
                  {selectedOption.badge}
                </span>
              )}
            </div>
            <p className="text-sm text-blue-700 mt-1">{selectedOption.description}</p>
          </div>
        </div>
      </div>

      {/* Strategy Options (Expandable) */}
      {isExpanded && (
        <div className="space-y-3">
          {STRATEGY_OPTIONS.map((option) => (
            <div
              key={option.value}
              className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                selectedStrategy === option.value
                  ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
              onClick={() => {
                if (!disabled && option.value !== selectedStrategy) {
                  console.log(`🎯 Strategy changed: ${selectedStrategy} → ${option.value}`)
                  console.log(`   📊 New strategy: ${option.description}`)
                  onStrategyChange(option.value)
                }
              }}
            >
              <div className="flex items-start space-x-3">
                <span className="text-xl">{option.icon}</span>
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <h4 className={`font-medium ${
                      selectedStrategy === option.value ? 'text-blue-900' : 'text-gray-900'
                    }`}>
                      {option.label}
                    </h4>
                    {option.badge && (
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        option.badge === 'Recommended' 
                          ? 'bg-green-100 text-green-800'
                          : 'bg-purple-100 text-purple-800'
                      }`}>
                        {option.badge}
                      </span>
                    )}
                    {selectedStrategy === option.value && (
                      <div className="flex items-center space-x-1 text-blue-600">
                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        <span className="text-sm font-medium">Selected</span>
                      </div>
                    )}
                  </div>
                  <p className={`text-sm mt-1 ${
                    selectedStrategy === option.value ? 'text-blue-700' : 'text-gray-600'
                  }`}>
                    {option.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Performance Indicators */}
      {isExpanded && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-900 mb-3">Performance Comparison</h4>
          <div className="space-y-2">
            {STRATEGY_OPTIONS.map((option) => (
              <div key={option.value} className="flex items-center justify-between text-sm">
                <span className="text-gray-600">{option.label}</span>
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-1">
                    <span className="text-gray-500">Speed:</span>
                    <div className="flex space-x-1">
                      {Array.from({ length: 3 }, (_, i) => (
                        <div
                          key={i}
                          className={`w-2 h-2 rounded-full ${
                            (option.value === 'basic' && i < 3) ||
                            (option.value === 'advanced_flashrank' && i < 2) ||
                            (option.value === 'advanced_cohere' && i < 1)
                              ? 'bg-green-500'
                              : 'bg-gray-300'
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center space-x-1">
                    <span className="text-gray-500">Accuracy:</span>
                    <div className="flex space-x-1">
                      {Array.from({ length: 3 }, (_, i) => (
                        <div
                          key={i}
                          className={`w-2 h-2 rounded-full ${
                            (option.value === 'basic' && i < 2) ||
                            (option.value === 'advanced_flashrank' && i < 3) ||
                            (option.value === 'advanced_cohere' && i < 3)
                              ? 'bg-blue-500'
                              : 'bg-gray-300'
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export { STRATEGY_OPTIONS }