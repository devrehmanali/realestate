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
      const res = await api.get(`/conversations/$\\{sessionId\\}`);
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
    <div className="flex flex-col h-full bg-white shadow-xl rounded-2xl overflow-hidden border border-gray-100 font-inter max-w-3xl mx-auto w-full">
      {/* Header */}
      <div className="bg-blue-600 px-6 py-4 flex items-center justify-between">
        <div>
          <h2 className="text-white font-semibold font-outfit text-lg">Real Estate Assistant</h2>
          <p className="text-blue-100 text-sm">Always ready to help you find your dream home</p>
        </div>
        <Bot className="text-white w-8 h-8 opacity-80" />
      </div>

      {/* Messages Window */}
      <div className="flex-1 p-6 overflow-y-auto bg-gray-50 flex flex-col gap-6">
        {loadingHistory && <div className="text-center text-gray-400 py-4"><Loader2 className="w-6 h-6 animate-spin mx-auto text-blue-500" /></div>}
        
        {messages.length === 0 && !loadingHistory && (
          <div className="text-center text-gray-500 my-auto py-10">
            <h3 className="font-semibold text-lg text-gray-700 mb-2">Welcome!</h3>
            <p>Tell me what kind of property you are looking for.</p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-4 $\\{msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'\\}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 $\\{msg.role === 'user' ? 'bg-gray-200 text-gray-600' : 'bg-blue-100 text-blue-600'\\}`}>
              {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
            </div>
            
            <div className={`max-w-[80%] flex flex-col gap-3 $\\{msg.role === 'user' ? 'items-end' : 'items-start'\\}`}>
              <div className={`px-4 py-2.5 rounded-2xl text-sm shadow-sm $\\{msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-sm' : 'bg-white border border-gray-100 text-gray-800 rounded-tl-sm'\\}`}>
                 {msg.content}
              </div>

              {/* Render Recommendations if Assistant Provided any */}
              {msg.recommendations && msg.recommendations.length > 0 && (
                <div className="flex flex-col gap-3 w-full mt-2">
                  {msg.recommendations.map(prop => (
                    <PropertyCard key={prop.id} property={prop} />
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {chatMutation.isPending && (
           <div className="flex gap-4 flex-row">
             <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 bg-blue-100 text-blue-600">
               <Bot className="w-5 h-5" />
             </div>
             <div className="px-4 py-2.5 rounded-2xl text-sm shadow-sm bg-white border border-gray-100 text-gray-500 rounded-tl-sm flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin" /> Thinking...
             </div>
           </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSend} className="p-4 bg-white border-t border-gray-100 flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="e.g. I am looking for a 2 bedroom apartment in Riyadh..."
          className="flex-1 bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-400 text-sm"
          disabled={chatMutation.isPending}
        />
        <button
          type="submit"
          disabled={!input.trim() || chatMutation.isPending}
          className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl px-5 flex items-center justify-center"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>
    </div>
  );
}
