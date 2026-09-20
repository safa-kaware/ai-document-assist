import { useState } from 'react'
import { uploadDocument } from '../services/api'

function UploadArea({ onUploadSuccess }) {
  const [status, setStatus] = useState('idle')
  const [errorMessage, setErrorMessage] = useState('')
  const [uploadedDoc, setUploadedDoc] = useState(null)

  const handleFileChange = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    setStatus('uploading')
    setErrorMessage('')

    try {
      const result = await uploadDocument(file)
      setUploadedDoc(result)
      setStatus('success')
      onUploadSuccess(result)
    } catch (err) {
      setErrorMessage(err.message)
      setStatus('error')
    }
  }

  return (
    <div className="upload-box">
      <input type="file" accept=".pdf" onChange={handleFileChange} className="form-control form-control-sm" />

      {status === 'uploading' && (
        <p className="upload-status">Uploading and extracting text...</p>
      )}

      {status === 'success' && uploadedDoc && (
        <div className="upload-status success">
          {uploadedDoc.filename} uploaded ({(uploadedDoc.size_bytes / 1024).toFixed(1)} KB)
          <div className="detail">
            {uploadedDoc.pages_with_text} of {uploadedDoc.page_count} pages have extractable text
          </div>
        </div>
      )}

      {status === 'error' && (
        <p className="upload-status error">{errorMessage}</p>
      )}
    </div>
  )
}

export default UploadArea