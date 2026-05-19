/* PitchCraft — Auth screen */

function AuthScreen({ onSignIn }) {
  const [mode, setMode] = useState("signin");
  const [email, setEmail] = useState("rakib.hasan@gmail.com");
  const [password, setPassword] = useState("••••••••••");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => onSignIn(), 600);
  };

  return (
    <div className="auth-stage">
      <div className="auth-side">
        <div className="auth-glow" />
        <div className="row" style={{ position: "relative", zIndex: 1 }}>
          <div className="sidebar-brand-mark">P</div>
          <div>
            <div className="sidebar-brand-name">PitchCraft</div>
            <div style={{ fontSize: 11, color: "var(--text-3)" }}>AI cover letters for Upwork</div>
          </div>
        </div>

        <div className="auth-quote">
          <div className="auth-quote-mark">"</div>
          <div className="auth-quote-text">
            I went from 4% reply rate to 31% in three weeks.
            The AI doesn't just write — it reads the job and figures out which of my projects to lead with.
          </div>
          <div className="auth-quote-author">
            <Avatar initials="JK" size="md" />
            <div>
              <div style={{ color: "var(--text-1)", fontWeight: 500 }}>Jonah K.</div>
              <div>Full-stack dev, Top Rated Plus · Upwork</div>
            </div>
          </div>

          <div className="auth-stat-strip">
            <div className="stat">
              <div className="stat-value">24K+</div>
              <div className="stat-label">Letters sent</div>
            </div>
            <div className="stat">
              <div className="stat-value">3.2×</div>
              <div className="stat-label">Avg reply lift</div>
            </div>
            <div className="stat">
              <div className="stat-value">$1.4M</div>
              <div className="stat-label">Earned via PitchCraft</div>
            </div>
          </div>
        </div>

        <div style={{ position: "relative", zIndex: 1, fontSize: 12, color: "var(--text-3)" }}>
          © 2026 PitchCraft Labs · <a style={{ color: "var(--text-2)" }} href="#">Privacy</a> · <a style={{ color: "var(--text-2)" }} href="#">Terms</a>
        </div>
      </div>

      <div className="auth-form-side">
        <div className="auth-form-card">
          <div className="auth-tab-toggle">
            <button className={mode === "signin" ? "active" : ""} onClick={() => setMode("signin")}>Sign in</button>
            <button className={mode === "signup" ? "active" : ""} onClick={() => setMode("signup")}>Create account</button>
          </div>

          <h1>{mode === "signin" ? "Welcome back" : "Start winning jobs"}</h1>
          <p>{mode === "signin" ? "Sign in to your PitchCraft workspace." : "Free for your first 5 letters. No card required."}</p>

          <Button variant="secondary" style={{ width: "100%", padding: 10 }} icon={<Icons.google />}>
            Continue with Google
          </Button>

          <div className="auth-divider">or with email</div>

          <form onSubmit={submit}>
            {mode === "signup" && (
              <div className="field">
                <label className="label">Full name</label>
                <input className="input" placeholder="Your full name" value={name} onChange={(e) => setName(e.target.value)} />
              </div>
            )}
            <div className="field">
              <label className="label">Email</label>
              <input className="input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <div className="field">
              <div className="between" style={{ marginBottom: 6 }}>
                <label className="label" style={{ marginBottom: 0 }}>Password</label>
                {mode === "signin" && <a href="#" style={{ fontSize: 12, color: "var(--accent-text)" }}>Forgot?</a>}
              </div>
              <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </div>

            <Button variant="primary" size="lg" style={{ width: "100%" }} loading={loading} type="submit">
              {mode === "signin" ? "Sign in" : "Create account"}
              {!loading && <Icons.arrowRight size={14} />}
            </Button>
          </form>

          <div style={{ marginTop: 18, fontSize: 12.5, color: "var(--text-3)", textAlign: "center" }}>
            {mode === "signin" ? "New here?" : "Already have an account?"}{" "}
            <a href="#" onClick={(e) => { e.preventDefault(); setMode(mode === "signin" ? "signup" : "signin"); }} style={{ color: "var(--accent-text)" }}>
              {mode === "signin" ? "Create an account" : "Sign in"}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

window.AuthScreen = AuthScreen;
