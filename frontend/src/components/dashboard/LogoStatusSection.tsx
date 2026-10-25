// "Logo pre-exists?" — the backend's similarity status with notes, sources and disclaimer.
import type { LogoStatus } from "../../types/api";
import DashboardSection from "./DashboardSection";

// Icon and border style per status (black and white only).
const STATUS_STYLE: Record<LogoStatus["status"], { icon: string; box: string }> = {
  no_significant_similarity: { icon: "✓", box: "border-black bg-white" },
  generic_elements: { icon: "○", box: "border-black bg-white" },
  potentially_similar: { icon: "!", box: "border-black border-2 bg-neutral-100" },
  matches_known_logo: { icon: "✕", box: "border-black bg-black text-white" },
};

export default function LogoStatusSection({ status }: { status: LogoStatus }) {
  const style = STATUS_STYLE[status.status] ?? STATUS_STYLE.generic_elements;
  const dark = status.status === "matches_known_logo";

  return (
    <DashboardSection id="logo-status" title="Logo pre-exists?" subtitle="Does your logo look like an existing well-known logo?">
      <div className={`rounded-lg border p-6 ${style.box}`}>
        <div className="flex items-start gap-4">
          <span
            aria-hidden="true"
            className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full border-2 text-lg font-bold ${
              dark ? "border-white" : "border-black"
            }`}
          >
            {style.icon}
          </span>
          <div>
            <h3 className="text-xl font-semibold">{status.title}</h3>
            <p className="mt-1">{status.message}</p>
            {status.recognized_brand && (
              <p className="mt-2 text-sm">
                Recognized brand: <strong>{status.recognized_brand}</strong>
              </p>
            )}
          </div>
        </div>

        {(status.notes?.length ?? 0) > 0 && (
          <ul className="mt-4 list-disc space-y-1 pl-14 text-sm">
            {status.notes.map((note, i) => (
              <li key={i}>{note}</li>
            ))}
          </ul>
        )}
      </div>

      <p className="mt-3 text-xs text-neutral-600">Checked with: {(status.sources_checked ?? []).join(", ")}</p>
      <p className="mt-1 text-xs text-neutral-600 italic">{status.disclaimer}</p>
    </DashboardSection>
  );
}
