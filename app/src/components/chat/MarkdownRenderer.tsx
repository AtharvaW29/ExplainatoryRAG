"use client";

import React, { useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Prism from "prismjs";
import { Check, Copy } from "lucide-react";


import "prismjs/components/prism-javascript";
import "prismjs/components/prism-typescript";
import "prismjs/components/prism-jsx";
import "prismjs/components/prism-tsx";
import "prismjs/components/prism-python";
import "prismjs/components/prism-css";
import "prismjs/components/prism-json";
import "prismjs/components/prism-bash";


import "prismjs/themes/prism-tomorrow.css";

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  useEffect(() => {
    Prism.highlightAll();
  }, [content]);

  return (
    <div className="prose prose-zinc dark:prose-invert max-w-none text-[15px] leading-relaxed text-zinc-800 dark:text-zinc-100 space-y-4">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Override block code structures to add styling layouts and copy functionality
          code({ node, className, children, ...props }) {
            const match = /language-(\w+)/.exec(className || "");
            const language = match ? match[1] : "text";
            const codeString = String(children).replace(/\n$/, "");
            const inline = !match;

            if (!inline) {
              return <CodeBlock language={language} value={codeString} />;
            }

            return (
              <code
                className="bg-zinc-100 dark:bg-[#2f2f2f] px-1.5 py-0.5 rounded text-sm font-mono text-pink-600 dark:text-pink-400 break-words before:content-none after:content-none"
                {...props}
              >
                {children}
              </code>
            );
          },

          p: ({ children }) => <p className="mb-4 last:mb-0">{children}</p>,
          ul: ({ children }) => <ul className="list-disc pl-6 mb-4 space-y-1">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal pl-6 mb-4 space-y-1">{children}</ol>,
          li: ({ children }) => <li className="mb-0.5">{children}</li>,
          h1: ({ children }) => <h1 className="text-2xl font-bold mt-6 mb-2 text-zinc-900 dark:text-white">{children}</h1>,
          h2: ({ children }) => <h2 className="text-xl font-semibold mt-5 mb-2 text-zinc-900 dark:text-white">{children}</h2>,
          h3: ({ children }) => <h3 className="text-lg font-medium mt-4 mb-1 text-zinc-900 dark:text-white">{children}</h3>,
          table: ({ children }) => (
            <div className="overflow-x-auto my-4 w-full">
              <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700 border border-zinc-200 dark:border-zinc-700 rounded-lg overflow-hidden text-sm">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => <thead className="bg-zinc-50 dark:bg-zinc-800/50">{children}</thead>,
          th: ({ children }) => <th className="px-4 py-2 text-left font-semibold text-zinc-700 dark:text-zinc-300 border-b border-zinc-200 dark:border-zinc-700">{children}</th>,
          td: ({ children }) => <td className="px-4 py-2 border-b border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400">{children}</td>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}


interface CodeBlockProps {
  language: string;
  value: string;
}

function CodeBlock({ language, value }: CodeBlockProps) {
  const [isCopied, setIsCopied] = React.useState(false);

  const copyToClipboard = async () => {
    if (!value) return;
    await navigator.clipboard.writeText(value);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  return (
    <div className="relative my-4 rounded-xl overflow-hidden border border-zinc-200 dark:border-zinc-800 bg-[#1e1e1e] group/code">
      <div className="flex items-center justify-between px-4 py-2 bg-zinc-100 dark:bg-[#2d2d2d] border-b border-zinc-200 dark:border-zinc-800 text-xs font-mono text-zinc-500 dark:text-zinc-400 select-none">
        <span>{language}</span>
        <button
          onClick={copyToClipboard}
          className="flex items-center gap-1.5 hover:text-zinc-800 dark:hover:text-zinc-200 transition-colors"
          type="button"
        >
          {isCopied ? (
            <>
              <Check className="h-3.5 w-3.5 text-green-500" />
              <span className="text-green-500">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="h-3.5 w-3.5" />
              <span>Copy code</span>
            </>
          )}
        </button>
      </div>


      <div className="overflow-x-auto p-4 text-sm font-mono leading-relaxed">
        <pre className={`language-${language} !bg-transparent !p-0 !m-0 overflow-visible`}>
          <code className={`language-${language} !bg-transparent`}>{value}</code>
        </pre>
      </div>
    </div>
  );
}
