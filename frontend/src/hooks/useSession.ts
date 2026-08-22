import { useEffect, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api/v1";

export const useSession = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const createSession = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`${API_BASE_URL}/session`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        const result = await response.json();

        console.log("Create session response:", result);

        if (!response.ok || !result.success) {
          throw new Error(
            result.message || result.detail || "Failed to create session."
          );
        }

        const id = result.data.session_id;

        setSessionId(id);
        sessionStorage.setItem("session_id", id);
      } catch (error) {
        console.error("Failed to create session:", error);

        setError(
          error instanceof Error
            ? error.message
            : "Failed to create session."
        );
      } finally {
        setLoading(false);
      }
    };

    createSession();
  }, []);

  return {
    sessionId,
    loading,
    error,
  };
};