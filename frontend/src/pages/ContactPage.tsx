// "Contact Us" page. Contact details come from config/site.ts.
import { SITE } from "../config/site";

export default function ContactPage() {
  const { email, github } = SITE.contact;

  return (
    <main className="mx-auto max-w-3xl px-4 py-12 sm:px-6">
      <h1 className="font-brand text-4xl font-bold">Contact Us</h1>
      <p className="mt-4 text-neutral-700">
        Questions, feedback or found a bug? We'd like to hear from you.
      </p>

      <ul className="mt-8 space-y-4">
        {email && (
          <li className="rounded-lg border border-black p-5">
            <p className="text-sm font-semibold">Email</p>
            <a href={`mailto:${email}`} className="mt-1 inline-block underline underline-offset-4">
              {email}
            </a>
          </li>
        )}
        <li className="rounded-lg border border-black p-5">
          <p className="text-sm font-semibold">GitHub</p>
          <a href={github} target="_blank" rel="noreferrer" className="mt-1 inline-block break-all underline underline-offset-4">
            {github}
          </a>
        </li>
      </ul>
    </main>
  );
}
