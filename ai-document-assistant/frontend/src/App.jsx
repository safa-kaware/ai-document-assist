import { useEffect, useState } from 'react'
import Header from './components/Header'
import UploadArea from './components/UploadArea'
import QuestionBox from './components/QuestionBox'
import { checkBackendHealth } from './services/api'

function App() {
  const [backendStatus, setBackendStatus] = useState('checking')

  useEffect(() => {
    checkBackendHealth()
      .then(() => setBackendStatus('connected'))
      .catch(() => setBackendStatus('error'))
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-3xl mx-auto px-4 py-8 space-y-6">
        <div className="text-sm">
          Backend status:{' '}
          {backendStatus === 'checking' && (
            <span className="text-gray-500">checking...</span>
          )}
          {backendStatus === 'connected' && (
            <span className="text-green-600 font-medium">connected ✅</span>
          )}
          {backendStatus === 'error' && (
            <span className="text-red-600 font-medium">
              not reachable ❌ — is the backend running?
            </span>
          )}
        </div>

        <UploadArea />
        <QuestionBox />

        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <h2 className="text-sm font-semibold text-gray-700 mb-2">Answer</h2>
          <p className="text-sm text-gray-400">
            Answers will appear here once the chat pipeline is built
          </p>
        </div>
      </main>
    </div>
  )
}

export default App