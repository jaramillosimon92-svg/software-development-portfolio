import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "./ui/card";

import type { ProjectData } from "../PortfolioContext";
import { useLike } from "../hooks/useLike";

interface ProjectProps {
  project: ProjectData;
}
// This gives every card its own independent liked state
export default function Project(props: ProjectProps) {
  const { liked, changeLike } = useLike();

  return (
    <Card
      className={`project-card ${props.project.important ? "featured" : ""
        } ${liked ? "liked-card" : ""
        }`}
    >
      <CardHeader className="project-card-header">
        {props.project.important && (
          <p className="featured-label">
            Featured Project
          </p>
        )}

        <img
          src={props.project.image}
          alt={props.project.title}
        />

        <CardTitle className="project-title">
          {props.project.title}
        </CardTitle>
      </CardHeader>

      <CardContent className="project-card-content">
        <p>{props.project.description}</p>

        {/*The Button calls changeLike with onClick*/}
        <button
          type="button"
          onClick={changeLike}
          className={
            liked
              ? "like-button liked"
              : "like-button"
          }
        >
          {liked ? "Liked" : "Like"}
        </button>
      </CardContent>
    </Card>
  );
}