// Frontend-only UI types (view state, dashboard sections, request state).
import type { ApiError } from "../api/httpClient";
import type { LogoAnalysis, LogoStatus } from "./api";

/** State of the logo analysis shared by the Home and Results pages. */
export type AnalysisState =
  | { status: "idle" }
  | { status: "loading"; fileName: string; previewUrl: string }
  | { status: "not_logo"; message: string; previewUrl: string }
  | { status: "error"; error: ApiError; previewUrl: string }
  | {
      status: "success";
      analysis: LogoAnalysis;
      logoStatus: LogoStatus;
      fileName: string;
      previewUrl: string;
    };

/** State of one on-demand request (AI prompt, designer recommendations). */
export type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: ApiError };

/** How the user's logo was made; decides which recommendations are shown. */
export type LogoSource = "ai" | "designer";

export type SectionId = "logo-status" | "overall-score" | "parameters" | "recommendations";
