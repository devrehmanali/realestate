import ChatInterface from "@/components/ChatInterface";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 p-4 md:p-8 flex items-center justify-center">
      <div className="w-full h-[90vh] max-h-[800px]">
        <ChatInterface />
      </div>
    </main>
  );
}
