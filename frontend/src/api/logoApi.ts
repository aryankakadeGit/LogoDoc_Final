// The 4 backend calls used by the app. Endpoints: docs/api-contract.md.
import { ANALYZE_TIMEOUT_MS, RECOMMENDATION_TIMEOUT_MS } from "../config/env";
import type { AnalyzeResponse, DesignerRecommendations, ImprovedPrompt, LogoAnalysis } from "../types/api";
import { filenameFromDisposition } from "../utils/download";
import { postFile, postJson, postJsonForFile } from "./httpClient";

const DEFAULT_TXT_NAME = "designer-recommendations.txt";

export function analyzeLogo(file: File, signal?: AbortSignal): Promise<AnalyzeResponse> {
  return postFile<AnalyzeResponse>("/api/logo/analyze", file, { signal, timeoutMs: ANALYZE_TIMEOUT_MS });
}

export function getAiPrompt(analysis: LogoAnalysis, signal?: AbortSignal): Promise<ImprovedPrompt> {
  return postJson<ImprovedPrompt>(
    "/api/logo/recommendations/ai-prompt",
    { analysis },
    { signal, timeoutMs: RECOMMENDATION_TIMEOUT_MS },
  );
}

export function getDesignerRecommendations(
  analysis: LogoAnalysis,
  signal?: AbortSignal,
): Promise<DesignerRecommendations> {
  return postJson<DesignerRecommendations>(
    "/api/logo/recommendations/designer",
    { analysis },
    { signal, timeoutMs: RECOMMENDATION_TIMEOUT_MS },
  );
}

export async function downloadDesignerRecommendations(
  analysis: LogoAnalysis,
  recommendations: DesignerRecommendations,
): Promise<{ blob: Blob; filename: string }> {
  const { blob, contentDisposition } = await postJsonForFile(
    "/api/logo/recommendations/designer/download",
    { analysis, recommendations },
    { timeoutMs: RECOMMENDATION_TIMEOUT_MS },
  );
  return { blob, filename: filenameFromDisposition(contentDisposition, DEFAULT_TXT_NAME) };
}
