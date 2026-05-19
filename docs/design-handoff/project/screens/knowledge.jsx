/* PitchCraft — Knowledge Base */

function KnowledgeBase({ kb, onUpdate }) {
  const [tab, setTab] = useState("guidelines");
  const [editing, setEditing] = useState(null);

  const updateGuideline = (idx, patch) => {
    const next = { ...kb, guidelines: kb.guidelines.map((g, i) => i === idx ? { ...g, ...patch } : g) };
    onUpdate(next);
  };
  const addGuideline = () => {
    onUpdate({ ...kb, guidelines: [...kb.guidelines, { title: "New rule", detail: "Add detail here…" }] });
    setEditing({ type: "guideline", index: kb.guidelines.length });
  };
  const removeGuideline = (idx) => {
    onUpdate({ ...kb, guidelines: kb.guidelines.filter((_, i) => i !== idx) });
  };

  return (
    <div className="page">
      <PageHeader
        title="Knowledge Base"
        subtitle="Your private playbook. The AI uses these guidelines and examples every time it writes."
        action={
          <Button variant="primary" size="sm" icon={<Icons.plus />} onClick={tab === "guidelines" ? addGuideline : null}>
            {tab === "guidelines" ? "Add rule" : "Add example"}
          </Button>
        }
      />

      <div className="tabs">
        <div className={`tab ${tab === "guidelines" ? "active" : ""}`} onClick={() => setTab("guidelines")}>
          <Icons.zap size={14} /> Guidelines
          <Badge>{kb.guidelines.length}</Badge>
        </div>
        <div className={`tab ${tab === "examples" ? "active" : ""}`} onClick={() => setTab("examples")}>
          <Icons.file size={14} /> Winning examples
          <Badge>{kb.examples.length}</Badge>
        </div>
      </div>

      {tab === "guidelines" && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 320px", gap: 20, alignItems: "start" }}>
          <div className="col" style={{ gap: 10 }}>
            {kb.guidelines.map((g, i) => (
              <div key={i} className="card" style={{ position: "relative" }}>
                <div className="row" style={{ alignItems: "flex-start", gap: 12 }}>
                  <div style={{ width: 28, height: 28, borderRadius: 8, background: "var(--accent-soft)", color: "var(--accent-text)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, fontWeight: 600, fontSize: 13 }}>
                    {i + 1}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    {editing?.type === "guideline" && editing.index === i ? (
                      <>
                        <input
                          className="input mb-2"
                          value={g.title}
                          onChange={(e) => updateGuideline(i, { title: e.target.value })}
                          style={{ fontWeight: 600 }}
                        />
                        <textarea
                          className="textarea"
                          value={g.detail}
                          onChange={(e) => updateGuideline(i, { detail: e.target.value })}
                          rows={3}
                        />
                        <div className="row mt-2">
                          <Button variant="primary" size="sm" onClick={() => setEditing(null)}>Done</Button>
                          <Button variant="danger" size="sm" icon={<Icons.trash />} onClick={() => { removeGuideline(i); setEditing(null); }}>Delete</Button>
                        </div>
                      </>
                    ) : (
                      <>
                        <div style={{ fontWeight: 600, marginBottom: 4 }}>{g.title}</div>
                        <div style={{ fontSize: 13, color: "var(--text-2)", lineHeight: 1.6 }}>{g.detail}</div>
                      </>
                    )}
                  </div>
                  {editing?.index !== i && (
                    <button className="btn btn-ghost btn-icon btn-sm" onClick={() => setEditing({ type: "guideline", index: i })}>
                      <Icons.edit />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="col" style={{ gap: 16, position: "sticky", top: 20 }}>
            <Card title="How it works">
              <div style={{ fontSize: 13, color: "var(--text-2)", lineHeight: 1.6 }}>
                Every guideline you save is injected into the AI's system prompt before it writes a letter.
                Be specific — vague rules ("be professional") do nothing. Sharp rules ("never start with 'Dear'") change every letter.
              </div>
            </Card>

            <Card title="Battle-tested defaults">
              <div className="col" style={{ gap: 6, fontSize: 13 }}>
                {["Avg cover letter on Upwork: 312 words", "Letters under 150w get 2.4× more replies", "Replies that ask a question: 38% hire rate", "Top 10% writers always mirror client vocabulary"].map((s, i) => (
                  <div key={i} className="row" style={{ alignItems: "flex-start", gap: 8 }}>
                    <Icons.target size={12} style={{ color: "var(--accent-text)", marginTop: 4, flexShrink: 0 }} />
                    <span style={{ color: "var(--text-2)" }}>{s}</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      )}

      {tab === "examples" && (
        <div className="kb-grid">
          {kb.examples.map((e, i) => (
            <div key={i} className="kb-example-card">
              <div className="kb-example-header">
                <div>
                  <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>{e.title}</div>
                  <div className="kb-example-tags">
                    {e.tags.map((t) => <Badge key={t}>{t}</Badge>)}
                  </div>
                </div>
                <Badge variant="success" dot>{e.outcome}</Badge>
              </div>
              <div className="kb-example-snippet">{e.letter}</div>
              <div className="row mt-3" style={{ gap: 6 }}>
                <Button variant="ghost" size="sm" icon={<Icons.eye />}>View full</Button>
                <Button variant="ghost" size="sm" icon={<Icons.copy />}>Copy</Button>
                <Button variant="ghost" size="sm" icon={<Icons.edit />}>Edit</Button>
              </div>
            </div>
          ))}
          <div className="kb-example-card" style={{ borderStyle: "dashed", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: 200, color: "var(--text-3)", cursor: "pointer" }}>
            <Icons.plus size={24} />
            <div style={{ fontSize: 13, fontWeight: 500, marginTop: 8 }}>Add a winning letter</div>
            <div style={{ fontSize: 12, textAlign: "center", maxWidth: 200, marginTop: 4 }}>
              Save your best-performing letters as references for future jobs.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

window.KnowledgeBase = KnowledgeBase;
