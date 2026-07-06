interface OverviewCardProps {
  title: string;
  value: string;
  detail: string;
}

export function OverviewCard({ title, value, detail }: OverviewCardProps) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-semibold uppercase tracking-[0.26em] text-slate-500">{title}</p>
      <p className="mt-3 text-3xl font-semibold text-slate-950">{value}</p>
      <p className="mt-2 text-sm leading-6 text-slate-600">{detail}</p>
    </div>
  );
}
