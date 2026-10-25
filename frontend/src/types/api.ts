// Friendly names for the backend API types.
// Object shapes come from api.generated.ts (npm run generate:types).
// The /analyze response union is written by hand because the generator turns the
// boolean `is_logo` discriminator into the strings "True"/"False".
import type { components } from "./api.generated";

type Schemas = components["schemas"];

export type LogoAnalysis = Schemas["LogoAnalysis"];
export type ParameterResult = Schemas["ParameterResult"];
export type Similarity = Schemas["Similarity"];
export type LogoStatus = Schemas["LogoStatus"];
export type ImprovedPrompt = Schemas["ImprovedPrompt"];
export type DesignerRecommendation = Schemas["DesignerRecommendation"];
export type DesignerRecommendations = Schemas["DesignerRecommendations"];

export interface AnalyzeLogoSuccess {
  is_logo: true;
  analysis: LogoAnalysis;
  logo_status: LogoStatus;
}

export interface NotALogoResponse {
  is_logo: false;
  message: string;
}

export type AnalyzeResponse = AnalyzeLogoSuccess | NotALogoResponse;

/** Every backend error: {"error": {"code", "message"}} */
export interface ApiErrorBody {
  error: { code: string; message: string };
}
