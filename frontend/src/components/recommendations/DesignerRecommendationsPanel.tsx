// Shows designer advice per weak parameter + overall advice, with a "Download .txt" button.
import type { DesignerRecommendations } from "../../types/api";
import type { RequestState } from "../../types/ui";
import { formatScore } from "../../utils/format";
import Button from "../ui/Button";
import { RequestError, RequestLoading } from "./RequestStatus";

interface DesignerRecommendationsPanelProps {
  state: RequestState<DesignerRecommendations>;
  onGenerate: () => void;
  onDownload: (recommendations: DesignerRecommendations) => void;
  downloading: boolean;
  downloadError: string | null;
}

const ADVICE_ROWS = [
  { field: "problem", label: "What is wrong" },
  { field: "why_it_matters", label: "Why it matters" },
  { field: "suggestion", label: "What to change" },
  { field: "preserve", label: "What to keep" },
] as const;

export default function DesignerRecommendationsPanel({
  state,
  onGenerate,
  onDownload,
  downloading,
  downloadError,
}: DesignerRecommendationsPanelProps) {
  if (state.status === "idle") {
    return <Button onClick={onGenerate}>Get designer recommendations</Button>;
  }
  if (state.status === "loading") return <RequestLoading text="Preparing recommendations for your designer…" />;
  if (state.status === "error") return <RequestError error={state.error} onRetry={onGenerate} />;

  const { recommendations, overall } = state.data;
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm text-neutral-600">Share these points with your designer, or download them as a text file.</p>
        <Button onClick={() => onDownload(state.data)} loading={downloading}>
          Download .txt
        </Button>
      </div>
      {downloadError && (
        <p role="alert" className="text-sm font-medium">
          ⚠ {downloadError}
        </p>
      )}

      {recommendations.length === 0 ? (
        <p className="rounded-lg border border-neutral-300 p-5 text-sm">
          No parameter needs major changes. See the overall advice below for fine-tuning.
        </p>
      ) : (
        <div className="space-y-4">
          {recommendations.map((rec) => (
            <article key={rec.key} className="rounded-lg border border-black p-5">
              <header className="flex items-center justify-between gap-3">
                <h3 className="text-base font-semibold">{rec.name}</h3>
                <span className="font-mono text-sm font-semibold">
                  {formatScore(rec.score)}
                  <span className="font-normal text-neutral-500">/10</span>
                </span>
              </header>
              <dl className="mt-3 grid gap-3 text-sm sm:grid-cols-2">
                {ADVICE_ROWS.map((row) => (
                  <div key={row.field}>
                    <dt className="font-semibold">{row.label}</dt>
                    <dd className="mt-0.5 text-neutral-700">{rec[row.field]}</dd>
                  </div>
                ))}
              </dl>
            </article>
          ))}
        </div>
      )}

      {overall.length > 0 && (
        <div className="rounded-lg bg-neutral-100 p-5">
          <h3 className="text-base font-semibold">Overall advice</h3>
          <ol className="mt-2 list-decimal space-y-1.5 pl-5 text-sm">
            {overall.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ol>
        </div>
      )}

      <Button variant="ghost" className="px-0" onClick={onGenerate}>
        Generate again
      </Button>
    </div>
  );
}
