import React, { useEffect, useState } from "react";
import type { Process } from "../../pages/Dashboard";
import type {
  SimulationSegment,
  SimulationSpeed,
} from "../../hooks/useSimulation";
import "./SimulationVisualization.css";

interface SimulationVisualizationProps {
  processes: Process[];
  messages: SimulationSegment[];
  simulationTime: number;
  speed: SimulationSpeed;
  paused: boolean;
  simulationStarted: boolean;
  resetKey: number;
}
const SimulationVisualization: React.FC<
  SimulationVisualizationProps
> = ({
  processes,
  messages,
  simulationTime,
  speed,
  paused,
  simulationStarted,
  resetKey,
}) => {
  const [readyQueue, setReadyQueue] =
    useState<number[]>([]);

  const [cpuProcess, setCpuProcess] =
    useState<number | null>(null);

  const [terminated, setTerminated] =
    useState<number[]>([]);

  const [currentIndex, setCurrentIndex] =
    useState(0);

  const [visualTime, setVisualTime] =
    useState(0);

  /*
   * --------------------------------
   * RESET WHEN PROCESSES CHANGE
   * --------------------------------
   */
  useEffect(() => {
    setReadyQueue(
      processes
        .filter(
          (process) =>
            process.arrival_time <= 0
        )
        .map(
          (process) => process.id
        )
    );

    setCpuProcess(null);
    setTerminated([]);
    setCurrentIndex(0);
    setVisualTime(0);
  }, [processes]);

  /*
   * --------------------------------
   * RESET SIMULATION
   * --------------------------------
   */
  useEffect(() => {
    setReadyQueue(
      processes
        .filter(
          (process) =>
            process.arrival_time <= 0
        )
        .map(
          (process) => process.id
        )
    );

    setCpuProcess(null);
    setTerminated([]);
    setCurrentIndex(0);
    setVisualTime(0);
  }, [resetKey]);

  /*
   * --------------------------------
   * FOLLOW BACKEND CLOCK
   * --------------------------------
   */
  useEffect(() => {
    setVisualTime((previous) =>
      Math.max(previous, simulationTime)
    );
  }, [simulationTime]);

  /*
   * --------------------------------
   * UPDATE READY QUEUE
   * --------------------------------
   */
  useEffect(() => {
    const terminatedSet =
      new Set(terminated);

    setReadyQueue(
      processes
        .filter(
          (process) =>
            process.arrival_time <= visualTime &&
            !terminatedSet.has(process.id) &&
            process.id !== cpuProcess
        )
        .map(
          (process) => process.id
        )
    );
  }, [
    visualTime,
    processes,
    terminated,
    cpuProcess,
  ]);

  /*
   * --------------------------------
   * CURRENT SEGMENT
   * --------------------------------
   */
  const currentSegment =
    messages[currentIndex];

  /*
   * --------------------------------
   * ADVANCE VISUAL TIME
   * --------------------------------
   */
  useEffect(() => {
    if (
      !simulationStarted ||
      paused ||
      !currentSegment
    ) {
      return;
    }

    const timer =
      window.setInterval(() => {
        setVisualTime((previous) => {
          const increment =
            0.05 * speed;

          return Math.min(
            previous + increment,
            currentSegment.end
          );
        });
      }, 50);

    return () => {
      window.clearInterval(timer);
    };
  }, [
    simulationStarted,
    paused,
    speed,
    currentSegment,
  ]);

  /*
   * --------------------------------
   * START CURRENT SEGMENT
   * --------------------------------
   */
  useEffect(() => {
    if (!currentSegment) {
      return;
    }

    if (
      visualTime <
      currentSegment.start
    ) {
      setCpuProcess(null);
      return;
    }

    setReadyQueue((previous) =>
      previous.filter(
        (id) =>
          id !==
          currentSegment.process_id
      )
    );

    setCpuProcess(
      currentSegment.process_id
    );
  }, [
    currentSegment,
    visualTime,
  ]);

  /*
   * --------------------------------
   * FINISH CURRENT SEGMENT
   * --------------------------------
   */
  useEffect(() => {
    if (!currentSegment) {
      return;
    }

    if (
      visualTime <
      currentSegment.end
    ) {
      return;
    }

    const processId =
      currentSegment.process_id;

    setCpuProcess((current) =>
      current === processId
        ? null
        : current
    );

    if (
      currentSegment.state ===
      "completed"
    ) {
      setTerminated((previous) =>
        previous.includes(processId)
          ? previous
          : [
              ...previous,
              processId,
            ]
      );
    } else if (
      currentSegment.state ===
      "ready"
    ) {
      setReadyQueue((previous) =>
        previous.includes(processId)
          ? previous
          : [
              ...previous,
              processId,
            ]
      );
    }

    setCurrentIndex(
      (previous) =>
        previous + 1
    );
  }, [
    visualTime,
    currentSegment,
  ]);

  return (
    <div className="simulation-visualization">

      <div className="simulation-visualization__title">
        SIMULATION VISUALIZATION
      </div>

      <div className="simulation-flow">

        {/* READY QUEUE */}

        <div className="simulation-queue">

          <div className="simulation-queue__label">
            READY QUEUE
          </div>

          <div className="simulation-queue__content">

            {readyQueue.map(
              (processId) => (
                <div
                  className="process-token"
                  key={processId}
                >
                  P{processId}
                </div>
              )
            )}

          </div>

        </div>

        {/* ARROW */}

        <div className="simulation-arrow">
          <span />
        </div>

        {/* CPU */}

        <div className="simulation-cpu">

          <div className="simulation-cpu__label">
            CPU
          </div>

          <div className="simulation-cpu__process">

            {cpuProcess !== null && (
              <div className="process-token">
                P{cpuProcess}
              </div>
            )}

          </div>

        </div>

        {/* ARROW */}

        <div className="simulation-arrow">
          <span />
        </div>

        {/* TERMINATED */}

        <div className="simulation-queue">

          <div className="simulation-queue__label">
            TERMINATED
          </div>

          <div className="simulation-queue__content">

            {terminated.map(
              (processId) => (
                <div
                  className="process-token"
                  key={processId}
                >
                  P{processId}
                </div>
              )
            )}

          </div>

        </div>

      </div>

    </div>
  );
};

export default SimulationVisualization;