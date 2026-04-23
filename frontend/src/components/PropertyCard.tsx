import { Home, BedDouble, MapPin } from "lucide-react";

interface PropertyProps {
  id: number;
  city: string;
  price: number;
  bedrooms: number;
  type: string;
  availability: boolean;
  reason?: string;
}

export default function PropertyCard({ property }: { property: PropertyProps }) {
  return (
    <div className="bg-white border border-gray-200 shadow-sm rounded-xl overflow-hidden mb-3 font-inter hover:shadow-md transition-shadow duration-200">
      <div className="p-4 border-b border-gray-100 flex items-start justify-between">
        <div>
          <h4 className="font-semibold text-slate-800 capitalize flex items-center gap-1.5 text-base">
            <Home className="w-4 h-4 text-indigo-600" />
            {property.type}
          </h4>
          <p className="text-slate-500 text-sm flex items-center gap-1 mt-1">
            <MapPin className="w-3.5 h-3.5 opacity-70" />
            {property.city}
          </p>
        </div>
        <div className="text-right">
          <p className="font-bold text-indigo-700 text-lg flex items-center justify-end gap-0.5">
             <span className="text-sm font-medium mr-0.5">SAR</span>{property.price.toLocaleString()}
          </p>
          <span className={`text-[11px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full inline-flex items-center gap-1.5 mt-1.5 ${
            property.availability 
              ? 'bg-emerald-50 text-emerald-700 border border-emerald-100' 
              : 'bg-rose-50 text-rose-700 border border-rose-100'
          }`}>
            <span className={`w-1.5 h-1.5 rounded-full ${property.availability ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
            {property.availability ? 'Available Now' : 'Unavailable'}
          </span>
        </div>
      </div>
      
      <div className="px-4 py-3 bg-slate-50 flex gap-5 text-sm text-slate-600">
        <div className="flex items-center gap-2">
          <BedDouble className="w-4 h-4 text-slate-400" />
          <span className="font-medium text-slate-700">{property.bedrooms} <span className="font-normal text-slate-500">Bed</span></span>
        </div>
        <div className="flex items-center gap-2">
           <div className="w-1 h-1 bg-slate-300 rounded-full"></div>
           <span className="capitalize">{property.type}</span>
        </div>
      </div>

      {property.reason && (
        <div className="px-4 py-3 bg-indigo-50/40 text-[13px] text-slate-600 border-t border-indigo-100/50">
          <p className="leading-relaxed">
            <span className="inline-block px-1.5 py-0.5 bg-indigo-100 text-indigo-700 rounded text-[10px] font-bold uppercase mr-2.5">Why this fits</span>
            {property.reason}
          </p>
        </div>
      )}
    </div>
  );
}
