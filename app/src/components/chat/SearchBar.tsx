"use client";
import { ArrowUp, Paperclip, Globe, Sparkles } from "lucide-react";
import React, { useRef, useEffect, useState } from 'react';


interface SearchBarProps {
    onSendMessage: (message: string) => void;
    isLoading?: boolean;
    placeholder: string;
}

export function SearchBar  ({
    onSendMessage,
    isLoading = false,
    placeholder = "Start a New Explaination Session"
}:SearchBarProps
) {
  const [input, setInput] = useState("");
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const textarea = textAreaRef.current;
    if(!textarea) return;

    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  }, [input])

  const handleSubmit = (e?: React.SubmitEvent<HTMLFormElement>) => {
    e?.preventDefault();
    if(!input.trim() || isLoading)
    {
        return;
    }
    onSendMessage(input.trim());
    setInput("");
  }

  const handleKeyDown = (e:React.KeyboardEvent<HTMLTextAreaElement>) => {
    if(e.key === "Enter" && !e.shiftKey)
    {
        e.preventDefault();
        handleSubmit();
    }
  }
  return (
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-3xl mx-auto relative flex flex-col bg-[#ececec] dark:bg-[#2f2f2f] rounded-[26px] p-1.5 transition-colors focus-within:ring-1 focus-within:ring-zinc-300 dark:focus-within:ring-zinc-600"
    >
      {/* Input Textarea Area */}
      <div className="w-full px-3 pt-2">
        <textarea
          ref={textAreaRef}
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="w-full resize-none bg-transparent outline-none pr-12 text-zinc-800 dark:text-zinc-100 placeholder-zinc-500 max-h-[200px] min-h-[44px] py-2 text-[15px] leading-relaxed scrollbar-thin"
        />
      </div>

      <div className="flex items-center justify-between px-2 pb-1 pt-1 mt-1">
        <div className="flex items-center gap-1">
          <button
            type="button"
            aria-label="Attach file"
            className="p-2 text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 rounded-full hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors"
          >
            <Paperclip className="h-4.5 w-4.5" />
          </button>

          {/* <button
            type="button"
            aria-label="Search the web"
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 rounded-full hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors"
          >
            <Globe className="h-3.5 w-3.5" />
            <span>Search</span>
          </button>

          <button
            type="button"
            aria-label="Reasoning mode"
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 rounded-full hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors"
          >
            <Sparkles className="h-3.5 w-3.5" />
            <span>Reason</span>
          </button> */}
        </div>

        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          aria-label="Send message"
          className={`p-2 rounded-full transition-all duration-200 ${
            input.trim() && !isLoading
              ? "bg-black text-white dark:bg-white dark:text-black hover:opacity-90 scale-100"
              : "bg-zinc-300 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500 cursor-not-allowed"
          }`}
        >
          <ArrowUp className="h-5 w-5 stroke-[2.5]" />
        </button>
      </div>
    </form>
  );
}
