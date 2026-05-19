import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 px-4 py-16">
      <div className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-slate-900">Interview Copilot</h1>
        <p className="mt-3 text-slate-600">
          AI-powered CV↔JD matching and mock interview practice platform.
        </p>

        <div className="mt-8 flex gap-3">
          <Link href="/login" className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700">
            Login
          </Link>
          <Link href="/register" className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100">
            Register
          </Link>
        </div>
      </div>
    </main>
  );
}
