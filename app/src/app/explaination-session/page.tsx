"use client";
import { SearchBar } from "@/components/chat";

export default function Page() {
  return (
    <div className="mx-auto flex min-h-full w-full max-w-3xl flex-col px-4 pb-6">
      <div className="flex-1 py-6">
        <p className="mt-20 text-center text-zinc-400">
          How can I help you today?
        </p>
      </div>

      <div className="sticky bottom-0 bg-white py-4 dark:bg-[#212121]">
        <SearchBar
          placeholder="Type your message..."
          onSendMessage={(message) => console.log(message)}
        />
      </div>
    </div>
  );
}
