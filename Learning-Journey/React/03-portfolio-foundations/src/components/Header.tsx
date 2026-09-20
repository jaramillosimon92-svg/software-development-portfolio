interface HeaderProps {
    data: {
      name: string;
      role: string;
      motto: string;
    };
  }
  
  export default function Header(props: HeaderProps) {
    return (
      <header className="site-header">
        <h1>{props.data.name}</h1>
        <h2>{props.data.role}</h2>
        <h3>{props.data.motto}</h3>
      </header>
    );
  }