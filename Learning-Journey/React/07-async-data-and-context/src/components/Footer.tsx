import { use } from "react";
import { PortfolioContext } from "../PortfolioContext";

// Recieves data (social links/technologies) from portfolioContext
export default function Footer() {
  const portfolioData = use(PortfolioContext);

  if (portfolioData === null) {
    return null;
  }

  return (
    <footer className="site-footer">
      <div className="footer-content">
        <section>
          <h2>Social Media</h2>

          <ul>
            {portfolioData.footer.socialLinks.map((link) => (
              <li key={link.id}>
                <a href={link.url} target="_blank">
                  {link.name}
                </a>
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h2>Technologies Used</h2>

          <ul>
            {portfolioData.footer.technologies.map((tech) => (
              <li key={tech.id}>{tech.name}</li>
            ))}
          </ul>
        </section>
      </div>
    </footer>
  );
}