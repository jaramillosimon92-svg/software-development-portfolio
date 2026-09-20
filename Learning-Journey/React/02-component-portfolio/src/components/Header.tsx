// This interface describes the data the Header component expects to receive.
interface HeaderProps {
  data: {
    name: string;
    role: string;
    motto: string;
  };
}

// This component displays the top header section of the portfolio.
export default function Header(props: HeaderProps) {
  return (
    <header className="site-header">
      {/* Expression embedding is used to display data from App.tsx */}
      <h1>{props.data.name}</h1>
      <h2>{props.data.role}</h2>
      <h3>{props.data.motto}</h3>
    </header>
  );
}