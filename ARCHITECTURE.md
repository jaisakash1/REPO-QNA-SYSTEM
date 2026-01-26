# Architecture Documentation

## System Overview

The GitHub Repository Q&A System is a Retrieval-Augmented Generation (RAG) application that enables semantic search and natural language queries over GitHub repositories.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │   Repo Form  │  │  Query Form  │  │   Answer Display    │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└────────────┬────────────────┬────────────────────────┬──────────┘
             │                │                        │
             ▼                ▼                        ▼
┌────────────────────────────────────────────────────────────────┐
│                                   │
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │  process-repository      │  │  query-repository        │   │
│  │  • Clone repo           │  │  • Embed query           │   │
│  │  • Extract files        │  │  • Vector search         │   │
│  │  • Chunk code           │  │  • RAG generation        │   │
│  │  • Generate embeddings  │  │  • Store results         │   │
│  └──────────────────────────┘  └──────────────────────────┘   │
└────────────┬────────────────────────────┬─────────────────────You are an expert full-stack and AI engineer specializing in building RAG systems, code analysis tools, and developer agents.

Your mission is to help me build a GitHub Repository Q&A System step-by-step.

The system goal: ---------------------------------------- User enters a GitHub repo URL → system clones repo → cleans folders → extracts text/code → chunks → embeds → stores vectors in FAISS or ChromaDB → user asks a question → semantic search retrieves relevant chunks → send to Gemini or OpenAI → structured answer returned. ---------------------------------------- ### PROJECT REQUIREMENTS
Follow this implementation pipeline:

Repo Ingestion

Accept GitHub URL
Clone repo locally
Exclude useless folders (node_modules, build, dist, .git, binary files)
Extract only relevant file types: .md, .py, .js, .ts, .go, .java, .cpp, .html, .json, etc.
Chunking

Use RecursiveCharacterTextSplitter (or equivalent) with:
chunk_size ~ 512–1024 tokens
chunk_overlap ~ 50 tokens
Store metadata: file_path, start_line, end_line, language, chunk_id
Embedding

Use Gemini embeddings
For each chunk produce embedding vector
Vector Storage

Use FAISS 
Store embeddings + metadata
Ensure persistent storage when possible
Query Processing

User enters natural language question (e.g., "What authentication is implemented?")
Embed the query
Search vector DB for top-k similar chunks (k=5 or k=10)
LLM Answer Generation

Build a RAG prompt that contains:
User question
Retrieved chunks as context
Send to Gemini to generate answer
If context insufficient, say "Not enough repository context to answer"
Post-processing

Convert answer into structured developer-friendly output:
Authentication type (if applicable)
Frameworks used
Dependencies
Relevant files
Explanation
### REQUIRED OUTPUT FORMAT FROM YOU
When responding, always produce:

Explanation of what's happening
Exact code for that step
Dependencies to install
Folder structure updates
Next action instruction
Example formatting:

Step 2 — Chunking Implementation -----------------------------------
Explanation: ...
Folder Structure Update: ...
Dependencies: ...
Code:┘
             │                            │
             ▼                            ▼
┌────────────────────────────────────────────────────────────────┐
│                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ repositories │  │ code_chunks  │  │   queries    │        │
│  │              │  │ + embeddings │  │              │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────────────────────────────────────────────────┘
             │                            │
             └────────────┬───────────────┘
                          ▼
                    ┌──────────┐
                    │ GEMINI  │
                    │ API      │
                    └──────────┘
```

## Data Flow

### Repository Processing Pipeline

```
1. User Input
   └─> GitHub URL submitted

2. Database Insert
   └─> Create repository record (status: pending)

3. Background Processing (Edge Function)
   ├─> Clone repository with git
   ├─> Walk directory tree
   ├─> Filter files (exclude node_modules, etc.)
   ├─> For each file:
   │   ├─> Read content
   │   ├─> Detect language
   │   ├─> Chunk text (800 chars, 100 overlap)
   │   ├─> For each chunk:
   │   │   ├─> Generate embedding (OpenAI)
   │   │   ├─> Extract metadata
   │   │   └─> Store in code_chunks table
   │   └─> Next chunk
   └─> Update repository (status: completed)

4. UI Update
   └─> Poll database for status changes
   └─> Display completed repository
```

### Query Processing Pipeline

```
1. User Question
   └─> Natural language input

2. Question Embedding
   └─> Generate vector embedding (OpenAI)

3. Vector Similarity Search
   ├─> Search code_chunks table
   ├─> Use HNSW index for fast search
   ├─> Return top-K similar chunks (K=10)
   └─> Include similarity scores

4. Context Assembly
   ├─> Format retrieved chunks
   ├─> Include file paths and line numbers
   └─> Build RAG prompt

5. LLM Generation
   ├─> Send to GPT-4-mini
   ├─> System prompt defines structure
   ├─> Generate structured JSON answer
   └─> Parse and validate response

6. Result Storage
   ├─> Store query in database
   ├─> Save retrieved chunks
   ├─> Record processing time
   └─> Return to frontend

7. Display Answer
   └─> Render structured output
   └─> Show relevant files
   └─> Display context chunks
```

## Component Breakdown

### Frontend Components

#### RepoIngestionForm.tsx
- **Purpose:** Accept GitHub repository URLs
- **State:** URL input, loading, error messages
- **Actions:**
  - Validate URL format
  - Extract repo name (owner/repo)
  - Insert into database
  - Trigger background processing
- **Dependencies:** Supabase client

#### RepositoryList.tsx
- **Purpose:** Display all repositories with status
- **State:** Repository list, loading, selected repo
- **Actions:**
  - Fetch repositories from database
  - Auto-refresh on status changes
  - Handle repository selection
- **Features:**
  - Status icons (pending, processing, completed, failed)
  - File and chunk counts
  - Error message display

#### QueryInterface.tsx
- **Purpose:** Accept user questions
- **State:** Question input, loading, error
- **Actions:**
  - Submit question to Edge Function
  - Handle response
  - Display errors
- **Features:**
  - Example questions
  - Real-time feedback
  - Disabled when no repo selected

#### AnswerDisplay.tsx
- **Purpose:** Render structured answers
- **State:** Query result object
- **Features:**
  - Parse JSON answer
  - Display all fields conditionally
  - Show relevant files
  - Display context chunks with similarity scores
  - Processing time indicator

### Backend Functions

#### process-repository/index.ts

**Input:**
```typescript
{
  repository_id: string
}
```

**Process:**
1. Fetch repository from database
2. Update status to 'processing'
3. Clone repository using git command
4. Walk directory tree recursively
5. Filter by file extensions and folders
6. For each file:
   - Read text content
   - Split into chunks
   - Generate embeddings
   - Store chunks with metadata
7. Update repository status and counts
8. Clean up temporary files

**Output:**
```typescript
{
  success: boolean,
  repository_id: string,
  total_files: number,
  total_chunks: number
}
```

**Error Handling:**
- Catches all errors
- Updates repository status to 'failed'
- Stores error message
- Cleans up temp directory

#### query-repository/index.ts

**Input:**
```typescript
{
  repository_id: string,
  question: string
}
```

**Process:**
1. Authenticate user from JWT token
2. Verify repository is completed
3. Generate question embedding
4. Call search_similar_chunks function
5. Format chunks as context
6. Build RAG prompt
7. Call GPT-4-mini API
8. Parse JSON response
9. Store query and results
10. Return answer

**Output:**
```typescript
{
  query_id: string,
  answer: string, // JSON string
  retrieved_chunks: Chunk[],
  processing_time_ms: number
}
```

**Error Handling:**
- Validates repository status
- Handles empty search results
- Catches OpenAI API errors
- Returns structured error messages

## Database Schema

### repositories

| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| github_url | text | Full GitHub URL |
| repo_name | text | owner/repo format |
| status | text | pending, processing, completed, failed |
| total_files | integer | Number of files processed |
| total_chunks | integer | Number of chunks created |
| error_message | text | Error details if failed |
| created_at | timestamptz | When added |
| processed_at | timestamptz | When completed |
| user_id | uuid | User who added repo |

**Indexes:**
- Primary key on id
- Unique on github_url
- Index on status
- Index on user_id
- Index on created_at (DESC)

### code_chunks

| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| repository_id | uuid | Foreign key to repositories |
| file_path | text | Relative path in repo |
| content | text | Chunk text content |
| language | text | Programming language |
| start_line | integer | Starting line number |
| end_line | integer | Ending line number |
| chunk_index | integer | Chunk number in file |
| chunk_size | integer | Character count |
| embedding | vector(1536) | OpenAI embedding vector |
| metadata | jsonb | Additional metadata |
| created_at | timestamptz | When created |

**Indexes:**
- Primary key on id
- Foreign key on repository_id
- Index on language
- Index on file_path
- **HNSW index on embedding** (most important!)

### queries

| Column | Type | Description |
|--------|------|-------------|
| id | uuid | Primary key |
| repository_id | uuid | Foreign key to repositories |
| user_id | uuid | User who asked |
| question | text | User's question |
| answer | text | JSON structured answer |
| retrieved_chunks | jsonb | Array of chunk objects |
| model_used | text | LLM model name |
| processing_time_ms | integer | Query duration |
| created_at | timestamptz | When asked |

**Indexes:**
- Primary key on id
- Foreign key on repository_id
- Index on user_id
- Index on created_at (DESC)

## Vector Search Details

### HNSW Index Configuration

```sql
CREATE INDEX idx_code_chunks_embedding ON code_chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

**Parameters:**
- `m = 16`: Number of bi-directional links per node
  - Higher = better recall, more memory
  - 16 is a good balance for most use cases

- `ef_construction = 64`: Size of dynamic candidate list during construction
  - Higher = better index quality, slower build
  - 64 provides good quality without excessive build time

**Distance Metric:**
- Using cosine distance (`vector_cosine_ops`)
- Formula: `1 - (A · B) / (||A|| × ||B||)`
- Range: 0 (identical) to 2 (opposite)

### Search Function

```sql
CREATE FUNCTION search_similar_chunks(
  query_embedding vector(1536),
  repo_id uuid,
  match_threshold float DEFAULT 0.5,
  match_count int DEFAULT 10
)
```

**Parameters:**
- `query_embedding`: The question's vector representation
- `repo_id`: Limit search to specific repository
- `match_threshold`: Minimum similarity (0.5 = 50% similar)
- `match_count`: Number of results to return

**Performance:**
- Sub-linear time complexity: O(log n)
- Approximate nearest neighbor search
- Trade-off: Speed vs. accuracy (tunable)

## Security

### Row Level Security (RLS)

All tables have RLS enabled with policies:

**repositories:**
- Anyone can SELECT (read all repos)
- Users can INSERT their own repos
- Users can UPDATE only their repos

**code_chunks:**
- Anyone can SELECT (needed for search)
- Only repo owner can INSERT chunks

**queries:**
- Users can only SELECT their own queries
- Users can only INSERT their own queries

### Authentication

Currently using Supabase Auth:
- JWT tokens in Authorization header
- User ID extracted from token
- Validated on each request

## API Integration

### OpenAI API

**Embeddings:**
- Model: `text-embedding-3-small`
- Dimensions: 1536
- Cost: ~$0.002 per 1K tokens
- Rate limit: 5000 requests/minute (tier dependent)

**Chat Completions:**
- Model: `gpt-4o-mini`
- Max tokens: 1500
- Temperature: 0.3 (more deterministic)
- Cost: ~$0.15 per 1M input tokens

### Error Handling

All API calls wrapped in try-catch blocks:
```typescript
try {
  const response = await fetch(openaiUrl, {...});
  if (!response.ok) throw new Error();
  return data;
} catch (error) {
  // Handle error, update status, return error response
}
```

## Performance Characteristics

### Repository Processing

**Time Complexity:**
- File walking: O(n) where n = number of files
- Chunking: O(m) where m = total characters
- Embedding: O(k) where k = number of chunks
- **Total: O(n + m + k)**

**Typical Times:**
- Small repo (10-50 files): 30 seconds - 2 minutes
- Medium repo (100-500 files): 3-10 minutes
- Large repo (1000+ files): 15-30 minutes

### Query Processing

**Time Complexity:**
- Embedding generation: O(1) - constant time
- Vector search: O(log n) - sub-linear with HNSW
- LLM generation: O(context_length)
- **Total: O(log n + context_length)**

**Typical Times:**
- Query processing: 2-5 seconds
- Most time spent in LLM generation
- Vector search typically <100ms

## Scalability Considerations

### Database
- pgvector scales to millions of vectors
- HNSW index supports fast search at scale
- Partition by repository for very large datasets

### Edge Functions
- Stateless, horizontally scalable
- Isolated execution per request
- Automatic scaling by Supabase

### Costs
- Primary cost: OpenAI API usage
- Grows linearly with repositories and queries
- Consider caching for repeated queries

## Monitoring and Observability

### Metrics to Track

1. **Repository Processing:**
   - Success/failure rate
   - Processing time per repo
   - Average chunks per file
   - Error rates by type

2. **Query Performance:**
   - Query latency (p50, p95, p99)
   - Search result quality (user feedback)
   - LLM response time
   - Cache hit rate (if implemented)

3. **Cost Metrics:**
   - OpenAI API usage
   - Tokens consumed
   - Cost per repository
   - Cost per query

4. **Database:**
   - Query performance
   - Index effectiveness
   - Storage growth rate
   - Connection pool usage

### Logging

Edge Functions log to Supabase dashboard:
- Request/response payloads
- Error stack traces
- Processing milestones
- Performance timings

## Future Architecture Enhancements

1. **Caching Layer:**
   - Cache embeddings for common queries
   - Cache LLM responses
   - Implement Redis or similar

2. **Queue System:**
   - Move repo processing to job queue
   - Enable retry logic
   - Support priority processing

3. **Multi-tenancy:**
   - Isolate user data
   - Per-user quotas
   - Team workspaces

4. **Advanced Search:**
   - Hybrid search (vector + keyword)
   - Filter by file type, language
   - Time-based relevance

5. **Real-time Updates:**
   - WebSocket connections
   - Live processing status
   - Collaborative queries

