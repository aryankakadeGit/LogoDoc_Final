// Shows the improved image-generation prompt with a Copy button.
import { useEffect, useRef, useState } from "react";
import type { ImprovedPrompt } from "../../types/api";
import type { RequestState } from "../../types/ui";
import { copyText } from "../../utils/clipboard";
import Button from "../ui/Button";
import { RequestError, RequestLoading } from "./RequestStatus";

interface AiPromptPanelProps {
  state: RequestState<ImprovedPrompt>;
  onGenerate: () => void;
}

export default function AiPromptPanel({ state, onGenerate }: AiPromptPanelProps) {
  const [copied, setCopied] = useState<"yes" | "failed" | null>(null);

  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => () => {
    if (timerRef.current) clearTimeout(timerRef.current);
  }, []);

  async function onCopy(text: string) {
    const ok = await copyText(text);
    setCopied(ok ? "yes" : "failed");
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => setCopied(null), 2000);
  }

  if (state.status === "idle") {
    return <Button onClick={onGenerate}>Generate improved prompt</Button>;
  }
  if (state.status === "loading") return <RequestLoading text="Writing an improved prompt for your AI image tool…" />;
  if (state.status === "error") return <RequestError error={state.error} onRetry={onGenerate} />;

  const { prompt } = state.data;
  return (
    <div>
      <p className="text-sm text-neutral-600">
        Paste this into your AI image tool to generate an improved version of your logo.
      </p>
      <div className="mt-3 rounded-lg border border-black">
        <div className="flex items-center justify-between border-b border-black px-4 py-2">
          <span className="text-sm font-semibold">Improved prompt</span>
          <Button variant="secondary" className="px-3 py-1.5" onClick={() => onCopy(prompt)}>
            {copied === "yes" ? "Copied ✓" : copied === "failed" ? "Copy failed" : "Copy"}
          </Button>
        </div>
        <pre className="max-h-96 overflow-auto p-4 font-mono text-sm leading-relaxed whitespace-pre-wrap">{prompt}</pre>
      </div>
      <Button variant="ghost" className="mt-2 px-0" onClick={onGenerate}>
        Generate again
      </Button>
    </div>
  );
}
