import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ParameterCard from "../components/dashboard/ParameterCard";
import ScoreMeter from "../components/dashboard/ScoreMeter";
import UploadDropzone from "../components/upload/UploadDropzone";
import { parameters, pngFile } from "./fixtures";

beforeAll(() => {
  URL.createObjectURL = vi.fn(() => "blob:preview");
  URL.revokeObjectURL = vi.fn();
});

describe("ParameterCard", () => {
  it("shows score, positives and negatives", () => {
    render(<ParameterCard parameter={parameters[0]} />);
    expect(screen.getByRole("heading", { name: "Visual Simplicity" })).toBeInTheDocument();
    expect(screen.getByLabelText("Score 6 out of 10")).toBeInTheDocument();
    expect(screen.getByText("Visual Simplicity positive")).toBeInTheDocument();
    expect(screen.getByText("Visual Simplicity negative")).toBeInTheDocument();
  });

  it("shows N/A with the reason when not applicable", () => {
    render(<ParameterCard parameter={parameters[1]} />);
    expect(screen.getByLabelText("Not applicable")).toHaveTextContent("N/A");
    expect(screen.getByText("Not applicable: this logo has no text.")).toBeInTheDocument();
  });
});

describe("ScoreMeter", () => {
  it("exposes the score as a meter", () => {
    render(<ScoreMeter score={7.4} />);
    const meter = screen.getByRole("meter", { name: "Overall score" });
    expect(meter).toHaveAttribute("aria-valuenow", "7.4");
    expect(meter).toHaveTextContent("7.4");
  });
});

describe("UploadDropzone", () => {
  it("accepts a valid file", async () => {
    const onFileChange = vi.fn();
    render(<UploadDropzone file={null} onFileChange={onFileChange} />);
    await userEvent.upload(screen.getByTestId("file-input"), pngFile());
    expect(onFileChange).toHaveBeenCalledWith(expect.any(File));
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("rejects an unsupported file with a message", async () => {
    const onFileChange = vi.fn();
    render(<UploadDropzone file={null} onFileChange={onFileChange} />);
    const gif = new File(["x"], "a.gif", { type: "image/gif" });
    await userEvent.upload(screen.getByTestId("file-input"), gif, { applyAccept: false });
    expect(onFileChange).toHaveBeenCalledWith(null);
    expect(screen.getByRole("alert")).toHaveTextContent("Only PNG, JPG, JPEG or SVG files are allowed.");
  });
});
