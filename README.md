# Personal AI Employee

A local-first, agent-driven, human-in-the-loop AI employee that monitors Gmail, WhatsApp, file drops, and manages business tasks.

## Overview

The Personal AI Employee is designed to act as a proactive consultant with human-in-the-loop approvals for sensitive actions. It monitors multiple communication channels simultaneously and manages tasks according to predefined business rules.

## Features

- **Multi-channel Monitoring**: Watches Gmail, WhatsApp, and filesystem for new information
- **Task Management**: Automatically categorizes and routes tasks to appropriate folders
- **Approval System**: Implements human-in-the-loop controls for sensitive actions
- **Local-first Architecture**: Prioritizes local processing for privacy and reliability
- **Audit Trail**: Comprehensive logging of all actions and decisions

## Architecture

The system consists of several key components:

- **Orchestrator**: Main coordinator that manages all subsystems
- **Watchers**: Monitor different channels (Gmail, WhatsApp, Filesystem)
- **Approval System**: Handles business rules for human approvals
- **Vault**: Organized folder structure for task management

## Configuration

Configuration is managed through environment variables in the `.env` file. Key settings include:

- Polling intervals for each watcher
- Priority keywords for urgent task identification
- Approval thresholds for payments and other sensitive actions
- Vault path for task organization

## Approval Rules

The system implements the following approval rules:

- Payments over $100 require human approval
- Invoices to new clients require approval
- Bulk email sends require approval
- Large social media posts require approval
- Small email replies and routine tasks are auto-approved

## Vault Structure

The system organizes tasks in the following folder structure:

- `Needs_Action`: Tasks requiring attention
- `Plans`: Planned activities
- `Done`: Completed tasks
- `Pending_Approval`: Tasks awaiting human approval
- `Approved`: Tasks approved by human
- `Rejected`: Tasks rejected by human
- `Logs`: System logs and audit trails
- `Invoices`: Invoice-related tasks
- `Updates`: Status updates

## Installation

1. Clone the repository
2. Install dependencies: `npm install`
3. Configure environment variables in `.env`
4. Build the project: `npm run build`
5. Run the application: `npm start`

## Development

For development, use:

```bash
npm run dev
```

This will start the application with hot reloading.

## Security

- Credentials are stored securely using environment variables
- All sensitive actions require human approval
- Comprehensive audit logging is maintained
- Local-first architecture minimizes exposure to external services

## Contributing

Please follow the Spec-Driven Development (SDD) approach:

1. Create specifications in `specs/` directory
2. Develop implementation plans
3. Break work into testable tasks
4. Implement with comprehensive testing