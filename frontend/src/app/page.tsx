'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { v4 as uuidv4 } from 'uuid';
import SessionSidebar from '@/components/SessionSidebar';
import { Bot, Sparkles, ArrowRight } from 'lucide-react';

export default function Home() {
  const router = useRouter();

  const handleNewChat = () => {
    const newId = uuidv4();
    router.push(`/chat/${newId}`);
  };

  return (
    <main className="flex h-[calc(100vh-4rem)] bg-slate-50 overflow-hidden">
      {/* Sidebar for Sessions */}
      <div className="w-64 lg:w-72 hidden md:block shrink-0 shadow-[4px_0_12px_rgba(0,0,0,0.02)] z-10 relative">
        <SessionSidebar activeSessionId={null} />
      </div>

      {/* Empty State */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center max-w-md">
          <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-violet-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-2xl shadow-indigo-200">
            <Bot className="w-10 h-10 text-white" />
          </div>
          <h2 className="font-outfit font-extrabold text-3xl text-slate-900 tracking-tight mb-3">
            Welcome to LuxeHome AI
          </h2>
          <p className="text-slate-500 text-[15px] leading-relaxed mb-8">
            Your intelligent real estate concierge. Start a new conversation or pick a session from the sidebar to continue where you left off.
          </p>
          <button
            onClick={handleNewChat}
            className="inline-flex items-center gap-2.5 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 text-white font-bold font-inter px-8 py-4 rounded-2xl shadow-xl shadow-indigo-200 transition-all active:scale-95 hover:shadow-2xl hover:shadow-indigo-300 text-[15px] group"
          >
            <Sparkles className="w-5 h-5" />
            Start New Search
            <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
          </button>
        </div>
      </div>
    </main>
  );
}
