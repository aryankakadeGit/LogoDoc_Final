// Half-circle gauge from 0 to 10 (as in the drawing). Display only: the score comes from the backend.
import { formatScore } from "../../utils/format";

const RADIUS = 90;
const ARC_LENGTH = Math.PI * RADIUS;
const ARC_PATH = `M 10 100 A ${RADIUS} ${RADIUS} 0 0 1 190 100`;

export default function ScoreMeter({ score, max = 10 }: { score: number; max?: number }) {
  const ratio = Math.min(Math.max(score / max, 0), 1);

  return (
    <div
      role="meter"
      aria-valuemin={0}
      aria-valuemax={max}
      aria-valuenow={score}
      aria-label="Overall score"
      className="w-full max-w-xs"
    >
      <svg viewBox="0 0 200 126" className="w-full">
        <path d={ARC_PATH} fill="none" stroke="#e5e5e5" strokeWidth="16" strokeLinecap="round" />
        <path
          d={ARC_PATH}
          fill="none"
          stroke="#000"
          strokeWidth="16"
          strokeLinecap="round"
          strokeDasharray={ARC_LENGTH}
          strokeDashoffset={ARC_LENGTH * (1 - ratio)}
          style={{ transition: "stroke-dashoffset 900ms ease-out" }}
        />
        <text x="100" y="88" textAnchor="middle" fontSize="36" fontWeight="600" fill="#000" fontFamily="var(--font-mono)">
          {formatScore(score)}
        </text>
        <text x="100" y="106" textAnchor="middle" fontSize="12" fill="#737373">
          out of {max}
        </text>
        <text x="10" y="124" textAnchor="middle" fontSize="11" fill="#000">
          0
        </text>
        <text x="190" y="124" textAnchor="middle" fontSize="11" fill="#000">
          {max}
        </text>
      </svg>
    </div>
  );
}
