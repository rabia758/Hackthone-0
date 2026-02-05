# Quickstart Guide: Personal AI Employee

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to Gmail account with API access enabled
- (Optional) WhatsApp Business Account API access
- Windows, macOS, or Linux operating system

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

### Environment Variables

```bash
# Gmail Configuration
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
GMAIL_REDIRECT_URI=your_redirect_uri

# WhatsApp Configuration (if using)
WHATSAPP_BUSINESS_ACCOUNT_ID=your_whatsapp_account_id
WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token

# Polling Intervals (in seconds)
GMAIL_POLL_INTERVAL=30
WHATSAPP_POLL_INTERVAL=60
FILE_POLL_INTERVAL=10

# Vault Configuration
VAULT_PATH=./AI_Employee_Vault
LOG_RETENTION_DAYS=90

# Security Settings
ENCRYPTION_KEY=your_encryption_key_here
MAX_CONCURRENT_TASKS=5
```

### Channel-Specific Configuration

#### Gmail Setup
1. Enable Gmail API in Google Cloud Console
2. Create OAuth 2.0 credentials
3. Add your redirect URI (typically http://localhost:3000/callback)
4. Configure the credentials in environment variables

#### WhatsApp Setup (Optional)
1. Obtain WhatsApp Business Account
2. Generate access token
3. Configure webhook if using real-time updates
4. Add credentials to environment variables

#### File Monitoring Setup
1. Ensure the AI_Employee_Vault directory exists
2. Set appropriate read/write permissions
3. Configure the path in VAULT_PATH environment variable

## Running the AI Employee

### Development Mode
```bash
npm run dev
# or
yarn dev
```

### Production Mode
```bash
npm start
# or
yarn start
```

### CLI Commands
```bash
# Start the AI employee
node ./dist/cli/main.js start

# Process messages once (no daemon)
node ./dist/cli/main.js process

# Check status
node ./dist/cli/main.js status

# View logs
node ./dist/cli/main.js logs
```

## Initial Setup

1. Run initial setup:
```bash
node ./dist/cli/main.js setup
```

2. Authenticate with services:
```bash
node ./dist/cli/main.js auth gmail
# Follow the OAuth flow for Gmail
```

3. Verify configuration:
```bash
node ./dist/cli/main.js verify
```

## Service Integration

### Gmail Integration
- The system will automatically check for new emails based on GMAIL_POLL_INTERVAL
- Emails are categorized based on subject and content
- Priority emails are flagged for immediate attention
- All email processing is logged in the audit trail

### WhatsApp Integration
- The system polls for new messages based on WHATSAPP_POLL_INTERVAL
- Messages are processed for customer inquiries and orders
- Priority keywords trigger alerts
- Session data is securely stored locally

### File Drop Monitoring
- Monitors the VAULT_PATH directory for new files
- Files are categorized based on naming conventions and content
- Business documents are automatically routed to appropriate folders
- All file operations are audited

## Human-in-the-Loop Approval

### Payment Approvals
- Transactions over $100 require explicit approval
- Approval requests are placed in Pending_Approval folder
- Use the CLI to approve or reject:
```bash
node ./dist/cli/main.js approve [transaction-id]
node ./dist/cli/main.js reject [transaction-id]
```

### Invoice Approvals
- New client invoices require approval
- Invoice requests appear in Pending_Approval folder
- Approval workflow via CLI commands

### Bulk Communications
- Bulk emails and social posts require approval
- Requests are queued in Pending_Approval folder
- Approval process ensures compliance

## Folder Organization

The AI_Employee_Vault maintains the following organization:

```
AI_Employee_Vault/
├── Needs_Action/          # Items requiring immediate attention
├── Plans/                 # Planned activities and schedules
├── Done/                  # Completed tasks
├── Pending_Approval/      # Items awaiting human approval
├── Rejected/              # Rejected items with reasons
├── Business_Goals.md      # Business objectives
├── Company_Handbook.md    # Company policies
└── ...                    # Other organizational files
```

## Monitoring and Maintenance

### Health Checks
```bash
node ./dist/cli/main.js health
```

### Log Management
- Logs are stored in ./logs/ directory
- Automatic rotation based on LOG_RETENTION_DAYS
- Sensitive information is encrypted in logs

### Performance Monitoring
- Concurrent task limit: MAX_CONCURRENT_TASKS
- Resource usage is monitored
- Automatic throttling when limits exceeded

## Troubleshooting

### Common Issues

#### Authentication Problems
- Verify environment variables are correctly set
- Re-run authentication: `node ./dist/cli/main.js auth gmail`
- Check OAuth credentials in Google Cloud Console

#### File Permission Errors
- Ensure AI_Employee_Vault directory has proper permissions
- Verify the application has read/write access
- Check that the path exists and is accessible

#### Service Unavailability
- Check network connectivity
- Verify service-specific configurations
- Review logs for specific error messages

### Diagnostic Commands
```bash
# View system status
node ./dist/cli/main.js status

# Check service connectivity
node ./dist/cli/main.js diagnose

# View recent logs
node ./dist/cli/main.js logs --recent 50
```

## Security Best Practices

1. Store encryption keys securely, not in version control
2. Rotate credentials regularly
3. Monitor audit logs for unusual activity
4. Limit access to the AI_Employee_Vault directory
5. Keep dependencies updated
6. Use strong, unique passwords for all services

## Next Steps

1. Complete the initial setup and authentication
2. Customize folder organization as needed
3. Configure notification settings for priority alerts
4. Train the system with your specific business rules
5. Monitor and refine categorization accuracy