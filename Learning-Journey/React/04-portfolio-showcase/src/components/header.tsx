interface HeaderData {
  name: string;
  role: string;
  motto: string;
}

interface HeaderProps {
  data: HeaderData;
}

export default function Header(props: HeaderProps) {
  const heading = props.data.name;
  const role = props.data.role;
  const motto = props.data.motto;

  return (
    <header className="header">
      <h1>{heading}</h1>
      <h2>{role}</h2>
      <h3>{motto}</h3>
    </header>
  );
}