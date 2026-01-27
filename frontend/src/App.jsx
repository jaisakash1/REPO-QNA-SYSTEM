import { useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

function App() {
  // State
  const [repoUrl, setRepoUrl] = useState('')
  const [repoName, setRepoName] = useState('')
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isIngesting, setIsIngesting] = useState(false)
  const [isQuerying, setIsQuerying] = useState(false)
  const [ingestStatus, setIngestStatus] = useState(null)
  const [queryStatus, setQueryStatus] = useState(null)
  const [chunkCount, setChunkCount] = useState(0)

  // Ingest repository
  const handleIngest = async () => {
    if (!repoUrl.trim()) return

    setIsIngesting(true)
    setIngestStatus({ type: 'loading', message: 'Cloning and processing repository...' })
    setResults([])
    setQueryStatus(null)

    try {
      const response = await fetch(`${API_BASE}/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: repoUrl })
      })

      const data = await response.json()

      if (response.ok) {
        setRepoName(data.repo_name)
        setChunkCount(data.chunk_count)
        setIngestStatus({
          type: 'success',
          message: `Repository processed successfully! ${data.chunk_count} code chunks indexed.`
        })
      } else {
        setIngestStatus({
          type: 'error',
          message: data.detail || 'Failed to process repository'
        })
      }
    } catch (error) {
      setIngestStatus({
        type: 'error',
        message: 'Failed to connect to server. Make sure the API is running.'
      })
    } finally {
      setIsIngesting(false)
    }
  }

  // Query repository
  const handleQuery = async () => {
    if (!query.trim() || !repoName) return

    setIsQuerying(true)
    setQueryStatus({ type: 'loading', message: 'Searching for relevant code...' })

    try {
      const response = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_name: repoName, query: query })
      })

      const data = await response.json()

      if (response.ok) {
        setResults(data.results)
        setQueryStatus({
          type: 'success',
          message: `Found ${data.results.length} matching code snippets`
        })
      } else {
        setQueryStatus({
          type: 'error',
          message: data.detail || 'Failed to query repository'
        })
      }
    } catch (error) {
      setQueryStatus({
        type: 'error',
        message: 'Failed to connect to server. Make sure the API is running.'
      })
    } finally {
      setIsQuerying(false)
    }
  }

  // Calculate similarity percentage from distance
  const getSimilarity = (distance) => {
    // Lower distance = higher similarity
    // Typically distance ranges from 0 to ~2
    const similarity = Math.max(0, Math.min(100, (1 - distance / 2) * 100))
    return similarity.toFixed(0)
  }

  // Get file name from path
  const getFileName = (path) => {
    const parts = path.replace(/\\/g, '/').split('/')
    return parts[parts.length - 1]
  }

  // Get relative path (remove data/repos prefix)
  const getRelativePath = (path) => {
    const normalized = path.replace(/\\/g, '/')
    const match = normalized.match(/data\/repos\/[^/]+\/(.+)/)
    return match ? match[1] : normalized
  }

  // Generate line numbers
  const generateLineNumbers = (code, startLine) => {
    const lines = code.split('\n')
    return lines.map((_, i) => startLine + i).join('\n')
  }

  return (
    <div className="app">
      {/* Background orbs */}
      <div className="bg-orb bg-orb-1"></div>
      <div className="bg-orb bg-orb-2"></div>
      <div className="bg-orb bg-orb-3"></div>

      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">🔍</div>
            <div className="logo-text">
              <h1>Repo QnA</h1>
              <p>Ask questions about any GitHub repository</p>
            </div>
          </div>
          {repoName && (
            <div className="status-badge">
              <span className="status-dot"></span>
              <span>{repoName} ready</span>
            </div>
          )}
        </div>
      </header>

      {/* Main content */}
      <main className="main-content">
        <div className="steps-container">
          {/* Step 1: Enter Repository URL */}
          <div className={`step-card ${repoName ? 'completed' : ''}`}>
            <div className="step-header">
              <div className={`step-number ${repoName ? 'completed' : ''}`}>
                {repoName ? '✓' : '1'}
              </div>
              <h2 className="step-title">Enter Repository URL</h2>
            </div>
            <p className="step-description">
              Paste a GitHub repository URL to index its code for natural language queries.
            </p>
            <div className="input-group">
              <div className="input-wrapper">
                <span className="input-icon">📦</span>
                <input
                  type="text"
                  className="text-input"
                  placeholder="https://github.com/username/repository"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  disabled={isIngesting}
                />
              </div>
              <button
                className="btn btn-primary"
                onClick={handleIngest}
                disabled={isIngesting || !repoUrl.trim()}
              >
                {isIngesting ? (
                  <>
                    <span className="spinner"></span>
                    Processing...
                  </>
                ) : (
                  <>
                    🚀 Index Repository
                  </>
                )}
              </button>
            </div>

            {/* Ingest status */}
            {ingestStatus && (
              <div className={`status-message ${ingestStatus.type}`}>
                {ingestStatus.type === 'loading' && <span className="spinner"></span>}
                {ingestStatus.type === 'success' && <span>✅</span>}
                {ingestStatus.type === 'error' && <span>❌</span>}
                <span>{ingestStatus.message}</span>
              </div>
            )}

            {/* Repo info */}
            {repoName && (
              <div className="repo-info">
                <div className="repo-info-icon">📁</div>
                <div className="repo-info-text">
                  <h3>{repoName}</h3>
                  <p>{chunkCount} code chunks indexed and ready for queries</p>
                </div>
              </div>
            )}
          </div>

          {/* Step 2: Ask Questions */}
          <div className={`step-card ${!repoName ? 'disabled' : ''}`}>
            <div className="step-header">
              <div className="step-number">2</div>
              <h2 className="step-title">Ask Questions</h2>
            </div>
            <p className="step-description">
              Ask natural language questions about the codebase. The system will find the most relevant code snippets.
            </p>
            <div className="input-group">
              <div className="input-wrapper">
                <span className="input-icon">💬</span>
                <input
                  type="text"
                  className="text-input"
                  placeholder="How does authentication work? What handles user login?"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  disabled={!repoName || isQuerying}
                  onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
                />
              </div>
              <button
                className="btn btn-primary"
                onClick={handleQuery}
                disabled={isQuerying || !query.trim() || !repoName}
              >
                {isQuerying ? (
                  <>
                    <span className="spinner"></span>
                    Searching...
                  </>
                ) : (
                  <>
                    🔍 Search
                  </>
                )}
              </button>
            </div>

            {/* Query status */}
            {queryStatus && (
              <div className={`status-message ${queryStatus.type}`}>
                {queryStatus.type === 'loading' && <span className="spinner"></span>}
                {queryStatus.type === 'success' && <span>✅</span>}
                {queryStatus.type === 'error' && <span>❌</span>}
                <span>{queryStatus.message}</span>
              </div>
            )}

            {/* Results */}
            {results.length > 0 && (
              <div className="results-container">
                {results.map((result, index) => (
                  <div
                    key={index}
                    className="result-card"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div className="result-header">
                      <div className="result-file">
                        <span className="result-file-icon">📄</span>
                        <span title={getRelativePath(result.file_path)}>
                          {getRelativePath(result.file_path)}
                        </span>
                      </div>
                      <div className="result-meta">
                        <span className="result-lines">
                          Lines {result.start_line} - {result.end_line}
                        </span>
                        <div className="result-distance">
                          <span>{getSimilarity(result.distance)}% match</span>
                          <div className="distance-bar">
                            <div
                              className="distance-fill"
                              style={{ width: `${getSimilarity(result.distance)}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="result-code">
                      <pre>
                        <div className="code-with-lines">
                          <div className="line-numbers">
                            {generateLineNumbers(result.code, result.start_line)}
                          </div>
                          <code>{result.code}</code>
                        </div>
                      </pre>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Empty state */}
            {repoName && !isQuerying && results.length === 0 && queryStatus?.type !== 'loading' && (
              <div className="empty-state">
                <div className="empty-state-icon">🔍</div>
                <p>Enter a question to search the codebase</p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>Repo QnA • Powered by FAISS & Sentence Transformers</p>
      </footer>
    </div>
  )
}

export default App
