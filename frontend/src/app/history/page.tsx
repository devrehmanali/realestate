'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/axios';
import { useSessionStore } from '@/lib/store';
import { Loader2, Calendar, MapPin, DollarSign, Bed } from 'lucide-react';

export default function HistoryPage() {
  const { sessionId } = useSessionStore();

  const { data: history, isPending } = useQuery({
    queryKey: ['conversation-history', sessionId],
    queryFn: async () => {
      const res = await api.get(`/conversations/$\\{sessionId\\}`);
      return res.data;
    },
  });

  return (
    <main className="min-h-screen bg-gray-50 py-10 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-10">
          <h1 className="text-3xl font-outfit font-bold text-gray-900 mb-2">My Search History</h1>
          <p className="text-gray-600 font-inter">View your previous interactions and saved preferences.</p>
        </header>

        {isPending ? (
          <div className="flex justify-center py-20">
             <Loader2 className="w-10 h-10 animate-spin text-blue-500" />
          </div>
        ) : (
          <div className="space-y-6">
            {/* Preferences Summary */}
            {history?.data?.metadata_filters && Object.keys(history.data.metadata_filters).length > 0 && (
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
                <h3 className="font-outfit font-bold text-lg mb-4 flex items-center gap-2">
                   Your Current Preferences
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                   {history.data.metadata_filters.city && (
                      <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-xl">
                        <MapPin className="text-blue-500 w-5 h-5" />
                        <div>
                          <p className="text-[10px] uppercase text-blue-400 font-bold">City</p>
                          <p className="text-sm font-bold text-blue-900">{history.data.metadata_filters.city}</p>
                        </div>
                      </div>
                   )}
                   {history.data.metadata_filters.max_price && (
                      <div className="flex items-center gap-3 p-3 bg-green-50 rounded-xl">
                        <DollarSign className="text-green-500 w-5 h-5" />
                        <div>
                          <p className="text-[10px] uppercase text-green-400 font-bold">Budget</p>
                          <p className="text-sm font-bold text-green-900">{history.data.metadata_filters.max_price.toLocaleString()}</p>
                        </div>
                      </div>
                   )}
                   {history.data.metadata_filters.bedrooms && (
                      <div className="flex items-center gap-3 p-3 bg-orange-50 rounded-xl">
                        <Bed className="text-orange-500 w-5 h-5" />
                        <div>
                          <p className="text-[10px] uppercase text-orange-400 font-bold">Beds</p>
                          <p className="text-sm font-bold text-orange-900">{history.data.metadata_filters.bedrooms}</p>
                        </div>
                      </div>
                   )}
                </div>
              </div>
            )}

            {/* Chat History List */}
            <div className="space-y-4">
               <h3 className="font-outfit font-bold text-lg text-gray-800 px-1">Recent Messages</h3>
               {history?.data?.messages?.map((msg: any) => (
                 <div key={msg.id} className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex gap-4">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 $\\{msg.role === 'user' ? 'bg-gray-100' : 'bg-blue-600'\\}`}>
                       <p className={`text-[10px] font-bold $\\{msg.role === 'user' ? 'text-gray-500' : 'text-white'\\}`}>
                          {msg.role === 'user' ? 'ME' : 'AI'}
                       </p>
                    </div>
                    <div>
                       <p className="text-sm text-gray-800">{msg.content}</p>
                       <p className="text-[10px] text-gray-400 mt-1 flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {new Date(msg.timestamp).toLocaleString()}
                       </p>
                    </div>
                 </div>
               ))}
               
               {history?.data?.messages?.length === 0 && (
                 <div className="text-center py-10 text-gray-400 font-inter bg-white rounded-2xl border border-gray-100 italic">
                    No conversation history found for this session.
                 </div>
               )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
