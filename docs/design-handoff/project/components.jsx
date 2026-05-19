/* PitchCraft — Shared UI components + Sidebar + Topbar */

const { useState, useEffect, useRef, useMemo, useCallback } = React;

// ===== Button =====
function Button({ children, variant = "secondary", size, icon, iconRight, loading, ...rest }) {
  const classes = ["btn", `btn-${variant}`];
  if (size) classes.push(`btn-${size}`);
  return (
    <button className={classes.join(" ")} disabled={loading || rest.disabled} {...rest}>
      {loading ? <span className="spinner"></span> : icon}
      {children && <span>{children}</span>}
      {iconRight}
    </button>
  );
}

// ===== Badge =====
function Badge({ children, variant = "default", dot }) {
  const className = variant === "default" ? "badge" : `badge badge-${variant}`;
  return (
    <span className={className}>
      {dot && <span className="badge-dot" />}
      {children}
    </span>
  );
}

// ===== Avatar =====
function Avatar({ initials, size, className }) {
  const c = ["avatar", size && `avatar-${size}`, className].filter(Boolean).join(" ");
  return <div className={c}>{initials}</div>;
}

// ===== Card =====
function Card({ title, action, children, className = "" }) {
  if (!title) return <div className={`card ${className}`}>{children}</div>;
  return (
    <div className={`card-bare ${className}`}>
      <div className="card-header">
        <h3 className="card-title">{title}</h3>
        {action}
      </div>
      <div className="card-body">{children}</div>
    </div>
  );
}

// ===== Switch =====
function Switch({ checked, onChange }) {
  return <div className={`switch ${checked ? "on" : ""}`} onClick={() => onChange(!checked)} />;
}

// ===== Segmented =====
function Segmented({ value, options, onChange }) {
  return (
    <div className="segmented">
      {options.map((o) => {
        const v = typeof o === "string" ? o : o.value;
        const label = typeof o === "string" ? o : o.label;
        return (
          <div
            key={v}
            className={`segmented-item ${value === v ? "active" : ""}`}
            onClick={() => onChange(v)}
          >
            {label}
          </div>
        );
      })}
    </div>
  );
}

// ===== Chip =====
function Chip({ children, active, onClick, onRemove }) {
  return (
    <span className={`chip ${active ? "active" : ""}`} onClick={onClick}>
      {children}
      {onRemove && (
        <span className="chip-remove" onClick={(e) => { e.stopPropagation(); onRemove(); }}>
          <Icons.x size={10} />
        </span>
      )}
    </span>
  );
}

// ===== Match score ring =====
function MatchRing({ score, size = 56 }) {
  const r = (size - 8) / 2;
  const c = 2 * Math.PI * r;
  const offset = c - (score / 100) * c;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ transform: "rotate(-90deg)" }}>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="var(--surface-3)" strokeWidth="4" />
      <circle
        cx={size/2}
        cy={size/2}
        r={r}
        fill="none"
        stroke="var(--accent)"
        strokeWidth="4"
        strokeDasharray={c}
        strokeDashoffset={offset}
        strokeLinecap="round"
        style={{ transition: "stroke-dashoffset 0.6s ease" }}
      />
      <text
        x="50%" y="50%"
        textAnchor="middle"
        dominantBaseline="middle"
        fontSize={size * 0.32}
        fontWeight="600"
        fill="var(--text-1)"
        style={{ transform: "rotate(90deg)", transformOrigin: "center" }}
      >
        {Math.round(score)}
      </text>
    </svg>
  );
}

// ===== Toast =====
function Toast({ message, onDone }) {
  useEffect(() => {
    if (!message) return;
    const t = setTimeout(onDone, 2200);
    return () => clearTimeout(t);
  }, [message]);
  if (!message) return null;
  return (
    <div className="toast">
      <Icons.checkCircle size={16} />
      {message}
    </div>
  );
}

// ===== Sidebar =====
function Sidebar({ current, onNavigate, user, history, onLogout }) {
  const items = [
    { id: "dashboard", label: "Dashboard", icon: <Icons.dashboard /> },
    { id: "generator", label: "Generator", icon: <Icons.wand />, badge: "AI" },
    { id: "history", label: "History", icon: <Icons.history />, badge: history.length },
    { id: "knowledge", label: "Knowledge Base", icon: <Icons.book /> },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-brand-mark">P</div>
        <div>
          <div className="sidebar-brand-name">PitchCraft</div>
          <div style={{ fontSize: 11, color: "var(--text-3)" }}>AI cover letters</div>
        </div>
      </div>

      <div className="sidebar-section-label">Workspace</div>
      {items.map((i) => (
        <div key={i.id} className={`nav-item ${current === i.id ? "active" : ""}`} onClick={() => onNavigate(i.id)}>
          {i.icon}
          <span>{i.label}</span>
          {i.badge !== undefined && <span className="nav-item-badge">{i.badge}</span>}
        </div>
      ))}

      <div className="sidebar-section-label">Account</div>
      <div className={`nav-item ${current === "settings" ? "active" : ""}`} onClick={() => onNavigate("settings")}>
        <Icons.settings />
        <span>Settings</span>
      </div>

      <div className="sidebar-footer">
        <div className="sidebar-user" onClick={() => onNavigate("settings")}>
          <Avatar initials={user.initials} />
          <div style={{ minWidth: 0, flex: 1 }}>
            <div style={{ fontSize: 13, fontWeight: 500 }} className="truncate">{user.name}</div>
            <div style={{ fontSize: 11.5, color: "var(--text-3)" }} className="truncate">Pro plan</div>
          </div>
          <button className="btn-icon btn btn-ghost" onClick={(e) => { e.stopPropagation(); onLogout(); }} title="Sign out">
            <Icons.logout size={14} />
          </button>
        </div>
      </div>
    </aside>
  );
}

// ===== Topbar =====
function Topbar({ onNew, onSearchFocus, title }) {
  return (
    <div className="topbar">
      <div className="row" style={{ gap: 14 }}>
        <div className="search-input" onClick={onSearchFocus} style={{ cursor: "pointer" }}>
          <Icons.search />
          <span>Search jobs, letters, KB…</span>
          <kbd>⌘K</kbd>
        </div>
      </div>
      <div className="row" style={{ gap: 8 }}>
        <button className="btn btn-ghost btn-sm btn-icon" title="Notifications"><Icons.bell /></button>
        <button className="btn btn-primary btn-sm" onClick={onNew}>
          <Icons.plus /> New letter
        </button>
      </div>
    </div>
  );
}

// ===== PageHeader =====
function PageHeader({ title, subtitle, action }) {
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

// ===== Empty state =====
function EmptyState({ icon, title, text, action }) {
  return (
    <div className="empty">
      <div className="empty-icon">{icon}</div>
      <div className="empty-title">{title}</div>
      <div className="empty-text">{text}</div>
      {action && <div style={{ marginTop: 8 }}>{action}</div>}
    </div>
  );
}

// Expose
Object.assign(window, {
  Button, Badge, Avatar, Card, Switch, Segmented, Chip, MatchRing, Toast,
  Sidebar, Topbar, PageHeader, EmptyState,
});
