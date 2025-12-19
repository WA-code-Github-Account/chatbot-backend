# Data Model: RAG System

## Document Model

**Entity**: Document
- id: UUID (Primary Key)
- title: String (max 255 characters)
- content: Text (full document content)
- metadata: JSON (author, creation date, source, etc.)
- upload_date: DateTime (timestamp when document was uploaded)
- source_type: String (PDF, text, web page, etc.)
- user_id: UUID (Foreign Key to User table)
- page_count: Integer (number of pages in document)

## DocumentChunk Model

**Entity**: DocumentChunk
- id: UUID (Primary Key)
- document_id: UUID (Foreign Key to Document table)
- content: Text (chunk content, max 1000 tokens)
- chunk_order: Integer (order number of this chunk in the document)
- metadata: JSON (chunk-specific metadata)
- embedding_id: String (ID in Qdrant vector database)
- token_count: Integer (number of tokens in the chunk)

## UserQuery Model

**Entity**: UserQuery
- id: UUID (Primary Key)
- query_text: Text (the original query from the user)
- user_id: UUID (Foreign Key to User table)
- timestamp: DateTime (when the query was made)
- response: Text (the generated response)
- source_citations: JSON (list of source citations in the format [Source: document_name, page/section])
- response_time_ms: Integer (time taken to generate response)
- language: String ('en' or 'ur' for English or Urdu)

## User Model

**Entity**: User
- id: UUID (Primary Key)
- username: String (unique username)
- email: String (unique email address)
- oauth2_token: String (JWT token)
- role: String (enum: 'user', 'admin', 'moderator')
- created_at: DateTime (when user account was created)
- last_login: DateTime (when user last logged in)

## Session Model

**Entity**: Session
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User table)
- session_token: String (session identifier)
- created_at: DateTime (session creation time)
- expires_at: DateTime (session expiration time)
- active: Boolean (whether session is still active)

## API Contract Model

**Entity**: APIContract
- id: UUID (Primary Key)
- name: String (name of the API endpoint)
- version: String (API version)
- schema: JSON (OpenAPI schema definition)
- created_at: DateTime

## Relationships

1. **User → Document**: One-to-Many
   - A user can upload many documents
   - A document belongs to one user

2. **Document → DocumentChunk**: One-to-Many
   - A document contains many chunks
   - A chunk belongs to one document

3. **User → UserQuery**: One-to-Many
   - A user can make many queries
   - A query is made by one user

4. **User → Session**: One-to-Many
   - A user can have many sessions
   - A session belongs to one user

## Validation Rules

1. **Document Model**:
   - Title is required and must be 1-255 characters
   - Content is required
   - Source type must be one of: 'PDF', 'text', 'web page', 'docx'
   - Document size must be <= 10MB
   - User ID must reference an existing user

2. **DocumentChunk Model**:
   - Content is required
   - Chunk order is required and must be >= 0
   - Token count must be between 1 and 1000
   - Document ID must reference an existing document

3. **UserQuery Model**:
   - Query text is required
   - User ID must reference an existing user
   - Language must be 'en' or 'ur'
   - Response time must be >= 0

4. **User Model**:
   - Username is required and unique
   - Email is required, valid format, and unique
   - Role must be 'user', 'admin', or 'moderator'

## State Transitions

1. **User Account States**:
   - Registration → Active (after email verification)
   - Active → Suspended (by admin action)
   - Suspended → Active (by admin action)
   - Any state → Deleted (by user request or admin action)

2. **Session States**:
   - Created → Active (when user logs in)
   - Active → Expired (when session time expires)
   - Active → Ended (when user logs out)

## Indexes

1. **Document Table**:
   - Index on user_id for efficient user document queries
   - Index on upload_date for chronological sorting

2. **DocumentChunk Table**:
   - Index on document_id for efficient document chunk retrieval
   - Index on embedding_id for efficient vector database lookups

3. **UserQuery Table**:
   - Index on user_id for efficient user query history
   - Index on timestamp for chronological sorting
   - Index on language for language-specific analytics

4. **User Table**:
   - Index on email for efficient login
   - Index on role for permission checks