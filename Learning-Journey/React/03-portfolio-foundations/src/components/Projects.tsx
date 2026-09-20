interface Project {
    id: number;
    title: string;
    description: string;
    image: string;
    important: boolean;
  }
  
  interface ProjectsProps {
    data: Project[];
  }
  
  export default function Projects(props: ProjectsProps) {
    return (
      <section className="section projects-section">
        <h2>Projects</h2>
  
        <div className="project-grid">
          {props.data.map((project) => (
            <article
              className={
                project.important
                  ? "project-card featured"
                  : "project-card"
              }
              key={project.id}
            >
              {project.important && (
                <p className="featured-label">
                  Featured Project
                </p>
              )}
  
              <img
                src={project.image}
                alt={project.title}
              />
  
              <h3>{project.title}</h3>
  
              <p>{project.description}</p>
            </article>
          ))}
        </div>
      </section>
    );
  }