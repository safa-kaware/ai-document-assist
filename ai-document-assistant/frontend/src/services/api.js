const API_BASE_URL = "http://127.0.0.1:8000";

export async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/`);
  if (!response.ok) {
    throw new Error(`Backend returned status ${response.status}`);
  }
  return response.json();
}

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    throw new Error(errorBody?.detail || `Upload failed (status ${response.status})`);
  }

  return response.json();
}

export { API_BASE_URL };