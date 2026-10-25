// Whole-app flows with fetch mocked: upload -> dashboard, not-a-logo, error, recommendations.
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { AppRoutes } from "../App";
import { analyzeSuccess, designerRecs, jsonResponse, pngFile } from "./fixtures";

const fetchMock = vi.fn<typeof fetch>();

beforeAll(() => {
  URL.createObjectURL = vi.fn(() => "blob:preview");
  URL.revokeObjectURL = vi.fn();
});
beforeEach(() => {
  fetchMock.mockReset();
  vi.stubGlobal("fetch", fetchMock);
});
afterEach(() => vi.unstubAllGlobals());

function renderApp() {
  render(
    <MemoryRouter initialEntries={["/"]}>
      <AppRoutes />
    </MemoryRouter>,
  );
}

async function uploadLogo() {
  await userEvent.upload(screen.getByTestId("file-input"), pngFile());
  await userEvent.click(screen.getByRole("button", { name: "Upload" }));
}

describe("App", () => {
  it("disables Upload until a file is chosen", () => {
    renderApp();
    expect(screen.getByRole("heading", { name: /Upload your\s*logo here/ })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Upload" })).toBeDisabled();
  });

  it("uploads a logo and shows the dashboard sections", async () => {
    fetchMock.mockResolvedValue(jsonResponse(analyzeSuccess));
    renderApp();
    await uploadLogo();

    expect(await screen.findByRole("heading", { name: "Logo pre-exists?" })).toBeInTheDocument();
    expect(screen.getByText("No significant similarity detected")).toBeInTheDocument();
    expect(screen.getByRole("meter", { name: "Overall score" })).toHaveAttribute("aria-valuenow", "7.4");
    expect(screen.getAllByRole("article")).toHaveLength(11);
    const sidebar = screen.getByRole("navigation", { name: "Results sections" });
    for (const label of ["Logo pre-exists?", "Score out of 10", "Score parameters", "Recommendations", "For AI", "For designer"]) {
      expect(within(sidebar).getByRole("button", { name: label })).toBeInTheDocument();
    }
  });

  it("shows the full-screen 'Please upload a logo' state", async () => {
    fetchMock.mockResolvedValue(jsonResponse({ is_logo: false, message: "The uploaded image does not appear to be a logo." }));
    renderApp();
    await uploadLogo();

    expect(await screen.findByRole("heading", { name: "Please upload a logo" })).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: "Upload a logo" }));
    expect(screen.getByRole("heading", { name: /Upload your\s*logo here/ })).toBeInTheDocument();
  });

  it("shows the backend error and retries", async () => {
    fetchMock
      .mockResolvedValueOnce(jsonResponse({ error: { code: "AI_UNAVAILABLE", message: "AI is busy." } }, 503))
      .mockResolvedValueOnce(jsonResponse(analyzeSuccess));
    renderApp();
    await uploadLogo();

    expect(await screen.findByText("AI is busy.")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: "Try again" }));
    expect(await screen.findByRole("heading", { name: "Logo pre-exists?" })).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("does not offer a retry for a file the backend rejects", async () => {
    fetchMock.mockResolvedValue(jsonResponse({ error: { code: "INVALID_IMAGE", message: "The image could not be read." } }, 422));
    renderApp();
    await uploadLogo();

    expect(await screen.findByText("The image could not be read.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Try again" })).not.toBeInTheDocument();
  });

  it("gets the AI prompt from the sidebar 'For AI' item and fetches it only once", async () => {
    fetchMock
      .mockResolvedValueOnce(jsonResponse(analyzeSuccess))
      .mockResolvedValueOnce(jsonResponse({ prompt: "A minimal flat vector logo with bold black strokes ..." }));
    renderApp();
    await uploadLogo();
    await screen.findByRole("heading", { name: "Logo pre-exists?" });

    const sidebar = screen.getByRole("navigation", { name: "Results sections" });
    await userEvent.click(within(sidebar).getByRole("button", { name: "For AI" }));

    expect(await screen.findByText(/A minimal flat vector logo/)).toBeInTheDocument();
    expect(screen.getByRole("radio", { name: /AI Generated/ })).toHaveAttribute("aria-checked", "true");
    const [url, init] = fetchMock.mock.calls[1];
    expect(url).toBe("http://localhost:8000/api/logo/recommendations/ai-prompt");
    expect(JSON.parse(init?.body as string)).toEqual({ analysis: analyzeSuccess.analysis });

    await userEvent.click(screen.getByRole("radio", { name: /Manually Designed/ }));
    await userEvent.click(screen.getByRole("radio", { name: /AI Generated/ }));
    expect(fetchMock.mock.calls.filter(([u]) => String(u).endsWith("/ai-prompt"))).toHaveLength(1);
  });

  it("shows designer recommendations with a download button", async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse(analyzeSuccess)).mockResolvedValueOnce(jsonResponse(designerRecs));
    renderApp();
    await uploadLogo();
    await screen.findByRole("heading", { name: "Logo pre-exists?" });

    await userEvent.click(screen.getByRole("radio", { name: /Manually Designed/ }));

    expect(await screen.findByText("No brand color.")).toBeInTheDocument();
    expect(screen.getByText("Make a square version.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Download .txt" })).toBeEnabled();
  });

  it("sends the user home when opening /results without an analysis", () => {
    render(
      <MemoryRouter initialEntries={["/results"]}>
        <AppRoutes />
      </MemoryRouter>,
    );
    expect(screen.getByRole("heading", { name: /Upload your\s*logo here/ })).toBeInTheDocument();
  });
});
