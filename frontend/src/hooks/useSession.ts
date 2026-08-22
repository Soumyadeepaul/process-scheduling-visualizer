import { useEffect, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api/v1";

interface UseSessionResult {
  sessionId: string;
  loading: boolean;
  error: string | null;
}

export const useSession = (): UseSessionResult => {
  const [sessionId, setSessionId] = useState("");
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
            result.message ||
            result.detail ||
            "Failed to create session."
          );
        }

        const id = result.data.session_id;

        if (!id) {
          throw new Error("Session ID was not returned by the server.");
        }

        setSessionId(id);

        sessionStorage.setItem(
          "session_id",
          id
        );

      } catch (error) {

        console.error(
          "Failed to create session:",
          error
        );

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