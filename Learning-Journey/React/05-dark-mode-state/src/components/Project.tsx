import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "./ui/card";

interface ProjectData {
  id: number;
  title: string;
  description: string;
  image: string;
  important: boolean;
}

interface ProjectProps {
  project: ProjectData;
  darkMode: boolean;
}

export default function Project(props: ProjectProps) {
  return (
    <Card
      className={
        props.darkMode
          ? "project-card dark-card"
          : props.project.important
          ? "project-card featured"
          : "project-card"
      }
    >
      <CardHeader className="project-card-header">
        {props.project.important && (
          <p className="featured-label">Featured Project</p>
        )}

        <img src={props.project.image} alt={props.project.title} />

        <CardTitle className="project-title">
          {props.project.title}
        </CardTitle>
      </CardHeader>

      <CardContent className="project-card-content">
        <p>{props.project.description}</p>
      </CardContent>
    </Card>
  );
}