/* PitchCraft — App root */

function App() {
  const [authed, setAuthed] = useState(true); // start logged-in for design review
  const [route, setRoute] = useState("dashboard");
  const [user, setUser] = useState(SAMPLE_USER);
  const [history, setHistory] = useState(SAMPLE_HISTORY);
  const [kb, setKb] = useState(SAMPLE_KB);

  // Tweaks
  const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
    "theme": "forest",
    "generatorLayout": "split",
    "density": "comfortable"
  }/*EDITMODE-END*/;
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  useEffect(() => {
    if (t.theme === "forest") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", t.theme);
  }, [t.theme]);

  const saveLetter = (data) => {
    const next = {
      id: "h-" + Date.now(),
      jobTitle: data.analysis?.jobTitle || "Untitled job",
      client: "New client",
      clientCountry: "—",
      budget: "—",
      date: new Date().toISOString().slice(0, 10),
      tone: data.tone.charAt(0).toUpperCase() + data.tone.slice(1),
      matchScore: data.matchScore,
      status: "draft",
      preview: data.letter,
    };
    setHistory((h) => [next, ...h]);
  };

  if (!authed) {
    return <AuthScreen onSignIn={() => { setAuthed(true); setRoute("dashboard"); }} />;
  }

  return (
    <>
      <div className="app" data-screen-label={`App / ${route}`}>
        <Sidebar
          current={route}
          onNavigate={setRoute}
          user={user}
          history={history}
          onLogout={() => setAuthed(false)}
        />
        <main className="app-main">
          <Topbar onNew={() => setRoute("generator")} onSearchFocus={() => {}} />
          {route === "dashboard" && <Dashboard user={user} history={history} onNavigate={setRoute} />}
          {route === "generator" && <Generator user={user} onSave={saveLetter} layout={t.generatorLayout} />}
          {route === "history" && <History history={history} />}
          {route === "knowledge" && <KnowledgeBase kb={kb} onUpdate={setKb} />}
          {route === "settings" && <Settings user={user} onUpdate={setUser} />}
        </main>
      </div>

      <TweaksPanel title="Tweaks">
        <TweakSection label="Color theme" />
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 6 }}>
          {[
            { id: "forest", color: "#14a800", label: "Forest" },
            { id: "midnight", color: "#38bdf8", label: "Midnight" },
            { id: "amber", color: "#f59e0b", label: "Amber" },
            { id: "violet", color: "#a855f7", label: "Violet" },
          ].map((th) => (
            <button
              key={th.id}
              onClick={() => setTweak("theme", th.id)}
              title={th.label}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 4,
                padding: "6px 4px",
                border: t.theme === th.id ? "1.5px solid #29261b" : "1px solid rgba(0,0,0,0.1)",
                background: t.theme === th.id ? "rgba(0,0,0,0.05)" : "transparent",
                borderRadius: 8,
                cursor: "pointer",
                fontSize: 10,
                color: "#29261b",
                fontWeight: 500,
              }}
            >
              <span style={{ width: 22, height: 22, borderRadius: 6, background: th.color, display: "block" }} />
              <span>{th.label}</span>
            </button>
          ))}
        </div>
        <TweakSection label="Generator layout" />
        <TweakRadio
          label="Layout"
          value={t.generatorLayout}
          options={["split", "single"]}
          onChange={(v) => setTweak("generatorLayout", v)}
        />
        <TweakSection label="Density" />
        <TweakRadio
          label="Spacing"
          value={t.density}
          options={["comfortable", "compact"]}
          onChange={(v) => setTweak("density", v)}
        />
      </TweaksPanel>
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
