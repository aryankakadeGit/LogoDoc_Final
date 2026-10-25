// Small shared helper for one on-demand request: idle -> loading -> success / error.
// Starting a new run cancels the previous one; leaving the page cancels it too.
import { useCallback, useEffect, useRef, useState } from "react";
import { ApiError, isAbortError } from "../api/httpClient";
import type { RequestState } from "../types/ui";

export function useRequest<T>() {
  const [state, setState] = useState<RequestState<T>>({ status: "idle" });
  const controllerRef = useRef<AbortController | null>(null);

  useEffect(() => () => controllerRef.current?.abort(), []);

  const run = useCallback(async (task: (signal: AbortSignal) => Promise<T>) => {
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;
    setState({ status: "loading" });
    try {
      const data = await task(controller.signal);
      if (!controller.signal.aborted) setState({ status: "success", data });
    } catch (error) {
      if (isAbortError(error) || controller.signal.aborted) return;
      const apiError =
        error instanceof ApiError ? error : new ApiError("UNKNOWN_ERROR", "Something went wrong. Please try again.");
      setState({ status: "error", error: apiError });
    }
  }, []);

  return { state, run };
}
