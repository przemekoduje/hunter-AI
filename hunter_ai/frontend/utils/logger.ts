export const getTraceId = (): string => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  // Fallback for environments where crypto.randomUUID is not available
  return 'xxxx-xxxx-xxxx-xxxx'.replace(/[x]/g, () =>
    (Math.random() * 16 | 0).toString(16)
  );
};

export const logError = (message: string, error?: any, traceId?: string) => {
  const currentTraceId = traceId || getTraceId();
  console.error(`[Trace ID: ${currentTraceId}] ${message}`, error || '');
  // Docelowo: wysyłka błędu do zewnętrznego systemu (Sentry, n8n webhook logów)
};

export const logInfo = (message: string, traceId?: string) => {
  const currentTraceId = traceId || getTraceId();
  console.info(`[Trace ID: ${currentTraceId}] ${message}`);
};
