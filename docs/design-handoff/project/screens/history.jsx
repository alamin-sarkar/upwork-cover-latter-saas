/* PitchCraft — History */

const STATUS_FILTERS = [
  { id: "all", label: "All" },
  { id: "draft", label: "Drafts" },
  { id: "sent", label: "Sent" },
  { id: "replied", label: "Replied" },
  { id: "hired", label: "Hired" },
  { id: "no-reply", label: "No reply" },
];

const STATUS_META = {
  sent: { label: "Sent", variant: "info" },
  replied: { label: "Replied", variant: "success" },
  hired: { label: "Hired ★", variant: "success" },
  draft: { label: "Draft", variant: "warning" },
  "no-reply": { label: "No reply", variant: "default" },
};

function History({ history, onView }) {
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);
  const [sortBy, setSortBy] = useState("date");

  const filtered = useMemo(() => {
    let list = history;
    if (filter !== "all") list = list.filter((h) => h.status === filter);
    if (search.trim()) {
      const q = search.toLowerCase();
      list = list.filter(
        (h) =>
          h.jobTitle.toLowerCase().includes(q) ||
          h.client.toLowerCase().includes(q) ||
          h.preview.toLowerCase().includes(q)
      );
    }
    if (sortBy === "score") list = [...list].sort((a, b) => b.matchScore - a.matchScore);
    if (sortBy === "date") list = [...list].sort((a, b) => b.date.localeCompare(a.date));
    return list;
  }, [history, filter, search, sortBy]);

  return (
    <div className="page">
      <PageHeader
        title="History"
        subtitle={`${history.length} cover letters · ${history.filter((h) => h.status === "hired").length} hires · ${Math.round((history.filter((h) => h.status === "replied" || h.status === "hired").length / Math.max(history.length, 1)) * 100)}% reply rate`}
        action={
          <div className="row">
            <Button variant="ghost" size="sm" icon={<Icons.download />}>Export CSV</Button>
            <Button variant="primary" size="sm" icon={<Icons.plus />}>New letter</Button>
          </div>
        }
      />

      {/* Filter bar */}
      <div className="card-bare mb-4">
        <div style={{ padding: "12px 16px", display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
          <div className="row" style={{ gap: 8, flex: 1, minWidth: 240 }}>
            <Icons.search size={14} style={{ color: "var(--text-3)" }} />
            <input
              className="input"
              placeholder="Search by client, job title, content…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ background: "transparent", border: "none", padding: 0, fontSize: 13 }}
            />
          </div>
          <div className="row" style={{ gap: 4 }}>
            {STATUS_FILTERS.map((s) => (
              <button
                key={s.id}
                className={`chip ${filter === s.id ? "active" : ""}`}
                onClick={() => setFilter(s.id)}
              >
                {s.label}
                {s.id !== "all" && (
                  <span style={{ marginLeft: 4, opacity: 0.6, fontSize: 11 }}>
                    {history.filter((h) => h.status === s.id).length}
                  </span>
                )}
              </button>
            ))}
          </div>
          <Segmented
            value={sortBy}
            options={[{ value: "date", label: "Newest" }, { value: "score", label: "Score" }]}
            onChange={setSortBy}
          />
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: selected ? "1fr 480px" : "1fr", gap: 20, alignItems: "start" }}>
        {/* List */}
        <div className="card-bare pad-0">
          <div style={{ display: "grid", gridTemplateColumns: "1fr 130px 100px 90px 36px", gap: 12, padding: "10px 18px", borderBottom: "1px solid var(--border)", fontSize: 11, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--text-3)" }}>
            <div>Job & Client</div>
            <div>Match</div>
            <div>Status</div>
            <div>Date</div>
            <div></div>
          </div>
          {filtered.length === 0 && (
            <EmptyState
              icon={<Icons.history />}
              title="No letters match"
              text="Try a different filter or search term."
            />
          )}
          {filtered.map((h) => (
            <div
              key={h.id}
              className="history-row"
              onClick={() => setSelected(h)}
              style={selected?.id === h.id ? { background: "var(--surface-2)" } : {}}
            >
              <div style={{ minWidth: 0 }}>
                <div className="history-job-title truncate">{h.jobTitle}</div>
                <div className="history-meta">
                  <Avatar initials={h.client.slice(0, 2).toUpperCase()} size={null} className="avatar" />
                  <span>{h.client}</span>
                  <span>·</span>
                  <span>{h.clientCountry}</span>
                  <span>·</span>
                  <span style={{ color: "var(--text-2)" }}>{h.budget}</span>
                </div>
              </div>
              <div className="row" style={{ gap: 8 }}>
                <div style={{ width: 28, height: 28 }}>
                  <MatchRing score={h.matchScore} size={28} />
                </div>
                <span style={{ fontSize: 12.5, color: "var(--text-2)" }}>{h.matchScore}</span>
              </div>
              <Badge variant={STATUS_META[h.status].variant} dot>{STATUS_META[h.status].label}</Badge>
              <div style={{ fontSize: 12, color: "var(--text-3)" }}>{h.date.slice(5)}</div>
              <button className="btn btn-ghost btn-icon btn-sm" onClick={(e) => e.stopPropagation()}>
                <Icons.more />
              </button>
            </div>
          ))}
        </div>

        {/* Detail panel */}
        {selected && (
          <div className="card-bare pad-0" style={{ position: "sticky", top: 20 }}>
            <div className="card-header">
              <h3 className="card-title">Letter details</h3>
              <button className="btn btn-ghost btn-icon btn-sm" onClick={() => setSelected(null)}>
                <Icons.x />
              </button>
            </div>
            <div className="card-body">
              <div style={{ fontSize: 11, color: "var(--text-3)", textTransform: "uppercase", letterSpacing: "0.06em", fontWeight: 600, marginBottom: 6 }}>
                Job
              </div>
              <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 4 }}>{selected.jobTitle}</div>
              <div style={{ fontSize: 12.5, color: "var(--text-2)", marginBottom: 16 }}>
                {selected.client} · {selected.clientCountry} · {selected.budget}
              </div>

              <div className="grid-2 mb-4">
                <div>
                  <div style={{ fontSize: 11, color: "var(--text-3)", textTransform: "uppercase", letterSpacing: "0.06em", fontWeight: 600, marginBottom: 6 }}>Match</div>
                  <div className="row">
                    <MatchRing score={selected.matchScore} size={36} />
                    <span style={{ fontWeight: 600 }}>{selected.matchScore}/100</span>
                  </div>
                </div>
                <div>
                  <div style={{ fontSize: 11, color: "var(--text-3)", textTransform: "uppercase", letterSpacing: "0.06em", fontWeight: 600, marginBottom: 6 }}>Tone</div>
                  <Badge>{selected.tone}</Badge>
                </div>
              </div>

              <div style={{ fontSize: 11, color: "var(--text-3)", textTransform: "uppercase", letterSpacing: "0.06em", fontWeight: 600, marginBottom: 6 }}>
                Letter
              </div>
              <div className="letter-output" style={{ minHeight: 0, padding: 14, fontSize: 13 }}>
                {selected.preview}
              </div>

              <div className="row mt-4" style={{ gap: 6 }}>
                <Button variant="secondary" size="sm" icon={<Icons.copy />}>Copy</Button>
                <Button variant="ghost" size="sm" icon={<Icons.refresh />}>Re-generate</Button>
                <Button variant="ghost" size="sm" icon={<Icons.bookmark />}>Template</Button>
                <Button variant="danger" size="sm" icon={<Icons.trash />}></Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

window.History = History;
