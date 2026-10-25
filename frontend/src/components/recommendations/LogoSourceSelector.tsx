// Asks how the logo was made: AI Generated (-> improved prompt) or Manually Designed (-> designer advice).
import type { LogoSource } from "../../types/ui";

const OPTIONS: { id: LogoSource; title: string; text: string }[] = [
  { id: "ai", title: "AI Generated", text: "I made it with an AI image tool. Give me a better prompt." },
  { id: "designer", title: "Manually Designed", text: "A designer made it. Give me advice to share with them." },
];

interface LogoSourceSelectorProps {
  value: LogoSource | null;
  onChange: (source: LogoSource) => void;
}

export default function LogoSourceSelector({ value, onChange }: LogoSourceSelectorProps) {
  return (
    <div role="radiogroup" aria-label="How was your logo made?" className="grid gap-3 sm:grid-cols-2">
      {OPTIONS.map((option) => {
        const selected = value === option.id;
        return (
          <button
            key={option.id}
            type="button"
            role="radio"
            aria-checked={selected}
            onClick={() => onChange(option.id)}
            className={`rounded-lg border-2 p-4 text-left transition-colors ${
              selected ? "border-black bg-black text-white" : "border-neutral-300 bg-white hover:border-black"
            }`}
          >
            <span className="block text-base font-semibold">{option.title}</span>
            <span className={`mt-1 block text-sm ${selected ? "text-neutral-200" : "text-neutral-600"}`}>{option.text}</span>
          </button>
        );
      })}
    </div>
  );
}
