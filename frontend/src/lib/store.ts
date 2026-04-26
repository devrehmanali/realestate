import { create } from 'zustand';

// Store is kept for any future shared client state.
// Session ID is now managed via URL params (/chat/[sessionId]).
interface AppState {
  _placeholder: null;
}

export const useAppStore = create<AppState>(() => ({
  _placeholder: null,
}));
