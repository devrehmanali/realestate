'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/axios';
import { useSessionStore } from '@/lib/store';
import { PlusCircle, MessageSquare } from 'lucide-react';
import { QueryClient, useQueryClient } from '@tanstack/react-query';

export default function SessionSidebar() {
  const { sessionId, setSessionId, generateNewSession } = useSessionStore();
  const queryClient = useQueryClient();

  const { data: conversations, isPending } = useQuery({
    queryKey: ['conversations'],
    queryFn: async () => {
      const res = await api.get('/conversations/');
      return res.data;
    },
  });

  const handleNewChat = () => {
    generateNewSession();
    // Invalidate conversation history so chat resets
    queryClient.invalidateQueries({ queryKey: ['conversation'] });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-white border-r border-slate-100 font-inter">
      <div className="p-5 border-b border-slate-50">
        <button 
          onClick={handleNewChat}
          className="w-full flex items-center justify-center gap-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-100 p-3 rounded-xl font-bold text-sm transition-all active:scale-95 shadow-sm shadow-indigo-50/50"
        >
          <PlusCircle className="w-5 h-5" />
          New Search
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-2 scrollbar-thin scrollbar-thumb-slate-100">
        <div className="flex items-center justify-between px-2 mb-3">
          <h3 className="text-[11px] font-bold text-slate-400 uppercase tracking-[0.1em]">
             History
          </h3>
          <span className="bg-slate-100 text-slate-500 text-[10px] px-1.5 py-0.5 rounded font-bold">
            {conversations?.data?.length || 0}
          </span>
        </div>
        
        {isPending ? (
           <div className="animate-pulse flex flex-col gap-3 px-1">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-14 bg-slate-50 rounded-xl w-full border border-slate-100"></div>
              ))}
           </div>
        ) : (
          conversations?.data?.map((conv: any) => {
            const isActive = conv.session_id === sessionId;
            const filters = conv.metadata_filters || {};
            const titleParts = [filters.city, filters.bedrooms ? `${filters.bedrooms} Bed` : null, filters.type].filter(Boolean);
            const displayTitle = titleParts.length > 0 ? titleParts.join(' ') : 'Property Search';
            
            return (
              <button
                key={conv.session_id}
                onClick={() => setSessionId(conv.session_id)}
                className={`w-full text-left px-4 py-3.5 rounded-xl flex items-center gap-3.5 transition-all group ${
                  isActive 
                    ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-lg shadow-indigo-100' 
                    : 'text-slate-600 hover:bg-slate-50 border border-transparent hover:border-slate-100'
                }`}
              >
                <div className={`shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
                  isActive ? 'bg-white/20' : 'bg-slate-100 group-hover:bg-white transition-colors'
                }`}>
                  <MessageSquare className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-indigo-500'}`} />
                </div>
                <div className="overflow-hidden flex-1">
                  <p className="text-[13px] font-bold truncate capitalize tracking-tight">{displayTitle}</p>
                  <p className={`text-[10px] truncate mt-0.5 font-medium ${isActive ? 'text-indigo-100' : 'text-slate-400'}`}>
                    {new Date(conv.updated_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                  </p>
                </div>
              </button>
            )
          })
        )}
      </div>
    </div>
  );
}
