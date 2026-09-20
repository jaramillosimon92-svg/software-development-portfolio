import { StrictMode, Suspense } from "react";
import { createRoot } from "react-dom/client";

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router";

import "./index.css";

import App from "./App";
import Projects from "./components/Projects";
import About from "./components/About";
import Contact from "./components/Contact";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Suspense fallback={<p>Loading portfolio...</p>}>
        <Routes>
          {/* Parent route uses App as the layout component. */}
          <Route path="/" element={<App />}>
            {/* Displays Projects at the root path. */}
            <Route index element={<Projects />} />

            {/* Displays the matching About and Contact components. */}
            <Route path="about" element={<About />} />
            <Route path="contact" element={<Contact />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  </StrictMode>
);