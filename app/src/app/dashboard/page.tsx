import { apiFetch } from "@/lib/api";

interface ExplanationSession {
  id: string;
  topic: string;
  created_at: string;
}

async function createSession(formData: FormData) {
  "use server";
  const topic = formData.get("topic");
  await apiFetch("/explanation_sessions", {
    method: "POST",
    body: JSON.stringify({ topic }),
  });
}

export default async function DashboardPage() {
  const res = await apiFetch("/explanation_sessions");
  const sessions: ExplanationSession[] = res.ok ? await res.json() : [];

  return (
    <div>
      <h1>Your explanation sessions</h1>
      <form action={createSession}>
        <input name="topic" placeholder="Topic, e.g. Backpropagation" required />
        <button type="submit">Start session</button>
      </form>
      <ul>
        {sessions.map((session) => (
          <li key={session.id}>{session.topic}</li>
        ))}
      </ul>
    </div>
  );
}
