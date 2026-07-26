// app/chat/ChatShell.tsx

"use client";

import React, { useState } from "react";
import { PanelLeftClose, PanelLeft } from "lucide-react";

interface ChatShellProps {
  children: React.ReactNode;
}

export function ChatShell({ children }: ChatShellProps) {
  const [isDesktopSidebarOpen, setIsDesktopSidebarOpen] = useState(false);

  return (
    <div className="flex h-dvh w-full overflow-hidden bg-white text-zinc-900 antialiased dark:bg-[#212121] dark:text-zinc-100">
      <aside
        className={[
          "hidden h-full shrink-0 flex-col overflow-hidden",
          "border-r border-zinc-200/50 bg-zinc-50",
          "transition-[width] duration-300 ease-in-out",
          "dark:border-zinc-800/50 dark:bg-[#171717]",
          "md:flex",
          isDesktopSidebarOpen ? "w-[260px]" : "w-0",
        ].join(" ")}
      >
        <div
          id="sidebar-target"
          className="min-w-[260px] flex-1 overflow-y-auto"
        >
          {/* Sidebar content */}
        </div>
      </aside>

      <div className="relative flex min-w-0 flex-1 flex-col overflow-hidden">
        <header className="flex h-14 shrink-0 items-center justify-between px-4 md:h-16">
          <button
            type="button"
            onClick={() => setIsDesktopSidebarOpen((open) => !open)}
            className="hidden rounded-lg p-2 text-zinc-400 transition-colors hover:bg-zinc-100 hover:text-zinc-600 dark:hover:bg-[#2f2f2f] dark:hover:text-zinc-200 md:flex"
            aria-label={
              isDesktopSidebarOpen ? "Close sidebar" : "Open sidebar"
            }
            aria-expanded={isDesktopSidebarOpen}
          >
            {isDesktopSidebarOpen ? (
              <PanelLeftClose className="h-5 w-5" />
            ) : (
              <PanelLeft className="h-5 w-5" />
            )}
          </button>

          <div className="rounded-xl px-3 py-1.5 text-sm font-semibold text-zinc-500 transition-colors hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-[#2f2f2f]">
            Explanatory GPT Sol 5.6
          </div>

          <div className="h-9 w-9" aria-hidden="true" />
        </header>

        <main className="min-h-0 flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
