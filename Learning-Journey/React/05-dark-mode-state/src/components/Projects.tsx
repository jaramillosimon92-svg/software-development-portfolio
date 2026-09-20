import Project from "./Project";

interface ProjectData {
  id: number;
  title: string;
  description: string;
  image: string;
  important: boolean;
}

interface ProjectsProps {
  data: ProjectData[];
  darkMode: boolean;
}

export default function Projects(props: ProjectsProps) {
  return (
    <section className="projects-section">
      <h2>Projects</h2>

      <div className="project-grid">
        {props.data.map((project) => (
          <Project
            key={project.id}
            project={project}
            darkMode={props.darkMode}
          />
        ))}
      </div>
    </section>
  );
}