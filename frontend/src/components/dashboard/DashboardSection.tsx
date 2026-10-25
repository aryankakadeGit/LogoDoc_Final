// Shared frame for each dashboard section: an anchor id the sidebar scrolls to, plus a title.
import type { ReactNode } from "react";
import type { SectionId } from "../../types/ui";

interface DashboardSectionProps {
  id: SectionId;
  title: string;
  subtitle?: string;
  children: ReactNode;
  className?: string;
}

export default function DashboardSection({ id, title, subtitle, children, className = "" }: DashboardSectionProps) {
  return (
    <section id={id} aria-labelledby={`${id}-title`} className={`scroll-mt-40 border-b border-neutral-200 py-10 last:border-b-0 lg:scroll-mt-28 ${className}`}>
      <h2 id={`${id}-title`} className="text-2xl font-bold">
        {title}
      </h2>
      {subtitle && <p className="mt-1 text-sm text-neutral-600">{subtitle}</p>}
      <div className="mt-6">{children}</div>
    </section>
  );
}
