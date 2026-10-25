import { ApiError, isAbortError, postJson } from "../api/httpClient";
import { analyzeLogo, downloadDesignerRecommendations } from "../api/logoApi";
import { analyzeSuccess, designerRecs, jsonResponse, pngFile } from "./fixtures";

const fetchMock = vi.fn<typeof fetch>();

beforeEach(() => {
  fetchMock.mockReset();
  vi.stubGlobal("fetch", fetchMock);
});
afterEach(() => vi.unstubAllGlobals());

describe("httpClient", () => {
  it("sends the file as the raw body to /api/logo/analyze", async () => {
    fetchMock.mockResolvedValue(jsonResponse(analyzeSuccess));
    const file = pngFile();
    const result = await analyzeLogo(file);

    expect(result.is_logo).toBe(true);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("http://localhost:8000/api/logo/analyze");
    expect(init?.method).toBe("POST");
    expect(init?.body).toBe(file);
    expect((init?.headers as Record<string, string>)["Content-Type"]).toBe("image/png");
  });

  it("turns the backend error shape into ApiError", async () => {
    fetchMock.mockResolvedValue(
      jsonResponse({ error: { code: "AI_UNAVAILABLE", message: "The AI service is temporarily unavailable." } }, 503),
    );
    await expect(postJson("/x", {}, { timeoutMs: 1000 })).rejects.toMatchObject({
      code: "AI_UNAVAILABLE",
      status: 503,
      message: "The AI service is temporarily unavailable.",
    });
  });

  it("uses a generic message when the error body is not JSON", async () => {
    fetchMock.mockResolvedValue(new Response("<html>Bad gateway</html>", { status: 502 }));
    await expect(postJson("/x", {}, { timeoutMs: 1000 })).rejects.toMatchObject({ code: "HTTP_502" });
  });

  it("reports network failures", async () => {
    fetchMock.mockRejectedValue(new TypeError("Failed to fetch"));
    await expect(postJson("/x", {}, { timeoutMs: 1000 })).rejects.toMatchObject({ code: "NETWORK_ERROR" });
  });

  it("reports timeouts", async () => {
    fetchMock.mockImplementation(
      (_url, init) =>
        new Promise((_resolve, reject) =>
          init?.signal?.addEventListener("abort", () => reject(new DOMException("aborted", "AbortError"))),
        ),
    );
    await expect(postJson("/x", {}, { timeoutMs: 20 })).rejects.toMatchObject({ code: "TIMEOUT" });
  });

  it("re-throws an AbortError when the caller cancels", async () => {
    fetchMock.mockImplementation(
      (_url, init) =>
        new Promise((_resolve, reject) =>
          init?.signal?.addEventListener("abort", () => reject(new DOMException("aborted", "AbortError"))),
        ),
    );
    const controller = new AbortController();
    const pending = postJson("/x", {}, { timeoutMs: 5000, signal: controller.signal });
    controller.abort();
    const error = await pending.catch((e: unknown) => e);
    expect(isAbortError(error)).toBe(true);
    expect(error).not.toBeInstanceOf(ApiError);
  });

  it("downloads the .txt with the filename from Content-Disposition", async () => {
    fetchMock.mockResolvedValue(
      new Response("TXT", {
        status: 200,
        headers: { "Content-Disposition": 'attachment; filename="designer-recommendations.txt"' },
      }),
    );
    const { blob, filename } = await downloadDesignerRecommendations(analyzeSuccess.analysis, designerRecs);
    expect(filename).toBe("designer-recommendations.txt");
    expect(await blob.text()).toBe("TXT");
    expect(JSON.parse(fetchMock.mock.calls[0][1]?.body as string)).toEqual({
      analysis: analyzeSuccess.analysis,
      recommendations: designerRecs,
    });
  });
});
