// "Score out of 10" — the overall score gauge, the uploaded logo and the AI's short description.
import DashboardSection from "./DashboardSection";
import ScoreMeter from "./ScoreMeter";

interface OverallScoreSectionProps {
  score: number;
  description: string;
  previewUrl: string;
  fileName: string;
}

export default function OverallScoreSection({ score, description, previewUrl, fileName }: OverallScoreSectionProps) {
  return (
    <DashboardSection
      id="overall-score"
      title="Score out of 10"
      subtitle="The average of all parameter scores that apply to your logo."
    >
      <div className="grid items-center gap-8 md:grid-cols-2">
        <div className="flex justify-center">
          <ScoreMeter score={score} />
        </div>
        <div className="flex flex-col items-center gap-3 md:items-start">
          <div className="flex h-32 w-full max-w-56 items-center justify-center rounded-lg border border-neutral-300 p-3">
            <img src={previewUrl} alt="Your uploaded logo" className="max-h-full max-w-full object-contain" />
          </div>
          <p className="text-xs break-all text-neutral-500">{fileName}</p>
          <p className="text-sm text-neutral-800">{description}</p>
        </div>
      </div>
    </DashboardSection>
  );
}
