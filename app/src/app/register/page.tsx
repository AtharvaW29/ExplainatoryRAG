"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setSubmitting(true);

    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });

    setSubmitting(false);

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      setError(data.error || data.message || "Registration failed. Please try again.");
      return;
    }

    router.push("/login");
  }

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-16 sm:px-8 lg:px-10">
      <section className="mx-auto max-w-2xl">
        <div className="rounded-3xl border border-slate-200 bg-white p-10 shadow-sm">
          <div className="space-y-3 mb-8">
            <p className="text-3xl font-semibold text-slate-950">Create your account</p>
            <p className="text-sm text-slate-600">
              Register and start using ExplainatoryRAG to track learning sessions and concepts.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="Full name"
              type="text"
              name="name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              required
            />

            <Input
              label="Email address"
              type="email"
              name="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              autoComplete="email"
              required
            />

            <Input
              label="Password"
              type="password"
              name="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete="new-password"
              required
            />

            {error ? (
              <p role="alert" className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </p>
            ) : null}

            <Button type="submit" className="w-full" disabled={submitting}>
              {submitting ? "Creating account…" : "Create account"}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-slate-600">
            Already have an account?{' '}
            <Link href="/login" className="font-semibold text-indigo-600 hover:text-indigo-700">
              Sign in here.
            </Link>
          </p>
        </div>
      </section>
    </main>
  );
}
