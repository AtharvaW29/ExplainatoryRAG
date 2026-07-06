import Link from "next/link";

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/dashboard/concepts", label: "Concepts" },
  { href: "/dashboard/graph", label: "Graph" },
  { href: "/login", label: "Login" },
];

export function Navigation() {
  return (
    <nav aria-label="Primary navigation" className="hidden items-center gap-8 md:flex">
      {navItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
