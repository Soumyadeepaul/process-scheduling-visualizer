import React from "react";
import type { SimulationSegment } from "../../hooks/useSimulation";

interface EventLogProps {
  messages: SimulationSegment[];
}

const EventLog: React.FC<EventLogProps> = ({ messages }) => {
  return (
    <div>
      <div className="dashboard-card__title">EVENT LOG</div>

      <div className="event-log">
        {messages.length === 0 ? (
          <div>No simulation events yet.</div>
        ) : (
          messages.map((message, index) => (
            <div className="event-log__item" key={`${message.process_id}-${message.start}-${index}`}>
              P{message.process_id} executed from {message.start} to {message.end} ({message.state})
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default EventLog;