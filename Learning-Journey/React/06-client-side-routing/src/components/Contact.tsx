import { use } from "react";
import { PortfolioContext } from "../PortfolioContext";

// Reads the eamil from context.
export default function Contact() {
  const portfolioData = use(PortfolioContext);

  if (portfolioData === null) {
    return null;
  }

  return (
    <section className="contact-section">
      <h2>Contact Me</h2>

      <p>
        Email:{" "}
        {/*displays the stored email, and allows user to open an email app.*/}
        <a href={`mailto:${portfolioData.contact.email}`}>
          {portfolioData.contact.email}
        </a>
      </p>
    </section>
  );
}