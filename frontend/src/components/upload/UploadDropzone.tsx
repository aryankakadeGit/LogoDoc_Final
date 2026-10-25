// Drag-and-drop / click upload area (PNG, JPG, JPEG, SVG). Shows a preview of the chosen file.
import { useEffect, useRef, useState, type DragEvent } from "react";
import { ACCEPT_ATTRIBUTE, formatFileSize, validateLogoFile } from "../../utils/fileValidation";

interface UploadDropzoneProps {
  file: File | null;
  onFileChange: (file: File | null) => void;
  disabled?: boolean;
}

export default function UploadDropzone({ file, onFileChange, disabled = false }: UploadDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  function pick(selected: File | undefined) {
    if (!selected) return;
    const problem = validateLogoFile(selected);
    setError(problem);
    onFileChange(problem ? null : selected);
  }

  function onDrop(event: DragEvent<HTMLButtonElement>) {
    event.preventDefault();
    setDragging(false);
    if (!disabled) pick(event.dataTransfer.files[0]);
  }

  return (
    <div>
      <button
        type="button"
        disabled={disabled}
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          if (!disabled) setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        aria-describedby={error ? "upload-error" : undefined}
        className={`flex aspect-[4/3] w-full flex-col items-center justify-center gap-3 rounded-lg border-2 p-6 text-center transition-colors disabled:cursor-not-allowed disabled:opacity-60 ${
          dragging ? "border-solid border-black bg-neutral-100" : "border-dashed border-black bg-white hover:bg-neutral-50"
        }`}
      >
        {file && previewUrl ? (
          <>
            <img src={previewUrl} alt="Selected logo preview" className="max-h-40 max-w-full object-contain" />
            <span className="text-sm font-medium break-all">{file.name}</span>
            <span className="text-xs text-neutral-500">
              {formatFileSize(file.size)} · Click to choose a different file
            </span>
          </>
        ) : (
          <>
            <svg viewBox="0 0 24 24" className="h-10 w-10" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
              <path d="M12 16V4m0 0-4 4m4-4 4 4M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <span className="text-lg font-semibold">Click to upload</span>
            <span className="text-sm text-neutral-500">or drag and drop your logo here</span>
          </>
        )}
      </button>

      <input
        ref={inputRef}
        type="file"
        accept={ACCEPT_ATTRIBUTE}
        className="hidden"
        data-testid="file-input"
        onChange={(e) => {
          pick(e.target.files?.[0]);
          e.target.value = ""; // allow choosing the same file again
        }}
      />

      {error && (
        <p id="upload-error" role="alert" className="mt-2 text-sm font-medium">
          ⚠ {error}
        </p>
      )}
    </div>
  );
}
