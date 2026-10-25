// Tracks which dashboard section is currently on screen, so the sidebar can highlight it.
// Returns [active, setActive]; setActive lets a sidebar click highlight its item right away.
import { useEffect, useState } from "react";

export function useActiveSection<T extends string>(ids: readonly T[]): [T, (id: T) => void] {
  const [active, setActive] = useState<T>(ids[0]);

  useEffect(() => {
    if (typeof IntersectionObserver === "undefined") return;

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((e) => e.isIntersecting);
        if (visible.length > 0) setActive(visible[0].target.id as T);
      },
      // A section counts as "active" when it crosses the upper part of the screen.
      { rootMargin: "-30% 0px -60% 0px" },
    );
    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    // The last section may be too short to reach that band: mark it active at the page bottom.
    const onScroll = () => {
      const atBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
      if (atBottom) setActive(ids[ids.length - 1]);
    };
    window.addEventListener("scroll", onScroll, { passive: true });

    return () => {
      observer.disconnect();
      window.removeEventListener("scroll", onScroll);
    };
  }, [ids]);

  return [active, setActive];
}
