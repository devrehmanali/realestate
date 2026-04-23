'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/axios';
import PropertyCard from '@/components/PropertyCard';
import { Loader2, Search, SlidersHorizontal } from 'lucide-react';

export default function PropertiesPage() {
  const [city, setCity] = useState('');
  const [propertyType, setPropertyType] = useState('');
  const [bedrooms, setBedrooms] = useState('');
  const [maxPrice, setMaxPrice] = useState('');

  const [activeFilters, setActiveFilters] = useState({
    city: '',
    property_type: '',
    bedrooms: '',
    max_price: ''
  });

  const { data, isPending, refetch } = useQuery({
    queryKey: ['all-properties', activeFilters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (activeFilters.city) params.append('city', activeFilters.city);
      if (activeFilters.property_type) params.append('property_type', activeFilters.property_type);
      if (activeFilters.bedrooms) params.append('bedrooms', activeFilters.bedrooms);
      if (activeFilters.max_price) params.append('max_price', activeFilters.max_price);
      
      const res = await api.get(`/properties/?${params.toString()}`);
      return res.data;
    },
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setActiveFilters({
      city,
      property_type: propertyType,
      bedrooms,
      max_price: maxPrice
    });
  };

  return (
    <main className="min-h-screen bg-gray-50 py-10 px-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row gap-8">
        
        {/* Filters Sidebar */}
        <aside className="w-full md:w-72 shrink-0 h-fit bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
           <div className="flex items-center gap-2 mb-6 text-gray-800">
              <SlidersHorizontal className="w-5 h-5" />
              <h2 className="font-outfit font-bold text-lg">Filters</h2>
           </div>

           <form onSubmit={handleSearch} className="space-y-5">
              <div>
                 <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">City</label>
                 <input 
                   type="text" 
                   value={city}
                   onChange={e => setCity(e.target.value)}
                   placeholder="e.g. Riyadh" 
                   className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-400"
                 />
              </div>

              <div>
                 <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Property Type</label>
                 <select 
                   value={propertyType}
                   onChange={e => setPropertyType(e.target.value)}
                   className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-400"
                 >
                    <option value="">Any Type</option>
                    <option value="apartment">Apartment</option>
                    <option value="villa">Villa</option>
                    <option value="house">House</option>
                    <option value="studio">Studio</option>
                 </select>
              </div>

              <div>
                 <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Bedrooms</label>
                 <select 
                   value={bedrooms}
                   onChange={e => setBedrooms(e.target.value)}
                   className="w-full bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-400"
                 >
                    <option value="">Any</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4+</option>
                 </select>
              </div>

              <div>
                 <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Max Price</label>
                 <div className="relative">
                   <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">$</span>
                   <input 
                     type="number" 
                     value={maxPrice}
                     onChange={e => setMaxPrice(e.target.value)}
                     placeholder="e.g. 500000" 
                     className="w-full bg-gray-50 border border-gray-200 rounded-lg pl-7 pr-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-400"
                   />
                 </div>
              </div>

              <button 
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg py-2.5 transition-colors flex items-center justify-center gap-2"
              >
                 <Search className="w-4 h-4" />
                 Apply Filters
              </button>
           </form>
        </aside>

        {/* Results Area */}
        <div className="flex-1">
          <header className="mb-8">
            <h1 className="text-3xl font-outfit font-bold text-gray-900 mb-2">Explore Properties</h1>
            <p className="text-gray-600 font-inter">Browse through our hand-picked selection of premium listings.</p>
          </header>

          {isPending ? (
            <div className="flex flex-col items-center justify-center py-20 text-gray-400">
               <Loader2 className="w-10 h-10 animate-spin text-blue-500 mb-4" />
               <p className="font-inter">Loading listings...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {data?.data?.map((prop: any) => (
                <PropertyCard key={prop.id} property={prop} />
              ))}
            </div>
          )}
          
          {data?.data?.length === 0 && (
            <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200">
               <p className="text-gray-500 font-inter">No properties found matching these filters. Try adjusting them.</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
