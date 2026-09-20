interface AboutProps {
  data: {
    paragraph: string;
  };
  darkMode: boolean;
}

export default function About(props: AboutProps) {
  return (
    <section className={props.darkMode ? "about-section dark-card" : "about-section"}>
      <h2>About Me</h2>
      <p>{props.data.paragraph}</p>
    </section>
  );
}