import { useState } from 'react'
import { uploadDocument } from '../services/api'

function UploadArea() {
  const [status, setStatus] = useState('idle') // idle | uploading | success | error
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
    } catch (err) {
      setErrorMessage(err.message)
      setStatus('error')
    }
  }

  return (
    <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center bg-white">
      <input
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
        className="block mx-auto text-sm text-gray-600"
      />

      {status === 'uploading' && (
        <p className="mt-3 text-sm text-gray-500">Uploading and extracting text...</p>
      )}

      {status === 'success' && uploadedDoc && (
        <div className="mt-3 text-sm text-green-600 font-medium">
          ✅ {uploadedDoc.filename} uploaded ({(uploadedDoc.size_bytes / 1024).toFixed(1)} KB)
          <div className="text-gray-500 font-normal mt-1">
            {uploadedDoc.pages_with_text} of {uploadedDoc.page_count} pages have extractable text
          </div>
        </div>
      )}

      {status === 'error' && (
        <p className="mt-3 text-sm text-red-600 font-medium">❌ {errorMessage}</p>
      )}
    </div>
  )
}

export default UploadArea