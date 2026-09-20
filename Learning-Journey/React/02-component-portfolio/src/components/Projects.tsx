// This interface describes what one project object should contain.
interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  important: boolean;
}

// This interface describes the data the Projects component expects to receive.
// The data is an array of Project objects.
interface ProjectsProps {
  data: Project[];
}

// This component displays all project cards in the portfolio.
export default function Projects(props: ProjectsProps) {
  return (
    <section className="section projects-section">
      <h2>Projects</h2>

      <div className="project-grid">
        {/* List rendering: map loops through the projects array */}
        {props.data.map((project) => (
          <article
            // Conditional class: featured projects get an extra CSS class
            className={
              project.important
                ? "project-card featured"
                : "project-card"
            }
            // React needs a unique key when rendering a list
            key={project.id}
          >
            {/* Conditional rendering: this only shows if important is true */}
            {project.important && (
              <p className="featured-label">
                Featured Project
              </p>
            )}

            {/* Expression embedding is used for the image source and alt text */}
            <img
              src={project.image}
              alt={project.title}
            />

            {/* Expression embedding displays each project's title */}
            <h3>{project.title}</h3>

            {/* Expression embedding displays each project's description */}
            <p>{project.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}