// Shares the analysis state between the Home page (starts it) and the Results page (shows it).
import { createContext, useContext, type ReactNode } from "react";
import { useLogoAnalysis } from "../hooks/useLogoAnalysis";

type AnalysisContextValue = ReturnType<typeof useLogoAnalysis>;

const AnalysisContext = createContext<AnalysisContextValue | null>(null);

export function AnalysisProvider({ children }: { children: ReactNode }) {
  const value = useLogoAnalysis();
  return <AnalysisContext.Provider value={value}>{children}</AnalysisContext.Provider>;
}

export function useAnalysis(): AnalysisContextValue {
  const value = useContext(AnalysisContext);
  if (!value) throw new Error("useAnalysis must be used inside <AnalysisProvider>");
  return value;
}
