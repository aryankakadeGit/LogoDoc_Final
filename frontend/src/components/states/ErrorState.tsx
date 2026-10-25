// Full-screen error after a failed analysis, with the backend's message and a retry.
import type { ApiError } from "../../api/httpClient";
import Button from "../ui/Button";

// Errors where sending the same file again will fail the same way.
const NOT_RETRYABLE = new Set([
  "EMPTY_FILE",
  "FILE_TOO_LARGE",
  "REQUEST_TOO_LARGE",
  "IMAGE_TOO_LARGE",
  "UNSUPPORTED_FORMAT",
  "INVALID_IMAGE",
  "UNSAFE_SVG",
]);

interface ErrorStateProps {
  error: ApiError;
  onRetry: () => void;
  onUploadAnother: () => void;
}

export default function ErrorState({ error, onRetry, onUploadAnother }: ErrorStateProps) {
  const canRetry = !NOT_RETRYABLE.has(error.code);

  return (
    <section
      role="alert"
      className="flex min-h-[calc(100vh-5rem)] flex-col items-center justify-center gap-5 px-4 text-center"
    >
      <span className="flex h-16 w-16 items-center justify-center rounded-full border-2 border-black text-3xl font-bold" aria-hidden="true">
        !
      </span>
      <h1 className="text-2xl font-bold">We couldn't analyze your logo</h1>
      <p className="max-w-md text-base">{error.message}</p>
      <p className="text-xs text-neutral-500">Error code: {error.code}</p>
      <div className="flex flex-wrap justify-center gap-3">
        {canRetry && <Button onClick={onRetry}>Try again</Button>}
        <Button variant={canRetry ? "secondary" : "primary"} onClick={onUploadAnother}>
          Upload a different file
        </Button>
      </div>
    </section>
  );
}
