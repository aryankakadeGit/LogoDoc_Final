// Results page (second drawing). Shows loading / not-a-logo / error states, then the dashboard:
// sidebar on the left, all sections on one page on the right; sidebar clicks scroll to a section.
import { useCallback, useState } from "react";
import { Navigate, useNavigate } from "react-router";
import LogoStatusSection from "../components/dashboard/LogoStatusSection";
import OverallScoreSection from "../components/dashboard/OverallScoreSection";
import ParametersSection from "../components/dashboard/ParametersSection";
import Sidebar from "../components/dashboard/Sidebar";
import RecommendationsSection from "../components/recommendations/RecommendationsSection";
import ErrorState from "../components/states/ErrorState";
import LoadingState from "../components/states/LoadingState";
import NotALogoState from "../components/states/NotALogoState";
import Button from "../components/ui/Button";
import { useAnalysis } from "../context/AnalysisContext";
import { useActiveSection } from "../hooks/useActiveSection";
import { useAiPrompt } from "../hooks/useAiPrompt";
import { useDesignerRecommendations } from "../hooks/useDesignerRecommendations";
import type { LogoAnalysis, LogoStatus } from "../types/api";
import type { LogoSource, SectionId } from "../types/ui";

const SECTION_IDS: readonly SectionId[] = ["logo-status", "overall-score", "parameters", "recommendations"];

function scrollToSection(id: SectionId) {
  document.getElementById(id)?.scrollIntoView?.({ behavior: "smooth", block: "start" });
}

export default function DashboardPage() {
  const { state, retry, reset } = useAnalysis();
  const navigate = useNavigate();

  const startOver = useCallback(() => {
    reset();
    navigate("/");
  }, [reset, navigate]);

  switch (state.status) {
    case "idle":
      return <Navigate to="/" replace />;
    case "loading":
      return <LoadingState fileName={state.fileName} previewUrl={state.previewUrl} onCancel={startOver} />;
    case "not_logo":
      return <NotALogoState message={state.message} previewUrl={state.previewUrl} onUploadAnother={startOver} />;
    case "error":
      return <ErrorState error={state.error} onRetry={retry} onUploadAnother={startOver} />;
    case "success":
      return (
        <Dashboard
          analysis={state.analysis}
          logoStatus={state.logoStatus}
          fileName={state.fileName}
          previewUrl={state.previewUrl}
          onAnalyzeAnother={startOver}
        />
      );
  }
}

interface DashboardProps {
  analysis: LogoAnalysis;
  logoStatus: LogoStatus;
  fileName: string;
  previewUrl: string;
  onAnalyzeAnother: () => void;
}

function Dashboard({ analysis, logoStatus, fileName, previewUrl, onAnalyzeAnother }: DashboardProps) {
  const [active, setActive] = useActiveSection(SECTION_IDS);
  const [source, setSource] = useState<LogoSource | null>(null);
  const aiPrompt = useAiPrompt();
  const designer = useDesignerRecommendations();

  // Choosing a type fetches its recommendations the first time (one AI call each); later it reuses them.
  function selectSource(next: LogoSource) {
    setSource(next);
    if (next === "ai" && aiPrompt.state.status === "idle") void aiPrompt.generate(analysis);
    if (next === "designer" && designer.state.status === "idle") void designer.generate(analysis);
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6">
      <div className="grid grid-cols-[minmax(0,1fr)] gap-6 lg:grid-cols-[15rem_minmax(0,1fr)] lg:gap-10">
        <aside className="sticky top-20 z-20 -mx-4 min-w-0 border-b border-neutral-200 bg-white px-4 py-3 sm:-mx-6 sm:px-6 lg:static lg:mx-0 lg:border-r lg:border-b-0 lg:px-0 lg:py-10 lg:pr-6">
          <div className="lg:sticky lg:top-28">
          <Sidebar
            active={active}
            source={source}
            onNavigate={(id) => {
              setActive(id);
              scrollToSection(id);
            }}
            onSelectSource={(s) => {
              selectSource(s);
              setActive("recommendations");
              scrollToSection("recommendations");
            }}
          />
          <div className="mt-6 hidden lg:block">
            <Button variant="secondary" className="w-full" onClick={onAnalyzeAnother}>
              Analyze another logo
            </Button>
          </div>
          </div>
        </aside>

        <main className="min-w-0">
          <LogoStatusSection status={logoStatus} />
          <OverallScoreSection
            score={analysis.overall_score}
            description={analysis.logo_description}
            previewUrl={previewUrl}
            fileName={fileName}
          />
          <ParametersSection parameters={analysis.parameters} />
          <RecommendationsSection
            source={source}
            onSelectSource={selectSource}
            aiPrompt={{ state: aiPrompt.state, generate: () => void aiPrompt.generate(analysis) }}
            designer={{
              state: designer.state,
              generate: () => void designer.generate(analysis),
              download: (recs) => void designer.download(analysis, recs),
              downloading: designer.downloading,
              downloadError: designer.downloadError,
            }}
          />
          <div className="pb-12 lg:hidden">
            <Button variant="secondary" className="w-full" onClick={onAnalyzeAnother}>
              Analyze another logo
            </Button>
          </div>
        </main>
      </div>
    </div>
  );
}
