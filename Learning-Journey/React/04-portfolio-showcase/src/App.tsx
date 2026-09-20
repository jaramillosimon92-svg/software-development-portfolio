import Header from './components/Header';
import About from './components/About';
import Projects from './components/Projects';
import Footer from './components/Footer';
import './App.css';

export default function App() {
  const portfolioData = {
    header: {
      name: 'Simon Jaramillo',
      role: 'Second Year software development and network engineering',
      motto: 'Life is like riding a bicycle. To keep your balance, you must keep moving'
    },

    about: {
      paragraph:
        'I am a Sheridan College student in the Software Development and Network Engineering program. I enjoy building projects, strengthening my problem-solving skills, and exploring new areas of technology through hands-on work.'
    },

    projects: [
      {
        id: 1,
        title: 'Inventory Calculator',
        description:
          'Inventory Calculator is part of a Java project I did in class. It is a typical inventory calculator, which can store items, quantities and some of the basic features of an inventory. It helped me to improve my Java programming, variables, calculations, and keeping my code organized.',
        image:
          'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5U2WovIemDDpETllVmeodsgvuxUkaDc2Cag&s',
        isImportant: true
      },
      {
        id: 2,
        title: 'Highway Escape',
        description:
          'Highway Escape is a game I co-created with my friend for a class it is based on classic arcade game. In this game, you’ll be driving your car on the highway, trying to avoid other moving cars as long as possible.',
        image:
          'https://static0.carbuzzimages.com/wordpress/wp-content/uploads/2024/09/2025-bmw-m4-cs.jpg',
        isImportant: true
      },
      {
        id: 3,
        title: 'Movies Suggestion ',
        description:
          'This is a website that again was created for a class project, where I coded a random movie suggestion website where users could choose a genre of their choice and get a random movie from that genre. This helped me to code using user inputs, random results, and displaying them on the webpage.',
        image:
          'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600',
        isImportant: false
      },
      {
        id: 4,
        title: 'Income Calculator',
        description:
          'Income Calculator is a project I created in my python class. It calculates income based on user input and helped me practice Python variables, calculations, input, and output.',
        image:
          'https://keydifferences.com/wp-content/uploads/2016/10/income-vs-wealth.jpg',
        isImportant: false
      },
      {
        id: 5,
        title: 'Pick the Number Game',
        description:
          'Pick the Number Game is a typical first python program almost everyone creates. The player tries to guess or pick the correct number, and the program gives feedback based on the user input (lower or higher). This was one of my first projects and it helped me practice Python input, conditions, and basic game logic.',
        image:
          'https://www.gamesbrief.com/assets/2019/04/questions.jpg',
        isImportant: false
      }
    ],




    footer: {
      socialLinks: [
        {
          id: 1,
          name: 'LinkedIn',
          url: 'https://www.linkedin.com/in/sjaramillo12'
        },
      
      ],

      technologies: [
        {
          id: 1,
          name: 'React'
        },
        {
          id: 2,
          name: 'TypeScript'
        },
        {
          id: 3,
          name: 'HTML'
        },
        {
          id: 4,
          name: 'CSS'
        }
      ]
    }
  };

  return (
    <div className="app">
      <Header data={portfolioData.header} />

      <main>
        <About data={portfolioData.about} />
        <Projects data={portfolioData.projects} />
      </main>

      <Footer data={portfolioData.footer} />
    </div>
  );
}
