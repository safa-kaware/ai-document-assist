function AnswerCard({ answer, sources, isLoading, error }) {
  return (
    <div className="answer-card">
      <h2 className="panel-label">Answer</h2>

      {isLoading && <p className="placeholder-text">Thinking...</p>}
      {error && <p className="error-text">{error}</p>}

      {!isLoading && !error && !answer && (
        <p className="placeholder-text">Answers will appear here once you ask a question</p>
      )}

      {!isLoading && !error && answer && (
        <div>
          <p className="answer-text">{answer}</p>

          {sources && sources.length > 0 && (
            <div className="sources-block">
              <h3 className="sources-label">Sources</h3>
              <ul className="list-unstyled mb-0">
                {sources.map((source, i) => (
                  <li key={i} className="source-item">
                    {source.document} — Page {source.page}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default AnswerCard