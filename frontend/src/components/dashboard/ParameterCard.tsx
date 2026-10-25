// One of the 11 parameters: name, score/10 (or N/A), what it means, ✓ positives, ⚠ negatives.
import type { ParameterResult } from "../../types/api";
import { formatScore } from "../../utils/format";

export default function ParameterCard({ parameter }: { parameter: ParameterResult }) {
  const { name, explanation, score, positives, negatives, not_applicable_reason } = parameter;
  const applicable = score !== null;

  return (
    <article className={`flex flex-col rounded-lg border p-5 ${applicable ? "border-black" : "border-dashed border-neutral-400"}`}>
      <header className="flex items-start justify-between gap-3">
        <h3 className="text-base font-semibold">{name}</h3>
        <span className="shrink-0 font-mono text-lg font-semibold" aria-label={applicable ? `Score ${formatScore(score)} out of 10` : "Not applicable"}>
          {applicable ? (
            <>
              {formatScore(score)}
              <span className="text-sm font-normal text-neutral-500">/10</span>
            </>
          ) : (
            <span className="text-neutral-500">N/A</span>
          )}
        </span>
      </header>

      {applicable && (
        <div className="mt-2 h-1.5 w-full rounded-full bg-neutral-200" aria-hidden="true">
          <div className="h-1.5 rounded-full bg-black" style={{ width: `${(score / 10) * 100}%` }} />
        </div>
      )}

      <p className="mt-3 text-sm text-neutral-600">{explanation}</p>

      {applicable ? (
        <div className="mt-4 space-y-3 text-sm">
          {positives.length > 0 && (
            <ul className="space-y-1.5" aria-label="Positives">
              {positives.map((point, i) => (
                <li key={i} className="flex gap-2">
                  <span aria-hidden="true" className="font-bold">✓</span>
                  <span>{point}</span>
                </li>
              ))}
            </ul>
          )}
          {negatives.length > 0 && (
            <ul className="space-y-1.5" aria-label="Negatives">
              {negatives.map((point, i) => (
                <li key={i} className="flex gap-2">
                  <span aria-hidden="true">⚠</span>
                  <span>{point}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      ) : (
        <p className="mt-4 text-sm text-neutral-600 italic">{not_applicable_reason || "Not applicable to this logo."}</p>
      )}
    </article>
  );
}
