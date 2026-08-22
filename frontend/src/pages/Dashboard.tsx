import React, { useState } from "react";
import { useSession } from "../hooks/useSession";
import { useSimulation } from "../hooks/useSimulation";
import ProcessTable from "../components/process/ProcessTable";
import SimulationVisualization from "../components/dashboard/SimulationVisualization";
import SimulationControls from "../components/controls/SimulationControls";
import EventLog from "../components/dashboard/EventLog";
import "./Dashboard.css";
import MainLayout from "../components/layout/MainLayout"

export interface Process {
  id: number;
  arrival_time: number;
  burst_time: number;
  priority: number;
}

const Dashboard: React.FC = () => {
  const { sessionId, loading, error } = useSession();

  const [processes, setProcesses] = useState<Process[]>([]);
  const [sentProcessIds, setSentProcessIds] = useState<number[]>([]);

  const [algorithm, setAlgorithm] = useState("FCFS");
  const [timeQuantum, setTimeQuantum] = useState<number | null>(null);

  const [resetKey, setResetKey] = useState(0);

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
  } = useSimulation(sessionId);

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

  if (error) {
    return (
      <MainLayout
        sessionId={sessionId}
        connected={false}
      >
        <div className="dashboard-error">
          <h2>Unable to start application</h2>
          <p>{error}</p>
        </div>
      </MainLayout>
    );
  }

  const addProcess = (process: Process) => {
    setProcesses((previous) => [
      ...previous,
      process,
    ]);
  };

  const removeProcess = (processId: number) => {
    setProcesses((previous) =>
      previous.filter(
        (process) => process.id !== processId
      )
    );
  };

  const handleReset = () => {
    reset();

    setResetKey(
      (previous) => previous + 1
    );
  };

  return (
    <MainLayout
      sessionId={sessionId}
      connected={connected}
    >
      <div className="dashboard">

        {/* --------------------------------
            TOP SECTION
        -------------------------------- */}

        <div className="dashboard__top">

          {/* PROCESS TABLE */}

          <section className="dashboard-card dashboard-card--process">
            <ProcessTable
              processes={processes}
              sentProcessIds={sentProcessIds}
              sessionId={sessionId}
              algorithm={algorithm}
              timeQuantum={timeQuantum}
              onAlgorithmChange={setAlgorithm}
              onTimeQuantumChange={setTimeQuantum}
              onAddProcess={addProcess}
              onRemoveProcess={removeProcess}
              onProcessesSent={setSentProcessIds}
            />
          </section>

          {/* SIMULATION VISUALIZATION */}

          <section className="dashboard-card dashboard-card--simulation">
            <SimulationVisualization
              processes={processes}
              messages={messages}
              speed={speed}
              resetKey={resetKey}
            />
          </section>

        </div>

        {/* --------------------------------
            CONTROLS
        -------------------------------- */}

        <section className="dashboard-card dashboard-card--controls">

          <SimulationControls
            connected={connected}
            simulationStarted={simulationStarted}
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

        {/* --------------------------------
            LIVE GANTT CHART
        -------------------------------- */}

        <section className="dashboard-card dashboard-card--gantt">

          <div className="dashboard-card__title">
            LIVE GANTT CHART
          </div>

          <div className="gantt-placeholder">
            Live Gantt Chart
          </div>

        </section>

        {/* --------------------------------
            METRICS
        -------------------------------- */}

        <section className="dashboard-card dashboard-card--metrics">

          <div className="dashboard-card__title">
            METRICS
          </div>

          <div className="metrics-placeholder">
            Metrics
          </div>

        </section>

        {/* --------------------------------
            EVENT LOG
        -------------------------------- */}

        <section className="dashboard-card dashboard-card--event-log">

          <EventLog
            messages={messages}
          />

        </section>

      </div>
    </MainLayout>
  );
};

export default Dashboard;