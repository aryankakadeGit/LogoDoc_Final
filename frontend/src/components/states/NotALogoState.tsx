// Full-screen "Please upload a logo" state when the AI says the image is not a logo.
import Button from "../ui/Button";

interface NotALogoStateProps {
  message: string;
  previewUrl: string;
  onUploadAnother: () => void;
}

export default function NotALogoState({ message, previewUrl, onUploadAnother }: NotALogoStateProps) {
  return (
    <section className="flex min-h-[calc(100vh-5rem)] flex-col items-center justify-center gap-5 px-4 text-center">
      <div className="flex h-40 w-40 items-center justify-center rounded-lg border-2 border-dashed border-neutral-400 p-3">
        <img src={previewUrl} alt="The image you uploaded" className="max-h-full max-w-full object-contain opacity-60" />
      </div>
      <h1 className="text-3xl font-bold">Please upload a logo</h1>
      <p className="max-w-md text-base text-neutral-700">{message}</p>
      <Button onClick={onUploadAnother}>Upload a logo</Button>
    </section>
  );
}
