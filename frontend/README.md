# LogoDoc — Frontend

React + TypeScript + Vite + Tailwind CSS. Black-and-white UI that only **shows** what the backend returns (no analysis logic here).

## Run

Needs Node.js 20.19+ (or 22.12+). Start the backend first (`uvicorn app.main:app --reload` in `backend/`).

```powershell
cd frontend
copy .env.example .env      # first time only
npm ci                      # installs exactly what package-lock.json lists
npm run dev                 # http://localhost:5173
```

Open **http://localhost:5173** (not 127.0.0.1 — the backend's CORS only allows `localhost:5173`).

| Command | What it does |
|---|---|
| `npm run dev` | Dev server with hot reload |
| `npm test` | Tests (Vitest, watch mode). `npx vitest run` runs once |
| `npm run typecheck` | TypeScript check |
| `npm run build` | Type check + production build into `dist/` |
| `npm run generate:types` | Regenerate `src/types/api.generated.ts` from the running backend |

Use `npm ci` rather than `npm install` on the first install: with npm 10, a fresh `npm install` without the lock file can fail with
`Cannot read properties of null (reading 'edgesOut')` (an npm bug with Vite's optional dev-tools packages).

## Pages

| URL | Page |
|---|---|
| `/` | Home — "Upload your logo here", upload box, Upload button, privacy notice |
| `/results` | Loading → "Please upload a logo" / error → dashboard (sidebar + all sections on one page) |
| `/score-parameters` | Explains the 11 parameters |
| `/about` | About LogoDoc |
| `/contact` | Contact details (edit `src/config/site.ts`) |

The analysis lives only in browser memory. Refreshing `/results` sends the user back to Home.

## Structure

```text
src/
├── main.tsx, App.tsx        bootstrap + routes
├── index.css                Tailwind + theme
├── config/                  env.ts (API URL, limits), site.ts (brand/contact), parameters.ts (info page copy)
├── types/                   api.generated.ts (generated), api.ts (friendly names), ui.ts (UI state)
├── api/                     httpClient.ts (fetch, timeout, ApiError), logoApi.ts (4 backend calls)
├── context/                 AnalysisContext.tsx (shares the analysis between Home and Results)
├── hooks/                   useLogoAnalysis, useAiPrompt, useDesignerRecommendations, useRequest, useActiveSection
├── components/
│   ├── layout/              Navbar, BrandLogo
│   ├── upload/              UploadDropzone, PrivacyNotice
│   ├── states/              LoadingState, NotALogoState, ErrorState
│   ├── dashboard/           Sidebar, DashboardSection, LogoStatusSection, OverallScoreSection, ScoreMeter, ParametersSection, ParameterCard
│   ├── recommendations/     RecommendationsSection, LogoSourceSelector, AiPromptPanel, DesignerRecommendationsPanel, RequestStatus
│   └── ui/                  Button
├── pages/                   UploadPage, DashboardPage, ScoreParametersPage, AboutPage, ContactPage
├── utils/                   clipboard, download, fileValidation, format
└── __tests__/               Vitest + Testing Library tests
```

## Flow

```text
UploadPage ──analyze(file)──► useLogoAnalysis ──POST /api/logo/analyze──► backend
                                   │
              DashboardPage reads the state:
              loading → LoadingState
              not_logo → NotALogoState ("Please upload a logo")
              error → ErrorState (backend message + retry)
              success → Sidebar + LogoStatus + OverallScore + Parameters + Recommendations
                                   │
              Recommendations: AI Generated → POST /recommendations/ai-prompt → prompt + Copy
                               Manually Designed → POST /recommendations/designer → advice
                                                   → POST /designer/download → .txt file
```
