import { redirect } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { getSessionToken } from "@/lib/session";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const token = await getSessionToken();
  if (!token) {
    redirect("/login");
  }

  const res = await apiFetch("/auth/me");
  if (!res.ok) {
    redirect("/login");
  }

  return <section>{children}</section>;
}
