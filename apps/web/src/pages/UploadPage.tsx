// TODO: Implement UploadPage
// - Drag-and-drop area (accepts PNG/JPG/TIFF up to 10 MB)
// - File picker fallback
// - Shows upload progress
// - On success: navigate to /notes/:id
export default function UploadPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="rounded-xl border-2 border-dashed border-gray-300 p-16 text-center">
        <h1 className="text-2xl font-semibold text-gray-700">AIPen</h1>
        <p className="mt-2 text-gray-500">Drop a handwriting image to convert it</p>
        {/* TODO: UploadDropzone component */}
      </div>
    </main>
  );
}
