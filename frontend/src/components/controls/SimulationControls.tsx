import React from "react";
import type { SimulationSpeed } from "../../hooks/useSimulation";
import "./SimulationControls.css";

interface SimulationControlsProps {
  connected: boolean;
  simulationStarted: boolean;
  paused: boolean;
  speed: SimulationSpeed;
  onConnect: () => void;
  onDisconnect: () => void;
  onPlay: () => void;
  onPause: () => void;
  onResume: () => void;
  onReset: () => void;
  onSpeedChange: (speed: SimulationSpeed) => void;
}

const SimulationControls: React.FC<SimulationControlsProps> = ({ connected, simulationStarted, paused, speed, onConnect, onDisconnect, onPlay, onPause, onResume, onReset, onSpeedChange }) => {
  return (
    <section className="simulation-controls">
      <div className="simulation-controls__left">
        <span className="simulation-controls__title">CONTROLS</span>

        <div className="simulation-controls__buttons">
          <button className="simulation-control-button" onClick={connected ? onDisconnect : onConnect}>
            <span className="control-icon">●</span>{connected ? "Disconnect" : "Connect"}
          </button>

          <button className="simulation-control-button" onClick={onPlay}>
            <span className="control-icon">▶</span>Play
          </button>

          <button className="simulation-control-button" onClick={onPause}>
            <span className="control-icon">Ⅱ</span>Pause
          </button>

          <button className="simulation-control-button" onClick={onResume}>
            <span className="control-icon">▶▶</span>Resume
          </button>

          <button className="simulation-control-button" onClick={onReset}>
            <span className="control-icon">↻</span>Reset
          </button>
        </div>
      </div>

      <div className="simulation-controls__right">
        <span className="simulation-controls__speed-title">SPEED</span>

        <div className="simulation-speed-buttons">
          <button className={`simulation-speed-button ${speed === 1 ? "simulation-speed-button--active" : ""}`} onClick={() => onSpeedChange(1)}>1×</button>
          <button className={`simulation-speed-button ${speed === 2 ? "simulation-speed-button--active" : ""}`} onClick={() => onSpeedChange(2)}>2×</button>
          <button className={`simulation-speed-button ${speed === 5 ? "simulation-speed-button--active" : ""}`} onClick={() => onSpeedChange(5)}>5×</button>
        </div>
      </div>
    </section>
  );
};

export default SimulationControls;