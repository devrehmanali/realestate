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
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-white border-r border-gray-100 font-inter">
      <div className="p-4 border-b border-gray-100">
        <button 
          onClick={handleNewChat}
          className="w-full flex items-center justify-center gap-2 bg-blue-50 hover:bg-blue-100 text-blue-600 border border-blue-200 p-2.5 rounded-lg font-medium transition-colors"
        >
          <PlusCircle className="w-5 h-5" />
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider px-3 mb-2">
           Recent Chats
        </h3>
        
        {isPending ? (
           <div className="animate-pulse flex flex-col gap-2 px-3">
              <div className="h-10 bg-gray-100 rounded-lg w-full"></div>
              <div className="h-10 bg-gray-100 rounded-lg w-full"></div>
           </div>
        ) : (
          conversations?.data?.map((conv: any) => {
            const isActive = conv.session_id === sessionId;
            // Get city or type from filters to make title, else generic
            const filters = conv.metadata_filters || {};
            const titleParts = [filters.city, filters.bedrooms ? `$\\{filters.bedrooms\\} Bed` : null, filters.type].filter(Boolean);
            const displayTitle = titleParts.length > 0 ? titleParts.join(' ') : 'New Property Search';
            
            return (
              <button
                key={conv.session_id}
                onClick={() => setSessionId(conv.session_id)}
                className={`w-full text-left px-3 py-3 rounded-lg flex items-center gap-3 transition-colors $\\{isActive ? 'bg-blue-600 text-white shadow-md' : 'text-gray-700 hover:bg-gray-100'\\}`}
              >
                <MessageSquare className={`w-4 h-4 shrink-0 $\\{isActive ? 'text-blue-200' : 'text-gray-400'\\}`} />
                <div className="overflow-hidden">
                  <p className="text-sm font-medium truncate capitalize">{displayTitle}</p>
                  <p className={`text-[10px] truncate $\\{isActive ? 'text-blue-200' : 'text-gray-400'\\}`}>
                    {new Date(conv.updated_at).toLocaleDateString()}
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
