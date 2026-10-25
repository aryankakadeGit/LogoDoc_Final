// "Score parameters" — the 11 parameter cards, in the order the backend sends them.
import type { ParameterResult } from "../../types/api";
import DashboardSection from "./DashboardSection";
import ParameterCard from "./ParameterCard";

export default function ParametersSection({ parameters }: { parameters: ParameterResult[] }) {
  return (
    <DashboardSection
      id="parameters"
      title="Score parameters"
      subtitle="Each parameter is scored from 0 to 10, with what works (✓) and what could be better (⚠)."
    >
      <div className="grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
        {parameters.map((p) => (
          <ParameterCard key={p.key} parameter={p} />
        ))}
      </div>
    </DashboardSection>
  );
}
