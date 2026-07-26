"use client";

import { Message } from "./MessageStream";
import { MarkdownRenderer } from "./MarkdownRenderer";

import { Copy } from "lucide-react";

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
  };

  return (
    <div className={`w-full flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`flex gap-4 max-w-2xl w-full ${
          isUser
            ? "flex-row-reverse bg-zinc-100 dark:bg-[#2f2f2f] rounded-[20px] px-4 py-2.5 max-w-[70%]"
            : "items-start"
        }`}
      >
        {/* Avatar Ring Block for Assistant Responses Only */}
        {!isUser && (
          <div className="w-8 h-8 rounded-full border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 flex items-center justify-center text-sm shadow-sm shrink-0 select-none">
            🤖
          </div>
        )}

        <div className="flex-1 flex flex-col gap-1 min-w-0">
          <div className="text-[15px] leading-relaxed text-zinc-800 dark:text-zinc-100 whitespace-pre-wrap break-words">
            {
              isUser ?
              (<div className="whitespace-pre-wrap break-words">{message.content}</div>)
              :
              (<MarkdownRenderer content={message.content} />)
            }
          </div>

          {!isUser && (
            <div className="flex items-center gap-1 mt-2 opacity-0 group-hover:opacity-100 md:group-hover:opacity-100 transition-opacity">
              <button
                onClick={handleCopy}
                className="p-1.5 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 rounded-md hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                title="Copy message"
              >
                <Copy className="h-3.5 w-3.5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
