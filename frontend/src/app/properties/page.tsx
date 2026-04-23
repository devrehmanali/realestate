'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/axios';
import PropertyCard from '@/components/PropertyCard';
import { Loader2, Search, SlidersHorizontal } from 'lucide-react';

export default function PropertiesPage() {
  const { data, isPending } = useQuery({
    queryKey: ['all-properties'],
    queryFn: async () => {
      const res = await api.get('/properties/');
      return res.data;
    },
  });

  return (
    <main className="min-h-screen bg-gray-50 py-10 px-4">
      <div className="max-w-7xl mx-auto">
        <header className="mb-10 text-center md:text-left flex flex-col md:flex-row md:items-end justify-between gap-6">
          <div>
            <h1 className="text-3xl font-outfit font-bold text-gray-900 mb-2">Explore Properties</h1>
            <p className="text-gray-600 font-inter">Browse through our hand-picked selection of premium listings.</p>
          </div>
          
          <div className="flex items-center gap-3 bg-white p-2 rounded-xl shadow-sm border border-gray-100 w-full md:w-auto">
             <div className="relative flex-1 md:w-64">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input 
                  type="text" 
                  placeholder="Search city or type..." 
                  className="w-full pl-9 pr-4 py-2 text-sm outline-none bg-transparent"
                />
             </div>
             <button className="bg-gray-100 hover:bg-gray-200 p-2 rounded-lg transition-colors">
                <SlidersHorizontal className="w-4 h-4 text-gray-600" />
             </button>
          </div>
        </header>

        {isPending ? (
          <div className="flex flex-col items-center justify-center py-20 text-gray-400">
             <Loader2 className="w-10 h-10 animate-spin text-blue-500 mb-4" />
             <p className="font-inter">Loading listings...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data?.data?.map((prop: any) => (
              <PropertyCard key={prop.id} property={prop} />
            ))}
          </div>
        )}
        
        {data?.data?.length === 0 && (
          <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200">
             <p className="text-gray-500 font-inter">No properties found. Try adjusting your search.</p>
          </div>
        )}
      </div>
    </main>
  );
}
