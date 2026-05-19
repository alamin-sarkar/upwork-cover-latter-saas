/* PitchCraft — Settings (profile sections) */

const SETTINGS_SECTIONS = [
  { id: "profile", label: "Personal intro", icon: "user" },
  { id: "skills", label: "Skills", icon: "code" },
  { id: "projects", label: "Projects", icon: "folder" },
  { id: "experience", label: "Work experience", icon: "briefcase" },
  { id: "education", label: "Education", icon: "graduation" },
  { id: "certifications", label: "Certifications", icon: "award" },
  { id: "tone", label: "Voice & tone", icon: "mic" },
  { id: "past-letters", label: "Past letters", icon: "file" },
];

function Settings({ user, onUpdate }) {
  const [section, setSection] = useState("profile");
  const update = (patch) => onUpdate({ ...user, ...patch });

  return (
    <div className="page">
      <PageHeader
        title="Settings"
        subtitle="Everything here feeds the AI. The more complete your profile, the sharper your cover letters."
        action={<Badge variant="accent" dot>Profile 92% complete</Badge>}
      />

      <div className="settings-grid">
        <div className="settings-side-nav">
          {SETTINGS_SECTIONS.map((s) => {
            const Ico = Icons[s.icon];
            return (
              <div key={s.id} className={`settings-side-item ${section === s.id ? "active" : ""}`} onClick={() => setSection(s.id)}>
                <Ico /> {s.label}
              </div>
            );
          })}
        </div>

        <div className="settings-section">
          {section === "profile" && <ProfileSection user={user} update={update} />}
          {section === "skills" && <SkillsSection user={user} update={update} />}
          {section === "projects" && <ProjectsSection user={user} update={update} />}
          {section === "experience" && <ExperienceSection user={user} update={update} />}
          {section === "education" && <EducationSection user={user} update={update} />}
          {section === "certifications" && <CertificationsSection user={user} update={update} />}
          {section === "tone" && <ToneSection user={user} update={update} />}
          {section === "past-letters" && <PastLettersSection />}
        </div>
      </div>
    </div>
  );
}

function SectionHeader({ title, desc, action }) {
  return (
    <div className="between mb-4">
      <div>
        <h2>{title}</h2>
        <p className="section-desc">{desc}</p>
      </div>
      {action}
    </div>
  );
}

function ProfileSection({ user, update }) {
  return (
    <>
      <SectionHeader
        title="Personal intro"
        desc="This 1-paragraph 'about me' anchors the AI's understanding of you."
      />

      <Card className="mb-4">
        <div className="row" style={{ gap: 18, alignItems: "flex-start" }}>
          <Avatar initials={user.initials} size="lg" />
          <div style={{ flex: 1 }}>
            <div className="grid-2 mb-2">
              <div className="field" style={{ marginBottom: 0 }}>
                <label className="label">Full name</label>
                <input className="input" defaultValue={user.name} />
              </div>
              <div className="field" style={{ marginBottom: 0 }}>
                <label className="label">Title / Headline</label>
                <input className="input" defaultValue={user.title} />
              </div>
            </div>
            <div className="grid-2">
              <div className="field" style={{ marginBottom: 0 }}>
                <label className="label">Location</label>
                <input className="input" defaultValue={user.location} />
              </div>
              <div className="field" style={{ marginBottom: 0 }}>
                <label className="label">Hourly rate (USD)</label>
                <input className="input" type="number" defaultValue={user.hourlyRate} />
              </div>
            </div>
          </div>
        </div>
      </Card>

      <Card title="About me" action={<Badge>Used in every letter</Badge>}>
        <div className="field" style={{ marginBottom: 0 }}>
          <label className="label">Tell the AI who you are and what you do</label>
          <textarea
            className="textarea"
            rows={5}
            defaultValue={user.about}
            onBlur={(e) => update({ about: e.target.value })}
          />
          <div className="field-hint">
            ~50–120 words is the sweet spot. Focus on outcomes you've delivered, not just titles. Use specific numbers.
          </div>
        </div>
      </Card>
    </>
  );
}

function SkillsSection({ user, update }) {
  const [newSkill, setNewSkill] = useState("");
  const add = () => {
    if (!newSkill.trim()) return;
    update({ skills: [...user.skills, { name: newSkill.trim(), level: "Intermediate", years: 1 }] });
    setNewSkill("");
  };
  const remove = (idx) => update({ skills: user.skills.filter((_, i) => i !== idx) });
  const setLevel = (idx, level) => update({
    skills: user.skills.map((s, i) => i === idx ? { ...s, level } : s),
  });

  return (
    <>
      <SectionHeader
        title="Skills"
        desc="The AI uses these to score job fit and decide which skills to lead with."
      />

      <Card className="mb-4">
        <div className="row mb-3">
          <input
            className="input"
            placeholder="Add a skill (e.g. Stripe, FastAPI, Three.js)"
            value={newSkill}
            onChange={(e) => setNewSkill(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && add()}
          />
          <Button variant="primary" icon={<Icons.plus />} onClick={add}>Add</Button>
        </div>
        <div style={{ fontSize: 12, color: "var(--text-3)" }}>{user.skills.length} skills · Drag to reorder</div>
      </Card>

      <Card title="Your skill stack">
        <div className="col" style={{ gap: 6 }}>
          {user.skills.map((s, i) => (
            <div key={i} className="between" style={{ padding: "8px 0", borderBottom: i < user.skills.length - 1 ? "1px solid var(--border)" : "none" }}>
              <div className="row" style={{ gap: 10 }}>
                <div style={{ width: 28, height: 28, borderRadius: 6, background: "var(--surface-2)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--text-2)" }}>
                  <Icons.code size={13} />
                </div>
                <div>
                  <div style={{ fontWeight: 500, fontSize: 13.5 }}>{s.name}</div>
                  <div style={{ fontSize: 12, color: "var(--text-3)" }}>{s.years} years experience</div>
                </div>
              </div>
              <div className="row">
                <Segmented
                  value={s.level}
                  options={["Intermediate", "Advanced", "Expert"]}
                  onChange={(v) => setLevel(i, v)}
                />
                <button className="btn btn-ghost btn-icon btn-sm" onClick={() => remove(i)} title="Remove">
                  <Icons.trash />
                </button>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </>
  );
}

function ProjectsSection({ user, update }) {
  return (
    <>
      <SectionHeader
        title="Projects"
        desc="Your portfolio. The AI picks the project that best matches each job and leads with it."
        action={<Button variant="primary" size="sm" icon={<Icons.plus />}>Add project</Button>}
      />

      <div className="col" style={{ gap: 14 }}>
        {user.projects.map((p, i) => (
          <Card key={i}>
            <div className="row" style={{ alignItems: "flex-start", gap: 14 }}>
              <div className="exp-row-thumb" style={{ width: 44, height: 44, fontSize: 16, background: "linear-gradient(135deg, var(--accent), var(--accent-press))", color: "white" }}>
                {p.title.slice(0, 2).toUpperCase()}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div className="between" style={{ marginBottom: 6 }}>
                  <div>
                    <div style={{ fontSize: 15, fontWeight: 600 }}>{p.title}</div>
                    <div style={{ fontSize: 13, color: "var(--text-2)" }}>{p.tagline}</div>
                  </div>
                  <div className="row">
                    <Badge variant="success" dot>{p.outcome}</Badge>
                    <button className="btn btn-ghost btn-icon btn-sm"><Icons.edit /></button>
                    <button className="btn btn-ghost btn-icon btn-sm"><Icons.more /></button>
                  </div>
                </div>
                <p style={{ fontSize: 13, color: "var(--text-2)", lineHeight: 1.6, margin: "0 0 10px" }}>{p.desc}</p>
                <div className="row" style={{ gap: 4, flexWrap: "wrap" }}>
                  {p.stack.map((s) => <Badge key={s}>{s}</Badge>)}
                  <div style={{ flex: 1 }} />
                  <a href={`https://${p.link}`} className="row" style={{ fontSize: 12, color: "var(--text-3)", gap: 4 }}>
                    <Icons.link size={11} /> {p.link}
                  </a>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </>
  );
}

function ExperienceSection({ user, update }) {
  return (
    <>
      <SectionHeader
        title="Work experience"
        desc="Your professional timeline. The AI references roles when relevant to the job context."
        action={<Button variant="primary" size="sm" icon={<Icons.plus />}>Add role</Button>}
      />

      <Card>
        {user.experience.map((e, i) => (
          <div key={i} className="exp-row">
            <div className="exp-row-thumb"><Icons.briefcase size={16} /></div>
            <div style={{ flex: 1 }}>
              <div className="between" style={{ marginBottom: 4 }}>
                <div>
                  <div style={{ fontWeight: 600, fontSize: 14 }}>{e.role}</div>
                  <div style={{ fontSize: 13, color: "var(--text-2)" }}>{e.company} · {e.period}</div>
                </div>
                <button className="btn btn-ghost btn-icon btn-sm"><Icons.edit /></button>
              </div>
              <ul style={{ margin: "6px 0 0", paddingLeft: 18, fontSize: 13, color: "var(--text-2)", lineHeight: 1.65 }}>
                {e.bullets.map((b, k) => <li key={k} style={{ marginBottom: 3 }}>{b}</li>)}
              </ul>
            </div>
          </div>
        ))}
      </Card>
    </>
  );
}

function EducationSection({ user, update }) {
  return (
    <>
      <SectionHeader
        title="Education"
        desc="Optional. Useful only for jobs where credentials matter."
        action={<Button variant="primary" size="sm" icon={<Icons.plus />}>Add</Button>}
      />
      <Card>
        {user.education.map((e, i) => (
          <div key={i} className="exp-row" style={{ borderBottom: i < user.education.length - 1 ? undefined : "none" }}>
            <div className="exp-row-thumb"><Icons.graduation size={16} /></div>
            <div style={{ flex: 1 }}>
              <div className="between">
                <div>
                  <div style={{ fontWeight: 600, fontSize: 14 }}>{e.school}</div>
                  <div style={{ fontSize: 13, color: "var(--text-2)" }}>{e.degree} · {e.period}</div>
                  <div style={{ fontSize: 12.5, color: "var(--text-3)", marginTop: 4 }}>{e.detail}</div>
                </div>
                <button className="btn btn-ghost btn-icon btn-sm"><Icons.edit /></button>
              </div>
            </div>
          </div>
        ))}
      </Card>
    </>
  );
}

function CertificationsSection({ user, update }) {
  return (
    <>
      <SectionHeader
        title="Certifications"
        desc="Credentials worth mentioning when relevant to a job."
        action={<Button variant="primary" size="sm" icon={<Icons.plus />}>Add</Button>}
      />
      <div className="col" style={{ gap: 10 }}>
        {user.certifications.map((c, i) => (
          <div key={i} className="card row" style={{ gap: 14, alignItems: "center", padding: 16 }}>
            <div style={{ width: 36, height: 36, borderRadius: 8, background: "var(--accent-soft)", color: "var(--accent-text)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
              <Icons.award size={18} />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 500, fontSize: 13.5 }}>{c.name}</div>
              <div style={{ fontSize: 12.5, color: "var(--text-3)" }}>{c.issuer} · {c.year}</div>
            </div>
            <button className="btn btn-ghost btn-icon btn-sm"><Icons.edit /></button>
            <button className="btn btn-ghost btn-icon btn-sm"><Icons.trash /></button>
          </div>
        ))}
      </div>
    </>
  );
}

function ToneSection({ user, update }) {
  const [voice, setVoice] = useState(user.tonePrefs.voice);
  const [signature, setSignature] = useState(user.tonePrefs.signature);
  const [defaultTone, setDefaultTone] = useState(user.tonePrefs.default);
  const [avoid, setAvoid] = useState(user.tonePrefs.avoid);
  const [newAvoid, setNewAvoid] = useState("");

  const save = () => update({ tonePrefs: { ...user.tonePrefs, voice, signature, default: defaultTone, avoid } });

  return (
    <>
      <SectionHeader
        title="Voice & tone"
        desc="Train the AI to write exactly like you — your phrasing, what you'd never say, your sign-off."
      />

      <Card title="Default tone" className="mb-4">
        <div className="tone-grid">
          {[
            { id: "confident", emoji: "💪", name: "Confident", desc: "Direct, sharp, evidence-led" },
            { id: "friendly", emoji: "👋", name: "Friendly", desc: "Warm, conversational" },
            { id: "formal", emoji: "🎩", name: "Formal", desc: "Polished, corporate" },
            { id: "casual", emoji: "🤙", name: "Casual", desc: "Short, breezy, human" },
          ].map((t) => (
            <div key={t.id} className={`tone-card ${defaultTone === t.id ? "active" : ""}`} onClick={() => { setDefaultTone(t.id); save(); }}>
              <span className="tone-card-emoji">{t.emoji}</span>
              <div className="tone-card-name">{t.name}</div>
              <div className="tone-card-desc">{t.desc}</div>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Your voice — describe it">
        <div className="field" style={{ marginBottom: 16 }}>
          <textarea
            className="textarea"
            rows={4}
            value={voice}
            onChange={(e) => setVoice(e.target.value)}
            onBlur={save}
          />
          <div className="field-hint">
            Describe how you write. E.g. "I lead with proof, use one number per paragraph, never use the word 'utilize'."
          </div>
        </div>

        <div className="field">
          <label className="label">Phrases to never use</label>
          <div className="row" style={{ flexWrap: "wrap", gap: 6, marginBottom: 8 }}>
            {avoid.map((p, i) => (
              <Chip key={i} onRemove={() => { const next = avoid.filter((_, k) => k !== i); setAvoid(next); save(); }}>
                {p}
              </Chip>
            ))}
          </div>
          <div className="row">
            <input
              className="input"
              placeholder="Add a phrase to ban"
              value={newAvoid}
              onChange={(e) => setNewAvoid(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && newAvoid.trim()) {
                  const next = [...avoid, newAvoid.trim()];
                  setAvoid(next);
                  setNewAvoid("");
                  save();
                }
              }}
            />
          </div>
        </div>

        <div className="field" style={{ marginBottom: 0 }}>
          <label className="label">Sign-off</label>
          <textarea
            className="textarea"
            rows={2}
            value={signature}
            onChange={(e) => setSignature(e.target.value)}
            onBlur={save}
          />
        </div>
      </Card>
    </>
  );
}

function PastLettersSection() {
  return (
    <>
      <SectionHeader
        title="Past successful letters"
        desc="Paste letters that worked for you. The AI studies your patterns and replicates them."
        action={<Button variant="primary" size="sm" icon={<Icons.plus />}>Add letter</Button>}
      />
      <Card>
        <EmptyState
          icon={<Icons.file />}
          title="No past letters yet"
          text="Have a cover letter that got you hired? Paste it here. The AI will reverse-engineer your style and use it as a reference."
          action={<Button variant="primary" size="sm" icon={<Icons.upload />}>Paste your first letter</Button>}
        />
      </Card>
    </>
  );
}

window.Settings = Settings;
