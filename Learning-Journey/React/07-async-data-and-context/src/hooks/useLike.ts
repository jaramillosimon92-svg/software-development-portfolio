import { useState } from "react";

// Hook uses useState to remeebr whether a project card is liked or not 
export function useLike() {
  const [liked, setLiked] = useState(false);

  function changeLike() {
    // Changes the value to the opposite of the previous value.
    setLiked((previousLiked) => !previousLiked);
  }

// Hook returns the liked value, and the changeLikefuntion so a component can use them.
  return { liked, changeLike };
}