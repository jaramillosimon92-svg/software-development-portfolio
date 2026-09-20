import { useState } from "react";

import Header from "./components/Header";
import About from "./components/About";
import Projects from "./components/Projects";
import Footer from "./components/Footer";

import calcImg from "./assets/calc.jpg";
import herosImg from "./assets/heros.jpg";
import carsImg from "./assets/cars.jpg";
import reactApp from "./assets/reactApp.jpeg";
import sheridanImg from "./assets/sheridan.jpg";

import "./App.css";

export default function App() {
  const [darkMode, setDarkMode] = useState(false);

  function handleDarkModeChange() {
    setDarkMode(!darkMode);
  }

  const portfolioData = {
    header: {
      name: "Simon Jaramillo",
      role: "Second Year Sheridan Software Engineering Student and Aspiring AI Engineer",
      motto: "Building the tools that change the world",
    },

    about: {
      paragraph:
        "I'm a student at Sheridan College. My passion is learning how to develop tools that can make a change in society. This portfolio includes projects that helped me practise components, data structures, list rendering, conditional rendering, and semantic HTML.",
    },

    projects: [
      {
        id: 1,
        title: "Superhero Name Generator",
        description:
          "A fun JavaScript project that generates random superhero names using arrays, variables, and functions. The application combines different words together to create unique superhero identities.",
        image: herosImg,
        important: true,
      },

      {
        id: 2,
        title: "Tax Calculator App",
        description:
          "A JavaScript tax calculator that allows users to enter income values and calculate estimated taxes dynamically. The project uses variables, functions, user input, and mathematical calculations.",
        image: calcImg,
        important: true,
      },

      {
        id: 3,
        title: "Highway Escape",
        description:
          "A driving game inspired by classic arcade games where the player avoids traffic and obstacles while surviving as long as possible on the highway. The project uses JavaScript logic, movement controls, and collision detection.",
        image: carsImg,
        important: false,
      },

      {
        id: 4,
        title: "React Developer Portfolio",
        description:
          "A personal portfolio created with React components, props, list rendering, conditional rendering, and CSS.",
        image: reactApp,
        important: false,
      },

      {
        id: 5,
        title: "Sheridan Student Dashboard",
        description:
          "A web page showing student information using semantic HTML, CSS styling, and embedded variables.",
        image: sheridanImg,
        important: false,
      },
    ],

    footer: {
      socialLinks: [
        {
          id: 1,
          name: "LinkedIn",
          url: "https://www.linkedin.com/in/sjaramillo12",
        },

        {
          id: 2,
          name: "Instagram",
          url: "https://www.instagram.com/sjaramilllo?igsh=MWJmbWt3bTA3bDN4bg%3D%3D&utm_source=qr",
        },

        {
          id: 3,
          name: "YouTube",
          url: "https://www.youtube.com/@coldbeatzzz",
        },
      ],

      technologies: [
        { id: 1, name: "React" },
        { id: 2, name: "TypeScript" },
        { id: 3, name: "HTML" },
        { id: 4, name: "CSS" },
        { id: 5, name: "Vite" },
        { id: 6, name: "Tailwind" },
        { id: 7, name: "shadcn" },
      ],
    },
  };

  return (
    <div className={darkMode ? "app dark" : "app"}>
      <Header data={portfolioData.header} />

      <main className="main-content">
        <label className="dark-mode-control flex items-center gap-2">
          <input
            type="checkbox"
            checked={darkMode}
            onChange={handleDarkModeChange}
          />
          Dark Mode
        </label>

        <About data={portfolioData.about} darkMode={darkMode} />

        <Projects data={portfolioData.projects} darkMode={darkMode} />
      </main>

      <Footer data={portfolioData.footer} />
    </div>
  );
}