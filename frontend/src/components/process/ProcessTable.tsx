import React, { useState } from "react";
import type { Process } from "../../pages/Dashboard";
import "./ProcessTable.css";

interface ProcessTableProps {
  processes: Process[];
  sentProcessIds: number[];
  sessionId: string;
  algorithm: string;
  timeQuantum: number | null;
  onAlgorithmChange: (algorithm: string) => void;
  onTimeQuantumChange: (timeQuantum: number | null) => void;
  onAddProcess: (process: Process) => void;
  onRemoveProcess: (processId: number) => void;
  onProcessesSent: React.Dispatch<React.SetStateAction<number[]>>;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

const ProcessTable: React.FC<ProcessTableProps> = ({ processes, sentProcessIds, sessionId, algorithm, timeQuantum, onAlgorithmChange, onTimeQuantumChange, onAddProcess, onRemoveProcess, onProcessesSent }) => {
  const [showForm, setShowForm] = useState(false);
  const [pid, setPid] = useState("");
  const [arrivalTime, setArrivalTime] = useState("");
  const [burstTime, setBurstTime] = useState("");
  const [priority, setPriority] = useState("");
  const [sending, setSending] = useState(false);
  const [sendingAlgorithm, setSendingAlgorithm] = useState(false);

  const addProcess = () => {
    if (pid === "" || arrivalTime === "" || burstTime === "" || priority === "") return;

    onAddProcess({ id: Number(pid), arrival_time: Number(arrivalTime), burst_time: Number(burstTime), priority: Number(priority) });
    setPid("");
    setArrivalTime("");
    setBurstTime("");
    setPriority("");
    setShowForm(false);
  };

  const sendProcesses = async () => {
    const unsentProcesses = processes.filter((process) => !sentProcessIds.includes(process.id));

    if (!unsentProcesses.length) {
      alert("No new processes to send.");
      return;
    }

    try {
      setSending(true);

      const response = await fetch(`${API_BASE_URL}/processes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, data: unsentProcesses }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) throw new Error(result.message || "Failed to send processes");

      onProcessesSent((previous) => [...previous, ...unsentProcesses.map((process) => process.id)]);
      alert("New processes uploaded.");
    } catch (error) {
      console.error("Failed to send processes:", error);
      alert("Failed to send processes.");
    } finally {
      setSending(false);
    }
  };

  const sendAlgorithm = async () => {
    if (algorithm === "ROUND_ROBIN" && (!timeQuantum || timeQuantum < 1)) {
      alert("Enter a valid time quantum.");
      return;
    }

    try {
      setSendingAlgorithm(true);

      const response = await fetch(`${API_BASE_URL}/scheduler`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, data: { algorithm, time_quantum: algorithm === "ROUND_ROBIN" ? timeQuantum : null } }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) throw new Error(result.message || "Failed to send algorithm");

      alert("Algorithm uploaded.");
    } catch (error) {
      console.error("Failed to send algorithm:", error);
      alert("Failed to send algorithm.");
    } finally {
      setSendingAlgorithm(false);
    }
  };

  return (
    <div className="process-table">
      <div className="process-table__title">PROCESS TABLE</div>

      <button className="process-table__add-button" onClick={() => setShowForm(true)}>+ Add Process</button>

      <label className="process-table__label">Algorithm</label>

      <select className="process-table__select" value={algorithm} onChange={(event) => onAlgorithmChange(event.target.value)}>
        <option value="FCFS">FCFS</option>
        <option value="SJF">SJF</option>
        <option value="SRTF">SRTF</option>
        <option value="PRIORITY">PRIORITY</option>
        <option value="PRIORITY_PREEMPTIVE">PRIORITY PREEMPTIVE</option>
        <option value="ROUND_ROBIN">ROUND ROBIN</option>
      </select>

      {algorithm === "ROUND_ROBIN" && (
        <div className="time-quantum">
          <label>Time Quantum</label>
          <input type="number" min="1" value={timeQuantum ?? ""} onChange={(event) => onTimeQuantumChange(event.target.value === "" ? null : Number(event.target.value))} />
        </div>
      )}

      <button className="process-table__send-button" onClick={sendAlgorithm} disabled={sendingAlgorithm}>
        {sendingAlgorithm ? "Sending..." : "Send Algorithm"}
      </button>

      <button className="process-table__send-button" onClick={sendProcesses} disabled={sending || !processes.length}>
        {sending ? "Sending..." : "Send Process"}
      </button>

      <div className="process-table__rows">
        {!processes.length ? (
          <div className="process-table__empty">Process rows appear here</div>
        ) : (
          processes.map((process) => {
            const isSent = sentProcessIds.includes(process.id);

            return (
              <div className="process-row" key={process.id}>
                <span>P{process.id}</span>
                <span>AT: {process.arrival_time}</span>
                <span>BT: {process.burst_time}</span>
                <span>Priority: {process.priority}</span>
                <button className="process-row__delete" disabled={isSent} onClick={() => onRemoveProcess(process.id)}>×</button>
              </div>
            );
          })
        )}
      </div>

      {showForm && (
        <div className="process-form-overlay">
          <div className="process-form">
            <div className="process-form__header">
              <h3>Add Process</h3>
              <button className="process-form__close" onClick={() => setShowForm(false)}>×</button>
            </div>

            <div className="process-form__field"><label>PID</label><input type="number" min="1" value={pid} onChange={(event) => setPid(event.target.value)} /></div>
            <div className="process-form__field"><label>Arrival Time</label><input type="number" min="0" value={arrivalTime} onChange={(event) => setArrivalTime(event.target.value)} /></div>
            <div className="process-form__field"><label>Burst Time</label><input type="number" min="1" value={burstTime} onChange={(event) => setBurstTime(event.target.value)} /></div>
            <div className="process-form__field"><label>Priority</label><input type="number" min="1" value={priority} onChange={(event) => setPriority(event.target.value)} /></div>

            <button className="process-form__submit" onClick={addProcess}>Add Process</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProcessTable;