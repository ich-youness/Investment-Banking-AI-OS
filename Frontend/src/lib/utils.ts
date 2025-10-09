import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Backend API base URL from Vite env
export const BACKEND_URL: string = ((): string => {
  const fromEnv = import.meta?.env?.VITE_BACKEND_URL as string | undefined;
  if (fromEnv && typeof fromEnv === 'string' && fromEnv.trim().length > 0) {
    return fromEnv.replace(/\/$/, '');
  }
  // Fallback for local dev
  return 'http://https://investment-banking-ai-os.onrender.com';
})();