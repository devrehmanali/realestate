import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

interface SessionState {
  sessionId: string;
  generateNewSession: () => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  sessionId: typeof window !== 'undefined' ? localStorage.getItem('realestate_session') || uuidv4() : uuidv4(),
  generateNewSession: () => {
    const newSession = uuidv4();
    if(typeof window !== 'undefined') localStorage.setItem('realestate_session', newSession);
    set({ sessionId: newSession });
  }
}));

if (typeof window !== 'undefined') {
    const currentSession = useSessionStore.getState().sessionId;
    localStorage.setItem('realestate_session', currentSession);
}
