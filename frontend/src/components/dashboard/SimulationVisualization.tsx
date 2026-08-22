import React, { useEffect, useMemo, useState } from "react";
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

  /*
   * --------------------------------
   * CURRENT SEGMENT INDEX
   * --------------------------------
   */
  const [currentIndex, setCurrentIndex] =
    useState(0);

  /*
   * --------------------------------
   * LOCAL VISUAL TIME
   * --------------------------------
   */
  const [visualTime, setVisualTime] =
    useState(0);

  /*
   * --------------------------------
   * RESET
   * --------------------------------
   */
  useEffect(() => {
    setReadyQueue(
      processes.map(
        (process) => process.id
      )
    );

    setCpuProcess(null);
    setTerminated([]);
    setCurrentIndex(0);
    setVisualTime(0);
  }, [processes]);

  useEffect(() => {
    setReadyQueue(
      processes.map(
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
   *
   * simulationTime tells us where the
   * backend currently is.
   *
   * We never move backwards.
   */
  useEffect(() => {
    setVisualTime((previous) =>
      Math.max(previous, simulationTime)
    );
  }, [simulationTime]);

  /*
   * --------------------------------
   * CURRENT MESSAGE
   * --------------------------------
   */
  const currentSegment =
    messages[currentIndex];

  /*
   * --------------------------------
   * ADVANCE VISUAL TIME
   * --------------------------------
   *
   * This is the same timing model used
   * by the Gantt chart.
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
   * PLAY CURRENT SEGMENT
   * --------------------------------
   */
  useEffect(() => {
    if (!currentSegment) {
      return;
    }

    /*
     * Do not show the CPU before the
     * process actually arrives.
     */
    if (
      visualTime <
      currentSegment.start
    ) {
      setCpuProcess(null);
      return;
    }

    /*
     * Process enters CPU.
     */
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