# Data Model: Personal AI Employee

## Entity Models

### MessageEntity
Represents a message from any communication channel.

```typescript
interface MessageEntity {
  id: string;                    // Unique identifier
  channelId: ChannelType;        // Source channel (GMAIL, WHATSAPP, FILE_DROP)
  externalId: string;            // Original message ID from source
  sender: string;                // Sender identifier
  recipient?: string;            // Recipient identifier (for outgoing)
  subject?: string;              // Subject/title of message
  content: string;               // Message content
  timestamp: Date;               // When received/sent
  priority: PriorityLevel;       // LOW, MEDIUM, HIGH, CRITICAL
  category: MessageCategory;     // INQUIRY, ORDER, PAYMENT, GENERAL, URGENT
  status: MessageStatus;         // NEW, PROCESSED, ROUTED, APPROVAL_PENDING
  metadata: Record<string, any>; // Channel-specific metadata
  attachments?: Attachment[];    // Associated file attachments
}
```

### TaskEntity
Represents a task derived from messages or system events.

```typescript
interface TaskEntity {
  id: string;                    // Unique identifier
  title: string;                 // Task title
  description: string;           // Detailed description
  sourceMessageId?: string;      // Originating message ID (if applicable)
  category: TaskCategory;        // NEEDS_ACTION, PLAN, DONE, PENDING_APPROVAL, REJECTED
  priority: PriorityLevel;       // LOW, MEDIUM, HIGH, CRITICAL
  assignee?: string;             // Assigned user (if known)
  dueDate?: Date;                // Deadline
  status: TaskStatus;            // CREATED, IN_PROGRESS, COMPLETED, CANCELLED
  createdAt: Date;               // Creation timestamp
  updatedAt: Date;               // Last update timestamp
  metadata: Record<string, any>; // Task-specific metadata
}
```

### CredentialEntity
Represents secure credential storage.

```typescript
interface CredentialEntity {
  id: string;                    // Unique identifier
  serviceType: ServiceType;      // GMAIL, WHATSAPP_BUSINESS, BANK_API, etc.
  encryptedData: string;         // Encrypted credential data
  encryptionKeyReference: string; // Reference to encryption key
  createdAt: Date;               // Creation timestamp
  lastAccessedAt: Date;          // Last access timestamp
  expiresAt?: Date;              // Expiration timestamp (if applicable)
  isActive: boolean;             // Whether credential is currently active
}
```

### AuditLogEntry
Represents an auditable system action.

```typescript
interface AuditLogEntry {
  id: string;                    // Unique identifier
  timestamp: Date;               // When action occurred
  userId?: string;               // User responsible (if human action)
  service: string;               // Service/component that performed action
  action: string;                // Type of action (PROCESS_MESSAGE, ROUTE_TASK, etc.)
  entityIds: string[];           // Affected entity IDs
  beforeState?: any;             // State before action (if applicable)
  afterState?: any;              // State after action (if applicable)
  result: ActionResult;          // SUCCESS, FAILURE, APPROVAL_REQUIRED
  details: Record<string, any>;  // Additional action details
  sensitive: boolean;            // Whether entry contains sensitive data
}
```

## Value Objects

### PriorityLevel
```typescript
enum PriorityLevel {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL'
}
```

### ChannelType
```typescript
enum ChannelType {
  GMAIL = 'GMAIL',
  WHATSAPP = 'WHATSAPP',
  FILE_DROP = 'FILE_DROP'
}
```

### MessageCategory
```typescript
enum MessageCategory {
  INQUIRY = 'INQUIRY',
  ORDER = 'ORDER',
  PAYMENT = 'PAYMENT',
  GENERAL = 'GENERAL',
  URGENT = 'URGENT',
  INFORMATIONAL = 'INFORMATIONAL'
}
```

### MessageStatus
```typescript
enum MessageStatus {
  NEW = 'NEW',
  PROCESSED = 'PROCESSED',
  ROUTED = 'ROUTED',
  APPROVAL_PENDING = 'APPROVAL_PENDING',
  ESCALATED = 'ESCALATED'
}
```

### TaskCategory
```typescript
enum TaskCategory {
  NEEDS_ACTION = 'NEEDS_ACTION',
  PLAN = 'PLAN',
  DONE = 'DONE',
  PENDING_APPROVAL = 'PENDING_APPROVAL',
  REJECTED = 'REJECTED'
}
```

### TaskStatus
```typescript
enum TaskStatus {
  CREATED = 'CREATED',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED',
  FAILED = 'FAILED'
}
```

### ServiceType
```typescript
enum ServiceType {
  GMAIL = 'GMAIL',
  WHATSAPP_BUSINESS = 'WHATSAPP_BUSINESS',
  BANK_API = 'BANK_API',
  FILE_SYSTEM = 'FILE_SYSTEM'
}
```

### ActionResult
```typescript
enum ActionResult {
  SUCCESS = 'SUCCESS',
  FAILURE = 'FAILURE',
  APPROVAL_REQUIRED = 'APPROVAL_REQUIRED',
  REJECTED = 'REJECTED'
}
```

### Attachment
```typescript
interface Attachment {
  id: string;
  fileName: string;
  mimeType: string;
  size: number;
  downloadUrl?: string;
  localPath?: string;
  encrypted: boolean;
}
```

## Relationships

### Message to Task
- One message can generate multiple tasks (1:N)
- Messages with payment/invoice content create approval tasks
- Inquiry messages may create follow-up tasks

### Task to Audit Log
- One task may have multiple audit entries (1:N)
- Each task status change is logged
- Approval actions are recorded

### Credential to Service
- One credential per service instance (1:1)
- Credentials tied to specific service types
- Audit trail for credential usage

## Validation Rules

### MessageEntity Validation
- Content must not exceed 10,000 characters
- Timestamp must be within reasonable range
- ChannelId must be a valid ChannelType
- Priority must be a valid PriorityLevel

### TaskEntity Validation
- Title must be 3-200 characters
- Category must be a valid TaskCategory
- Priority must be a valid PriorityLevel
- Due date cannot be in the past (for new tasks)

### CredentialEntity Validation
- ServiceType must be a valid ServiceType
- EncryptedData must be properly formatted
- Expiration date must be in the future (if provided)

### AuditLogEntry Validation
- Timestamp must be current or past
- Action must be a recognized system action
- Result must be a valid ActionResult

## State Transitions

### Message States
```
NEW -> PROCESSED -> ROUTED
         |
         v
    APPROVAL_PENDING -> PROCESSED (after approval)
         |
         v
      ESCALATED
```

### Task States
```
CREATED -> IN_PROGRESS -> COMPLETED
   |                        |
   |                        v
   +-> CANCELLED <- FAILED  SUCCESS
   |
   +-> APPROVAL_PENDING -> COMPLETED (after approval)
```

## Indexes

### MessageEntity
- channelId + timestamp (for chronological retrieval)
- priority + status (for prioritized processing)
- category + status (for categorized views)

### TaskEntity
- category + status (for dashboard views)
- assignee + status (for assignment tracking)
- dueDate + priority (for deadline management)

### AuditLogEntry
- timestamp (for chronological audit trail)
- service + action (for operational monitoring)
- entityIds (for entity-specific audit trail)