/* PitchCraft — Dashboard */

function Dashboard({ user, history, onNavigate }) {
  const totalLetters = history.length;
  const replies = history.filter((h) => h.status === "replied" || h.status === "hired").length;
  const hired = history.filter((h) => h.status === "hired").length;
  const replyRate = Math.round((replies / Math.max(totalLetters, 1)) * 100);
  const avgScore = Math.round(history.reduce((s, h) => s + h.matchScore, 0) / Math.max(history.length, 1));

  const recent = history.slice(0, 4);
  const statusColors = {
    sent: "info", replied: "success", hired: "success", draft: "warning", "no-reply": "default",
  };
  const statusLabel = {
    sent: "Sent", replied: "Replied", hired: "Hired ★", draft: "Draft", "no-reply": "No reply",
  };

  return (
    <div className="page">
      <PageHeader
        title={`Welcome back, ${user.name.split(" ")[0]}`}
        subtitle="Here's how your pitches are performing this week."
        action={
          <Button variant="primary" icon={<Icons.wand />} onClick={() => onNavigate("generator")}>
            New cover letter
          </Button>
        }
      />

      {/* Stats */}
      <div className="grid-4" style={{ marginBottom: 28 }}>
        <Card>
          <div className="stat">
            <div className="stat-label">Letters this month</div>
            <div className="stat-value">{totalLetters}</div>
            <div className="stat-delta">
              <Icons.trending size={12} /> +{Math.floor(totalLetters / 2)} vs last week
            </div>
          </div>
        </Card>
        <Card>
          <div className="stat">
            <div className="stat-label">Reply rate</div>
            <div className="stat-value">{replyRate}%</div>
            <div className="progress mt-2"><div className="progress-bar" style={{ width: `${replyRate}%` }} /></div>
          </div>
        </Card>
        <Card>
          <div className="stat">
            <div className="stat-label">Hired</div>
            <div className="stat-value">{hired}</div>
            <div className="stat-delta">
              <Icons.dollar size={12} /> ~${(hired * 2400).toLocaleString()} earned
            </div>
          </div>
        </Card>
        <Card>
          <div className="stat">
            <div className="stat-label">Avg match score</div>
            <div className="stat-value">{avgScore}<span style={{ fontSize: 14, color: "var(--text-3)" }}>/100</span></div>
            <div className="stat-delta accent-text">
              <Icons.target size={12} /> Strong targeting
            </div>
          </div>
        </Card>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 320px", gap: 20 }}>
        {/* Quick start panel */}
        <Card className="pad-0">
          <div style={{ padding: 24, borderBottom: "1px solid var(--border)" }}>
            <div className="row" style={{ marginBottom: 6 }}>
              <Icons.zap size={16} style={{ color: "var(--accent-text)" }} />
              <div style={{ fontSize: 13, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--accent-text)" }}>
                Quick start
              </div>
            </div>
            <h2 style={{ margin: "0 0 6px", fontSize: 22, letterSpacing: "-0.02em" }}>
              Paste a job. Get a winning pitch in 12 seconds.
            </h2>
            <p style={{ margin: "0 0 16px", color: "var(--text-2)", fontSize: 14 }}>
              PitchCraft reads the job, pulls the right project from your portfolio, and writes in your voice.
            </p>
            <Button variant="primary" size="lg" icon={<Icons.wand />} onClick={() => onNavigate("generator")}>
              Open generator
              <Icons.arrowRight size={14} />
            </Button>
          </div>

          {/* Recent */}
          <div style={{ padding: 18 }}>
            <div className="between" style={{ marginBottom: 12 }}>
              <h3 className="card-title">Recent letters</h3>
              <Button variant="ghost" size="sm" onClick={() => onNavigate("history")}>
                View all <Icons.arrowRight size={12} />
              </Button>
            </div>
            <div>
              {recent.map((r) => (
                <div key={r.id} className="history-row" style={{ padding: "12px 4px", gridTemplateColumns: "1fr 110px 84px 90px 32px" }} onClick={() => onNavigate("history")}>
                  <div style={{ minWidth: 0 }}>
                    <div className="history-job-title truncate">{r.jobTitle}</div>
                    <div className="history-meta">
                      <span>{r.client}</span>
                      <span>·</span>
                      <span>{r.budget}</span>
                    </div>
                  </div>
                  <div className="row" style={{ gap: 6, color: "var(--accent-text)", fontSize: 12.5, fontWeight: 500 }}>
                    <Icons.target size={12} /> {r.matchScore}/100
                  </div>
                  <Badge variant={statusColors[r.status]} dot>{statusLabel[r.status]}</Badge>
                  <div style={{ fontSize: 12, color: "var(--text-3)" }}>{r.date.slice(5)}</div>
                  <button className="btn btn-ghost btn-icon btn-sm"><Icons.chevronRight /></button>
                </div>
              ))}
            </div>
          </div>
        </Card>

        {/* Side column */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <Card title="Your profile" action={<Button variant="ghost" size="sm" onClick={() => onNavigate("settings")}>Edit</Button>}>
            <div className="row" style={{ marginBottom: 14 }}>
              <Avatar initials={user.initials} size="lg" />
              <div>
                <div style={{ fontWeight: 600 }}>{user.name}</div>
                <div style={{ fontSize: 12.5, color: "var(--text-2)" }}>{user.title}</div>
                <div style={{ fontSize: 12, color: "var(--text-3)", marginTop: 2 }}>📍 {user.location}</div>
              </div>
            </div>
            <div className="divider" />
            <div className="col" style={{ gap: 8 }}>
              <div className="between">
                <span style={{ fontSize: 12.5, color: "var(--text-2)" }}>Profile completeness</span>
                <span style={{ fontSize: 12, fontWeight: 600 }} className="accent-text">92%</span>
              </div>
              <div className="progress"><div className="progress-bar" style={{ width: "92%" }} /></div>
              <div style={{ fontSize: 12, color: "var(--text-3)", marginTop: 2 }}>
                Add 1 client testimonial to reach 100%.
              </div>
            </div>
          </Card>

          <Card title="Tip of the day">
            <div className="row" style={{ alignItems: "flex-start", gap: 10 }}>
              <div style={{ width: 28, height: 28, borderRadius: 8, background: "var(--accent-soft)", color: "var(--accent-text)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                <Icons.info size={14} />
              </div>
              <div>
                <div style={{ fontWeight: 500, marginBottom: 4 }}>Mirror their words exactly</div>
                <div style={{ fontSize: 12.5, color: "var(--text-2)", lineHeight: 1.55 }}>
                  If the job says "RAG", say "RAG" — not "retrieval-augmented generation". Match terms 1:1; clients scan for keywords on the first read.
                </div>
                <Button variant="ghost" size="sm" style={{ padding: "4px 0", marginTop: 8 }} onClick={() => onNavigate("knowledge")}>
                  More guidelines <Icons.arrowRight size={11} />
                </Button>
              </div>
            </div>
          </Card>

          <Card title="Niches you're winning in">
            <div className="col" style={{ gap: 10 }}>
              {[
                { name: "AI / RAG systems", count: 4, win: 75 },
                { name: "React dashboards", count: 2, win: 50 },
                { name: "Cold email tools", count: 1, win: 100 },
              ].map((n) => (
                <div key={n.name}>
                  <div className="between" style={{ marginBottom: 5 }}>
                    <span style={{ fontSize: 13 }}>{n.name}</span>
                    <span style={{ fontSize: 12, color: "var(--text-3)" }}>{n.count} sent · {n.win}% reply</span>
                  </div>
                  <div className="progress"><div className="progress-bar" style={{ width: `${n.win}%` }} /></div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

window.Dashboard = Dashboard;
