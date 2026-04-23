'use client';

import { useState, useEffect, useRef } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '@/lib/axios';
import { useSessionStore } from '@/lib/store';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import PropertyCard from './PropertyCard';

interface PropertyRecommendation {
  id: number;
  city: string;
  price: number;
  bedrooms: number;
  type: string;
  availability: boolean;
  reason: string;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  recommendations?: PropertyRecommendation[];
}

export default function ChatInterface() {
  const { sessionId } = useSessionStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  // Fetch history on mount
  const { data: history, isPending: loadingHistory } = useQuery({
    queryKey: ['conversation', sessionId],
    queryFn: async () => {
      const res = await api.get(`/conversations/${sessionId}`);
      return res.data;
    },
  });

  useEffect(() => {
    if (history?.data?.messages && messages.length === 0) {
      setMessages(history.data.messages.map((m: { role: 'user' | 'assistant'; content: string; timestamp: string }) => ({
        role: m.role,
        content: m.content,
        timestamp: m.timestamp
      })));
    }
  }, [history]);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'auto' });
  }, [messages]);

  const chatMutation = useMutation({
    mutationFn: async (text: string) => {
      const res = await api.post('/assistant/chat', {
        user_input: text,
        session_id: sessionId,
        history: [] // Not strictly needed since backend loads from persistent session
      });
      return res.data;
    },
    onSuccess: (response) => {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.data.message,
          recommendations: response.data.recommendations
        }
      ]);
    },
    onError: (error) => {
      console.error("Chat Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
      ]);
    }
  });

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || chatMutation.isPending) return;

    const userText = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userText }]);
    chatMutation.mutate(userText);
  };

  return (
    <div className="flex flex-col h-full bg-white shadow-[0_8px_30px_rgb(0,0,0,0.04)] rounded-2xl overflow-hidden border border-slate-100 font-inter max-w-3xl mx-auto w-full">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-violet-700 px-6 py-5 flex items-center justify-between shadow-sm">
        <div>
          <h2 className="text-white font-bold font-outfit text-xl tracking-tight">Real Estate Assistant</h2>
          <div className="flex items-center gap-2 mt-1">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
            <p className="text-indigo-100 text-xs font-medium uppercase tracking-wider">Online & Responsive</p>
          </div>
        </div>
        <div className="bg-white/10 p-2.5 rounded-xl backdrop-blur-md">
          <Bot className="text-white w-6 h-6" />
        </div>
      </div>

      {/* Messages Window */}
      <div className="flex-1 p-6 overflow-y-auto bg-[#F8FAFC] flex flex-col gap-6 scrollbar-thin scrollbar-thumb-slate-200">
        {loadingHistory && <div className="text-center text-slate-400 py-4"><Loader2 className="w-6 h-6 animate-spin mx-auto text-indigo-500" /></div>}

        {messages.length === 0 && !loadingHistory && (
          <div className="text-center text-slate-500 my-auto py-10 px-6 bg-white/50 rounded-3xl border border-slate-100 border-dashed">
            <div className="w-16 h-16 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Bot className="w-8 h-8" />
            </div>
            <h3 className="font-bold text-xl text-slate-800 mb-2 font-outfit">How can I help you today?</h3>
            <p className="text-slate-500 max-w-sm mx-auto">I can help you find properties, compare prices, or check availability across Riyadh.</p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
            <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 shadow-sm transition-transform hover:scale-105 ${msg.role === 'user'
                ? 'bg-gradient-to-br from-slate-700 to-slate-900 text-white'
                : 'bg-gradient-to-br from-indigo-500 to-indigo-600 text-white'
              }`}>
              {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
            </div>

            <div className={`max-w-[85%] flex flex-col gap-3 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`px-5 py-3 rounded-2xl text-[15px] leading-relaxed shadow-sm ${msg.role === 'user'
                  ? 'bg-indigo-600 text-white rounded-tr-none shadow-indigo-100'
                  : 'bg-white border border-slate-100 text-slate-800 rounded-tl-none shadow-slate-100'
                }`}>
                {msg.content}
              </div>

              {/* Render Recommendations if Assistant Provided any */}
              {msg.recommendations && msg.recommendations.length > 0 && (
                <div className="flex flex-col gap-4 w-full mt-2 animate-in fade-in slide-in-from-bottom-2 duration-500">
                  <div className="flex items-center gap-2 px-1">
                    <div className="h-px bg-slate-200 flex-1"></div>
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Recommended for You</span>
                    <div className="h-px bg-slate-200 flex-1"></div>
                  </div>
                  {msg.recommendations.map(prop => (
                    <PropertyCard key={prop.id} property={prop} />
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {chatMutation.isPending && (
          <div className="flex gap-4 flex-row animate-pulse">
            <div className="w-9 h-9 rounded-xl flex items-center justify-center shrink-0 bg-indigo-100 text-indigo-600">
              <Bot className="w-5 h-5" />
            </div>
            <div className="px-5 py-3 rounded-2xl text-[15px] shadow-sm bg-white border border-slate-100 text-slate-500 rounded-tl-none flex items-center gap-3">
              <div className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce"></span>
              </div>
              Checking properties...
            </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>

      {/* Input Form */}
      <div className="p-5 bg-white border-t border-slate-100">
        <form onSubmit={handleSend} className="flex gap-3 bg-slate-50 p-2 rounded-2xl border border-slate-200 focus-within:border-indigo-400 focus-within:ring-4 focus-within:ring-indigo-50 transition-all duration-200">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Search Riyadh properties (e.g. '2 bed apartment under 50k')..."
            className="flex-1 bg-transparent px-4 py-3 outline-none text-slate-700 placeholder:text-slate-400 font-medium"
            disabled={chatMutation.isPending}
          />
          <button
            type="submit"
            disabled={!input.trim() || chatMutation.isPending}
            className="bg-indigo-600 hover:bg-indigo-700 active:scale-95 disabled:opacity-40 disabled:scale-100 text-white rounded-xl px-6 py-3 flex items-center justify-center transition-all duration-200 shadow-md shadow-indigo-100"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
        <p className="text-[10px] text-center text-slate-400 mt-3 font-medium uppercase tracking-tight">AI may generate inaccurate information. Always verify details.</p>
      </div>
    </div>
  );
}
