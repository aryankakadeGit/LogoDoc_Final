// Full-screen wait screen while the logo is analyzed (can take up to ~2 minutes).
// The step text only changes with time to reassure the user; it is not real progress.
import { useEffect, useState } from "react";
import Button from "../ui/Button";

const STEPS = [
  { after: 0, text: "Uploading your logo…" },
  { after: 3, text: "Checking that it is a logo…" },
  { after: 8, text: "Scoring 11 design parameters…" },
  { after: 20, text: "Checking similarity with well-known logos…" },
  { after: 40, text: "Still working. The AI can be slow when it is busy — this may take up to 2 minutes." },
];

interface LoadingStateProps {
  fileName: string;
  previewUrl: string;
  onCancel: () => void;
}

export default function LoadingState({ fileName, previewUrl, onCancel }: LoadingStateProps) {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  const step = [...STEPS].reverse().find((s) => seconds >= s.after) ?? STEPS[0];

  return (
    <section
      className="flex min-h-[calc(100vh-5rem)] flex-col items-center justify-center gap-6 px-4 text-center"
      aria-live="polite"
      aria-busy="true"
    >
      <div className="relative flex h-40 w-40 items-center justify-center rounded-full border border-neutral-200">
        <span className="absolute inset-0 animate-spin rounded-full border-4 border-black border-t-transparent" aria-hidden="true" />
        <img src={previewUrl} alt="" className="max-h-24 max-w-24 object-contain" />
      </div>
      <div>
        <h1 className="text-2xl font-bold">Analyzing your logo</h1>
        <p className="mt-1 text-sm break-all text-neutral-500">{fileName}</p>
      </div>
      <p className="max-w-md text-base">{step.text}</p>
      <p className="text-sm text-neutral-500">{seconds}s elapsed · usually 10–60 seconds</p>
      <Button variant="secondary" onClick={onCancel}>
        Cancel
      </Button>
    </section>
  );
}
