// Sample backend responses shared by the tests (same shapes as the real API).
import type { AnalyzeLogoSuccess, DesignerRecommendations, ParameterResult } from "../types/api";

const KEYS = [
  ["visual_simplicity", "Visual Simplicity"],
  ["legibility", "Legibility"],
  ["scalability", "Scalability"],
  ["distinctiveness", "Distinctiveness"],
  ["brand_relevance", "Brand Relevance"],
  ["typography", "Typography"],
  ["colors", "Colors"],
  ["composition", "Composition"],
  ["memorability", "Memorability"],
  ["versatility", "Versatility"],
  ["technical_quality", "Technical Quality"],
] as const;

export const parameters: ParameterResult[] = KEYS.map(([key, name], i) =>
  key === "typography" || key === "legibility"
    ? {
        key,
        name,
        explanation: `${name} explanation`,
        score: null,
        positives: [],
        negatives: [],
        not_applicable_reason: "Not applicable: this logo has no text.",
      }
    : {
        key,
        name,
        explanation: `${name} explanation`,
        score: 6 + (i % 4),
        positives: [`${name} positive`],
        negatives: [`${name} negative`],
        not_applicable_reason: null,
      },
);

export const analyzeSuccess: AnalyzeLogoSuccess = {
  is_logo: true,
  analysis: {
    is_logo: true,
    overall_score: 7.4,
    logo_description: "A round black emblem.",
    parameters,
    similarity: { recognized_brand: null, match_level: "none", notes: [] },
  },
  logo_status: {
    status: "no_significant_similarity",
    title: "No significant similarity detected",
    message: "We did not find a close match with well-known logos.",
    recognized_brand: null,
    notes: [],
    sources_checked: ["AI visual recognition of well-known logos"],
    disclaimer: "This is an automated visual check against well-known logos. It is not a trademark search or legal advice.",
  },
};

export const designerRecs: DesignerRecommendations = {
  recommendations: [
    {
      key: "colors",
      name: "Colors",
      score: 6,
      problem: "No brand color.",
      why_it_matters: "Color aids recognition.",
      suggestion: "Add one accent color.",
      preserve: "Keep the black base.",
    },
  ],
  overall: ["Make a square version."],
};

export function jsonResponse(body: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...headers },
  });
}

export function pngFile(name = "logo.png", size = 100): File {
  return new File([new Uint8Array(size)], name, { type: "image/png" });
}
