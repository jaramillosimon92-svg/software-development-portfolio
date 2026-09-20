interface AboutProps {
    data: {
      paragraph: string;
    };
  }
  
  export default function About(props: AboutProps) {
    return (
      <section className="section about-section">
        <h2>About Me</h2>
        <p>{props.data.paragraph}</p>
      </section>
    );
  }