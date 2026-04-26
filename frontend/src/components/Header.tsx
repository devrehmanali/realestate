'use client';

import { Home, Search, MessageSquare, History } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();

  const isActive = (href: string) => {
    if (href === '/') return pathname === '/';
    return pathname.startsWith(href);
  };

  const navLinks = [
    { href: '/chat', label: 'Assistant', icon: MessageSquare },
    { href: '/properties', label: 'Properties', icon: Search },
    { href: '/history', label: 'My Activity', icon: History },
  ];

  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-slate-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-9 h-9 bg-gradient-to-br from-indigo-600 to-violet-700 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-100">
            <Home className="text-white w-5 h-5" />
          </div>
          <div>
            <h1 className="font-outfit font-extrabold text-xl leading-none text-slate-900 tracking-tight">LuxeHome</h1>
            <p className="text-[10px] uppercase tracking-[0.2em] text-indigo-500 font-bold mt-0.5">AI Concierge</p>
          </div>
        </Link>

        <nav className="hidden md:flex items-center gap-8 font-inter text-[13px] font-bold text-slate-500">
          {navLinks.map(({ href, label, icon: Icon }) => {
            const active = isActive(href);
            return (
              <Link
                key={href}
                href={href === '/chat' ? '/' : href}
                className={`flex items-center gap-2 transition-all relative pb-0.5 ${
                  active
                    ? 'text-indigo-600 after:absolute after:bottom-[-21px] after:left-0 after:right-0 after:h-0.5 after:bg-indigo-600'
                    : 'hover:text-indigo-600'
                }`}
              >
                <Icon className="w-4 h-4" />
                {label}
              </Link>
            );
          })}
        </nav>

        <button className="bg-slate-900 text-white px-6 py-2.5 rounded-xl text-[13px] font-bold font-inter hover:bg-slate-800 transition-all shadow-lg shadow-slate-100 active:scale-95">
          Sign In
        </button>
      </div>
    </header>
  );
}
