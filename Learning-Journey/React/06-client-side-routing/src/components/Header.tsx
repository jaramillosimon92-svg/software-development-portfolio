import { use } from "react";
import { PortfolioContext } from "../PortfolioContext";

export default function Header() {
  // Reacts use function osed to access the context.
  const portfolioData = use(PortfolioContext);

  if (portfolioData === null) {
    return null;
  }

  return (
    <header className="site-header">
      <h1>{portfolioData.header.name}</h1>
      <h2>{portfolioData.header.role}</h2>
      <h3>{portfolioData.header.motto}</h3>
    </header>
  );
}