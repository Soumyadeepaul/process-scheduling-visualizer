import React, { useState } from "react";
import { useSession } from "../hooks/useSession";
import { useSimulation } from "../hooks/useSimulation";
import ProcessTable from "../components/process/ProcessTable";
import SimulationVisualization from "../components/dashboard/SimulationVisualization";
import SimulationControls from "../components/controls/SimulationControls";
import EventLog from "../components/dashboard/EventLog";
import "./Dashboard.css";
import MainLayout from "../components/layout/MainLayout";
import Metrics from "../components/metrics/Metrics";
import GanttChart from "../components/gantt/GanttChart";

export interface Process {
  id: number;
  arrival_time: number;
  burst_time: number;
  priority: number;
}

const Dashboard: React.FC = () => {
  const {
    sessionId,
    loading,
    error,
  } = useSession();

  const [processes, setProcesses] =
    useState<Process[]>([]);

  const [sentProcessIds, setSentProcessIds] =
    useState<number[]>([]);

  const [algorithm, setAlgorithm] =
    useState("FCFS");

  const [timeQuantum, setTimeQuantum] =
    useState<number | null>(null);

  const [resetKey, setResetKey] =
    useState(0);

  /*
   * --------------------------------
   * LOADING
   * --------------------------------
   */

  if (loading) {
    return (
      <MainLayout
        sessionId={sessionId}
        connected={false}
      >
        <div className="dashboard-loading">
          Creating session...
        </div>
      </MainLayout>
    );
  }

  /*
   * --------------------------------
   * ERROR
   * --------------------------------
   */

  if (error || !sessionId) {
    return (
      <MainLayout
        sessionId={sessionId}
        connected={false}
      >
        <div className="dashboard-error">
          <h2>
            Unable to start application
          </h2>

          <p>
            {error || "Session ID not available."}
          </p>
        </div>
      </MainLayout>
    );
  }

  /*
   * --------------------------------
   * SIMULATION
   *
   * From this point onward sessionId
   * is guaranteed to be a string.
   * --------------------------------
   */

  return (
    <DashboardContent
      sessionId={sessionId}
      processes={processes}
      setProcesses={setProcesses}
      sentProcessIds={sentProcessIds}
      setSentProcessIds={setSentProcessIds}
      algorithm={algorithm}
      setAlgorithm={setAlgorithm}
      timeQuantum={timeQuantum}
      setTimeQuantum={setTimeQuantum}
      resetKey={resetKey}
      setResetKey={setResetKey}
    />
  );
};


/*
 * ============================================
 * DASHBOARD CONTENT
 * ============================================
 *
 * This component is rendered only after
 * sessionId is confirmed to be a string.
 */

interface DashboardContentProps {
  sessionId: string;

  processes: Process[];
  setProcesses: React.Dispatch<
    React.SetStateAction<Process[]>
  >;

  sentProcessIds: number[];
  setSentProcessIds: React.Dispatch<
    React.SetStateAction<number[]>
  >;

  algorithm: string;
  setAlgorithm: React.Dispatch<
    React.SetStateAction<string>
  >;

  timeQuantum: number | null;
  setTimeQuantum: React.Dispatch<
    React.SetStateAction<number | null>
  >;

  resetKey: number;
  setResetKey: React.Dispatch<
    React.SetStateAction<number>
  >;
}

const DashboardContent: React.FC<
  DashboardContentProps
> = ({
  sessionId,
  processes,
  setProcesses,
  sentProcessIds,
  setSentProcessIds,
  algorithm,
  setAlgorithm,
  timeQuantum,
  setTimeQuantum,
  resetKey,
  setResetKey,
}) => {

  const {
    connected,
    simulationStarted,
    paused,
    speed,

    connect,
    disconnect,

    play,
    pause,
    resume,
    reset,

    setSpeed,

    messages,
    simulationTime,
  } = useSimulation(sessionId);

  /*
   * --------------------------------
   * PROCESS MANAGEMENT
   * --------------------------------
   */

  const addProcess = (
    process: Process
  ) => {

    setProcesses(
      (previous) => [
        ...previous,
        process,
      ]
    );
  };

  const removeProcess = (
    processId: number
  ) => {

    setProcesses(
      (previous) =>
        previous.filter(
          (process) =>
            process.id !== processId
        )
    );
  };

  /*
   * --------------------------------
   * RESET
   * --------------------------------
   */

  const handleReset = () => {

    reset();

    /*
     * This tells both visualization
     * components to reset their local
     * visual state.
     */
    setResetKey(
      (previous) =>
        previous + 1
    );
  };

  /*
   * --------------------------------
   * RENDER
   * --------------------------------
   */

  return (
    <MainLayout
      sessionId={sessionId}
      connected={connected}
    >

      <div className="dashboard">

        {/* =================================
            TOP SECTION
        ================================= */}

        <div className="dashboard__top">

          {/* --------------------------------
              PROCESS TABLE
          -------------------------------- */}

          <section
            className="
              dashboard-card
              dashboard-card--process
            "
          >

            <ProcessTable
              processes={processes}
              sentProcessIds={sentProcessIds}
              sessionId={sessionId}

              algorithm={algorithm}
              timeQuantum={timeQuantum}

              onAlgorithmChange={
                setAlgorithm
              }

              onTimeQuantumChange={
                setTimeQuantum
              }

              onAddProcess={
                addProcess
              }

              onRemoveProcess={
                removeProcess
              }

              onProcessesSent={
                setSentProcessIds
              }
            />

          </section>


          {/* --------------------------------
              SIMULATION VISUALIZATION
          -------------------------------- */}

          <section
            className="
              dashboard-card
              dashboard-card--simulation
            "
          >

            <SimulationVisualization
              processes={processes}
              messages={messages}
              simulationTime={simulationTime}
              speed={speed}
              paused={paused}
              simulationStarted={simulationStarted}
              resetKey={resetKey}
            />
          </section>

        </div>


        {/* =================================
            CONTROLS
        ================================= */}

        <section
          className="
            dashboard-card
            dashboard-card--controls
          "
        >

          <SimulationControls
            connected={connected}

            simulationStarted={
              simulationStarted
            }

            paused={paused}

            speed={speed}

            onConnect={connect}
            onDisconnect={disconnect}

            onPlay={play}
            onPause={pause}
            onResume={resume}

            onReset={handleReset}

            onSpeedChange={setSpeed}
          />

        </section>


        {/* =================================
            LIVE GANTT CHART
        ================================= */}

        <section
          className="
            dashboard-card
            dashboard-card--gantt
          "
        >

          <GanttChart
            messages={messages}
            simulationTime={simulationTime}
            speed={speed}
            paused={paused}
            simulationStarted={simulationStarted}
            resetKey={resetKey}
          />

        </section>


        {/* =================================
            METRICS
        ================================= */}

        <section
          className="
            dashboard-card
            dashboard-card--metrics
          "
        >

          <Metrics
            sessionId={sessionId}
          />

        </section>


        {/* =================================
            EVENT LOG
        ================================= */}

        <section
          className="
            dashboard-card
            dashboard-card--event-log
          "
        >

          <EventLog
            messages={messages}
          />

        </section>

      </div>

    </MainLayout>
  );
};

export default Dashboard;