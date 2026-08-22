import React, { useEffect, useState } from "react";
import type { Process } from "../../pages/Dashboard";
import type { SimulationSegment, SimulationSpeed } from "../../hooks/useSimulation";
import "./SimulationVisualization.css";

interface SimulationVisualizationProps {
  processes: Process[];
  messages: SimulationSegment[];
  speed: SimulationSpeed;
  resetKey: number;
}

const SimulationVisualization: React.FC<SimulationVisualizationProps> = ({ processes, messages, speed, resetKey }) => {
  const [readyQueue, setReadyQueue] = useState<number[]>([]);
  const [cpuProcess, setCpuProcess] = useState<number | null>(null);
  const [terminated, setTerminated] = useState<number[]>([]);
  const [processedCount, setProcessedCount] = useState(0);

  useEffect(() => {
    setReadyQueue(processes.map((process) => process.id));
    setCpuProcess(null);
    setTerminated([]);
    setProcessedCount(0);
  }, [processes]);

  useEffect(() => {
    if (messages.length <= processedCount) return;

    const segment = messages[processedCount];
    setProcessedCount((previous) => previous + 1);

    const processId = segment.process_id;
    const duration = Math.max(0, segment.end - segment.start);
    const displayDuration = (duration * 1000) / speed;

    setReadyQueue((previous) => previous.filter((id) => id !== processId));
    setCpuProcess(processId);

    window.setTimeout(() => {
      setCpuProcess((current) => current === processId ? null : current);

      if (segment.state === "completed") {
        setTerminated((previous) => previous.includes(processId) ? previous : [...previous, processId]);
      } else if (segment.state === "ready") {
        setReadyQueue((previous) => previous.includes(processId) ? previous : [...previous, processId]);
      }
    }, displayDuration);
  }, [messages, processedCount, speed]);

  useEffect(() => {
    setReadyQueue(processes.map((process) => process.id));
    setCpuProcess(null);
    setTerminated([]);
    setProcessedCount(messages.length);
  }, [resetKey]);

  return (
    <div className="simulation-visualization">
      <div className="simulation-visualization__title">SIMULATION VISUALIZATION</div>

      <div className="simulation-flow">
        <div className="simulation-queue">
          <div className="simulation-queue__label">READY QUEUE</div>

          <div className="simulation-queue__content">
            {readyQueue.map((processId) => (
              <div className="process-token" key={processId}>P{processId}</div>
            ))}
          </div>
        </div>

        <div className="simulation-arrow">
          <span />
        </div>

        <div className="simulation-cpu">
          <div className="simulation-cpu__label">CPU</div>

          <div className="simulation-cpu__process">
            {cpuProcess !== null && (
              <div className="process-token">P{cpuProcess}</div>
            )}
          </div>
        </div>

        <div className="simulation-arrow">
          <span />
        </div>

        <div className="simulation-queue">
          <div className="simulation-queue__label">TERMINATED</div>

          <div className="simulation-queue__content">
            {terminated.map((processId) => (
              <div className="process-token" key={processId}>P{processId}</div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimulationVisualization;