# Personal AI Employee Constitution

## Core Principles

### I. Human-in-the-Loop Control
Critical business decisions require explicit human approval. The AI employee acts as an autonomous assistant but defers to human judgment for sensitive actions like payments over $100, invoices to new clients, bulk emails, and large social posts. This ensures accountability and prevents unintended consequences.

### II. Local-First Architecture
Data and processing should occur locally when possible. Sensitive information like Gmail, WhatsApp messages, and financial data should be processed on local infrastructure rather than sent to external services. This enhances privacy and reduces dependency on external APIs.

### III. Multi-Channel Monitoring
The system must monitor multiple communication channels simultaneously (Gmail, WhatsApp, file drops) to capture all business-relevant information. Each channel has its own polling intervals and priority keywords to ensure urgent matters are addressed promptly.

### IV. Proactive Task Management
The AI employee should proactively categorize, prioritize, and route tasks to appropriate folders (Needs Action, Plans, Done, Pending Approval, etc.) based on business rules and priority keywords. This creates an organized workflow for human review.

### V. Comprehensive Audit Trail
All actions taken by the AI employee must be logged with full audit capability. This includes credential handling, decision-making processes, and executed actions. Logs must be retained for 90 days to ensure accountability and compliance.

### VI. Secure Credential Handling
Credentials must be stored securely using appropriate mechanisms: environment variables for Gmail, secrets manager for banking, and local encryption for WhatsApp sessions. No plaintext credentials should be stored in the codebase.

## Additional Constraints

### Technology Stack
- Node.js/TypeScript for main orchestration
- MCP (Model Context Protocol) for browser, email, and calendar integrations
- File system watchers for local file monitoring
- Local encrypted storage for sensitive session data

### Security Requirements
- All sensitive data must be encrypted at rest
- Audit logging for all actions
- Human approval required for sensitive operations
- Regular credential rotation capability

### Performance Standards
- Polling intervals configurable per service
- Retry strategies with exponential backoff
- Maximum 5 concurrent tasks to avoid overwhelming systems
- Graceful degradation when services are unavailable

## Development Workflow

### Feature Development
- All features must follow the Spec-Driven Development (SDD) approach
- Specifications, plans, and tasks must be documented before implementation
- Small, testable changes with clear acceptance criteria
- Integration tests for all watcher modules

### Review Process
- Code reviews must verify compliance with constitution
- Security implications must be considered for all changes
- Human-in-the-loop requirements must be preserved

### Quality Gates
- All watchers must have proper error handling and retry mechanisms
- Approval system must be bypassed only for explicitly auto-approved actions
- Audit logging must capture all significant operations

## Governance

The constitution serves as the authoritative guide for all development decisions. Any changes to the core principles of human control, local-first architecture, or security requirements must be explicitly documented and approved. All pull requests and code reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
