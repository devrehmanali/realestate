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
    <div className="bg-white border border-gray-100 shadow-sm rounded-xl overflow-hidden mb-3 font-inter">
      <div className="p-4 border-b border-gray-50 flex items-start justify-between">
        <div>
          <h4 className="font-semibold text-gray-800 capitalize flex items-center gap-1.5">
            <Home className="w-4 h-4 text-blue-500" />
            {property.type}
          </h4>
          <p className="text-gray-500 text-sm flex items-center gap-1 mt-1">
            <MapPin className="w-3.5 h-3.5" />
            {property.city}
          </p>
        </div>
        <div className="text-right">
          <p className="font-bold text-blue-600 flex items-center justify-end gap-0.5">
             {property.price.toLocaleString()}
          </p>
          <span className={`text-xs px-2 py-0.5 rounded-full inline-block mt-1 $\\{property.availability ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'\\}`}>
            {property.availability ? 'Available' : 'Unavailable'}
          </span>
        </div>
      </div>
      
      <div className="px-4 py-3 bg-gray-50/50 flex gap-4 text-sm text-gray-600">
        <div className="flex items-center gap-1.5">
          <BedDouble className="w-4 h-4 text-gray-400" />
          <span>{property.bedrooms} Bed</span>
        </div>
      </div>

      {property.reason && (
        <div className="px-4 py-3 bg-blue-50/30 text-sm text-gray-600 border-t border-blue-50/50">
          <p className="inline-block"><strong className="font-medium text-gray-800">Why this fits:</strong> {property.reason}</p>
        </div>
      )}
    </div>
  );
}
