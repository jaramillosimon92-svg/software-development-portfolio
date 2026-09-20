interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  isImportant: boolean;
}

interface ProjectsProps {
  data: Project[];
}

export default function Projects(props: ProjectsProps) {
  const projects = props.data;
  const sectionTitle = 'My Projects';

  return (
    <section className="projects">
      <h2>{sectionTitle}</h2>

      <div className="project-grid">
        {projects.map((project) => {
          return (
            <article
              className={project.isImportant ? 'project-card important' : 'project-card'}
              key={project.id}
            >
              {project.isImportant ? (
                <p className="featured">{'Featured Project'}</p>
              ) : (
                <p className="regular">{'Regular Project'}</p>
              )}

              <img src={project.image} alt={project.title} />

              <h3>{project.title}</h3>

              <p>{project.description}</p>
            </article>
          );
        })}
      </div>
    </section>
  );
}