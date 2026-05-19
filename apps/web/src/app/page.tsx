"use client";

import React, { useState, useEffect, useRef } from "react";

// ─────────────────────────────────────────────
// ICONS
// ─────────────────────────────────────────────
type IconProps = { size?: number; style?: React.CSSProperties; className?: string };
const Ic = ({
  children,
  size = 16,
  ...r
}: IconProps & { children: React.ReactNode }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...r}
  >
    {children}
  </svg>
);

const Dashboard = (p: IconProps) => (
  <Ic {...p}>
    <rect x="3" y="3" width="7" height="7" />
    <rect x="14" y="3" width="7" height="7" />
    <rect x="3" y="14" width="7" height="7" />
    <rect x="14" y="14" width="7" height="7" />
  </Ic>
);
const Wand = (p: IconProps) => (
  <Ic {...p}>
    <path d="M15 4V2" />
    <path d="M15 16v-2" />
    <path d="M8 9h2" />
    <path d="M20 9h2" />
    <path d="M17.8 11.8 19 13" />
    <path d="M15 9h.01" />
    <path d="M17.8 6.2 19 5" />
    <path d="m3 21 9-9" />
    <path d="M12.2 6.2 11 5" />
  </Ic>
);
const History = (p: IconProps) => (
  <Ic {...p}>
    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
    <path d="M3 3v5h5" />
    <path d="M12 7v5l4 2" />
  </Ic>
);
const Book = (p: IconProps) => (
  <Ic {...p}>
    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
  </Ic>
);
const User = (p: IconProps) => (
  <Ic {...p}>
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
    <circle cx="12" cy="7" r="4" />
  </Ic>
);
const Settings = (p: IconProps) => (
  <Ic {...p}>
    <circle cx="12" cy="12" r="3" />
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
  </Ic>
);
const Briefcase = (p: IconProps) => (
  <Ic {...p}>
    <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
  </Ic>
);
const Code = (p: IconProps) => (
  <Ic {...p}>
    <polyline points="16 18 22 12 16 6" />
    <polyline points="8 6 2 12 8 18" />
  </Ic>
);
const Graduation = (p: IconProps) => (
  <Ic {...p}>
    <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
    <path d="M6 12v5c3 3 9 3 12 0v-5" />
  </Ic>
);
const Award = (p: IconProps) => (
  <Ic {...p}>
    <circle cx="12" cy="8" r="6" />
    <path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11" />
  </Ic>
);
const Mic = (p: IconProps) => (
  <Ic {...p}>
    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z" />
    <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
    <line x1="12" y1="19" x2="12" y2="22" />
  </Ic>
);
const Folder = (p: IconProps) => (
  <Ic {...p}>
    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
  </Ic>
);
const Message = (p: IconProps) => (
  <Ic {...p}>
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  </Ic>
);
const Send = (p: IconProps) => (
  <Ic {...p}>
    <line x1="22" y1="2" x2="11" y2="13" />
    <polygon points="22 2 15 22 11 13 2 9 22 2" />
  </Ic>
);
const Copy = (p: IconProps) => (
  <Ic {...p}>
    <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
  </Ic>
);
const Check = (p: IconProps) => (
  <Ic {...p}>
    <polyline points="20 6 9 17 4 12" />
  </Ic>
);
const CheckCircle = (p: IconProps) => (
  <Ic {...p}>
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
    <polyline points="22 4 12 14.01 9 11.01" />
  </Ic>
);
const X = (p: IconProps) => (
  <Ic {...p}>
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </Ic>
);
const Plus = (p: IconProps) => (
  <Ic {...p}>
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </Ic>
);
const Search = (p: IconProps) => (
  <Ic {...p}>
    <circle cx="11" cy="11" r="8" />
    <line x1="21" y1="21" x2="16.65" y2="16.65" />
  </Ic>
);
const Edit = (p: IconProps) => (
  <Ic {...p}>
    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
  </Ic>
);
const Refresh = (p: IconProps) => (
  <Ic {...p}>
    <polyline points="23 4 23 10 17 10" />
    <polyline points="1 20 1 14 7 14" />
    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
  </Ic>
);
const Download = (p: IconProps) => (
  <Ic {...p}>
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
    <polyline points="7 10 12 15 17 10" />
    <line x1="12" y1="15" x2="12" y2="3" />
  </Ic>
);
const Trash = (p: IconProps) => (
  <Ic {...p}>
    <polyline points="3 6 5 6 21 6" />
    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
  </Ic>
);
const More = (p: IconProps) => (
  <Ic {...p}>
    <circle cx="12" cy="12" r="1" />
    <circle cx="19" cy="12" r="1" />
    <circle cx="5" cy="12" r="1" />
  </Ic>
);
const ChevronRight = (p: IconProps) => (
  <Ic {...p}>
    <polyline points="9 18 15 12 9 6" />
  </Ic>
);
const ChevronDown = (p: IconProps) => (
  <Ic {...p}>
    <polyline points="6 9 12 15 18 9" />
  </Ic>
);
const ArrowRight = (p: IconProps) => (
  <Ic {...p}>
    <line x1="5" y1="12" x2="19" y2="12" />
    <polyline points="12 5 19 12 12 19" />
  </Ic>
);
const Upload = (p: IconProps) => (
  <Ic {...p}>
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
    <polyline points="17 8 12 3 7 8" />
    <line x1="12" y1="3" x2="12" y2="15" />
  </Ic>
);
const Link = (p: IconProps) => (
  <Ic {...p}>
    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
  </Ic>
);
const Zap = (p: IconProps) => (
  <Ic {...p}>
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
  </Ic>
);
const Target = (p: IconProps) => (
  <Ic {...p}>
    <circle cx="12" cy="12" r="10" />
    <circle cx="12" cy="12" r="6" />
    <circle cx="12" cy="12" r="2" />
  </Ic>
);
const Trending = (p: IconProps) => (
  <Ic {...p}>
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
    <polyline points="17 6 23 6 23 12" />
  </Ic>
);
const File = (p: IconProps) => (
  <Ic {...p}>
    <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
    <polyline points="13 2 13 9 20 9" />
  </Ic>
);
const Star = (p: IconProps) => (
  <Ic {...p}>
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
  </Ic>
);
const Bookmark = (p: IconProps) => (
  <Ic {...p}>
    <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
  </Ic>
);
const Bell = (p: IconProps) => (
  <Ic {...p}>
    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
    <path d="M13.73 21a2 2 0 0 1-3.46 0" />
  </Ic>
);
const Logout = (p: IconProps) => (
  <Ic {...p}>
    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
    <polyline points="16 17 21 12 16 7" />
    <line x1="21" y1="12" x2="9" y2="12" />
  </Ic>
);
const Info = (p: IconProps) => (
  <Ic {...p}>
    <circle cx="12" cy="12" r="10" />
    <line x1="12" y1="8" x2="12" y2="12" />
    <line x1="12" y1="16" x2="12.01" y2="16" />
  </Ic>
);
const Dollar = (p: IconProps) => (
  <Ic {...p}>
    <line x1="12" y1="1" x2="12" y2="23" />
    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
  </Ic>
);
const Eye = (p: IconProps) => (
  <Ic {...p}>
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
    <circle cx="12" cy="12" r="3" />
  </Ic>
);
const Google = (p: IconProps) => (
  <Ic {...p}>
    <path d="M15.545 6.558a9.42 9.42 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0a7.689 7.689 0 0 1 5.352 2.082l-2.284 2.284A4.347 4.347 0 0 0 8 3.166c-2.087 0-4.36 1.408-4.36 4.834 0 3.426 2.273 4.834 4.36 4.834 1.487 0 2.552-.405 3.256-1.068.698-.66 1.066-1.647 1.1-2.71H8v-3.09h7.545z" />
  </Ic>
);

// ─────────────────────────────────────────────
// DATA TYPES
// ─────────────────────────────────────────────
type SkillLevel = "Intermediate" | "Advanced" | "Expert";

interface Skill {
  id: string;
  name: string;
  level: SkillLevel;
  years: number;
}

interface Project {
  id: string;
  title: string;
  description: string;
  tags: string[];
  url?: string;
  results?: string;
}

interface Experience {
  id: string;
  company: string;
  role: string;
  start: string;
  end: string;
  bullets: string[];
}

interface Education {
  id: string;
  institution: string;
  degree: string;
  field: string;
  year: string;
}

interface Certification {
  id: string;
  name: string;
  issuer: string;
  year: string;
}

interface TonePrefs {
  defaultTone: string;
  voiceNote: string;
  avoidPhrases: string[];
  signOff: string;
}

type HistoryStatus = "draft" | "sent" | "replied" | "hired" | "no_reply";

interface HistoryEntry {
  id: string;
  jobTitle: string;
  client: string;
  matchScore: number;
  status: HistoryStatus;
  date: string;
  preview: string;
  letterText?: string;
}

interface Guideline {
  id: string;
  title: string;
  body: string;
  active: boolean;
}

interface Example {
  id: string;
  title: string;
  tags: string[];
  snippet: string;
  outcome: string;
  rating: number;
}

interface KB {
  guidelines: Guideline[];
  examples: Example[];
}

interface UserData {
  id: string;
  name: string;
  title: string;
  location: string;
  hourlyRate: number;
  about: string;
  skills: Skill[];
  projects: Project[];
  experience: Experience[];
  education: Education[];
  certifications: Certification[];
  tonePrefs: TonePrefs;
  niches: { label: string; strength: number }[];
  avatar?: string;
}

// ─────────────────────────────────────────────
// MOCK DATA
// ─────────────────────────────────────────────
const SAMPLE_USER: UserData = {
  id: "u1",
  name: "Rakib Hasan",
  title: "Full-Stack Engineer & AI Integration Specialist",
  location: "Dhaka, Bangladesh",
  hourlyRate: 65,
  about:
    "I build production-grade web apps and integrate AI/ML into business workflows. 7 years with React, Node, Python, and FastAPI. I ship fast, write tests, and keep code clean.",
  skills: [
    { id: "s1", name: "React / Next.js", level: "Expert", years: 6 },
    { id: "s2", name: "Node.js / FastAPI", level: "Expert", years: 5 },
    { id: "s3", name: "LangChain / LangGraph", level: "Advanced", years: 2 },
    { id: "s4", name: "PostgreSQL", level: "Advanced", years: 5 },
    { id: "s5", name: "TypeScript", level: "Expert", years: 4 },
    { id: "s6", name: "Python", level: "Advanced", years: 4 },
    { id: "s7", name: "Docker / DevOps", level: "Intermediate", years: 3 },
  ],
  projects: [
    {
      id: "p1",
      title: "AI Legal Document Analyzer",
      description:
        "RAG pipeline that ingests 10K+ legal docs, extracts clauses, and answers natural-language queries with citations.",
      tags: ["LangChain", "pgvector", "FastAPI", "React"],
      results: "Reduced contract review time by 70% for a 50-lawyer firm",
    },
    {
      id: "p2",
      title: "E-commerce Analytics Dashboard",
      description:
        "Real-time sales, inventory, and customer cohort analytics for a $4M/yr Shopify brand.",
      tags: ["Next.js", "PostgreSQL", "Recharts", "Celery"],
      results: "3× faster reporting, $200K attributed revenue improvement",
    },
    {
      id: "p3",
      title: "Multi-tenant SaaS Boilerplate",
      description:
        "Production-ready template: JWT auth, role-based access, billing via Stripe, team workspaces.",
      tags: ["Next.js", "FastAPI", "Stripe", "Alembic"],
      results: "Used by 12 indie hackers; 4 reached paying customers in <30 days",
    },
  ],
  experience: [
    {
      id: "e1",
      company: "Upwork (Freelance)",
      role: "Senior Full-Stack Engineer",
      start: "2019",
      end: "Present",
      bullets: [
        "100% Job Success, Top-Rated Plus badge",
        "Delivered 40+ projects across legal tech, fintech, and e-commerce",
        "$180K+ earned on platform",
      ],
    },
    {
      id: "e2",
      company: "TechVentures BD",
      role: "Lead Frontend Engineer",
      start: "2017",
      end: "2019",
      bullets: [
        "Led 5-person frontend team building a fintech dashboard",
        "Migrated codebase from jQuery to React, cutting load time by 60%",
      ],
    },
  ],
  education: [
    {
      id: "ed1",
      institution: "BUET",
      degree: "B.Sc.",
      field: "Computer Science & Engineering",
      year: "2017",
    },
  ],
  certifications: [
    { id: "c1", name: "AWS Certified Developer – Associate", issuer: "AWS", year: "2022" },
    { id: "c2", name: "Professional Scrum Master I", issuer: "Scrum.org", year: "2021" },
  ],
  tonePrefs: {
    defaultTone: "Confident",
    voiceNote:
      "Direct and results-first. Lead with the client's problem, then prove I've solved it before.",
    avoidPhrases: ["I am passionate about", "I would love to", "I think I could"],
    signOff: "Looking forward to a quick call,\nRakib",
  },
  niches: [
    { label: "AI / LLM Integration", strength: 92 },
    { label: "SaaS / Full-Stack", strength: 88 },
    { label: "Legal Tech", strength: 71 },
    { label: "E-commerce", strength: 65 },
    { label: "Fintech", strength: 58 },
  ],
};

const SAMPLE_HISTORY: HistoryEntry[] = [
  {
    id: "h1",
    jobTitle: "AI-Powered Legal Contract Reviewer",
    client: "LexTech Inc.",
    matchScore: 94,
    status: "hired",
    date: "May 12, 2025",
    preview:
      "Your contract review bottleneck is exactly the problem I solved for a 50-lawyer firm last year — cutting their review cycle from 3 days to 4 hours using a RAG pipeline...",
    letterText: `Your contract review bottleneck is exactly the problem I solved for a 50-lawyer firm last year — cutting their review cycle from 3 days to 4 hours using a RAG pipeline on top of their existing document store.

Here's what I'd bring to your project:

• Built and shipped a production LangChain + pgvector system that ingests 10K+ legal docs, extracts key clauses, flags risk language, and answers natural-language queries with pinned citations
• Integrated with a custom FastAPI backend serving a React front-end used daily by 50+ lawyers
• Familiar with the specific challenges of legal NLP: entity recognition, citation linking, confidentiality constraints

I noticed you mentioned needing SOC2-aware storage — I've handled that before and can walk you through my approach in a 20-minute call.

Timeline and rate: I can start Monday. My rate for AI/legal-tech projects is $65/hr; happy to discuss a milestone-based contract if preferred.

Looking forward to a quick call,
Rakib`,
  },
  {
    id: "h2",
    jobTitle: "Next.js SaaS Dashboard with Stripe Billing",
    client: "Bootstrapify",
    matchScore: 88,
    status: "replied",
    date: "May 9, 2025",
    preview:
      "Multi-tenant SaaS with Stripe is my wheelhouse — I've shipped three of these in the past 18 months, and I keep a production-ready template that cuts the billing plumbing to...",
  },
  {
    id: "h3",
    jobTitle: "Python Automation for Data Pipeline",
    client: "DataFlow Co.",
    matchScore: 79,
    status: "sent",
    date: "May 7, 2025",
    preview:
      "Your pipeline needs a resilient ETL layer — I've built Celery + Redis pipelines that handle 500K rows/day with automatic retry and dead-letter queues...",
  },
  {
    id: "h4",
    jobTitle: "E-commerce Analytics Dashboard",
    client: "ShopMetrics",
    matchScore: 85,
    status: "hired",
    date: "Apr 28, 2025",
    preview:
      "Real-time Shopify analytics is something I've shipped for a $4M/yr brand — here's the exact stack I used and why it scales...",
  },
  {
    id: "h5",
    jobTitle: "React Native Mobile App — Fintech",
    client: "PayEase",
    matchScore: 62,
    status: "no_reply",
    date: "Apr 20, 2025",
    preview:
      "While React Native isn't my primary stack, I've delivered two hybrid apps and can bridge to your existing FastAPI backend seamlessly...",
  },
  {
    id: "h6",
    jobTitle: "FastAPI Microservices Architect",
    client: "ScaleUp Labs",
    matchScore: 91,
    status: "replied",
    date: "Apr 15, 2025",
    preview:
      "FastAPI microservices at scale — I've designed three such systems, including one handling 50K RPM with async Celery workers and Redis caching...",
  },
  {
    id: "h7",
    jobTitle: "LangGraph Chatbot for Customer Support",
    client: "SupportAI",
    matchScore: 89,
    status: "draft",
    date: "May 14, 2025",
    preview:
      "LangGraph is what I reach for when a simple chain isn't enough — here's how I'd design your support bot to handle escalation paths...",
  },
];

const SAMPLE_KB: KB = {
  guidelines: [
    {
      id: "g1",
      title: "Lead with the client's problem",
      body: "First sentence names their specific pain point. Never open with 'I am a developer with X years of experience.'",
      active: true,
    },
    {
      id: "g2",
      title: "Cite one concrete result within the first 3 lines",
      body: "Include a measurable outcome (time saved, revenue impact, scale handled) tied to a real project.",
      active: true,
    },
    {
      id: "g3",
      title: "Match their vocabulary",
      body: "Mirror keywords from the job post. If they say 'pipeline', use 'pipeline', not 'workflow'.",
      active: true,
    },
    {
      id: "g4",
      title: "End with a low-friction CTA",
      body: "Close with a specific ask: 'happy to do a 20-minute call' or 'can share the GitHub repo'. Never just 'looking forward to hearing from you'.",
      active: true,
    },
    {
      id: "g5",
      title: "Keep it under 250 words",
      body: "Clients skim. If it's longer than 250 words, cut ruthlessly. The best letters are 150–200 words.",
      active: false,
    },
    {
      id: "g6",
      title: "Address the hidden risk",
      body: "Identify one unstated risk in the project (timeline, tech complexity, integration) and show you've handled it before.",
      active: true,
    },
  ],
  examples: [
    {
      id: "ex1",
      title: "Legal AI — RAG Pipeline",
      tags: ["LangChain", "Legal Tech", "Hired"],
      snippet:
        "Your contract review bottleneck is exactly the problem I solved for a 50-lawyer firm last year — cutting their review cycle from 3 days to 4 hours...",
      outcome: "Hired at $65/hr · 6-month contract",
      rating: 5,
    },
    {
      id: "ex2",
      title: "SaaS Dashboard + Stripe Billing",
      tags: ["Next.js", "Stripe", "Replied"],
      snippet:
        "Multi-tenant SaaS with Stripe is my wheelhouse. I've shipped three in 18 months and keep a production-ready template that cuts billing plumbing to a day of work...",
      outcome: "Interview → hired at $60/hr",
      rating: 5,
    },
    {
      id: "ex3",
      title: "E-commerce Analytics",
      tags: ["React", "PostgreSQL", "Hired"],
      snippet:
        "Real-time Shopify analytics for a $4M/yr brand — I built exactly this. The stack: Next.js + PostgreSQL + Recharts, live in 3 weeks, 3× faster than their old BI tool...",
      outcome: "Hired · $8,400 project",
      rating: 4,
    },
    {
      id: "ex4",
      title: "FastAPI Microservices",
      tags: ["FastAPI", "Celery", "Architecture"],
      snippet:
        "Designing FastAPI microservices that stay maintainable at scale is something I've done three times. The key decisions I'd make for your system: async workers, Redis caching layer, and OpenAPI contract-first design...",
      outcome: "Invited to interview",
      rating: 4,
    },
  ],
};

const SAMPLE_JOB = `We're building a Legal AI SaaS platform and need a senior full-stack engineer to lead the development of our document analysis module.

The role involves:
- Building a RAG pipeline to ingest, chunk, and embed legal contracts (PDF, DOCX)
- Creating a FastAPI backend with async endpoints for document ingestion and querying
- Developing a React/Next.js frontend for document upload, clause highlighting, and Q&A
- Integrating with OpenAI GPT-4 and Claude APIs via a provider fallback layer
- Ensuring SOC2-compliant data handling and storage

Requirements:
- 3+ years with Python/FastAPI and React/Next.js
- Experience with vector databases (pgvector, Pinecone, or Weaviate)
- LangChain or similar RAG frameworks
- Strong understanding of legal document structure (preferred)
- Available to start within 1 week

Budget: $50–$75/hr | 3-month contract, likely to extend
`;

// ─────────────────────────────────────────────
// SHARED COMPONENTS
// ─────────────────────────────────────────────

interface BtnProps {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "lg" | "icon";
  loading?: boolean;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  className?: string;
  children?: React.ReactNode;
  style?: React.CSSProperties;
}

function Btn({
  variant = "primary",
  size,
  loading,
  onClick,
  type = "button",
  disabled,
  className = "",
  children,
  style,
}: BtnProps) {
  const cls = [
    "btn",
    `btn-${variant}`,
    size ? `btn-${size}` : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");
  return (
    <button
      className={cls}
      onClick={onClick}
      type={type}
      disabled={disabled || loading}
      style={style}
    >
      {loading ? <span className="spinner" /> : children}
    </button>
  );
}

interface BadgeProps {
  variant?: "default" | "accent" | "success" | "warning" | "info" | "danger";
  dot?: boolean;
  children: React.ReactNode;
}
function Badge({ variant = "default", dot, children }: BadgeProps) {
  const cls = ["badge", variant !== "default" ? `badge-${variant}` : ""]
    .filter(Boolean)
    .join(" ");
  return (
    <span className={cls}>
      {dot && <span className="badge-dot" />}
      {children}
    </span>
  );
}

interface AvProps {
  name: string;
  size?: "sm" | "md" | "lg";
}
function Av({ name, size }: AvProps) {
  const initials = name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
  const cls = ["avatar", size === "lg" ? "avatar-lg" : size === "md" ? "avatar-md" : ""]
    .filter(Boolean)
    .join(" ");
  return <div className={cls}>{initials}</div>;
}

interface CardProps {
  title?: string;
  action?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}
function Card({ title, action, children, className = "", style }: CardProps) {
  if (title) {
    return (
      <div className={`card-bare ${className}`} style={style}>
        <div className="card-header">
          <p className="card-title">{title}</p>
          {action}
        </div>
        <div className="card-body">{children}</div>
      </div>
    );
  }
  return (
    <div className={`card ${className}`} style={style}>
      {children}
    </div>
  );
}

interface SwitchProps {
  checked: boolean;
  onChange: (v: boolean) => void;
}
function SwitchToggle({ checked, onChange }: SwitchProps) {
  return (
    <div
      className={`switch ${checked ? "on" : ""}`}
      onClick={() => onChange(!checked)}
    />
  );
}

interface SegProps {
  value: string;
  options: string[] | { value: string; label: string }[];
  onChange: (v: string) => void;
  style?: React.CSSProperties;
}
function Seg({ value, options, onChange, style }: SegProps) {
  const normalized = options.map((o) =>
    typeof o === "string" ? { value: o, label: o } : o
  );
  return (
    <div className="segmented" style={style}>
      {normalized.map((o) => (
        <div
          key={o.value}
          className={`segmented-item ${value === o.value ? "active" : ""}`}
          onClick={() => onChange(o.value)}
        >
          {o.label}
        </div>
      ))}
    </div>
  );
}

interface ChipProps {
  active?: boolean;
  onClick?: () => void;
  onRemove?: () => void;
  children: React.ReactNode;
}
function ChipTag({ active, onClick, onRemove, children }: ChipProps) {
  return (
    <span className={`chip ${active ? "active" : ""}`} onClick={onClick}>
      {children}
      {onRemove && (
        <span
          className="chip-remove"
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
        >
          <X size={10} />
        </span>
      )}
    </span>
  );
}

interface MatchRingProps {
  score: number;
  size?: number;
}
function MatchRing({ score, size = 56 }: MatchRingProps) {
  const r = (size - 8) / 2;
  const circ = 2 * Math.PI * r;
  const dash = (score / 100) * circ;
  const color =
    score >= 85 ? "var(--accent)" : score >= 65 ? "var(--warning)" : "var(--danger)";
  return (
    <svg width={size} height={size} style={{ flexShrink: 0 }}>
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke="var(--surface-3)"
        strokeWidth="4"
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="4"
        strokeDasharray={`${dash} ${circ}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        style={{ transition: "stroke-dasharray 0.4s" }}
      />
      <text
        x={size / 2}
        y={size / 2 + 5}
        textAnchor="middle"
        fill={color}
        fontSize={size < 48 ? 11 : 13}
        fontWeight="600"
        fontFamily="var(--font-sans)"
      >
        {score}
      </text>
    </svg>
  );
}

interface ToastProps {
  message: string;
  onDone: () => void;
}
function Toast({ message, onDone }: ToastProps) {
  useEffect(() => {
    const t = setTimeout(onDone, 2800);
    return () => clearTimeout(t);
  }, [onDone]);
  return (
    <div className="toast">
      <CheckCircle size={15} style={{ color: "var(--accent-text)" }} />
      {message}
    </div>
  );
}

interface EmptyStateProps {
  icon: React.ReactNode;
  title: string;
  text: string;
  action?: React.ReactNode;
}
function EmptyState({ icon, title, text, action }: EmptyStateProps) {
  return (
    <div className="empty">
      <div className="empty-icon">{icon}</div>
      <p className="empty-title">{title}</p>
      <p className="empty-text">{text}</p>
      {action}
    </div>
  );
}

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}
function PageHeader({ title, subtitle, action }: PageHeaderProps) {
  return (
    <div className="page-header">
      <div>
        <h1 className="page-title">{title}</h1>
        {subtitle && <p className="page-subtitle">{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

// ─────────────────────────────────────────────
// STATUS HELPERS
// ─────────────────────────────────────────────
const STATUS_LABELS: Record<HistoryStatus, string> = {
  draft: "Draft",
  sent: "Sent",
  replied: "Replied",
  hired: "Hired",
  no_reply: "No reply",
};
const STATUS_VARIANTS: Record<HistoryStatus, BadgeProps["variant"]> = {
  draft: "default",
  sent: "info",
  replied: "warning",
  hired: "success",
  no_reply: "default",
};

// ─────────────────────────────────────────────
// AUTH SCREEN
// ─────────────────────────────────────────────
function AuthScreen({ onSignIn }: { onSignIn: () => void }) {
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      onSignIn();
    }, 900);
  };

  return (
    <div className="auth-stage">
      {/* Left side */}
      <div className="auth-side">
        <div className="auth-glow" />
        <div style={{ position: "relative", zIndex: 1 }}>
          <div className="row" style={{ gap: 10, marginBottom: 40 }}>
            <div className="sidebar-brand-mark" style={{ width: 32, height: 32, fontSize: 16 }}>
              P
            </div>
            <span style={{ fontWeight: 700, fontSize: 17, letterSpacing: "-0.01em" }}>
              PitchCraft
            </span>
          </div>
        </div>
        <div className="auth-quote">
          <div className="auth-quote-mark">&ldquo;</div>
          <p className="auth-quote-text">
            I went from 2% reply rate to 28% in 6 weeks. PitchCraft reads the job post better than I
            do — and it never forgets my best lines.
          </p>
          <div className="auth-quote-author">
            <Av name="Jonah K" />
            <div>
              <div style={{ fontWeight: 500, color: "var(--text-1)", fontSize: 13 }}>Jonah K.</div>
              <div>Full-Stack Developer · Top-Rated Plus</div>
            </div>
          </div>
        </div>
        <div className="auth-stat-strip">
          <div className="stat">
            <div className="stat-value">24K+</div>
            <div className="stat-label">Active freelancers</div>
          </div>
          <div className="stat">
            <div className="stat-value">3.2×</div>
            <div className="stat-label">Avg reply rate lift</div>
          </div>
          <div className="stat">
            <div className="stat-value">$1.4M</div>
            <div className="stat-label">Contracts attributed</div>
          </div>
        </div>
      </div>

      {/* Right side */}
      <div className="auth-form-side">
        <div className="auth-form-card">
          <div className="auth-tab-toggle">
            <button
              className={mode === "signin" ? "active" : ""}
              onClick={() => setMode("signin")}
            >
              Sign in
            </button>
            <button
              className={mode === "signup" ? "active" : ""}
              onClick={() => setMode("signup")}
            >
              Create account
            </button>
          </div>
          <h1>{mode === "signin" ? "Welcome back" : "Get started free"}</h1>
          <p>
            {mode === "signin"
              ? "Sign in to your PitchCraft account."
              : "Your first 10 letters are on us."}
          </p>
          <form onSubmit={handleSubmit}>
            <div className="field">
              <label className="label">Email</label>
              <input
                className="input"
                type="email"
                placeholder="you@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="field">
              <label className="label">Password</label>
              <input
                className="input"
                type="password"
                placeholder={mode === "signup" ? "Create a password" : "Your password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <Btn
              type="submit"
              variant="primary"
              size="lg"
              loading={loading}
              style={{ width: "100%", marginBottom: 0 }}
            >
              {mode === "signin" ? "Sign in" : "Create account"}
            </Btn>
          </form>
          <div className="auth-divider">or</div>
          <Btn
            variant="secondary"
            size="lg"
            style={{ width: "100%" }}
            onClick={onSignIn}
          >
            <Google size={15} />
            Continue with Google
          </Btn>
          {mode === "signin" && (
            <p
              style={{
                marginTop: 16,
                textAlign: "center",
                fontSize: 12,
                color: "var(--text-3)",
              }}
            >
              Forgot password?{" "}
              <span style={{ color: "var(--accent-text)", cursor: "pointer" }}>Reset it</span>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// SIDEBAR
// ─────────────────────────────────────────────
type Route = "dashboard" | "generator" | "history" | "knowledge" | "settings";

interface SidebarProps {
  route: Route;
  setRoute: (r: Route) => void;
  user: UserData;
  historyCount: number;
  onLogout: () => void;
}

function Sidebar({ route, setRoute, user, historyCount, onLogout }: SidebarProps) {
  const nav = (
    r: Route,
    icon: React.ReactNode,
    label: string,
    badge?: string
  ) => (
    <div
      className={`nav-item ${route === r ? "active" : ""}`}
      onClick={() => setRoute(r)}
    >
      {icon}
      <span style={{ flex: 1 }}>{label}</span>
      {badge && <span className="nav-item-badge">{badge}</span>}
    </div>
  );

  return (
    <div className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-brand-mark">P</div>
        <span className="sidebar-brand-name">PitchCraft</span>
      </div>

      <div className="sidebar-section-label">Workspace</div>
      {nav("dashboard", <Dashboard />, "Dashboard")}
      {nav("generator", <Wand />, "Generator", "AI")}
      {nav("history", <History />, "History", String(historyCount))}
      {nav("knowledge", <Book />, "Knowledge Base")}

      <div className="sidebar-section-label">Account</div>
      {nav("settings", <Settings />, "Settings")}

      <div className="sidebar-footer">
        <div className="sidebar-user">
          <Av name={user.name} />
          <div className="grow">
            <div style={{ fontSize: 13, fontWeight: 500, color: "var(--text-1)" }}>
              {user.name}
            </div>
            <div style={{ fontSize: 11, color: "var(--text-3)" }}>Top-Rated Plus</div>
          </div>
          <div
            onClick={onLogout}
            style={{ cursor: "pointer", color: "var(--text-3)", padding: 4 }}
            title="Logout"
          >
            <Logout size={14} />
          </div>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// TOPBAR
// ─────────────────────────────────────────────
interface TopbarProps {
  onNewLetter: () => void;
}
function Topbar({ onNewLetter }: TopbarProps) {
  return (
    <div className="topbar">
      <div className="search-input">
        <Search size={14} />
        <span>Search history, templates…</span>
        <kbd>⌘K</kbd>
      </div>
      <div className="row">
        <Btn variant="ghost" size="sm">
          <Bell size={15} />
        </Btn>
        <Btn variant="primary" size="sm" onClick={onNewLetter}>
          <Plus size={13} />
          New letter
        </Btn>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// DASHBOARD SCREEN
// ─────────────────────────────────────────────
interface DashboardProps {
  user: UserData;
  history: HistoryEntry[];
  onGenerate: () => void;
}
function DashboardScreen({ user, history, onGenerate }: DashboardProps) {
  const letterCount = history.length;
  const hiredCount = history.filter((h) => h.status === "hired").length;
  const repliedCount = history.filter(
    (h) => h.status === "replied" || h.status === "hired"
  ).length;
  const replyRate =
    letterCount > 0 ? Math.round((repliedCount / letterCount) * 100) : 0;
  const avgMatch =
    letterCount > 0
      ? Math.round(history.reduce((a, h) => a + h.matchScore, 0) / letterCount)
      : 0;

  const recent = [...history].sort((a, b) => b.id.localeCompare(a.id)).slice(0, 5);

  return (
    <div className="page">
      <PageHeader
        title="Dashboard"
        subtitle={`Good day, ${user.name.split(" ")[0]}. Ready to land the next one?`}
        action={
          <Btn variant="primary" onClick={onGenerate}>
            <Wand size={14} />
            Generate letter
          </Btn>
        }
      />

      {/* Stats */}
      <div className="grid-4" style={{ marginBottom: 24 }}>
        {[
          { label: "Letters sent", value: letterCount, delta: "+3 this week", icon: <Send size={16} /> },
          { label: "Reply rate", value: `${replyRate}%`, delta: "+4% vs last month", icon: <Trending size={16} /> },
          { label: "Hired", value: hiredCount, delta: `${hiredCount} contracts`, icon: <CheckCircle size={16} /> },
          { label: "Avg match score", value: avgMatch, delta: "Top 12%", icon: <Target size={16} /> },
        ].map((s) => (
          <Card key={s.label}>
            <div className="between" style={{ marginBottom: 12 }}>
              <div
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: 8,
                  background: "var(--accent-soft)",
                  color: "var(--accent-text)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {s.icon}
              </div>
            </div>
            <div className="stat">
              <div className="stat-value">{s.value}</div>
              <div className="stat-label">{s.label}</div>
              <div className="stat-delta">
                <Trending size={11} />
                {s.delta}
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 320px", gap: 20 }}>
        {/* Left: Quick-start + history */}
        <div className="col">
          {/* Quick start CTA */}
          <div
            style={{
              background:
                "radial-gradient(circle at 0% 50%, var(--accent-soft) 0%, transparent 60%), var(--surface)",
              border: "1px solid var(--border)",
              borderRadius: "var(--r-lg)",
              padding: "28px 24px",
              marginBottom: 4,
            }}
          >
            <div className="row" style={{ gap: 10, marginBottom: 12 }}>
              <Badge variant="accent">
                <Zap size={11} />
                Quick start
              </Badge>
            </div>
            <h2
              style={{
                fontSize: 20,
                fontWeight: 600,
                margin: "0 0 8px",
                letterSpacing: "-0.02em",
              }}
            >
              Paste a job. Get a winning pitch in 12 seconds.
            </h2>
            <p style={{ color: "var(--text-2)", fontSize: 13.5, marginBottom: 20 }}>
              PitchCraft analyzes the post, matches it to your profile evidence, and drafts a
              cover letter that sounds like you — at your best.
            </p>
            <Btn variant="primary" size="lg" onClick={onGenerate}>
              <ArrowRight size={15} />
              Start generating
            </Btn>
          </div>

          {/* Recent history */}
          <Card title="Recent letters" action={<Btn variant="ghost" size="sm">View all</Btn>}>
            {recent.length === 0 ? (
              <EmptyState
                icon={<File size={20} />}
                title="No letters yet"
                text="Generate your first cover letter to see it here."
              />
            ) : (
              <div style={{ margin: "-20px" }}>
                {recent.map((h) => (
                  <div className="history-row" key={h.id}>
                    <div>
                      <div className="history-job-title">{h.jobTitle}</div>
                      <div className="history-meta">
                        <span>{h.client}</span>
                        <span>·</span>
                        <span>{h.date}</span>
                      </div>
                    </div>
                    <MatchRing score={h.matchScore} size={40} />
                    <Badge variant={STATUS_VARIANTS[h.status]}>
                      {STATUS_LABELS[h.status]}
                    </Badge>
                    <span style={{ fontSize: 12, color: "var(--text-3)" }}>{h.date}</span>
                    <Btn variant="ghost" size="icon">
                      <More size={14} />
                    </Btn>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>

        {/* Right: Profile + tip + niches */}
        <div className="col">
          {/* Profile card */}
          <Card>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                textAlign: "center",
                padding: "8px 0 4px",
              }}
            >
              <Av name={user.name} size="lg" />
              <div
                style={{ fontWeight: 600, fontSize: 15, marginTop: 10, letterSpacing: "-0.01em" }}
              >
                {user.name}
              </div>
              <div style={{ fontSize: 12.5, color: "var(--text-2)", marginTop: 4 }}>
                {user.title}
              </div>
              <div style={{ fontSize: 12, color: "var(--text-3)", marginTop: 4 }}>
                {user.location}
              </div>
              <div className="row" style={{ marginTop: 12, gap: 6 }}>
                <Badge variant="success">Top-Rated Plus</Badge>
                <Badge>
                  <Dollar size={10} />
                  ${user.hourlyRate}/hr
                </Badge>
              </div>
            </div>
            <div className="divider" />
            <div style={{ fontSize: 12, color: "var(--text-2)", lineHeight: 1.6 }}>
              {user.about.slice(0, 120)}…
            </div>
          </Card>

          {/* Tip of the day */}
          <Card>
            <div className="row" style={{ marginBottom: 10 }}>
              <div
                style={{
                  width: 24,
                  height: 24,
                  borderRadius: 6,
                  background: "var(--warning-soft)",
                  color: "var(--warning)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Star size={13} />
              </div>
              <span style={{ fontSize: 12, fontWeight: 600, color: "var(--text-2)" }}>
                TIP OF THE DAY
              </span>
            </div>
            <p style={{ fontSize: 13, color: "var(--text-1)", lineHeight: 1.6, margin: 0 }}>
              Address one unstated risk in the job post — timeline, integration complexity, or
              technical debt. Clients hire freelancers who see what others miss.
            </p>
          </Card>

          {/* Niche strength */}
          <Card title="Niche strength">
            <div className="col" style={{ gap: 12 }}>
              {user.niches.map((n) => (
                <div key={n.label}>
                  <div className="between" style={{ marginBottom: 5 }}>
                    <span style={{ fontSize: 12.5, color: "var(--text-1)" }}>{n.label}</span>
                    <span style={{ fontSize: 12, color: "var(--accent-text)", fontWeight: 500 }}>
                      {n.strength}%
                    </span>
                  </div>
                  <div className="progress">
                    <div className="progress-bar" style={{ width: `${n.strength}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// GENERATOR SCREEN
// ─────────────────────────────────────────────
interface GeneratorProps {
  onSave: (entry: HistoryEntry) => void;
}

const TONES = [
  { name: "Confident", emoji: "💪", desc: "Direct, results-first" },
  { name: "Friendly", emoji: "😊", desc: "Warm, approachable" },
  { name: "Formal", emoji: "🎩", desc: "Professional, structured" },
  { name: "Casual", emoji: "✌️", desc: "Relaxed, conversational" },
];

function GeneratorScreen({ onSave }: GeneratorProps) {
  const [jobText, setJobText] = useState(SAMPLE_JOB);
  const [tone, setTone] = useState("Confident");
  const [length, setLength] = useState("Medium");
  const [generating, setGenerating] = useState(false);
  const [generated, setGenerated] = useState(false);
  const [letterText, setLetterText] = useState("");
  const [matchScore] = useState(94);
  const [copied, setCopied] = useState(false);
  const [saved, setSaved] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  const suggestedQuestions = [
    "Can you walk me through your RAG pipeline architecture for legal documents?",
    "How do you handle SOC2 compliance in your document storage approach?",
    "What's your availability and timeline for the first milestone?",
  ];

  const handleGenerate = () => {
    if (!jobText.trim()) return;
    setGenerating(true);
    setGenerated(false);
    setLetterText("");
    setTimeout(() => {
      setGenerating(false);
      setGenerated(true);
      setLetterText(SAMPLE_HISTORY[0].letterText || SAMPLE_HISTORY[0].preview);
    }, 1500);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(letterText).catch(() => {});
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSave = () => {
    if (!letterText) return;
    const entry: HistoryEntry = {
      id: `h${Date.now()}`,
      jobTitle: "AI-Powered Legal Contract Reviewer",
      client: "LexTech Inc.",
      matchScore,
      status: "draft",
      date: new Date().toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      }),
      preview: letterText.slice(0, 120) + "…",
      letterText,
    };
    onSave(entry);
    setSaved(true);
    setToast("Saved to history");
  };

  return (
    <div className="page">
      <PageHeader
        title="Generator"
        subtitle="Paste a job post and let AI craft a letter matched to your profile."
      />

      <div className="gen-stage">
        {/* Left panel — input */}
        <div className="col" style={{ gap: 16 }}>
          <div className="gen-panel">
            <div className="gen-panel-header">
              <div className="gen-panel-title">
                <div className="gen-panel-title-icon">
                  <Briefcase />
                </div>
                Job Post
              </div>
              <Btn variant="ghost" size="sm" onClick={() => setJobText("")}>
                Clear
              </Btn>
            </div>
            <div className="gen-panel-body">
              <textarea
                className="gen-job-input"
                placeholder="Paste the full Upwork job description here…"
                value={jobText}
                onChange={(e) => setJobText(e.target.value)}
              />
            </div>
          </div>

          {/* Tone picker */}
          <div className="gen-panel">
            <div className="gen-panel-header">
              <div className="gen-panel-title">
                <div className="gen-panel-title-icon">
                  <Mic />
                </div>
                Tone
              </div>
            </div>
            <div className="gen-panel-body">
              <div className="tone-grid">
                {TONES.map((t) => (
                  <div
                    key={t.name}
                    className={`tone-card ${tone === t.name ? "active" : ""}`}
                    onClick={() => setTone(t.name)}
                  >
                    <span className="tone-card-emoji">{t.emoji}</span>
                    <div className="tone-card-name">{t.name}</div>
                    <div className="tone-card-desc">{t.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Length + generate */}
          <div className="gen-panel">
            <div className="gen-panel-header">
              <div className="gen-panel-title">
                <div className="gen-panel-title-icon">
                  <File />
                </div>
                Length
              </div>
            </div>
            <div className="gen-panel-body">
              <Seg
                value={length}
                options={["Short", "Medium", "Long"]}
                onChange={setLength}
                style={{ width: "100%", justifyContent: "stretch" }}
              />
              <p className="field-hint" style={{ marginTop: 10 }}>
                {length === "Short"
                  ? "~120 words — punchy, high-signal"
                  : length === "Medium"
                  ? "~200 words — balanced with proof points"
                  : "~320 words — detailed with full evidence"}
              </p>
            </div>
          </div>

          <Btn
            variant="primary"
            size="lg"
            loading={generating}
            onClick={handleGenerate}
            style={{ width: "100%" }}
          >
            <Wand size={15} />
            {generating ? "Analyzing & generating…" : "Analyze & Generate"}
          </Btn>
        </div>

        {/* Right panel — output */}
        <div className="col" style={{ gap: 16 }}>
          {generated && (
            <div className="match-score-card">
              <MatchRing score={matchScore} size={60} />
              <div>
                <div className="match-score-label">Profile match</div>
                <div className="match-score-text">
                  Strong fit — your RAG pipeline experience directly maps to the core requirement.
                  3 of 4 key skills matched.
                </div>
              </div>
            </div>
          )}

          <div className="gen-panel">
            <div className="gen-panel-header">
              <div className="gen-panel-title">
                <div className="gen-panel-title-icon">
                  <Message />
                </div>
                Cover Letter
              </div>
              {generated && (
                <div className="row" style={{ gap: 6 }}>
                  <Btn variant="ghost" size="sm" onClick={handleCopy}>
                    {copied ? <Check size={13} /> : <Copy size={13} />}
                    {copied ? "Copied" : "Copy"}
                  </Btn>
                  <Btn variant="ghost" size="sm">
                    <Download size={13} />
                  </Btn>
                  <Btn variant="ghost" size="sm" onClick={handleGenerate}>
                    <Refresh size={13} />
                  </Btn>
                </div>
              )}
            </div>
            <div className="gen-panel-body">
              {generating && (
                <div style={{ padding: "32px 0", textAlign: "center" }}>
                  <div className="spinner" style={{ margin: "0 auto 14px" }} />
                  <p style={{ color: "var(--text-3)", fontSize: 13 }}>
                    Analyzing job post and matching your profile…
                  </p>
                </div>
              )}
              {!generating && !generated && (
                <EmptyState
                  icon={<Wand size={20} />}
                  title="No letter yet"
                  text="Paste a job post and click Generate to create your cover letter."
                />
              )}
              {generated && !generating && (
                <div
                  className="letter-output"
                  contentEditable
                  suppressContentEditableWarning
                  onInput={(e) => setLetterText(e.currentTarget.textContent || "")}
                >
                  {letterText}
                </div>
              )}
            </div>
          </div>

          {/* Suggested questions */}
          {generated && !generating && (
            <div className="gen-panel">
              <div className="gen-panel-header">
                <div className="gen-panel-title">
                  <div className="gen-panel-title-icon">
                    <Zap />
                  </div>
                  Suggested screening questions
                </div>
              </div>
              <div className="gen-panel-body">
                {suggestedQuestions.map((q, i) => (
                  <div className="sq-item" key={i}>
                    <div className="sq-num">{i + 1}</div>
                    <span>{q}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {generated && !generating && (
            <Btn
              variant="secondary"
              size="lg"
              style={{ width: "100%" }}
              onClick={handleSave}
              disabled={saved}
            >
              <Bookmark size={14} />
              {saved ? "Saved to history" : "Save to history"}
            </Btn>
          )}
        </div>
      </div>

      {toast && <Toast message={toast} onDone={() => setToast(null)} />}
    </div>
  );
}

// ─────────────────────────────────────────────
// HISTORY SCREEN
// ─────────────────────────────────────────────
interface HistoryProps {
  history: HistoryEntry[];
}

function HistoryScreen({ history }: HistoryProps) {
  const [filter, setFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("Date");
  const [selected, setSelected] = useState<HistoryEntry | null>(null);

  const filterOptions = ["All", "Drafts", "Sent", "Replied", "Hired", "No reply"];
  const filterMap: Record<string, HistoryStatus | null> = {
    All: null,
    Drafts: "draft",
    Sent: "sent",
    Replied: "replied",
    Hired: "hired",
    "No reply": "no_reply",
  };

  const filtered = history
    .filter((h) => {
      const statusMatch = !filterMap[filter] || h.status === filterMap[filter];
      const searchMatch =
        !search ||
        h.jobTitle.toLowerCase().includes(search.toLowerCase()) ||
        h.client.toLowerCase().includes(search.toLowerCase());
      return statusMatch && searchMatch;
    })
    .sort((a, b) => {
      if (sortBy === "Match") return b.matchScore - a.matchScore;
      return b.id.localeCompare(a.id);
    });

  return (
    <div className="page">
      <PageHeader
        title="History"
        subtitle={`${history.length} cover letters generated`}
        action={
          <Btn variant="primary" size="sm">
            <Plus size={13} />
            New letter
          </Btn>
        }
      />

      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
        <div className="row" style={{ gap: 6, flex: 1 }}>
          {filterOptions.map((f) => (
            <ChipTag key={f} active={filter === f} onClick={() => setFilter(f)}>
              {f}
            </ChipTag>
          ))}
        </div>
        <Seg
          value={sortBy}
          options={["Date", "Match"]}
          onChange={setSortBy}
        />
      </div>

      <div
        className="search-input"
        style={{ width: "100%", marginBottom: 16, cursor: "text" }}
      >
        <Search size={14} />
        <input
          style={{
            flex: 1,
            background: "none",
            border: "none",
            outline: "none",
            color: "var(--text-1)",
          }}
          placeholder="Search by job title or client…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="card-bare" style={{ overflow: "hidden" }}>
        {/* Header row */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 130px 100px 90px 36px",
            gap: 12,
            padding: "10px 18px",
            borderBottom: "1px solid var(--border)",
            fontSize: 11.5,
            fontWeight: 600,
            textTransform: "uppercase",
            letterSpacing: "0.06em",
            color: "var(--text-3)",
          }}
        >
          <span>Job + Client</span>
          <span>Match</span>
          <span>Status</span>
          <span>Date</span>
          <span />
        </div>

        {filtered.length === 0 ? (
          <EmptyState
            icon={<History size={20} />}
            title="No letters found"
            text="Try adjusting the filter or search query."
          />
        ) : (
          filtered.map((h) => (
            <div
              className="history-row"
              key={h.id}
              onClick={() => setSelected(selected?.id === h.id ? null : h)}
              style={selected?.id === h.id ? { background: "var(--surface-2)" } : undefined}
            >
              <div>
                <div className="history-job-title">{h.jobTitle}</div>
                <div className="history-meta">
                  <span>{h.client}</span>
                  <span>·</span>
                  <span>{h.preview.slice(0, 60)}…</span>
                </div>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <MatchRing score={h.matchScore} size={38} />
                <span
                  style={{
                    fontSize: 12,
                    color:
                      h.matchScore >= 85
                        ? "var(--accent-text)"
                        : h.matchScore >= 65
                        ? "var(--warning)"
                        : "var(--danger)",
                  }}
                >
                  {h.matchScore}%
                </span>
              </div>
              <Badge variant={STATUS_VARIANTS[h.status]}>
                {STATUS_LABELS[h.status]}
              </Badge>
              <span style={{ fontSize: 12, color: "var(--text-3)" }}>{h.date}</span>
              <Btn variant="ghost" size="icon" onClick={() => {}}>
                <More size={14} />
              </Btn>
            </div>
          ))
        )}
      </div>

      {/* Detail panel */}
      {selected && (
        <div
          style={{
            marginTop: 20,
            background: "var(--surface)",
            border: "1px solid var(--border)",
            borderRadius: "var(--r-lg)",
            padding: 24,
          }}
        >
          <div className="between" style={{ marginBottom: 16 }}>
            <div>
              <div style={{ fontWeight: 600, fontSize: 15 }}>{selected.jobTitle}</div>
              <div style={{ fontSize: 12, color: "var(--text-3)", marginTop: 2 }}>
                {selected.client} · {selected.date}
              </div>
            </div>
            <div className="row" style={{ gap: 8 }}>
              <MatchRing score={selected.matchScore} size={44} />
              <Badge variant={STATUS_VARIANTS[selected.status]}>
                {STATUS_LABELS[selected.status]}
              </Badge>
              <Btn variant="ghost" size="icon" onClick={() => setSelected(null)}>
                <X size={14} />
              </Btn>
            </div>
          </div>
          <div className="letter-output" style={{ minHeight: 160 }}>
            {selected.letterText || selected.preview}
          </div>
          <div className="row" style={{ marginTop: 14, gap: 8 }}>
            <Btn variant="secondary" size="sm">
              <Copy size={13} />
              Copy
            </Btn>
            <Btn variant="secondary" size="sm">
              <Edit size={13} />
              Edit
            </Btn>
            <Btn variant="secondary" size="sm">
              <Refresh size={13} />
              Regenerate
            </Btn>
            <div style={{ flex: 1 }} />
            <Btn variant="danger" size="sm">
              <Trash size={13} />
              Delete
            </Btn>
          </div>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────
// KNOWLEDGE SCREEN
// ─────────────────────────────────────────────
interface KnowledgeProps {
  kb: KB;
  setKb: (kb: KB) => void;
}

function KnowledgeScreen({ kb, setKb }: KnowledgeProps) {
  const [tab, setTab] = useState("guidelines");
  const [editId, setEditId] = useState<string | null>(null);
  const [editBody, setEditBody] = useState("");

  const toggleGuideline = (id: string) => {
    setKb({
      ...kb,
      guidelines: kb.guidelines.map((g) =>
        g.id === id ? { ...g, active: !g.active } : g
      ),
    });
  };

  const saveEdit = (id: string) => {
    setKb({
      ...kb,
      guidelines: kb.guidelines.map((g) =>
        g.id === id ? { ...g, body: editBody } : g
      ),
    });
    setEditId(null);
  };

  return (
    <div className="page">
      <PageHeader
        title="Knowledge Base"
        subtitle="Guidelines and winning examples that shape every letter."
        action={
          <Btn variant="primary" size="sm">
            <Plus size={13} />
            Add guideline
          </Btn>
        }
      />

      <div className="tabs">
        {[
          { id: "guidelines", label: "Guidelines", count: kb.guidelines.length },
          { id: "examples", label: "Winning examples", count: kb.examples.length },
        ].map((t) => (
          <div
            key={t.id}
            className={`tab ${tab === t.id ? "active" : ""}`}
            onClick={() => setTab(t.id)}
          >
            {t.label}
            <span
              style={{
                fontSize: 11,
                background: "var(--surface-3)",
                padding: "1px 6px",
                borderRadius: 999,
                color: "var(--text-3)",
              }}
            >
              {t.count}
            </span>
          </div>
        ))}
      </div>

      {tab === "guidelines" && (
        <div className="col" style={{ gap: 10 }}>
          {kb.guidelines.map((g) => (
            <div
              key={g.id}
              style={{
                background: "var(--surface)",
                border: `1px solid ${g.active ? "var(--border)" : "var(--border)"}`,
                borderRadius: "var(--r-md)",
                padding: "14px 16px",
                opacity: g.active ? 1 : 0.55,
                transition: "opacity 0.2s",
              }}
            >
              <div className="between" style={{ marginBottom: 8 }}>
                <div className="row" style={{ gap: 10 }}>
                  <SwitchToggle checked={g.active} onChange={() => toggleGuideline(g.id)} />
                  <span style={{ fontWeight: 500, fontSize: 13.5, color: "var(--text-1)" }}>
                    {g.title}
                  </span>
                </div>
                <div className="row" style={{ gap: 4 }}>
                  <Btn
                    variant="ghost"
                    size="icon"
                    onClick={() => {
                      setEditId(g.id);
                      setEditBody(g.body);
                    }}
                  >
                    <Edit size={13} />
                  </Btn>
                  <Btn variant="ghost" size="icon">
                    <Trash size={13} />
                  </Btn>
                </div>
              </div>
              {editId === g.id ? (
                <div>
                  <textarea
                    className="textarea"
                    value={editBody}
                    onChange={(e) => setEditBody(e.target.value)}
                    style={{ fontSize: 13 }}
                  />
                  <div className="row" style={{ marginTop: 8, gap: 6 }}>
                    <Btn variant="primary" size="sm" onClick={() => saveEdit(g.id)}>
                      Save
                    </Btn>
                    <Btn variant="ghost" size="sm" onClick={() => setEditId(null)}>
                      Cancel
                    </Btn>
                  </div>
                </div>
              ) : (
                <p style={{ fontSize: 13, color: "var(--text-2)", margin: 0, lineHeight: 1.6 }}>
                  {g.body}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {tab === "examples" && (
        <div>
          <div className="kb-grid">
            {kb.examples.map((ex) => (
              <div className="kb-example-card" key={ex.id}>
                <div className="kb-example-header">
                  <span style={{ fontWeight: 600, fontSize: 13.5 }}>{ex.title}</span>
                  <div className="row" style={{ gap: 4 }}>
                    {Array.from({ length: ex.rating }).map((_, i) => (
                      <Star
                        key={i}
                        size={12}
                        style={{ color: "var(--warning)", fill: "var(--warning)" }}
                      />
                    ))}
                  </div>
                </div>
                <div className="kb-example-tags" style={{ marginBottom: 10 }}>
                  {ex.tags.map((t) => (
                    <Badge key={t}>{t}</Badge>
                  ))}
                </div>
                <div className="kb-example-snippet">{ex.snippet}</div>
                <div
                  style={{
                    marginTop: 14,
                    paddingTop: 12,
                    borderTop: "1px solid var(--border)",
                    fontSize: 12,
                    color: "var(--accent-text)",
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                  }}
                >
                  <CheckCircle size={12} />
                  {ex.outcome}
                </div>
              </div>
            ))}

            {/* Add card placeholder */}
            <div
              style={{
                background: "transparent",
                border: "1px dashed var(--border-strong)",
                borderRadius: "var(--r-lg)",
                padding: 18,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 10,
                cursor: "pointer",
                minHeight: 180,
                color: "var(--text-3)",
                transition: "border-color 0.12s, color 0.12s",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLDivElement).style.borderColor = "var(--border-focus)";
                (e.currentTarget as HTMLDivElement).style.color = "var(--text-2)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLDivElement).style.borderColor = "var(--border-strong)";
                (e.currentTarget as HTMLDivElement).style.color = "var(--text-3)";
              }}
            >
              <div
                style={{
                  width: 36,
                  height: 36,
                  borderRadius: 8,
                  background: "var(--surface-2)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Plus size={16} />
              </div>
              <span style={{ fontSize: 13 }}>Add winning example</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────
// SETTINGS SCREEN
// ─────────────────────────────────────────────
interface SettingsProps {
  user: UserData;
  setUser: (u: UserData) => void;
}

type SettingsSection =
  | "profile"
  | "skills"
  | "projects"
  | "experience"
  | "education"
  | "certifications"
  | "voice"
  | "pastletters";

const SETTINGS_SECTIONS: { id: SettingsSection; label: string; icon: React.ReactNode }[] = [
  { id: "profile", label: "Personal intro", icon: <User size={14} /> },
  { id: "skills", label: "Skills", icon: <Code size={14} /> },
  { id: "projects", label: "Projects", icon: <Folder size={14} /> },
  { id: "experience", label: "Work experience", icon: <Briefcase size={14} /> },
  { id: "education", label: "Education", icon: <Graduation size={14} /> },
  { id: "certifications", label: "Certifications", icon: <Award size={14} /> },
  { id: "voice", label: "Voice & tone", icon: <Mic size={14} /> },
  { id: "pastletters", label: "Past letters", icon: <Message size={14} /> },
];

function SettingsScreen({ user, setUser }: SettingsProps) {
  const [section, setSection] = useState<SettingsSection>("profile");
  const [newSkill, setNewSkill] = useState("");
  const [newAvoid, setNewAvoid] = useState("");
  const [toast, setToast] = useState<string | null>(null);

  const save = () => setToast("Changes saved");

  const addSkill = () => {
    if (!newSkill.trim()) return;
    const skill: Skill = {
      id: `s${Date.now()}`,
      name: newSkill.trim(),
      level: "Intermediate",
      years: 1,
    };
    setUser({ ...user, skills: [...user.skills, skill] });
    setNewSkill("");
  };

  const removeSkill = (id: string) => {
    setUser({ ...user, skills: user.skills.filter((s) => s.id !== id) });
  };

  const setSkillLevel = (id: string, level: SkillLevel) => {
    setUser({
      ...user,
      skills: user.skills.map((s) => (s.id === id ? { ...s, level } : s)),
    });
  };

  const addAvoid = () => {
    if (!newAvoid.trim()) return;
    setUser({
      ...user,
      tonePrefs: {
        ...user.tonePrefs,
        avoidPhrases: [...user.tonePrefs.avoidPhrases, newAvoid.trim()],
      },
    });
    setNewAvoid("");
  };

  const removeAvoid = (phrase: string) => {
    setUser({
      ...user,
      tonePrefs: {
        ...user.tonePrefs,
        avoidPhrases: user.tonePrefs.avoidPhrases.filter((p) => p !== phrase),
      },
    });
  };

  return (
    <div className="page">
      <PageHeader
        title="Settings"
        subtitle="Configure your profile, tone, and knowledge assets."
      />

      <div className="settings-grid">
        {/* Side nav */}
        <div className="settings-side-nav">
          {SETTINGS_SECTIONS.map((s) => (
            <div
              key={s.id}
              className={`settings-side-item ${section === s.id ? "active" : ""}`}
              onClick={() => setSection(s.id)}
            >
              {s.icon}
              {s.label}
            </div>
          ))}
        </div>

        {/* Content */}
        <div className="settings-section">
          {/* Profile */}
          {section === "profile" && (
            <div>
              <h2>Personal intro</h2>
              <p className="section-desc">
                This is how AI introduces you in every cover letter.
              </p>
              <div className="grid-2">
                <div className="field">
                  <label className="label">Full name</label>
                  <input
                    className="input"
                    value={user.name}
                    onChange={(e) => setUser({ ...user, name: e.target.value })}
                  />
                </div>
                <div className="field">
                  <label className="label">Professional title</label>
                  <input
                    className="input"
                    value={user.title}
                    onChange={(e) => setUser({ ...user, title: e.target.value })}
                  />
                </div>
                <div className="field">
                  <label className="label">Location</label>
                  <input
                    className="input"
                    value={user.location}
                    onChange={(e) => setUser({ ...user, location: e.target.value })}
                  />
                </div>
                <div className="field">
                  <label className="label">Hourly rate (USD)</label>
                  <input
                    className="input"
                    type="number"
                    value={user.hourlyRate}
                    onChange={(e) =>
                      setUser({ ...user, hourlyRate: Number(e.target.value) })
                    }
                  />
                </div>
              </div>
              <div className="field">
                <label className="label">About / bio</label>
                <textarea
                  className="textarea"
                  rows={5}
                  value={user.about}
                  onChange={(e) => setUser({ ...user, about: e.target.value })}
                />
                <p className="field-hint">
                  Used as context for every generation. Be specific about results.
                </p>
              </div>
              <Btn variant="primary" onClick={save}>
                Save changes
              </Btn>
            </div>
          )}

          {/* Skills */}
          {section === "skills" && (
            <div>
              <h2>Skills</h2>
              <p className="section-desc">
                AI uses your skill levels to calculate match scores and lead with your strongest evidence.
              </p>
              <div className="field" style={{ display: "flex", gap: 8 }}>
                <input
                  className="input"
                  placeholder="Add a skill…"
                  value={newSkill}
                  onChange={(e) => setNewSkill(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && addSkill()}
                />
                <Btn variant="secondary" onClick={addSkill}>
                  <Plus size={14} />
                  Add
                </Btn>
              </div>
              <div className="col" style={{ gap: 8 }}>
                {user.skills.map((s) => (
                  <div
                    key={s.id}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 12,
                      padding: "10px 14px",
                      background: "var(--surface)",
                      border: "1px solid var(--border)",
                      borderRadius: "var(--r-sm)",
                    }}
                  >
                    <span style={{ flex: 1, fontSize: 13.5 }}>{s.name}</span>
                    <Seg
                      value={s.level}
                      options={["Intermediate", "Advanced", "Expert"]}
                      onChange={(v) => setSkillLevel(s.id, v as SkillLevel)}
                    />
                    <Btn variant="ghost" size="icon" onClick={() => removeSkill(s.id)}>
                      <X size={13} />
                    </Btn>
                  </div>
                ))}
              </div>
              <div style={{ marginTop: 16 }}>
                <Btn variant="primary" onClick={save}>
                  Save changes
                </Btn>
              </div>
            </div>
          )}

          {/* Projects */}
          {section === "projects" && (
            <div>
              <h2>Projects</h2>
              <p className="section-desc">
                Case studies and project evidence that AI cites to prove your claims.
              </p>
              <div className="col" style={{ gap: 12 }}>
                {user.projects.map((p) => (
                  <div
                    key={p.id}
                    style={{
                      background: "var(--surface)",
                      border: "1px solid var(--border)",
                      borderRadius: "var(--r-md)",
                      padding: 16,
                    }}
                  >
                    <div className="between" style={{ marginBottom: 8 }}>
                      <span style={{ fontWeight: 600, fontSize: 14 }}>{p.title}</span>
                      <div className="row" style={{ gap: 4 }}>
                        <Btn variant="ghost" size="icon">
                          <Edit size={13} />
                        </Btn>
                        <Btn variant="ghost" size="icon">
                          <Trash size={13} />
                        </Btn>
                      </div>
                    </div>
                    <p style={{ fontSize: 13, color: "var(--text-2)", margin: "0 0 10px", lineHeight: 1.6 }}>
                      {p.description}
                    </p>
                    {p.results && (
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 6,
                          fontSize: 12.5,
                          color: "var(--accent-text)",
                          marginBottom: 10,
                        }}
                      >
                        <CheckCircle size={12} />
                        {p.results}
                      </div>
                    )}
                    <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                      {p.tags.map((t) => (
                        <Badge key={t}>{t}</Badge>
                      ))}
                    </div>
                  </div>
                ))}
                <Btn variant="secondary" style={{ alignSelf: "flex-start" }}>
                  <Plus size={13} />
                  Add project
                </Btn>
              </div>
            </div>
          )}

          {/* Experience */}
          {section === "experience" && (
            <div>
              <h2>Work experience</h2>
              <p className="section-desc">
                Your professional history — AI uses this to establish credibility.
              </p>
              <div className="card-bare">
                <div className="card-body">
                  {user.experience.map((e) => (
                    <div className="exp-row" key={e.id}>
                      <div className="exp-row-thumb">{e.company[0]}</div>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 500, fontSize: 13.5 }}>{e.role}</div>
                        <div style={{ fontSize: 12, color: "var(--text-2)", marginBottom: 8 }}>
                          {e.company} · {e.start}–{e.end}
                        </div>
                        <ul style={{ margin: 0, paddingLeft: 16 }}>
                          {e.bullets.map((b, i) => (
                            <li
                              key={i}
                              style={{ fontSize: 12.5, color: "var(--text-2)", marginBottom: 4, lineHeight: 1.5 }}
                            >
                              {b}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <Btn variant="ghost" size="icon">
                        <Edit size={13} />
                      </Btn>
                    </div>
                  ))}
                </div>
              </div>
              <div style={{ marginTop: 14 }}>
                <Btn variant="secondary">
                  <Plus size={13} />
                  Add experience
                </Btn>
              </div>
            </div>
          )}

          {/* Education */}
          {section === "education" && (
            <div>
              <h2>Education</h2>
              <p className="section-desc">Degrees and institutions.</p>
              <div className="card-bare">
                <div className="card-body">
                  {user.education.map((ed) => (
                    <div className="exp-row" key={ed.id}>
                      <div className="exp-row-thumb">{ed.institution[0]}</div>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 500, fontSize: 13.5 }}>
                          {ed.degree} in {ed.field}
                        </div>
                        <div style={{ fontSize: 12, color: "var(--text-2)" }}>
                          {ed.institution} · {ed.year}
                        </div>
                      </div>
                      <Btn variant="ghost" size="icon">
                        <Edit size={13} />
                      </Btn>
                    </div>
                  ))}
                </div>
              </div>
              <div style={{ marginTop: 14 }}>
                <Btn variant="secondary">
                  <Plus size={13} />
                  Add education
                </Btn>
              </div>
            </div>
          )}

          {/* Certifications */}
          {section === "certifications" && (
            <div>
              <h2>Certifications</h2>
              <p className="section-desc">Credentials that signal trust and expertise.</p>
              <div className="card-bare">
                <div className="card-body">
                  {user.certifications.map((c) => (
                    <div className="exp-row" key={c.id}>
                      <div className="exp-row-thumb">
                        <Award size={16} />
                      </div>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 500, fontSize: 13.5 }}>{c.name}</div>
                        <div style={{ fontSize: 12, color: "var(--text-2)" }}>
                          {c.issuer} · {c.year}
                        </div>
                      </div>
                      <Btn variant="ghost" size="icon">
                        <Edit size={13} />
                      </Btn>
                    </div>
                  ))}
                </div>
              </div>
              <div style={{ marginTop: 14 }}>
                <Btn variant="secondary">
                  <Plus size={13} />
                  Add certification
                </Btn>
              </div>
            </div>
          )}

          {/* Voice & tone */}
          {section === "voice" && (
            <div>
              <h2>Voice &amp; tone</h2>
              <p className="section-desc">
                Shape how AI writes — your voice, your rules.
              </p>

              <div className="field">
                <label className="label">Default tone</label>
                <div className="tone-grid">
                  {TONES.map((t) => (
                    <div
                      key={t.name}
                      className={`tone-card ${user.tonePrefs.defaultTone === t.name ? "active" : ""}`}
                      onClick={() =>
                        setUser({
                          ...user,
                          tonePrefs: { ...user.tonePrefs, defaultTone: t.name },
                        })
                      }
                    >
                      <span className="tone-card-emoji">{t.emoji}</span>
                      <div className="tone-card-name">{t.name}</div>
                      <div className="tone-card-desc">{t.desc}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="field">
                <label className="label">Voice note</label>
                <textarea
                  className="textarea"
                  rows={3}
                  value={user.tonePrefs.voiceNote}
                  onChange={(e) =>
                    setUser({
                      ...user,
                      tonePrefs: { ...user.tonePrefs, voiceNote: e.target.value },
                    })
                  }
                />
                <p className="field-hint">
                  Describe your writing style in plain English. AI uses this as a style guide.
                </p>
              </div>

              <div className="field">
                <label className="label">Avoid phrases</label>
                <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
                  <input
                    className="input"
                    placeholder="Add a phrase to avoid…"
                    value={newAvoid}
                    onChange={(e) => setNewAvoid(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && addAvoid()}
                  />
                  <Btn variant="secondary" onClick={addAvoid}>
                    Add
                  </Btn>
                </div>
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                  {user.tonePrefs.avoidPhrases.map((p) => (
                    <ChipTag key={p} onRemove={() => removeAvoid(p)}>
                      {p}
                    </ChipTag>
                  ))}
                </div>
              </div>

              <div className="field">
                <label className="label">Sign-off</label>
                <textarea
                  className="textarea"
                  rows={2}
                  value={user.tonePrefs.signOff}
                  onChange={(e) =>
                    setUser({
                      ...user,
                      tonePrefs: { ...user.tonePrefs, signOff: e.target.value },
                    })
                  }
                />
              </div>

              <Btn variant="primary" onClick={save}>
                Save changes
              </Btn>
            </div>
          )}

          {/* Past letters */}
          {section === "pastletters" && (
            <div>
              <h2>Past letters</h2>
              <p className="section-desc">
                Upload high-performing letters you wrote manually — AI learns your best patterns.
              </p>
              <EmptyState
                icon={<Upload size={20} />}
                title="No past letters uploaded"
                text="Upload .txt or .docx files of letters that got you hired. AI will extract your best phrases and structures."
                action={
                  <Btn variant="secondary" size="sm">
                    <Upload size={13} />
                    Upload letters
                  </Btn>
                }
              />
            </div>
          )}
        </div>
      </div>

      {toast && <Toast message={toast} onDone={() => setToast(null)} />}
    </div>
  );
}

// ─────────────────────────────────────────────
// ROOT APP
// ─────────────────────────────────────────────
export default function App() {
  const [authed, setAuthed] = useState(false);
  const [route, setRoute] = useState<Route>("dashboard");
  const [user, setUser] = useState<UserData>(SAMPLE_USER);
  const [history, setHistory] = useState<HistoryEntry[]>(SAMPLE_HISTORY);
  const [kb, setKb] = useState<KB>(SAMPLE_KB);

  const handleSaveHistory = (entry: HistoryEntry) => {
    setHistory((prev) => [entry, ...prev]);
  };

  const handleNewLetter = () => setRoute("generator");

  if (!authed) {
    return <AuthScreen onSignIn={() => setAuthed(true)} />;
  }

  return (
    <div className="app">
      <Sidebar
        route={route}
        setRoute={setRoute}
        user={user}
        historyCount={history.length}
        onLogout={() => setAuthed(false)}
      />
      <div className="app-main">
        <Topbar onNewLetter={handleNewLetter} />
        {route === "dashboard" && (
          <DashboardScreen
            user={user}
            history={history}
            onGenerate={() => setRoute("generator")}
          />
        )}
        {route === "generator" && <GeneratorScreen onSave={handleSaveHistory} />}
        {route === "history" && <HistoryScreen history={history} />}
        {route === "knowledge" && <KnowledgeScreen kb={kb} setKb={setKb} />}
        {route === "settings" && <SettingsScreen user={user} setUser={setUser} />}
      </div>
    </div>
  );
}

