// Top-level layout and routes. The analysis state lives in AnalysisProvider so the
// Home page can start it and the Results page can show it.
import { BrowserRouter, Navigate, Route, Routes } from "react-router";
import Navbar from "./components/layout/Navbar";
import { AnalysisProvider } from "./context/AnalysisContext";
import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";
import DashboardPage from "./pages/DashboardPage";
import ScoreParametersPage from "./pages/ScoreParametersPage";
import UploadPage from "./pages/UploadPage";

export function AppRoutes() {
  return (
    <AnalysisProvider>
      <Navbar />
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/results" element={<DashboardPage />} />
        <Route path="/score-parameters" element={<ScoreParametersPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AnalysisProvider>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}
