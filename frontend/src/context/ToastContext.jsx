import { createContext, useCallback, useContext, useEffect, useState } from "react";

const ToastContext = createContext(null);
export function ToastProvider({ children }) {
  const [toast, setToast] = useState(null);
  const showToast = useCallback((message, type = "success") => setToast({ message, type }), []);
  useEffect(() => {
    if (!toast) return undefined;
    const timer = setTimeout(() => setToast(null), 3500);
    return () => clearTimeout(timer);
  }, [toast]);
  return <ToastContext.Provider value={showToast}>{children}{toast && <div className="fixed right-6 top-6 z-50 w-[min(24rem,calc(100vw-3rem))]" role="status"><div className={`rounded-xl border px-4 py-3 text-sm font-medium shadow-2xl ${toast.type === "error" ? "border-red-400/40 bg-red-950 text-red-100" : "border-emerald-400/40 bg-emerald-950 text-emerald-100"}`}>{toast.message}</div></div>}</ToastContext.Provider>;
}
export function useToast() { return useContext(ToastContext); }
