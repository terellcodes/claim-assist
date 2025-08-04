# Changelog

All notable changes to ClaimAssist will be documented in this file.

## [Unreleased] - 2025-08-04

### Enhanced
- **Claim Editing UX**: Edit button now smoothly scrolls to claim form for better user experience
- **Form Validation**: Fixed textarea readonly state and styling consistency in ClaimForm component
- **Resubmission Flow**: Enabled claim resubmission after editing with proper form validation

### Added
- **Policy Citations**: Added support for AI agent to provide specific policy references supporting analysis
- **Citations UI**: Beautiful blue-themed citations section with document icons and markdown rendering

### Fixed
- **Agent Responses**: Replaced unreliable text parsing with structured JSON responses from AI agent
- **Status Determination**: Added explicit `is_valid` boolean field for accurate claim status determination
- **Type Safety**: Updated backend schema to support suggestions as `List[str]` to match frontend expectations
- **Text Readability**: Improved text contrast in evaluation results for better readability
- **Code Quality**: Removed 50+ lines of error-prone text parsing logic
- **ReactMarkdown Error**: Fixed className prop error in citations rendering