import {
  use,
  useState,
  type ChangeEvent,
} from "react";

import Project from "./Project";

import {
  PortfolioContext,
  type ProjectData,
} from "../PortfolioContext";

// Projects receives the complete projects array from PortfolioContext and stores it in ProjectsData
export default function Projects() {
  const portfolioData = use(PortfolioContext);
  const projectsData = portfolioData
    ? portfolioData.projects
    : [];

  // FilterText stores text entered by user 
  const [filterText, setFilterText] = useState("");

  // FilteredData stores the project cards
  const [filteredData, setFilteredData] =
    useState<ProjectData[]>(projectsData);

  // Runs whenever the input changes
  function handleFilterChange(
    event: ChangeEvent<HTMLInputElement>
  ) {
    const userInput = event.target.value;

    setFilterText(userInput);
    // When input is empty, project data is placed into FilteredData
    if (userInput === "") {
      setFilteredData(projectsData);
    } else {
      setFilteredData(
        // Otherwise the filter only keeps the projects that contains the users text.
        projectsData.filter((project) =>
          project.title
            .toLowerCase()
            .includes(userInput.toLowerCase())
        )
      );
    }
  }

  if (portfolioData === null) {
    return null;
  }

  return (
    <section className="projects-section">
      <h2>Projects</h2>

      <label>
        Filter projects by title:

        <input
          type="text"
          value={filterText}
          onChange={handleFilterChange}
          placeholder="Enter a project title"
          className="mb-6 mt-2 block w-full rounded-lg border border-gray-300 bg-white p-3 text-black"
        />
      </label>

      <div className="project-grid">
        {filteredData.map((project) => (
          <Project
            key={project.id}
            project={project}
          />
        ))}
      </div>
    </section>
  );
}