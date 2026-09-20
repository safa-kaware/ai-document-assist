import { useState } from 'react'

function QuestionBox({ documentId, onAsk, isLoading }) {
  const [question, setQuestion] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!question.trim() || !documentId || isLoading) return
    onAsk(question)
    setQuestion('')
  }

  const disabled = !documentId || isLoading

  return (
    <form onSubmit={handleSubmit} className="question-box">
      <div className="d-flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={documentId ? 'Ask a question about your document...' : 'Select a document first...'}
          disabled={disabled}
          className="form-control flex-grow-1"
        />
        <button type="submit" disabled={disabled || !question.trim()} className="ask-btn">
          {isLoading ? 'Asking...' : 'Ask'}
        </button>
      </div>
    </form>
  )
}

export default QuestionBox