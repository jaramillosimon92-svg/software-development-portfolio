interface AboutData {
  paragraph: string;
}

interface AboutProps {
  data: AboutData;
}

export default function About(props: AboutProps) {
  const aboutText = props.data.paragraph;

  return (
    <section className="about">
      <h2>{'About Me'}</h2>
      <p>{aboutText}</p>
    </section>
  );
}