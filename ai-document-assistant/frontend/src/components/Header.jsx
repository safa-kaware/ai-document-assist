function Header() {
  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="max-w-3xl mx-auto px-4 py-4">
        <h1 className="text-xl font-bold text-gray-900">
          AI Document Assistant
        </h1>
        <p className="text-sm text-gray-500">
          Upload a document and ask questions about it
        </p>
      </div>
    </header>
  )
}

export default Header