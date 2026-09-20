import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

// Import from react router
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
      <Routes>
        {/*Parent route, uses App as the layout component*/}
        <Route path="/" element={<App />}>
          {/*display Projects at the root path*/}
          <Route index element={<Projects />} />
          {/*display their matching compoents (/about and /contact) */}
          <Route path="about" element={<About />} />
          <Route path="contact" element={<Contact />} />
        </Route>
      </Routes>
      {/*enables routing in the application*/}
    </BrowserRouter>
  </StrictMode>
);