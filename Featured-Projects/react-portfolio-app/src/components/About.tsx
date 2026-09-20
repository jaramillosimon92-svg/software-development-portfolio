import { use } from "react";
import { PortfolioContext } from "../PortfolioContext";

// reads About paragraph from PortfolioContext.
export default function About() {
  const portfolioData = use(PortfolioContext);

  if (portfolioData === null) {
    return null;
  }

  return (
    <section className="about-section">
      <h2>About Me</h2>
      <p>{portfolioData.about.paragraph}</p>
    </section>
  );
}