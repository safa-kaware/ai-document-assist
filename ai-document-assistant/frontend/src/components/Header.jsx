function Header({ status }) {
  const statusConfig = {
    checking: { cls: 'checking', label: 'checking...' },
    connected: { cls: 'connected', label: 'connected' },
    error: { cls: 'error', label: 'not reachable — is the backend running?' },
  }
  const current = statusConfig[status]

  return (
    <header className="app-header">
      <div className="container-lg d-flex flex-column flex-sm-row justify-content-between align-items-sm-end gap-1">
        <div>
          <h1 className="wordmark">AI Document Assistant</h1>
          <p className="tagline">Upload a document and ask questions about it</p>
        </div>
        <div className="d-flex align-items-center small text-secondary">
          <span className={`status-dot ${current.cls}`} />
          {current.label}
        </div>
      </div>
    </header>
  )
}

export default Header
