const express = require('express');
const { randomSuperhero } = require('superheroes');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// Power lists by birth month
const MONTH_POWERS = {
  1:  { power: 'Cryokinesis',       color: '#a8d8ea' },
  2:  { power: 'Telepathy',          color: '#c9b1ff' },
  3:  { power: 'Storm Control',      color: '#b2f0e8' },
  4:  { power: 'Super Strength',     color: '#f9c784' },
  5:  { power: 'Nature Manipulation',color: '#90d26d' },
  6:  { power: 'Solar Absorption',   color: '#ffe066' },
  7:  { power: 'Time Manipulation',  color: '#ffb347' },
  8:  { power: 'Pyrokinesis',        color: '#ff6b6b' },
  9:  { power: 'Gravity Control',    color: '#d4a5a5' },
  10: { power: 'Shadow Shifting',    color: '#9b5de5' },
  11: { power: 'Electrokinesis',     color: '#00f5d4' },
  12: { power: 'Astral Projection',  color: '#74c2e1' }
};

// Adjective from first letter of name
const LETTER_ADJECTIVES = {
  A:'Almighty', B:'Blazing', C:'Cosmic', D:'Daring', E:'Eternal',
  F:'Fearless', G:'Galactic', H:'Heroic', I:'Invincible', J:'Just',
  K:'Kinetic', L:'Legendary', M:'Mighty', N:'Noble', O:'Omnipotent',
  P:'Phantom', Q:'Quantum', R:'Radiant', S:'Supreme', T:'Titanic',
  U:'Unstoppable', V:'Valiant', W:'Warp', X:'Xenon', Y:'Yielding', Z:'Zealous'
};

app.get('/generate', (req, res) => {
  const { name, month } = req.query;

  if (!name || !month) {
    return res.status(400).json({ error: 'Name and month are required.' });
  }

  const monthNum = parseInt(month);
  if (monthNum < 1 || monthNum > 12) {
    return res.status(400).json({ error: 'Month must be between 1 and 12.' });
  }

  // Pick a random superhero name from the npm package
  const heroName = randomSuperhero();

  // Build personalized alias
  const firstLetter = name.trim()[0].toUpperCase();
  const adjective = LETTER_ADJECTIVES[firstLetter] || 'Amazing';
  const { power, color } = MONTH_POWERS[monthNum];

  res.json({
    alias: `${adjective} ${heroName}`,
    power,
    color,
    message: `Born in month ${monthNum}, you wield the power of ${power}!`
  });
});

app.listen(PORT, () => {
  console.log(`🦸 Superhero Name Generator running at http://localhost:${PORT}`);
});
