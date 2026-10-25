import { filenameFromDisposition } from "../utils/download";
import { validateLogoFile } from "../utils/fileValidation";
import { formatScore } from "../utils/format";
import { pngFile } from "./fixtures";

describe("filenameFromDisposition", () => {
  it("reads a quoted filename", () => {
    expect(filenameFromDisposition('attachment; filename="designer-recommendations.txt"', "x.txt")).toBe(
      "designer-recommendations.txt",
    );
  });
  it("reads an encoded filename", () => {
    expect(filenameFromDisposition("attachment; filename*=UTF-8''my%20file.txt", "x.txt")).toBe("my file.txt");
  });
  it("falls back when the header is missing", () => {
    expect(filenameFromDisposition(null, "fallback.txt")).toBe("fallback.txt");
  });
});

describe("validateLogoFile", () => {
  it("accepts png, jpg, jpeg and svg", () => {
    expect(validateLogoFile(pngFile("a.png"))).toBeNull();
    expect(validateLogoFile(new File(["x"], "a.jpg", { type: "image/jpeg" }))).toBeNull();
    expect(validateLogoFile(new File(["x"], "a.JPEG", { type: "image/jpeg" }))).toBeNull();
    expect(validateLogoFile(new File(["<svg/>"], "a.svg", { type: "image/svg+xml" }))).toBeNull();
  });
  it("rejects other types", () => {
    expect(validateLogoFile(new File(["x"], "a.gif", { type: "image/gif" }))).toMatch(/Only PNG/);
    expect(validateLogoFile(new File(["x"], "a.png", { type: "application/pdf" }))).toMatch(/Only PNG/);
  });
  it("rejects empty and too-large files", () => {
    expect(validateLogoFile(pngFile("a.png", 0))).toMatch(/empty/);
    expect(validateLogoFile(pngFile("a.png", 5 * 1024 * 1024 + 1))).toMatch(/larger than 5 MB/);
  });
});

describe("formatScore", () => {
  it("shows whole numbers without decimals and others with one", () => {
    expect(formatScore(8)).toBe("8");
    expect(formatScore(7.5)).toBe("7.5");
  });
});
