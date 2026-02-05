# API Contracts: Personal AI Employee

## Overview
This document defines the API contracts for the Personal AI Employee system, specifying the interfaces between different components and external services.

## Internal Service APIs

### Message Processing API

#### Process Incoming Message
```
POST /api/messages/process
```

**Description**: Process an incoming message from any channel and perform initial categorization.

**Request Body**:
```json
{
  "channelId": "GMAIL|WHATSAPP|FILE_DROP",
  "externalId": "string",
  "sender": "string",
  "recipient": "string",
  "subject": "string",
  "content": "string",
  "timestamp": "ISO 8601 datetime",
  "attachments": [
    {
      "fileName": "string",
      "mimeType": "string",
      "size": "number"
    }
  ]
}
```

**Response**:
```json
{
  "messageId": "string",
  "status": "NEW|PROCESSED|ROUTED|APPROVAL_PENDING",
  "category": "INQUIRY|ORDER|PAYMENT|GENERAL|URGENT|INFORMATIONAL",
  "priority": "LOW|MEDIUM|HIGH|CRITICAL",
  "tasksCreated": ["taskId1", "taskId2"],
  "needsApproval": "boolean",
  "nextAction": "ROUTE|APPROVE|COMPLETE"
}
```

#### Get Message Details
```
GET /api/messages/{messageId}
```

**Description**: Retrieve detailed information about a specific message.

**Response**:
```json
{
  "id": "string",
  "channelId": "GMAIL|WHATSAPP|FILE_DROP",
  "externalId": "string",
  "sender": "string",
  "recipient": "string",
  "subject": "string",
  "content": "string",
  "timestamp": "ISO 8601 datetime",
  "priority": "LOW|MEDIUM|HIGH|CRITICAL",
  "category": "INQUIRY|ORDER|PAYMENT|GENERAL|URGENT|INFORMATIONAL",
  "status": "NEW|PROCESSED|ROUTED|APPROVAL_PENDING",
  "relatedTasks": ["taskId1", "taskId2"],
  "attachments": [...],
  "metadata": {}
}
```

### Task Management API

#### Create Task
```
POST /api/tasks
```

**Description**: Create a new task based on processed message or system event.

**Request Body**:
```json
{
  "title": "string (3-200 chars)",
  "description": "string",
  "category": "NEEDS_ACTION|PLAN|DONE|PENDING_APPROVAL|REJECTED",
  "priority": "LOW|MEDIUM|HIGH|CRITICAL",
  "sourceMessageId": "string (optional)",
  "dueDate": "ISO 8601 datetime (optional)",
  "assignee": "string (optional)"
}
```

**Response**:
```json
{
  "taskId": "string",
  "status": "CREATED|IN_PROGRESS|COMPLETED|CANCELLED|FAILED",
  "createdAt": "ISO 8601 datetime",
  "updatedAt": "ISO 8601 datetime"
}
```

#### Update Task Status
```
PUT /api/tasks/{taskId}/status
```

**Request Body**:
```json
{
  "status": "IN_PROGRESS|COMPLETED|CANCELLED|FAILED",
  "notes": "string (optional)"
}
```

**Response**:
```json
{
  "taskId": "string",
  "status": "IN_PROGRESS|COMPLETED|CANCELLED|FAILED",
  "updatedAt": "ISO 8601 datetime",
  "result": "SUCCESS|FAILURE"
}
```

### Approval System API

#### Request Approval
```
POST /api/approvals/request
```

**Description**: Submit an item for human approval (payment, invoice, bulk communication).

**Request Body**:
```json
{
  "requestType": "PAYMENT|INVOICE|BULK_EMAIL|SOCIAL_POST",
  "amount": "number (for payments)",
  "recipient": "string",
  "details": "string",
  "priority": "HIGH|CRITICAL",
  "expiresAt": "ISO 8601 datetime"
}
```

**Response**:
```json
{
  "approvalRequestId": "string",
  "status": "PENDING|APPROVED|REJECTED",
  "placedInFolder": "Pending_Approval",
  "estimatedProcessingTime": "ISO 8601 duration"
}
```

#### Approve/Reject Request
```
POST /api/approvals/{approvalRequestId}/{action}
```

**Path Parameters**:
- `approvalRequestId`: The ID of the approval request
- `action`: "approve" or "reject"

**Request Body**:
```json
{
  "reason": "string (required for rejection)"
}
```

**Response**:
```json
{
  "approvalRequestId": "string",
  "action": "APPROVED|REJECTED",
  "processedAt": "ISO 8601 datetime",
  "result": "SUCCESS|FAILURE"
}
```

### Audit Logging API

#### Log Action
```
POST /api/audit/log
```

**Description**: Log a system action for audit trail.

**Request Body**:
```json
{
  "service": "string (service/component name)",
  "action": "string (action type)",
  "entityIds": ["string"],
  "beforeState": {},
  "afterState": {},
  "result": "SUCCESS|FAILURE|APPROVAL_REQUIRED|REJECTED",
  "details": {},
  "sensitive": "boolean (default: false)"
}
```

**Response**:
```json
{
  "logId": "string",
  "timestamp": "ISO 8601 datetime",
  "result": "LOGGED|REJECTED (if violates security)"
}
```

#### Query Audit Logs
```
GET /api/audit/logs
```

**Query Parameters**:
- `startDate`: ISO 8601 datetime
- `endDate`: ISO 8601 datetime
- `service`: string
- `action`: string
- `entityId`: string
- `limit`: number (default: 100)
- `offset`: number (default: 0)

**Response**:
```json
{
  "logs": [
    {
      "id": "string",
      "timestamp": "ISO 8601 datetime",
      "service": "string",
      "action": "string",
      "entityIds": ["string"],
      "result": "SUCCESS|FAILURE|APPROVAL_REQUIRED|REJECTED",
      "details": {},
      "sensitive": "boolean"
    }
  ],
  "total": "number",
  "hasMore": "boolean"
}
```

## External Service Adapters (MCP)

### Gmail MCP Adapter Contract

The Gmail adapter implements the standard MCP protocol for email services:

```
Service: mcp://gmail.adapter
Capabilities:
- mail.read: Read emails from inbox
- mail.send: Send outgoing emails
- mail.labels: Manage email labels/folders
- mail.search: Search emails by criteria
```

### WhatsApp MCP Adapter Contract

The WhatsApp adapter implements the standard MCP protocol for messaging services:

```
Service: mcp://whatsapp.adapter
Capabilities:
- message.read: Read incoming messages
- message.send: Send outgoing messages
- message.attachments: Handle message attachments
- contact.info: Access contact information
```

### File System MCP Adapter Contract

The file system adapter implements the standard MCP protocol for file operations:

```
Service: mcp://filesystem.adapter
Capabilities:
- fs.watch: Monitor file system changes
- fs.read: Read file contents
- fs.write: Write file contents
- fs.move: Move/rename files
- fs.encrypt: Encrypt file contents
- fs.decrypt: Decrypt file contents
```

## Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "string (error code)",
    "message": "string (human-readable message)",
    "details": "object (optional, specific error details)",
    "timestamp": "ISO 8601 datetime",
    "correlationId": "string (for tracing)"
  }
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Request validation failed
- `AUTHENTICATION_FAILED`: Authentication required or failed
- `AUTHORIZATION_DENIED`: Insufficient permissions
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `SERVICE_UNAVAILABLE`: External service unavailable
- `RATE_LIMIT_EXCEEDED`: Rate limit reached
- `ENCRYPTION_ERROR`: Encryption/decryption failed
- `AUDIT_LOGGING_FAILED`: Failed to log audit entry