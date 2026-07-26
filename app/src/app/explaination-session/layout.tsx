import { redirect } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { getSessionToken } from "@/lib/session";
import { ChatShell } from "./ChatShell";

interface ChatLayoutProps {
  children: React.ReactNode;
}

export default async function ChatLayout({
  children,
}: ChatLayoutProps) {
  const token = await getSessionToken();

  if (!token) {
    redirect("/login");
  }

  const res = await apiFetch("/auth/me");

  if (!res.ok) {
    redirect("/login");
  }

  return <ChatShell>{children}</ChatShell>;
}
