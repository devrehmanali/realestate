import ChatInterface from "@/components/ChatInterface";
import SessionSidebar from "@/components/SessionSidebar";

interface ChatPageProps {
  params: Promise<{ sessionId: string }>;
}

export default async function ChatPage({ params }: ChatPageProps) {
  const { sessionId } = await params;

  return (
    <main className="flex h-[calc(100vh-4rem)] bg-slate-50 overflow-hidden">
      {/* Sidebar for Sessions */}
      <div className="w-64 lg:w-72 hidden md:block shrink-0 shadow-[4px_0_12px_rgba(0,0,0,0.02)] z-10 relative">
        <SessionSidebar activeSessionId={sessionId} />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 p-4 sm:p-6 lg:p-8 flex items-center justify-center overflow-y-auto w-full">
        <div className="w-full h-full max-w-4xl">
          <ChatInterface sessionId={sessionId} />
        </div>
      </div>
    </main>
  );
}
