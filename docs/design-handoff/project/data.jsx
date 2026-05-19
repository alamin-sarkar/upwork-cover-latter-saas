/* PitchCraft — Sample data store */

const SAMPLE_USER = {
  name: "Rakib Hasan",
  email: "rakib.hasan@gmail.com",
  initials: "RH",
  title: "Full-Stack Developer · AI/ML",
  location: "Dhaka, Bangladesh",
  hourlyRate: 35,
  about: "Full-stack developer with 5+ years building production AI applications. Specialized in LLM integration, RAG pipelines, and React-based dashboards. I help SaaS founders ship AI features that actually work — not just demos.",
  skills: [
    { name: "React", level: "Expert", years: 5 },
    { name: "TypeScript", level: "Expert", years: 4 },
    { name: "Node.js", level: "Expert", years: 5 },
    { name: "Python", level: "Advanced", years: 4 },
    { name: "OpenAI API", level: "Expert", years: 2 },
    { name: "LangChain", level: "Advanced", years: 2 },
    { name: "Pinecone / Vector DBs", level: "Advanced", years: 2 },
    { name: "Next.js", level: "Expert", years: 3 },
    { name: "PostgreSQL", level: "Advanced", years: 4 },
    { name: "AWS", level: "Intermediate", years: 3 },
    { name: "Tailwind CSS", level: "Expert", years: 3 },
    { name: "Prisma", level: "Advanced", years: 2 },
  ],
  projects: [
    {
      title: "DocuChat AI",
      tagline: "PDF chatbot SaaS — 12K MAU",
      desc: "Built end-to-end RAG pipeline using LangChain + Pinecone. Scaled from 0 → 12K MAU in 6 months. Reduced answer latency by 60% via embedding caching.",
      stack: ["Next.js", "Pinecone", "OpenAI", "Stripe"],
      link: "docuchat.example.com",
      outcome: "$8K MRR within 4 months",
    },
    {
      title: "SalesGPT — Outbound automation",
      tagline: "Cold email AI for B2B teams",
      desc: "Multi-tenant SaaS that personalizes cold emails using LinkedIn data. Built scraping pipeline, GPT-4 prompt chain, and Gmail OAuth integration.",
      stack: ["React", "Node.js", "GPT-4", "Puppeteer"],
      link: "github.com/rakib/salesgpt",
      outcome: "300+ users, 22% reply rate avg",
    },
    {
      title: "MedNote — Clinical assistant",
      tagline: "HIPAA-compliant transcription",
      desc: "Real-time medical scribe using Whisper + custom medical entity extraction. Reduced doctor documentation time by 4 hrs/day.",
      stack: ["React Native", "Whisper", "Python", "AWS"],
      link: "—",
      outcome: "Deployed to 3 clinics",
    },
  ],
  experience: [
    {
      role: "Senior AI Engineer (Contract)",
      company: "Lumen Health",
      period: "2024 — Present",
      bullets: [
        "Lead AI engineer building patient-facing chatbot using GPT-4 + RAG over clinical guidelines",
        "Reduced hallucination rate from 14% → 2.1% via citation-required prompting",
        "Mentor 2 junior devs on prompt engineering & evaluation",
      ],
    },
    {
      role: "Founding Engineer",
      company: "Threadly (YC W23)",
      period: "2023 — 2024",
      bullets: [
        "Built MVP in 6 weeks; shipped to Product Hunt #2 product of the day",
        "Owned the entire RAG stack — ingestion, embedding, retrieval, evaluation",
      ],
    },
    {
      role: "Full-Stack Developer",
      company: "Cognify Studio (Agency)",
      period: "2021 — 2023",
      bullets: [
        "Delivered 14 client projects across fintech, e-commerce, and healthtech",
        "Lead engineer on $120K rebuild project — finished 3 weeks ahead of deadline",
      ],
    },
  ],
  education: [
    {
      school: "Bangladesh University of Engineering and Technology (BUET)",
      degree: "B.Sc. in Computer Science & Engineering",
      period: "2017 — 2021",
      detail: "CGPA 3.78 / 4.0 · Final-year project on transformer-based code summarization",
    },
  ],
  certifications: [
    { name: "DeepLearning.AI — LangChain for LLM Application Development", issuer: "DeepLearning.AI", year: "2024" },
    { name: "AWS Certified Solutions Architect — Associate", issuer: "Amazon Web Services", year: "2023" },
    { name: "Google Cloud Professional Data Engineer", issuer: "Google", year: "2022" },
  ],
  tonePrefs: {
    default: "confident",
    voice: "Direct, technical, and outcome-focused. Avoid filler phrases like 'I hope this finds you well'. Lead with a concrete observation about the job.",
    avoid: ["'I am writing to express my interest'", "'humbly request'", "'kindly consider'", "long preambles", "generic praise for the company"],
    signature: "Best,\nRakib",
  },
};

const SAMPLE_HISTORY = [
  {
    id: "h-001",
    jobTitle: "Senior Full-Stack Developer for AI SaaS — RAG pipeline",
    client: "VertexLabs Inc.",
    clientCountry: "United States",
    budget: "$3,000 — $5,000",
    date: "2026-05-17",
    tone: "Confident",
    matchScore: 94,
    status: "sent",
    preview: "I noticed your job mentions reducing hallucination on legal documents — I shipped exactly this for Lumen Health and brought hallucination from 14% to 2.1%...",
  },
  {
    id: "h-002",
    jobTitle: "Build me a custom GPT-4 chatbot with vector DB",
    client: "Marcus T.",
    clientCountry: "Australia",
    budget: "$1,500 fixed",
    date: "2026-05-15",
    tone: "Friendly",
    matchScore: 88,
    status: "replied",
    preview: "Your spec maps closely to DocuChat AI, a RAG SaaS I built and scaled to 12K MAU. I can have a working prototype within 5 days...",
  },
  {
    id: "h-003",
    jobTitle: "React + Node engineer — long-term contract",
    client: "TaylorBuild Studios",
    clientCountry: "Canada",
    budget: "$40/hr — $60/hr",
    date: "2026-05-14",
    tone: "Formal",
    matchScore: 81,
    status: "draft",
    preview: "I've spent the last 3 years inside React/Node codebases at agency scale (14 projects delivered at Cognify Studio)...",
  },
  {
    id: "h-004",
    jobTitle: "AI Cold Email Tool — need help finishing MVP",
    client: "Priya S.",
    clientCountry: "India",
    budget: "$800 fixed",
    date: "2026-05-12",
    tone: "Confident",
    matchScore: 96,
    status: "hired",
    preview: "I literally built this exact product — SalesGPT, an outbound AI tool. 300+ users on it now. I can finish your MVP in under 2 weeks because most of the patterns are already in my head...",
  },
  {
    id: "h-005",
    jobTitle: "Need WordPress developer urgently",
    client: "Dean M.",
    clientCountry: "United Kingdom",
    budget: "$200 — $400",
    date: "2026-05-10",
    tone: "Casual",
    matchScore: 42,
    status: "no-reply",
    preview: "Quick note — while my primary stack is React/Node, I've done a handful of WordPress sites and can definitely help here...",
  },
  {
    id: "h-006",
    jobTitle: "Build internal AI tool for sales team",
    client: "Helio CRM",
    clientCountry: "Germany",
    budget: "$5,000 — $10,000",
    date: "2026-05-08",
    tone: "Confident",
    matchScore: 91,
    status: "replied",
    preview: "Two questions before I dive in: (1) is the sales team currently using Salesforce or HubSpot, and (2) what's the ideal latency for the assistant?...",
  },
  {
    id: "h-007",
    jobTitle: "Next.js dashboard for analytics startup",
    client: "Datapulse",
    clientCountry: "Singapore",
    budget: "$30/hr — $50/hr",
    date: "2026-05-05",
    tone: "Friendly",
    matchScore: 79,
    status: "sent",
    preview: "Dashboards are my favorite work — I've shipped 6 of them over the last year. Looking at your screenshots, I'd recommend...",
  },
];

const SAMPLE_KB = {
  guidelines: [
    {
      title: "Open with a specific observation, not a greeting",
      detail: "Skip 'Dear hiring manager' entirely. The first sentence should reference something specific in their job post — a tech, a goal, a constraint, or a number. This signals you actually read it.",
    },
    {
      title: "Lead with proof, not promises",
      detail: "Don't say 'I am skilled in X'. Show it: 'I shipped X for Y, here is the result'. One sentence of evidence beats a paragraph of claims.",
    },
    {
      title: "Mirror their vocabulary",
      detail: "If they say 'RAG', say 'RAG' — not 'retrieval-augmented generation'. If they call it a 'chatbot', call it a 'chatbot' — not an 'AI agent'. Match terms exactly.",
    },
    {
      title: "End with a question, not a CTA",
      detail: "Asking a sharp clarifying question makes you look like a senior, and almost forces a reply. 'Two CTAs' or 'Looking forward to hearing from you' kills momentum.",
    },
    {
      title: "Keep it under 150 words",
      detail: "Most cover letters are read on mobile during a 30-second scroll. If they have to scroll, you've already lost. Aim for 120–150 words max.",
    },
    {
      title: "One concrete number, always",
      detail: "Hallucination 14% → 2.1%. 12K MAU. 300+ users. Numbers anchor the brain. If you don't have a number, find one before sending.",
    },
  ],
  examples: [
    {
      title: "RAG / chatbot job",
      tags: ["AI", "RAG", "Confident"],
      outcome: "Hired — $4,200",
      letter: "I noticed your job mentions reducing hallucination on legal documents — I shipped exactly this for Lumen Health and brought hallucination from 14% down to 2.1% by enforcing citation-required prompting.\n\nMy approach for you:\n1. Audit your current eval set (or build one if missing)\n2. Switch to citation-mode prompts + retrieval reranking\n3. Add a refusal classifier for off-topic queries\n\nTwo quick questions before I quote: (1) what's your current eval coverage, and (2) is the chatbot user-facing or internal?\n\nBest,\nRakib",
    },
    {
      title: "Cold email automation",
      tags: ["AI", "B2B", "Confident"],
      outcome: "Hired — $800",
      letter: "I literally built this exact product before — SalesGPT, an outbound AI tool with 300+ active users and a 22% reply rate average.\n\nLooking at your spec, the LinkedIn enrichment is the hard part — most teams underestimate it. I'd start there, then layer the GPT-4 prompt chain on top.\n\nI can ship a working MVP in 10 days at your fixed budget. What's the volume you're aiming for at launch?\n\n— Rakib",
    },
    {
      title: "Long-term React contract",
      tags: ["React", "Long-term", "Formal"],
      outcome: "Interview scheduled",
      letter: "Long-term React contracts are exactly the kind of work I'm looking to commit to right now. I've spent the last 3 years inside React/Node codebases — 14 production projects at Cognify Studio, plus founding engineer at Threadly (YC W23).\n\nI work async, write proper PR descriptions, and don't ghost. Most of my clients renew.\n\nHappy to share GitHub access on a private repo as a portfolio sample. What's the team size and the current stack?\n\nBest,\nRakib",
    },
    {
      title: "Quick fix / urgent job",
      tags: ["Quick win", "Casual"],
      outcome: "Hired — $350",
      letter: "Saw this just went up. I can start in the next hour and have it done today.\n\nBased on the screenshot, this looks like a state-not-resetting issue between route changes. 90% confident I know the fix. Worst case it takes 2 hours.\n\nFixed price works for me. Want me to start?\n\n— Rakib",
    },
  ],
};

const SAMPLE_JOB = `We're a fast-growing AI SaaS (Series A, ~25 people) building a legal research assistant for mid-sized law firms in the US. Our chatbot is live but hallucinates too often on case-law citations, and we need a senior engineer to fix it.

Specifically:
- Audit our current RAG pipeline (LangChain + Pinecone, ~80K docs indexed)
- Reduce hallucination on cited case names and dates
- Improve retrieval recall on multi-jurisdictional queries
- Set up an eval framework so we can track regressions

You should be senior (5+ years), have shipped a production RAG system before, and be comfortable owning this independently. We move fast — no committee. Contract initially, with strong potential to extend.

Stack: Next.js, Python, LangChain, Pinecone, GPT-4 + Claude, AWS.

Budget: $3,000 — $5,000 for the initial audit + first round of fixes.

Bonus: experience with legal-tech or any compliance-heavy domain.`;

window.SAMPLE_USER = SAMPLE_USER;
window.SAMPLE_HISTORY = SAMPLE_HISTORY;
window.SAMPLE_KB = SAMPLE_KB;
window.SAMPLE_JOB = SAMPLE_JOB;
