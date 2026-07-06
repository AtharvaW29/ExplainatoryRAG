"use client";

import { useState } from "react";
import Link from "next/link";

const items = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/dashboard/concepts", label: "Concepts" },
  { href: "/dashboard/graph", label: "Graph" },
  { href: "/login", label: "Login" },
];

export function MobileMenu() {
  const [open, setOpen] = useState(false);

  return (
    <div className="md:hidden">
      <button
        type="button"
        onClick={() => setOpen((current) => !current)}
        aria-expanded={open}
        aria-label="Toggle navigation menu"
        className="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 shadow-sm transition hover:border-slate-300"
      >
        <span aria-hidden="true">{open ? "✕" : "☰"}</span>
      </button>
      {open ? (
        <div className="mt-3 space-y-3 rounded-3xl border border-slate-200 bg-white p-4 shadow-lg">
          {items.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="block rounded-xl px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
              onClick={() => setOpen(false)}
            >
              {item.label}
            </Link>
          ))}
        </div>
      ) : null}
    </div>
  );
}
