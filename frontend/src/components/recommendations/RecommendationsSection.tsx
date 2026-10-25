// "Recommendations" — choose AI Generated / Manually Designed, then show the matching panel.
import type { DesignerRecommendations, ImprovedPrompt } from "../../types/api";
import type { LogoSource, RequestState } from "../../types/ui";
import DashboardSection from "../dashboard/DashboardSection";
import AiPromptPanel from "./AiPromptPanel";
import DesignerRecommendationsPanel from "./DesignerRecommendationsPanel";
import LogoSourceSelector from "./LogoSourceSelector";

interface RecommendationsSectionProps {
  source: LogoSource | null;
  onSelectSource: (source: LogoSource) => void;
  aiPrompt: { state: RequestState<ImprovedPrompt>; generate: () => void };
  designer: {
    state: RequestState<DesignerRecommendations>;
    generate: () => void;
    download: (recommendations: DesignerRecommendations) => void;
    downloading: boolean;
    downloadError: string | null;
  };
}

export default function RecommendationsSection({ source, onSelectSource, aiPrompt, designer }: RecommendationsSectionProps) {
  return (
    <DashboardSection
      id="recommendations"
      title="Recommendations"
      subtitle="How was your logo made? We'll tailor the advice to it."
      className="min-h-[calc(100vh-8rem)]"
    >
      <LogoSourceSelector value={source} onChange={onSelectSource} />

      <div className="mt-6">
        {source === "ai" && <AiPromptPanel state={aiPrompt.state} onGenerate={aiPrompt.generate} />}
        {source === "designer" && (
          <DesignerRecommendationsPanel
            state={designer.state}
            onGenerate={designer.generate}
            onDownload={designer.download}
            downloading={designer.downloading}
            downloadError={designer.downloadError}
          />
        )}
        {source === null && <p className="text-sm text-neutral-500">Choose an option above to see your recommendations.</p>}
      </div>
    </DashboardSection>
  );
}
