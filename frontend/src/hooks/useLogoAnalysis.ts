// Runs the logo analysis and keeps its state (used once, inside AnalysisProvider).
// idle -> loading -> success | not_logo | error. The uploaded image is previewed from
// the browser's memory (object URL); nothing is stored anywhere.
import { useCallback, useEffect, useRef, useState } from "react";
import { ApiError, isAbortError } from "../api/httpClient";
import { analyzeLogo } from "../api/logoApi";
import type { AnalysisState } from "../types/ui";

export function useLogoAnalysis() {
  const [state, setState] = useState<AnalysisState>({ status: "idle" });
  const controllerRef = useRef<AbortController | null>(null);
  const previewUrlRef = useRef<string | null>(null);
  const lastFileRef = useRef<File | null>(null);

  const releasePreview = useCallback(() => {
    if (previewUrlRef.current) URL.revokeObjectURL(previewUrlRef.current);
    previewUrlRef.current = null;
  }, []);

  useEffect(
    () => () => {
      controllerRef.current?.abort();
      releasePreview();
    },
    [releasePreview],
  );

  const analyze = useCallback(
    async (file: File) => {
      controllerRef.current?.abort();
      const controller = new AbortController();
      controllerRef.current = controller;

      if (lastFileRef.current !== file) {
        releasePreview();
        previewUrlRef.current = URL.createObjectURL(file);
        lastFileRef.current = file;
      }
      const previewUrl = previewUrlRef.current!;
      setState({ status: "loading", fileName: file.name, previewUrl });

      try {
        const result = await analyzeLogo(file, controller.signal);
        if (controller.signal.aborted) return;
        if (result.is_logo) {
          setState({
            status: "success",
            analysis: result.analysis,
            logoStatus: result.logo_status,
            fileName: file.name,
            previewUrl,
          });
        } else {
          setState({ status: "not_logo", message: result.message, previewUrl });
        }
      } catch (error) {
        if (isAbortError(error) || controller.signal.aborted) return;
        const apiError =
          error instanceof ApiError ? error : new ApiError("UNKNOWN_ERROR", "Something went wrong. Please try again.");
        setState({ status: "error", error: apiError, previewUrl });
      }
    },
    [releasePreview],
  );

  const retry = useCallback(() => {
    if (lastFileRef.current) void analyze(lastFileRef.current);
  }, [analyze]);

  const reset = useCallback(() => {
    controllerRef.current?.abort();
    releasePreview();
    lastFileRef.current = null;
    setState({ status: "idle" });
  }, [releasePreview]);

  return { state, analyze, retry, reset };
}
