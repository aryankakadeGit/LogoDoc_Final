// Requests designer recommendations, and downloads them as a .txt file.
import { useCallback, useState } from "react";
import { ApiError } from "../api/httpClient";
import { downloadDesignerRecommendations, getDesignerRecommendations } from "../api/logoApi";
import type { DesignerRecommendations, LogoAnalysis } from "../types/api";
import { saveBlob } from "../utils/download";
import { useRequest } from "./useRequest";

export function useDesignerRecommendations() {
  const { state, run } = useRequest<DesignerRecommendations>();
  const [downloading, setDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  const generate = useCallback(
    (analysis: LogoAnalysis) => run((signal) => getDesignerRecommendations(analysis, signal)),
    [run],
  );

  const download = useCallback(async (analysis: LogoAnalysis, recommendations: DesignerRecommendations) => {
    setDownloading(true);
    setDownloadError(null);
    try {
      const { blob, filename } = await downloadDesignerRecommendations(analysis, recommendations);
      saveBlob(blob, filename);
    } catch (error) {
      setDownloadError(error instanceof ApiError ? error.message : "The download failed. Please try again.");
    } finally {
      setDownloading(false);
    }
  }, []);

  return { state, generate, download, downloading, downloadError };
}
