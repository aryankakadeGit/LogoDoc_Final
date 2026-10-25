// Top bar: brand on the left, page links on the right (collapses to a menu on small screens).
import { useState } from "react";
import { Link, NavLink } from "react-router";
import BrandLogo from "./BrandLogo";

const LINKS = [
  { to: "/", label: "Home" },
  { to: "/score-parameters", label: "Score Parameters" },
  { to: "/about", label: "About Us" },
  { to: "/contact", label: "Contact Us" },
] as const;

function linkClass({ isActive }: { isActive: boolean }) {
  return `block rounded-md px-3 py-2 text-sm font-medium transition-colors ${
    isActive ? "bg-black text-white" : "text-black hover:bg-neutral-100"
  }`;
}

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-30 border-b border-black bg-white">
      <nav className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6" aria-label="Main">
        <Link to="/" className="flex items-center border-r border-dashed border-neutral-400 pr-6" onClick={() => setOpen(false)}>
          <BrandLogo />
        </Link>

        <ul className="hidden items-center gap-2 md:flex">
          {LINKS.map((link) => (
            <li key={link.to}>
              <NavLink to={link.to} end className={linkClass}>
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>

        <button
          type="button"
          className="rounded-md border border-black px-3 py-2 text-sm font-medium md:hidden"
          aria-expanded={open}
          aria-controls="mobile-menu"
          onClick={() => setOpen((v) => !v)}
        >
          {open ? "Close" : "Menu"}
        </button>
      </nav>

      {open && (
        <ul id="mobile-menu" className="space-y-1 border-t border-neutral-200 px-4 py-3 md:hidden">
          {LINKS.map((link) => (
            <li key={link.to}>
              <NavLink to={link.to} end className={linkClass} onClick={() => setOpen(false)}>
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>
      )}
    </header>
  );
}
