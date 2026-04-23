import { Home, Search, MessageSquare, History } from "lucide-react";
import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-200">
            <Home className="text-white w-6 h-6" />
          </div>
          <div>
            <h1 className="font-outfit font-bold text-xl leading-tight text-gray-900">LuxeHome</h1>
            <p className="text-[10px] uppercase tracking-widest text-gray-500 font-inter font-semibold">AI Assistant</p>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-8 font-inter text-sm font-medium text-gray-600">
          <Link href="/" className="text-blue-600 hover:text-blue-700 transition-colors flex items-center gap-2">
             <MessageSquare className="w-4 h-4" /> Chat
          </Link>
          <Link href="/properties" className="hover:text-blue-600 transition-colors flex items-center gap-2">
             <Search className="w-4 h-4" /> Explore
          </Link>
          <Link href="/history" className="hover:text-blue-600 transition-colors flex items-center gap-2">
             <History className="w-4 h-4" /> My Search
          </Link>
        </nav>

        <button className="bg-gray-900 text-white px-5 py-2 rounded-full text-sm font-medium font-inter hover:bg-gray-800 transition-all shadow-md">
          Sign In
        </button>
      </div>
    </header>
  );
}
