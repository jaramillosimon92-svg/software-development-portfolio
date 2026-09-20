interface SocialLink {
  id: number;
  name: string;
  url: string;
}

interface Technology {
  id: number;
  name: string;
}

interface FooterData {
  socialLinks: SocialLink[];
  technologies: Technology[];
}

interface FooterProps {
  data: FooterData;
}

export default function Footer(props: FooterProps) {
  const socialLinks = props.data.socialLinks;
  const technologies = props.data.technologies;
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <section>
        <h2>{'Social Media'}</h2>

        <ul>
          {socialLinks.map((link) => {
            return (
              <li key={link.id}>
                <a href={link.url}>{link.name}</a>
              </li>
            );
          })}
        </ul>
      </section>

      <section>
        <h2>{'Technologies Used'}</h2>

        <ul>
          {technologies.map((technology) => {
            return <li key={technology.id}>{technology.name}</li>;
          })}
        </ul>
      </section>

      <p>{`© ${currentYear} My React Portfolio`}</p>
    </footer>
  );
}