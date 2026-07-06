import Link from "next/link";
import { LoginForm } from "./LoginForm";

export default function LoginPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-16 sm:px-8 lg:px-10">
      <section className="mx-auto max-w-2xl">
        <div className="mb-10 rounded-3xl border border-slate-200 bg-white p-10 shadow-sm">
          <LoginForm />
          <div className="mt-6 text-center text-sm text-slate-600">
            Don&apos;t have an account?{' '}
            <Link href="/register" className="font-semibold text-indigo-600 hover:text-indigo-700">
              Create one here.
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
