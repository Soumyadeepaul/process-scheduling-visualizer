import { useCallback, useEffect, useRef, useState } from "react";

export type SimulationSpeed = 1 | 2 | 5;

export interface SimulationSegment {
  type?: string;
  process_id: number;
  start: number;
  end: number;
  state: "ready" | "completed";
}

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || "ws://127.0.0.1:8000/api/v1";

export const useSimulation = (sessionId: string) => {
  const socketRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [simulationStarted, setSimulationStarted] = useState(false);
  const [paused, setPaused] = useState(false);
  const [speed, setSpeed] = useState<SimulationSpeed>(1);
  const [messages, setMessages] = useState<SimulationSegment[]>([]);

  const connect = useCallback(() => {
    if (!sessionId || socketRef.current) return;

    const socket = new WebSocket(`${WS_BASE_URL}/ws/${sessionId}`);

    socket.onopen = () => {
      setConnected(true);
    };

    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);

        if (message.type === "PROCESS_START") {
          setMessages((previous) => [...previous, message.data]);
          setSimulationStarted(true);
        }

        if (message.type === "SIMULATION_COMPLETE") {
          setSimulationStarted(false);
          setPaused(false);
        }
      } catch (error) {
        console.error("Invalid WebSocket message:", error);
      }
    };

    socket.onclose = () => {
      socketRef.current = null;
      setConnected(false);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socketRef.current = socket;
  }, [sessionId]);

  const disconnect = useCallback(() => {
    socketRef.current?.close();
    socketRef.current = null;
    setConnected(false);
  }, []);

  const sendAction = useCallback((action: string, extra: Record<string, unknown> = {}) => {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) return;

    socketRef.current.send(JSON.stringify({ action, ...extra }));
  }, []);

  const play = useCallback(() => {
    if (!connected) return;
    setSimulationStarted(true);
    setPaused(false);
    sendAction("PLAY");
  }, [connected, sendAction]);

  const pause = useCallback(() => {
    if (!connected) return;
    setPaused(true);
    sendAction("PAUSE");
  }, [connected, sendAction]);

  const resume = useCallback(() => {
    if (!connected) return;
    setPaused(false);
    sendAction("RESUME");
  }, [connected, sendAction]);

  const reset = useCallback(() => {
    if (!connected) return;

    sendAction("RESET");
    setMessages([]);
    setSimulationStarted(false);
    setPaused(false);
  }, [connected, sendAction]);

  const changeSpeed = useCallback((newSpeed: SimulationSpeed) => {
    setSpeed(newSpeed);
    sendAction("SPEED", { speed: newSpeed });
  }, [sendAction]);

  useEffect(() => {
    return () => {
      socketRef.current?.close();
      socketRef.current = null;
    };
  }, []);

  return {
    connected,
    simulationStarted,
    paused,
    speed,
    messages,
    connect,
    disconnect,
    play,
    pause,
    resume,
    reset,
    setSpeed: changeSpeed,
  };
};