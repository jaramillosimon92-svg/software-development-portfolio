interface FooterProps {
  data: {
    socialLinks: {
      id: number;
      name: string;
      url: string;
    }[];

    technologies: {
      id: number;
      name: string;
    }[];
  };
}

export default function Footer(props: FooterProps) {
  return (
    <footer className="site-footer">
      <div className="footer-content">
        <section>
          <h2>Social Media</h2>

          <ul>
            {props.data.socialLinks.map((link) => (
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
            {props.data.technologies.map((tech) => (
              <li key={tech.id}>{tech.name}</li>
            ))}
          </ul>
        </section>
      </div>
    </footer>
  );
}