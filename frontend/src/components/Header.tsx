import { Home, Search, MessageSquare, History } from "lucide-react";
import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-slate-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-gradient-to-br from-indigo-600 to-violet-700 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-100">
            <Home className="text-white w-5 h-5" />
          </div>
          <div>
            <h1 className="font-outfit font-extrabold text-xl leading-none text-slate-900 tracking-tight">LuxeHome</h1>
            <p className="text-[10px] uppercase tracking-[0.2em] text-indigo-500 font-bold mt-0.5">AI Concierge</p>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-10 font-inter text-[13px] font-bold text-slate-500">
          <Link href="/" className="text-indigo-600 flex items-center gap-2 relative after:absolute after:bottom-[-21px] after:left-0 after:right-0 after:h-0.5 after:bg-indigo-600">
             <MessageSquare className="w-4 h-4" /> Assistant
          </Link>
          <Link href="/properties" className="hover:text-indigo-600 transition-all flex items-center gap-2">
             <Search className="w-4 h-4" /> Properties
          </Link>
          <Link href="/history" className="hover:text-indigo-600 transition-all flex items-center gap-2">
             <History className="w-4 h-4" /> My Activity
          </Link>
        </nav>

        <button className="bg-slate-900 text-white px-6 py-2.5 rounded-xl text-[13px] font-bold font-inter hover:bg-slate-800 transition-all shadow-lg shadow-slate-100 active:scale-95">
          Sign In
        </button>
      </div>
    </header>
  );
}
