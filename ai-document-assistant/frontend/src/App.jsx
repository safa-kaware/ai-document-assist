import { useEffect, useState } from 'react'
import Header from './components/Header'
import UploadArea from './components/UploadArea'
import DocumentList from './components/DocumentList'
import QuestionBox from './components/QuestionBox'
import AnswerCard from './components/AnswerCard'
import { checkBackendHealth, sendChatMessage, listDocuments } from './services/api'

function App() {
  const [backendStatus, setBackendStatus] = useState('checking')
  const [documents, setDocuments] = useState([])
  const [selectedDocId, setSelectedDocId] = useState(null)
  const [answer, setAnswer] = useState(null)
  const [sources, setSources] = useState([])
  const [isAsking, setIsAsking] = useState(false)
  const [chatError, setChatError] = useState('')

  const refreshDocuments = async () => {
    try {
      const docs = await listDocuments()
      setDocuments(docs)
      return docs
    } catch {
      return []
    }
  }

  useEffect(() => {
    const initialize = async () => {
      try {
        await checkBackendHealth()
        setBackendStatus('connected')
      } catch {
        setBackendStatus('error')
      }
      await refreshDocuments()
    }
    initialize()
  }, [])

  const handleUploadSuccess = async (uploadedDoc) => {
    await refreshDocuments()
    setSelectedDocId(uploadedDoc.id)
    setAnswer(null)
    setSources([])
    setChatError('')
  }

  const handleSelectDocument = (docId) => {
    setSelectedDocId(docId)
    setAnswer(null)
    setSources([])
    setChatError('')
  }

  const handleDocumentDeleted = (deletedId) => {
    setDocuments((prev) => prev.filter((d) => d.id !== deletedId))
    if (selectedDocId === deletedId) {
      setSelectedDocId(null)
      setAnswer(null)
      setSources([])
    }
  }

  const handleAsk = async (question) => {
    setIsAsking(true)
    setChatError('')
    setAnswer(null)

    try {
      const result = await sendChatMessage(selectedDocId, question)
      setAnswer(result.answer)
      setSources(result.sources)
    } catch (err) {
      setChatError(err.message)
    } finally {
      setIsAsking(false)
    }
  }

  return (
    <div className="app-shell">
      <Header status={backendStatus} />

      <main className="app-body">
        <div className="app-body-flex">
          <div className="doc-rail mb-4 mb-md-0">
            <h2 className="panel-label">Documents</h2>
            <UploadArea onUploadSuccess={handleUploadSuccess} />
            <DocumentList
              documents={documents}
              selectedId={selectedDocId}
              onSelect={handleSelectDocument}
              onDeleted={handleDocumentDeleted}
            />
          </div>

          <div className="chat-panel">
            <QuestionBox documentId={selectedDocId} onAsk={handleAsk} isLoading={isAsking} />
            <AnswerCard answer={answer} sources={sources} isLoading={isAsking} error={chatError} />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App