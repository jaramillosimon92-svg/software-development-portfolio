import { createContext } from "react";

export interface HeaderData {
  name: string;
  role: string;
  motto: string;
}

export interface AboutData {
  paragraph: string;
}

export interface ContactData {
  email: string;
}

export interface ProjectData {
  id: number;
  title: string;
  description: string;
  image: string;
  important: boolean;
}

export interface SocialLink {
  id: number;
  name: string;
  url: string;
}

export interface Technology {
  id: number;
  name: string;
}

export interface FooterData {
  socialLinks: SocialLink[];
  technologies: Technology[];
}

export interface PortfolioData {
  header: HeaderData;
  about: AboutData;
  contact: ContactData;
  projects: ProjectData[];
  footer: FooterData;
}

// Creates PorfolioContext, value can contain the complete portfolioData object, or null.
export const PortfolioContext = createContext<PortfolioData | null>(null);