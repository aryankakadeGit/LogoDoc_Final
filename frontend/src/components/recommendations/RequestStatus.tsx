// Loading and error blocks shared by both recommendation panels.
import type { ApiError } from "../../api/httpClient";
import Button from "../ui/Button";

export function RequestLoading({ text }: { text: string }) {
  return (
    <div className="flex items-center gap-3 rounded-lg border border-neutral-300 p-5" aria-live="polite" aria-busy="true">
      <span aria-hidden="true" className="h-5 w-5 animate-spin rounded-full border-2 border-black border-t-transparent" />
      <span className="text-sm">{text}</span>
    </div>
  );
}

export function RequestError({ error, onRetry }: { error: ApiError; onRetry: () => void }) {
  return (
    <div role="alert" className="rounded-lg border-2 border-black p-5">
      <p className="font-semibold">⚠ {error.message}</p>
      <Button variant="secondary" className="mt-3" onClick={onRetry}>
        Try again
      </Button>
    </div>
  );
}
