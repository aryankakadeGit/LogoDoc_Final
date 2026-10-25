// Requests the improved image-generation prompt for an AI-generated logo.
import { useCallback } from "react";
import { getAiPrompt } from "../api/logoApi";
import type { ImprovedPrompt, LogoAnalysis } from "../types/api";
import { useRequest } from "./useRequest";

export function useAiPrompt() {
  const { state, run } = useRequest<ImprovedPrompt>();
  const generate = useCallback(
    (analysis: LogoAnalysis) => run((signal) => getAiPrompt(analysis, signal)),
    [run],
  );
  return { state, generate };
}
