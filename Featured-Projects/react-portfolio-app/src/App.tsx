import { use, useState } from "react";
import { Link, Outlet } from "react-router";

import Header from "./components/Header";
import Footer from "./components/Footer";

import { PortfolioContext } from "./PortfolioContext";

import "./App.css";

const fetchPortfolioData = async () => {
        try {
                const response = await fetch("portfolioData.json");

                if (!response.ok) {
                        throw new Error("Network response was not ok");
                }

                return response.json();
        } catch (error) {
                console.error("Error fetching portfolio data:", error);
                return null;
        }
      };

// Calls the asynchronous function outside the App component.
const portfolioPromise = fetchPortfolioData();

export default function App() {
        const [darkMode, setDarkMode] = useState(false);

        // Uses React 19's use hook to access the fetched data.
        const portfolioData = use(portfolioPromise);

        function handleDarkModeChange() {
                setDarkMode(!darkMode);
        }

        // Displays an error if the JSON file could not be loaded.
        if (portfolioData === null) {
                return <p>Unable to load portfolio data.</p>;
        }

        return (
                // Makes the fetched portfolio data available to all components.
                <PortfolioContext value={portfolioData}>
                        <div className={darkMode ? "app dark" : "app"}>
                                <Header />

                                {/* Move between routes without reloading the page. */}
                                <nav className="flex flex-wrap items-center justify-center gap-3 p-4">
                                        <Link
                                                to="/"
                                                className="rounded-lg bg-blue-600 px-4 py-2 font-bold text-white hover:bg-blue-700"
                                        >
                                                Projects
                                        </Link>

                                        <Link
                                                to="/about"
                                                className="rounded-lg bg-blue-600 px-4 py-2 font-bold text-white hover:bg-blue-700"
                                        >
                                                About
                                        </Link>

                                        <Link
                                                to="/contact"
                                                className="rounded-lg bg-blue-600 px-4 py-2 font-bold text-white hover:bg-blue-700"
                                        >
                                                Contact
                                        </Link>
                                </nav>

                                <main className="main-content">
                                        <label className="dark-mode-control flex items-center gap-2">
                                                <input
                                                        type="checkbox"
                                                        checked={darkMode}
                                                        onChange={handleDarkModeChange}
                                                />
                                                Dark Mode
                                        </label>

                                        <Outlet />
                                </main>

                                {/* Header, Outlet and Footer remain visible with nested routing. */}
                                <Footer />
                        </div>
                </PortfolioContext>
        );
}