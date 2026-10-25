// LogoDoc brand mark: the word "Logo" held by a stethoscope, plus the "Logo / Doc" wordmark.

export function StethoscopeMark({ className = "h-14 w-auto" }: { className?: string }) {
  return (
    <svg viewBox="0 0 76 62" className={className} role="img" aria-label="LogoDoc logo">
      <g fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
        {/* ear tubes forming a cradle around the word */}
        <path d="M8 7 V27 Q8 36 17 36 H37 Q46 36 46 27 V7" />
        {/* main tube down to the chest piece */}
        <path d="M27 36 V45 Q27 56 38 56 Q50 56 55 47" />
        {/* chest piece */}
        <circle cx="60" cy="42" r="6.5" />
        <circle cx="60" cy="42" r="2.2" fill="currentColor" />
      </g>
      {/* ear tips */}
      <circle cx="8" cy="5" r="3" fill="currentColor" />
      <circle cx="46" cy="5" r="3" fill="currentColor" />
      <text
        x="27"
        y="27"
        textAnchor="middle"
        fontFamily="Fraunces, Georgia, 'Times New Roman', serif"
        fontWeight="700"
        fontSize="14"
        fill="currentColor"
      >
        Logo
      </text>
    </svg>
  );
}

export default function BrandLogo() {
  return (
    <span className="flex items-center gap-2 text-black">
      <StethoscopeMark />
      <span className="font-brand text-xl leading-tight font-bold">
        Logo
        <br />
        Doc
      </span>
    </span>
  );
}
