// Left menu: Logo pre-exists?, Score out of 10, Score parameters, Recommendations (For AI / For designer).
// Clicking an item scrolls to that section on the same page. On small screens it becomes a top strip.
import type { LogoSource, SectionId } from "../../types/ui";

const ITEMS: { id: SectionId; label: string }[] = [
  { id: "logo-status", label: "Logo pre-exists?" },
  { id: "overall-score", label: "Score out of 10" },
  { id: "parameters", label: "Score parameters" },
  { id: "recommendations", label: "Recommendations" },
];

const SOURCES: { id: LogoSource; label: string }[] = [
  { id: "ai", label: "For AI" },
  { id: "designer", label: "For designer" },
];

interface SidebarProps {
  active: SectionId;
  source: LogoSource | null;
  onNavigate: (id: SectionId) => void;
  onSelectSource: (source: LogoSource) => void;
}

function itemClass(selected: boolean) {
  return `w-full whitespace-nowrap rounded-md px-3 py-2 text-left text-sm font-medium transition-colors ${
    selected ? "bg-black text-white" : "text-black hover:bg-neutral-100"
  }`;
}

export default function Sidebar({ active, source, onNavigate, onSelectSource }: SidebarProps) {
  return (
    <nav aria-label="Results sections">
      <ul className="flex gap-1 overflow-x-auto lg:flex-col lg:overflow-visible">
        {ITEMS.map((item) => (
          <li key={item.id}>
            <button
              type="button"
              className={itemClass(active === item.id)}
              aria-current={active === item.id ? "true" : undefined}
              onClick={() => onNavigate(item.id)}
            >
              {item.label}
            </button>
            {item.id === "recommendations" && (
              <ul className="hidden border-l border-neutral-300 lg:ml-4 lg:mt-1 lg:block lg:pl-2">
                {SOURCES.map((s) => (
                  <li key={s.id}>
                    <button
                      type="button"
                      className={`w-full rounded-md px-3 py-1.5 text-left text-sm transition-colors ${
                        source === s.id ? "font-semibold underline" : "text-neutral-700 hover:bg-neutral-100"
                      }`}
                      onClick={() => onSelectSource(s.id)}
                    >
                      {s.label}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}
