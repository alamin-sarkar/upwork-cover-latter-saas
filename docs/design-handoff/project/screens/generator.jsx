/* PitchCraft — Generator (main feature) */

const TONES = [
  { id: "confident", emoji: "💪", name: "Confident", desc: "Direct, sharp, evidence-led" },
  { id: "friendly", emoji: "👋", name: "Friendly", desc: "Warm, conversational" },
  { id: "formal", emoji: "🎩", name: "Formal", desc: "Polished, corporate" },
  { id: "casual", emoji: "🤙", name: "Casual", desc: "Short, breezy, human" },
];

const LENGTHS = [
  { id: "short", label: "Short (~80w)" },
  { id: "medium", label: "Medium (~140w)" },
  { id: "long", label: "Long (~200w)" },
];

function Generator({ user, onSave, layout = "split" }) {
  const [jobText, setJobText] = useState(window.SAMPLE_JOB);
  const [tone, setTone] = useState("confident");
  const [length, setLength] = useState("medium");
  const [analysis, setAnalysis] = useState(null);
  const [letter, setLetter] = useState("");
  const [questions, setQuestions] = useState([]);
  const [matchScore, setMatchScore] = useState(null);
  const [matchReason, setMatchReason] = useState("");
  const [loading, setLoading] = useState(false);
  const [phase, setPhase] = useState("idle"); // idle | analyzing | writing | done
  const [toast, setToast] = useState("");
  const [variants, setVariants] = useState([]);
  const [selectedVariant, setSelectedVariant] = useState(0);

  const runFullFlow = async () => {
    if (!jobText.trim()) return;
    setLoading(true);
    setPhase("analyzing");
    setAnalysis(null);
    setLetter("");
    setQuestions([]);
    setMatchScore(null);

    try {
      // Single AI call returns structured data
      const profile = JSON.stringify({
        name: user.name,
        title: user.title,
        about: user.about,
        skills: user.skills.map((s) => `${s.name} (${s.level})`),
        projects: user.projects.map((p) => `${p.title}: ${p.tagline}. ${p.outcome ? "Outcome: " + p.outcome : ""}`),
        experience: user.experience.map((e) => `${e.role} at ${e.company} (${e.period})`),
        tonePrefs: user.tonePrefs,
      });

      const prompt = `You are an expert Upwork cover letter coach. Analyze the job and write a tailored cover letter.

USER PROFILE:
${profile}

JOB POST:
"""
${jobText}
"""

TASK: Reply with ONLY a valid JSON object (no markdown fence, no commentary). Schema:
{
  "jobTitle": "short job title (max 12 words)",
  "keyRequirements": ["3-5 bullet points of must-have requirements"],
  "clientSignals": ["2-3 read-between-lines insights about this client — what they actually care about, urgency, red flags, decision criteria"],
  "budgetType": "fixed/hourly/range",
  "matchScore": 0-100 integer based on how well this user's profile fits,
  "matchReason": "one sentence explaining the score and the single strongest selling point for this user",
  "letter": "the cover letter, ${length} length (~${length === "short" ? 80 : length === "long" ? 200 : 140} words), in a ${tone} tone, following these rules: lead with a specific observation from the job (NOT a greeting), drop one concrete piece of proof from the user's portfolio with a number, mirror the client's vocabulary, end with a sharp clarifying question. Sign as '${user.tonePrefs.signature || "— " + user.name.split(" ")[0]}'. DO NOT start with 'Dear', 'Hello', 'I am writing', or 'I hope this finds you well'.",
  "suggestedQuestions": ["2-3 sharp clarifying questions the user could ask the client to seem senior"]
}`;

      const result = await window.claude.complete(prompt);
      const cleaned = result.replace(/^```json\s*/i, "").replace(/```\s*$/, "").trim();
      const data = JSON.parse(cleaned);

      setAnalysis({
        jobTitle: data.jobTitle,
        keyRequirements: data.keyRequirements || [],
        clientSignals: data.clientSignals || [],
        budgetType: data.budgetType,
      });
      setMatchScore(data.matchScore || 0);
      setMatchReason(data.matchReason || "");
      setPhase("writing");

      // animate letter typing
      const full = data.letter || "";
      setLetter("");
      let i = 0;
      const chunk = Math.max(4, Math.floor(full.length / 80));
      const interval = setInterval(() => {
        i = Math.min(i + chunk, full.length);
        setLetter(full.slice(0, i));
        if (i >= full.length) {
          clearInterval(interval);
          setQuestions(data.suggestedQuestions || []);
          setPhase("done");
          setLoading(false);
        }
      }, 28);
    } catch (e) {
      console.error(e);
      setToast("Generation failed. Please try again.");
      setLoading(false);
      setPhase("idle");
    }
  };

  const regenerate = () => runFullFlow();

  const copyLetter = () => {
    navigator.clipboard?.writeText(letter);
    setToast("Letter copied to clipboard");
  };

  const wordCount = letter.trim().split(/\s+/).filter(Boolean).length;
  const charCount = letter.length;

  const useCardsLayout = layout === "cards";
  const useSingleLayout = layout === "single";

  return (
    <div className="page">
      <PageHeader
        title="Cover letter generator"
        subtitle="Paste an Upwork job. PitchCraft analyzes it, scores the fit, and writes a tailored pitch in your voice."
        action={
          <div className="row">
            <Button variant="ghost" size="sm" icon={<Icons.bookmark />}>Save template</Button>
            <Button variant="secondary" size="sm" icon={<Icons.refresh />} onClick={regenerate} disabled={!letter || loading}>
              Regenerate
            </Button>
          </div>
        }
      />

      <div className={`gen-stage layout-${layout}`}>
        {/* LEFT — Job input + analysis */}
        <div className="col" style={{ gap: 16 }}>
          <div className="gen-panel">
            <div className="gen-panel-header">
              <div className="gen-panel-title">
                <div className="gen-panel-title-icon"><Icons.briefcase /></div>
                Upwork job description
              </div>
              <div className="row">
                <Badge>{jobText.trim().split(/\s+/).filter(Boolean).length} words</Badge>
                <Button variant="ghost" size="sm" onClick={() => setJobText("")}>Clear</Button>
              </div>
            </div>
            <div className="gen-panel-body">
              <textarea
                className="gen-job-input"
                value={jobText}
                onChange={(e) => setJobText(e.target.value)}
                placeholder="Paste the Upwork job description here…"
                style={{ width: "100%" }}
              />

              {/* Controls */}
              <div className="mt-4">
                <label className="label">Tone</label>
                <div className="tone-grid">
                  {TONES.map((t) => (
                    <div key={t.id} className={`tone-card ${tone === t.id ? "active" : ""}`} onClick={() => setTone(t.id)}>
                      <span className="tone-card-emoji">{t.emoji}</span>
                      <div className="tone-card-name">{t.name}</div>
                      <div className="tone-card-desc">{t.desc}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="row mt-4" style={{ justifyContent: "space-between" }}>
                <div>
                  <label className="label">Length</label>
                  <Segmented value={length} options={LENGTHS.map((l) => ({ value: l.id, label: l.label }))} onChange={setLength} />
                </div>
                <Button variant="primary" size="lg" icon={loading ? null : <Icons.wand />} loading={loading} onClick={runFullFlow} disabled={!jobText.trim()}>
                  {phase === "analyzing" ? "Analyzing job…" : phase === "writing" ? "Writing letter…" : "Analyze & Generate"}
                </Button>
              </div>
            </div>
          </div>

          {/* Analysis result */}
          {(analysis || phase === "analyzing") && (
            <div className="gen-panel">
              <div className="gen-panel-header">
                <div className="gen-panel-title">
                  <div className="gen-panel-title-icon"><Icons.target /></div>
                  Job analysis
                </div>
                {analysis && <Badge variant="info">{analysis.budgetType}</Badge>}
              </div>
              <div className="gen-panel-body">
                {!analysis && (
                  <div className="col" style={{ gap: 10 }}>
                    <div className="shimmer" style={{ height: 14, width: "70%" }} />
                    <div className="shimmer" style={{ height: 14, width: "90%" }} />
                    <div className="shimmer" style={{ height: 14, width: "55%" }} />
                  </div>
                )}
                {analysis && (
                  <>
                    {matchScore !== null && (
                      <div className="match-score-card mb-4">
                        <MatchRing score={matchScore} />
                        <div>
                          <div className="match-score-label">Match score</div>
                          <div className="match-score-text">{matchReason}</div>
                        </div>
                      </div>
                    )}

                    <div style={{ fontSize: 11, color: "var(--text-3)", textTransform: "uppercase", letterSpacing: "0.06em", fontWeight: 600, marginBottom: 8 }}>
                      Key requirements
                    </div>
                    <div className="col" style={{ gap: 6, marginBottom: 16 }}>
                      {analysis.keyRequirements.map((r, i) => (
                        <div key={i} className="row" style={{ alignItems: "flex-start", gap: 8, fontSize: 13 }}>
                          <Icons.check size={14} style={{ color: "var(--accent-text)", marginTop: 2, flexShrink: 0 }} />
                          <span>{r}</span>
                        </div>
                      ))}
                    </div>

                    <div style={{ fontSize: 11, color: "var(--text-3)", textTransform: "uppercase", letterSpacing: "0.06em", fontWeight: 600, marginBottom: 8 }}>
                      Client signals
                    </div>
                    <div className="col" style={{ gap: 6 }}>
                      {analysis.clientSignals.map((r, i) => (
                        <div key={i} className="row" style={{ alignItems: "flex-start", gap: 8, fontSize: 13 }}>
                          <Icons.eye size={14} style={{ color: "var(--info)", marginTop: 2, flexShrink: 0 }} />
                          <span>{r}</span>
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>
            </div>
          )}
        </div>

        {/* RIGHT — Letter output */}
        <div className="col" style={{ gap: 16 }}>
          <div className="gen-panel">
            <div className="gen-panel-header">
              <div className="gen-panel-title">
                <div className="gen-panel-title-icon"><Icons.send /></div>
                Your cover letter
              </div>
              <div className="row">
                {letter && <Badge>{wordCount}w · {charCount}c</Badge>}
                {letter && <Button variant="ghost" size="sm" icon={<Icons.refresh />} onClick={regenerate}>Regenerate</Button>}
                {letter && <Button variant="secondary" size="sm" icon={<Icons.copy />} onClick={copyLetter}>Copy</Button>}
                {letter && <Button variant="ghost" size="sm" icon={<Icons.download />} title="Download as .txt"></Button>}
              </div>
            </div>
            <div className="gen-panel-body">
              {!letter && phase === "idle" && (
                <EmptyState
                  icon={<Icons.wand />}
                  title="Your letter will appear here"
                  text="Paste a job description on the left, pick a tone, and hit Analyze & Generate."
                />
              )}
              {!letter && (phase === "analyzing" || phase === "writing") && (
                <div className="col" style={{ gap: 8, padding: "8px 4px" }}>
                  <div className="shimmer" style={{ height: 14, width: "85%" }} />
                  <div className="shimmer" style={{ height: 14, width: "95%" }} />
                  <div className="shimmer" style={{ height: 14, width: "70%" }} />
                  <div className="shimmer" style={{ height: 14, width: "80%" }} />
                  <div className="shimmer" style={{ height: 14, width: "60%" }} />
                  <div className="shimmer" style={{ height: 14, width: "92%" }} />
                  <div style={{ marginTop: 8, fontSize: 12.5, color: "var(--text-3)" }} className="row">
                    <div className="spinner" />
                    {phase === "analyzing" ? "Reading job description, scoring fit…" : "Drafting in your voice…"}
                  </div>
                </div>
              )}
              {letter && (
                <div className="letter-output">
                  {letter}
                  {phase === "writing" && <span style={{ opacity: 0.5 }}>▋</span>}
                </div>
              )}
            </div>
          </div>

          {/* Suggested questions */}
          {questions.length > 0 && (
            <div className="gen-panel">
              <div className="gen-panel-header">
                <div className="gen-panel-title">
                  <div className="gen-panel-title-icon"><Icons.message /></div>
                  Ask the client
                </div>
                <Badge variant="accent">Senior move</Badge>
              </div>
              <div className="gen-panel-body">
                <p style={{ margin: "0 0 10px", fontSize: 12.5, color: "var(--text-2)" }}>
                  Sharp questions make you look senior and almost guarantee a reply.
                </p>
                {questions.map((q, i) => (
                  <div key={i} className="sq-item">
                    <div className="sq-num">{i + 1}</div>
                    <div>{q}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {phase === "done" && (
            <div className="row" style={{ justifyContent: "flex-end", gap: 8 }}>
              <Button variant="ghost" size="sm" icon={<Icons.bookmark />}>Save as template</Button>
              <Button variant="secondary" size="sm" icon={<Icons.edit />}>Edit & polish</Button>
              <Button variant="primary" size="sm" icon={<Icons.checkCircle />} onClick={() => { onSave({ jobText, letter, analysis, matchScore, tone }); setToast("Saved to history"); }}>
                Save to history
              </Button>
            </div>
          )}
        </div>
      </div>

      <Toast message={toast} onDone={() => setToast("")} />
    </div>
  );
}

window.Generator = Generator;
