import { useState } from 'react'
import { deleteDocument } from '../services/api'

function DocumentList({ documents, selectedId, onSelect, onDeleted }) {
  const [deletingId, setDeletingId] = useState(null)

  const handleDelete = async (e, docId) => {
    e.stopPropagation()
    setDeletingId(docId)
    try {
      await deleteDocument(docId)
      onDeleted(docId)
    } catch (err) {
      alert(`Failed to delete: ${err.message}`)
    } finally {
      setDeletingId(null)
    }
  }

  if (documents.length === 0) {
    return (
      <div className="doc-list">
        <p className="empty-state">No documents uploaded yet</p>
      </div>
    )
  }

  return (
    <div className="doc-list">
      {documents.map((doc) => (
        <div
          key={doc.id}
          onClick={() => onSelect(doc.id)}
          className={`doc-item ${doc.id === selectedId ? 'selected' : ''}`}
        >
          <div className="flex-grow-1 min-w-0">
            <p className="doc-name">{doc.filename}</p>
            <p className="doc-meta">
              {doc.pages_with_text}/{doc.page_count} pages · {(doc.size_bytes / 1024).toFixed(1)} KB
            </p>
          </div>
          <button
            onClick={(e) => handleDelete(e, doc.id)}
            disabled={deletingId === doc.id}
            className="delete-btn"
          >
            {deletingId === doc.id ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      ))}
    </div>
  )
}

export default DocumentList