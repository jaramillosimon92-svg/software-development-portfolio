import {
  use,
  useState,
  type FormEvent,
} from "react";

import { PortfolioContext } from "../PortfolioContext";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "./ui/alert-dialog";

export default function Contact() {
  const portfolioData = use(PortfolioContext);

  // Stores the values entered into the form.
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [comment, setComment] = useState("");

  // Controls whether the thank-you popup is visible.
  const [showMessage, setShowMessage] = useState(false);

  if (portfolioData === null) {
    return null;
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    // Prevents the page from refreshing.
    event.preventDefault();

    // Displays the thank-you popup.
    setShowMessage(true);

    // Clears the form after it is submitted.
    setName("");
    setEmail("");
    setComment("");
  }

  return (
    <section className="contact-section">
      <h2>Contact Me</h2>

      <p>
        Email:{" "}
        <a href={`mailto:${portfolioData.contact.email}`}>
          {portfolioData.contact.email}
        </a>
      </p>

      <form onSubmit={handleSubmit} className="contact-form">
        <div>
          <label htmlFor="name">Name</label>

          <input
            id="name"
            name="name"
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="email">Email</label>

          <input
            id="email"
            name="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="comment">Comment</label>

          <textarea
            id="comment"
            name="comment"
            value={comment}
            onChange={(event) => setComment(event.target.value)}
            required
          />
        </div>

        <button type="submit">
          Submit
        </button>
      </form>

      <AlertDialog
        open={showMessage}
        onOpenChange={setShowMessage}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>
              Comment Submitted
            </AlertDialogTitle>

            <AlertDialogDescription>
              Thank you for your comment
            </AlertDialogDescription>
          </AlertDialogHeader>

          <AlertDialogFooter>
            <AlertDialogAction>
              Close
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </section>
  );
}