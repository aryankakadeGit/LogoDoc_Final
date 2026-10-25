// Quick check before uploading, for faster feedback. The backend still checks the real file.
import { MAX_UPLOAD_BYTES, MAX_UPLOAD_MB } from "../config/env";

export const ACCEPTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".svg"] as const;
export const ACCEPTED_MIME_TYPES = ["image/png", "image/jpeg", "image/svg+xml"] as const;
export const ACCEPT_ATTRIBUTE = [...ACCEPTED_MIME_TYPES, ...ACCEPTED_EXTENSIONS].join(",");

/** Returns an error message, or null when the file can be uploaded. */
export function validateLogoFile(file: File): string | null {
  const name = file.name.toLowerCase();
  const extensionOk = ACCEPTED_EXTENSIONS.some((ext) => name.endsWith(ext));
  const mimeOk = !file.type || (ACCEPTED_MIME_TYPES as readonly string[]).includes(file.type);
  if (!extensionOk || !mimeOk) return "Only PNG, JPG, JPEG or SVG files are allowed.";
  if (file.size === 0) return "The selected file is empty.";
  if (file.size > MAX_UPLOAD_BYTES) return `The file is larger than ${MAX_UPLOAD_MB} MB.`;
  return null;
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
