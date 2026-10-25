// "About Us" page: what LogoDoc does and how it works.
import { Link } from "react-router";
import { StethoscopeMark } from "../components/layout/BrandLogo";
import { SITE } from "../config/site";

const STEPS = [
  { title: "Upload", text: "Upload your logo as PNG, JPG, JPEG or SVG." },
  { title: "Check-up", text: "AI confirms it is a logo and scores 11 design parameters." },
  { title: "Results", text: "See your score, strengths, weaknesses and similarity to well-known logos." },
  { title: "Improve", text: "Get an improved AI prompt, or advice to share with your designer." },
];

export default function AboutPage() {
  return (
    <main className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <div className="flex items-center gap-4">
        <StethoscopeMark className="h-16 w-auto" />
        <h1 className="font-brand text-4xl font-bold">About {SITE.name}</h1>
      </div>
      <p className="mt-6 text-lg text-neutral-700">
        {SITE.name} is a doctor for logos. It gives your logo a quick, honest check-up and tells you in plain
        language what works, what doesn't, and what to change.
      </p>

      <h2 className="mt-10 text-xl font-bold">How it works</h2>
      <ol className="mt-4 grid gap-4 sm:grid-cols-2">
        {STEPS.map((step, i) => (
          <li key={step.title} className="rounded-lg border border-black p-5">
            <span className="text-sm font-bold text-neutral-400">Step {i + 1}</span>
            <h3 className="mt-1 font-semibold">{step.title}</h3>
            <p className="mt-1 text-sm text-neutral-600">{step.text}</p>
          </li>
        ))}
      </ol>

      <h2 className="mt-10 text-xl font-bold">Good to know</h2>
      <ul className="mt-3 list-disc space-y-2 pl-5 text-neutral-700">
        <li>Your logo is processed in memory and not stored by {SITE.name}.</li>
        <li>The analysis is done by AI (Google Gemini), so treat it as expert-style guidance, not a final verdict.</li>
        <li>The similarity check is an automated visual check, not a trademark search or legal advice.</li>
      </ul>

      <Link to="/" className="mt-10 inline-block rounded-md bg-black px-5 py-2.5 text-sm font-semibold text-white">
        Check your logo
      </Link>
    </main>
  );
}
