function QuestionBox() {
  return (
    <div className="bg-white rounded-lg p-4 border border-gray-200">
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Ask a question about your document..."
          disabled
          className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm disabled:bg-gray-50 disabled:text-gray-400"
        />
        <button
          disabled
          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Ask
        </button>
      </div>
      <p className="mt-2 text-xs text-gray-400">
        Enabled once document upload and chat are implemented
      </p>
    </div>
  )
}

export default QuestionBox