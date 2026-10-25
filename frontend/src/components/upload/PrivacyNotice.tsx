// Tells the user how their logo is handled before they upload it.

export default function PrivacyNotice() {
  return (
    <aside className="rounded-lg border border-neutral-300 bg-neutral-50 p-4 text-sm text-neutral-700">
      <p className="font-semibold text-black">Privacy</p>
      <p className="mt-1">
        Your logo is processed in memory and is not stored by LogoDoc. To analyze it, the image is sent to Google
        Gemini (AI). On Gemini's free tier, Google may use submitted content to improve its services, so please
        don't upload confidential designs.
      </p>
    </aside>
  );
}
