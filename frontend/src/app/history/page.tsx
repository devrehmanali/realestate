'use client';

import { useQuery } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/axios';
import { Loader2, Calendar, MapPin, DollarSign, Bed, MessageSquare, ArrowRight } from 'lucide-react';

export default function HistoryPage() {
  const router = useRouter();

  // Fetch ALL conversations across all sessions
  const { data: conversations, isPending } = useQuery({
    queryKey: ['conversations'],
    queryFn: async () => {
      const res = await api.get('/conversations/');
      return res.data;
    },
  });

  const handleOpenSession = (sessionId: string) => {
    router.push(`/chat/${sessionId}`);
  };

  return (
    <main className="min-h-screen bg-slate-50 py-10 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-10">
          <h1 className="text-3xl font-outfit font-extrabold text-slate-900 mb-2 tracking-tight">My Activity</h1>
          <p className="text-slate-500 font-inter">All your past property search sessions in one place.</p>
        </header>

        {isPending ? (
          <div className="flex justify-center py-20">
            <Loader2 className="w-10 h-10 animate-spin text-indigo-500" />
          </div>
        ) : (
          <div className="space-y-4">
            {(!conversations?.data || conversations.data.length === 0) && (
              <div className="text-center py-16 text-slate-400 font-inter bg-white rounded-2xl border border-slate-100 italic">
                No conversation history found. Start a new search to get going!
              </div>
            )}

            {conversations?.data?.map((conv: any) => {
              const filters = conv.metadata_filters || {};
              const titleParts = [
                filters.city,
                filters.bedrooms ? `${filters.bedrooms} Bed` : null,
                filters.type,
              ].filter(Boolean);
              const displayTitle = titleParts.length > 0 ? titleParts.join(' · ') : 'Property Search';
              const messageCount = conv.message_count ?? 0;

              return (
                <div
                  key={conv.session_id}
                  className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 hover:border-indigo-100 hover:shadow-md transition-all group"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-center gap-4 flex-1 min-w-0">
                      <div className="w-11 h-11 rounded-xl bg-indigo-50 flex items-center justify-center shrink-0">
                        <MessageSquare className="w-5 h-5 text-indigo-500" />
                      </div>
                      <div className="min-w-0 flex-1">
                        <h2 className="font-outfit font-bold text-slate-800 capitalize truncate text-[15px]">
                          {displayTitle}
                        </h2>
                        <p className="text-[11px] text-slate-400 mt-0.5 flex items-center gap-1 font-medium">
                          <Calendar className="w-3 h-3 shrink-0" />
                          {new Date(conv.updated_at).toLocaleString(undefined, {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit',
                          })}
                          {messageCount > 0 && (
                            <span className="ml-2 bg-slate-100 text-slate-500 text-[10px] px-1.5 py-0.5 rounded font-bold">
                              {messageCount} msg{messageCount !== 1 ? 's' : ''}
                            </span>
                          )}
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={() => handleOpenSession(conv.session_id)}
                      className="shrink-0 flex items-center gap-1.5 text-indigo-600 hover:text-white hover:bg-indigo-600 border border-indigo-200 hover:border-indigo-600 font-bold text-[12px] px-3 py-2 rounded-xl transition-all active:scale-95"
                    >
                      Open
                      <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                    </button>
                  </div>

                  {/* Filter Tags */}
                  {Object.keys(filters).length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-4 pl-[3.75rem]">
                      {filters.city && (
                        <span className="flex items-center gap-1 bg-blue-50 text-blue-700 text-[11px] font-bold px-2.5 py-1 rounded-lg">
                          <MapPin className="w-3 h-3" /> {filters.city}
                        </span>
                      )}
                      {filters.max_price && (
                        <span className="flex items-center gap-1 bg-green-50 text-green-700 text-[11px] font-bold px-2.5 py-1 rounded-lg">
                          <DollarSign className="w-3 h-3" /> Up to {filters.max_price.toLocaleString()}
                        </span>
                      )}
                      {filters.bedrooms && (
                        <span className="flex items-center gap-1 bg-orange-50 text-orange-700 text-[11px] font-bold px-2.5 py-1 rounded-lg">
                          <Bed className="w-3 h-3" /> {filters.bedrooms} Bedrooms
                        </span>
                      )}
                      {filters.type && (
                        <span className="bg-violet-50 text-violet-700 text-[11px] font-bold px-2.5 py-1 rounded-lg capitalize">
                          {filters.type}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </main>
  );
}
