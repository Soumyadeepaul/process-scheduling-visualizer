import React from "react";
import "./MainLayout.css";

interface MainLayoutProps {
  children: React.ReactNode;
  sessionId: string;
  connected: boolean;
}

const MainLayout: React.FC<MainLayoutProps> = ({
  children,
  sessionId,
  connected,
}) => {
  return (
    <div className="main-layout">

      <header className="main-layout__header">

        <div className="main-layout__brand">
          <div className="main-layout__logo">
            PSV
          </div>

          <div className="main-layout__brand-text">
            <div className="main-layout__title">
              Process Scheduling Visualizer
            </div>

            <div className="main-layout__subtitle">
              CPU Scheduling Simulation
            </div>
          </div>
        </div>

        <div className="main-layout__session">

          <div className="main-layout__session-id">
            <span>Session ID</span>
            <strong>{sessionId}</strong>
          </div>

          <div className="main-layout__connection">
            <span
              className={`main-layout__status-dot ${
                connected
                  ? "main-layout__status-dot--connected"
                  : "main-layout__status-dot--disconnected"
              }`}
            />

            <span>
              {connected ? "Connected" : "Disconnected"}
            </span>
          </div>

        </div>

      </header>

      <main className="main-layout__content">
        {children}
      </main>

    </div>
  );
};

export default MainLayout;