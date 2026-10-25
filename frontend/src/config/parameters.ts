// Display copy of the 11 score parameters for the "Score Parameters" page.
// Source of truth: backend/app/modules/analysis/parameters.py (keep the two in sync).
// The dashboard itself uses the names/explanations sent by the backend, not this list.

export interface ParameterInfo {
  name: string;
  explanation: string;
  needsText?: boolean;
}

export const PARAMETER_INFO: readonly ParameterInfo[] = [
  { name: "Visual Simplicity", explanation: "How clean and uncluttered your logo is." },
  { name: "Legibility", explanation: "How easy the text in your logo is to read.", needsText: true },
  { name: "Scalability", explanation: "How clear your logo stays when it is very small or very large." },
  { name: "Distinctiveness", explanation: "How much your logo stands out from other logos." },
  { name: "Brand Relevance", explanation: "How well your logo fits the kind of business it seems to represent." },
  { name: "Typography", explanation: "How well the fonts suit the logo and work together.", needsText: true },
  { name: "Colors", explanation: "How well the colors work together and in different settings." },
  { name: "Composition", explanation: "How well the parts of your logo are arranged and balanced." },
  { name: "Memorability", explanation: "How easy your logo is to remember after a quick look." },
  {
    name: "Versatility",
    explanation: "How well your logo works on different backgrounds, in one color, and on different products.",
  },
  { name: "Technical Quality", explanation: "How clean the logo is technically: sharp edges, no blur, proper alignment." },
];
