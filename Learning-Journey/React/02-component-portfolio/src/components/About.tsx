// This interface describes the type of data this component expects to receive.
interface AboutProps {
  data: {
    // The about paragraph must be a string.
    paragraph: string;
  };
}

// This component displays the About Me section of the portfolio.
export default function About(props: AboutProps) {
  return (
    <section className="section about-section">
      <h2>About Me</h2>

      {/* Expression embedding is used here to display the paragraph from App.tsx */}
      <p>{props.data.paragraph}</p>
    </section>
  );
}