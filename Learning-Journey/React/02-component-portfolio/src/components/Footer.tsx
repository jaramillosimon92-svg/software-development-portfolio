// This interface describes the data the Footer component expects to receive.
interface FooterProps {
  data: {
    // socialLinks is an array of objects.
    socialLinks: {
      id: number;
      name: string;
      url: string;
    }[];

    // technologies is also an array of objects.
    technologies: {
      id: number;
      name: string;
    }[];
  };
}

// This component displays the footer section of the portfolio.
export default function Footer(props: FooterProps) {
  return (
    <footer className="site-footer">
      <section>
        <h2>Social Media</h2>

        <ul>
          {/* List rendering: map loops through each social media link */}
          {props.data.socialLinks.map((link) => (
            <li key={link.id}>
              {/* Expression embedding is used for the link url and name */}
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
          {/* List rendering: map loops through each technology */}
          {props.data.technologies.map((tech) => (
            <li key={tech.id}>{tech.name}</li>
          ))}
        </ul>
      </section>
    </footer>
  );
}