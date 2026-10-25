// "Score Parameters" page: explains the 11 parameters and how the score works.
import { Link } from "react-router";
import { PARAMETER_INFO } from "../config/parameters";

export default function ScoreParametersPage() {
  return (
    <main className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <h1 className="font-brand text-4xl font-bold">Score Parameters</h1>
      <p className="mt-4 text-neutral-700">
        Every logo is checked on the same 11 parameters. Each one gets a score from 0 to 10, with what works well (✓)
        and what could be better (⚠). Your overall score is the average of the parameters that apply to your logo.
      </p>

      <ol className="mt-8 divide-y divide-neutral-200 border-y border-neutral-200">
        {PARAMETER_INFO.map((p, i) => (
          <li key={p.name} className="flex gap-4 py-4">
            <span className="w-8 shrink-0 text-lg font-bold text-neutral-400">{String(i + 1).padStart(2, "0")}</span>
            <div>
              <h2 className="font-semibold">{p.name}</h2>
              <p className="mt-0.5 text-sm text-neutral-600">{p.explanation}</p>
              {p.needsText && (
                <p className="mt-1 text-xs text-neutral-500 italic">Shown as N/A when the logo has no text.</p>
              )}
            </div>
          </li>
        ))}
      </ol>

      <Link to="/" className="mt-8 inline-block rounded-md bg-black px-5 py-2.5 text-sm font-semibold text-white">
        Check your logo
      </Link>
    </main>
  );
}
