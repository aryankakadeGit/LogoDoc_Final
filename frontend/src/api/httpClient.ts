// Base fetch wrapper: base URL, timeout, JSON/file handling and one error type (ApiError)
// built from the backend's {"error": {"code", "message"}} shape.
import { API_BASE_URL } from "../config/env";
import type { ApiErrorBody } from "../types/api";

export class ApiError extends Error {
  readonly code: string;
  readonly status: number;

  constructor(code: string, message: string, status = 0) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.status = status;
  }
}

export interface RequestOptions {
  signal?: AbortSignal;
  timeoutMs: number;
}

export function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === "AbortError";
}

function isErrorBody(value: unknown): value is ApiErrorBody {
  const error = (value as ApiErrorBody | null)?.error;
  return typeof error?.code === "string" && typeof error?.message === "string";
}

async function toApiError(response: Response): Promise<ApiError> {
  try {
    const body: unknown = await response.json();
    if (isErrorBody(body)) {
      return new ApiError(body.error.code, body.error.message, response.status);
    }
  } catch {
    // Not JSON (e.g. a proxy error page): fall through to a generic message.
  }
  return new ApiError(`HTTP_${response.status}`, "Something went wrong. Please try again.", response.status);
}

/**
 * Sends a request and returns the Response when it is 2xx.
 * Throws ApiError for HTTP errors, network errors and timeouts.
 * Re-throws the AbortError when the caller cancelled (callers ignore it).
 */
export async function request(path: string, init: RequestInit, options: RequestOptions): Promise<Response> {
  const controller = new AbortController();
  let timedOut = false;
  const timer = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, options.timeoutMs);
  const onCallerAbort = () => controller.abort();
  options.signal?.addEventListener("abort", onCallerAbort);
  if (options.signal?.aborted) controller.abort();

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, { ...init, signal: controller.signal });
    if (!response.ok) throw await toApiError(response);
    return response;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    if (timedOut) {
      throw new ApiError("TIMEOUT", "The server took too long to respond. Please try again.");
    }
    if (options.signal?.aborted || isAbortError(error)) {
      throw new DOMException("Request cancelled", "AbortError");
    }
    throw new ApiError("NETWORK_ERROR", "Could not reach the server. Check your connection and try again.");
  } finally {
    clearTimeout(timer);
    options.signal?.removeEventListener("abort", onCallerAbort);
  }
}

export async function postJson<T>(path: string, body: unknown, options: RequestOptions): Promise<T> {
  const response = await request(
    path,
    { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) },
    options,
  );
  return (await response.json()) as T;
}

const MIME_BY_EXTENSION: Record<string, string> = {
  png: "image/png",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  svg: "image/svg+xml",
};

function mimeFromName(name: string): string {
  const ext = name.split(".").pop()?.toLowerCase() ?? "";
  return MIME_BY_EXTENSION[ext] ?? "application/octet-stream";
}

/** Sends a file as the raw request body (what POST /api/logo/analyze expects). */
export async function postFile<T>(path: string, file: File, options: RequestOptions): Promise<T> {
  const response = await request(
    path,
    { method: "POST", headers: { "Content-Type": file.type || mimeFromName(file.name) }, body: file },
    options,
  );
  return (await response.json()) as T;
}

/** Sends JSON and returns the response as a downloadable file. */
export async function postJsonForFile(
  path: string,
  body: unknown,
  options: RequestOptions,
): Promise<{ blob: Blob; contentDisposition: string | null }> {
  const response = await request(
    path,
    { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) },
    options,
  );
  return { blob: await response.blob(), contentDisposition: response.headers.get("Content-Disposition") };
}
