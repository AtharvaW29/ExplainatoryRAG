"use client";

import React, { useRef, useEffect, useState } from "react";
import { ArrowDown } from "lucide-react";
import { MessageBubble } from "./MessageBubble";

export interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  createdAt?: Date;
}

interface MessageStreamProps {
  messages: Message[];
  isLoading?: boolean;
}

export function MessageStream({ messages, isLoading = false }: MessageStreamProps) {
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [showScrollButton, setShowScrollButton] = useState(false);
  const [isAutoScrolling, setIsAutoScrolling] = useState(true);

  const handleScroll = () => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const { scrollTop, scrollHeight, clientHeight } = container;

    const isAtBottom = scrollHeight - scrollTop - clientHeight < 100;

    setIsAutoScrolling(isAtBottom);
    setShowScrollButton(!isAtBottom);
  };

  const scrollToBottom = () => {
    scrollContainerRef.current?.scrollTo({
      top: scrollContainerRef.current.scrollHeight,
      behavior: "smooth",
    });
  };

  useEffect(() => {
    if (isAutoScrolling) {
      requestAnimationFrame(() => {
        if (scrollContainerRef.current) {
          scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
        }
      });
    }
  }, [messages, isLoading, isAutoScrolling]);

  return (
    <div className="relative flex-1 h-full w-full overflow-hidden">

      {/* Scrollable Container Box */}
      <div
        ref={scrollContainerRef}
        onScroll={handleScroll}
        className="h-full w-full overflow-y-auto px-4 py-6 md:px-0 scroll-smooth"
      >
        <div className="max-w-3xl mx-auto flex flex-col gap-6 pb-36">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center pt-24 text-center">
              <div className="w-12 h-12 rounded-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center text-xl mb-4">
                ✨
              </div>
              <h2 className="text-xl font-medium text-zinc-800 dark:text-zinc-200">
                How can I help you today?
              </h2>
            </div>
          ) : (
            messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))
          )}

          {isLoading && messages[messages.length - 1]?.role === "user" && (
            <div className="flex items-start gap-4 max-w-3xl mx-auto w-full group">
              <div className="w-8 h-8 rounded-full border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 flex items-center justify-center text-sm shadow-sm shrink-0">
                🤖
              </div>
              <div className="flex flex-col pt-1 gap-1">
                <div className="flex items-center gap-1.5">
                  <div className="w-2 h-2 rounded-full bg-zinc-400 dark:bg-zinc-500 animate-bounce [animation-delay:-0.3s]" />
                  <div className="w-2 h-2 rounded-full bg-zinc-400 dark:bg-zinc-500 animate-bounce [animation-delay:-0.15s]" />
                  <div className="w-2 h-2 rounded-full bg-zinc-400 dark:bg-zinc-500 animate-bounce" />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {showScrollButton && (
        <button
          onClick={scrollToBottom}
          className="absolute bottom-4 right-1/2 translate-x-1/2 md:right-8 md:translate-x-0 p-2 rounded-full border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-[#2f2f2f] text-zinc-600 dark:text-zinc-300 shadow-md hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-all z-20 outline-none"
          aria-label="Scroll to bottom"
        >
          <ArrowDown className="h-4 w-4 stroke-[2.5]" />
        </button>
      )}
    </div>
  );
}
