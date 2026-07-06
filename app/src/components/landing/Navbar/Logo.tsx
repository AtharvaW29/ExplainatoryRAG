import Link from "next/link";

export function Logo() {
  return (
    <Link href="/" className="flex items-center gap-3 text-slate-900 transition hover:text-slate-700" aria-label="ExplainatoryRAG home">
      <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-lg font-semibold text-white">
        ER
      </div>
      <div>
        <p className="text-base font-semibold">ExplainatoryRAG</p>
        <p className="text-xs text-slate-500">Learning by explanation</p>
      </div>
    </Link>
  );
}
