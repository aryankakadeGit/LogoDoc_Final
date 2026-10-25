// Home page (first drawing): "Upload your logo here" on the left, upload box + Upload button on the right.
import { useState } from "react";
import { Link, useNavigate } from "react-router";
import UploadDropzone from "../components/upload/UploadDropzone";
import PrivacyNotice from "../components/upload/PrivacyNotice";
import Button from "../components/ui/Button";
import { MAX_UPLOAD_MB } from "../config/env";
import { useAnalysis } from "../context/AnalysisContext";

export default function UploadPage() {
  const { state, analyze } = useAnalysis();
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);

  function onUpload() {
    if (!file) return;
    void analyze(file);
    navigate("/results");
  }

  return (
    <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:py-20">
      <div className="grid items-center gap-10 lg:grid-cols-[1fr_auto_1.1fr]">
        <div>
          <h1 className="font-brand text-4xl leading-tight font-bold sm:text-5xl">
            Upload your
            <br />
            logo here
          </h1>
          <p className="mt-4 text-lg text-neutral-700">(JPEG, PNG, SVG, JPG only)</p>
          <p className="mt-4 max-w-md text-neutral-600">
            LogoDoc gives your logo a check-up: a score out of 10, 11 design parameters with strengths and
            weaknesses, a check against well-known logos, and clear recommendations. Max {MAX_UPLOAD_MB} MB.
          </p>
          {state.status === "success" && (
            <Link to="/results" className="mt-6 inline-block text-sm font-semibold underline underline-offset-4">
              View your last results →
            </Link>
          )}
        </div>

        <div className="hidden text-4xl text-neutral-400 lg:block" aria-hidden="true">
          - - →
        </div>

        <div className="space-y-4">
          <UploadDropzone file={file} onFileChange={setFile} />
          <div className="flex justify-center">
            <Button onClick={onUpload} disabled={!file} className="min-w-40">
              Upload
            </Button>
          </div>
        </div>
      </div>

      <div className="mt-12">
        <PrivacyNotice />
      </div>
    </main>
  );
}
