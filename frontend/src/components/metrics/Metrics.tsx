import React, { useState } from "react";
import "./Metrics.css";

interface MetricsProps {
  sessionId: string | null;
}

interface MetricBreakdown {
  average: number;
  per_process: Record<number, number>;
}

interface MetricsData {
  waiting_time: MetricBreakdown;
  turnaround_time: MetricBreakdown;
  response_time: MetricBreakdown;
  completion_time: Record<number, number>;
  cpu_utilization: number;
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api/v1";

const Metrics: React.FC<MetricsProps> = ({ sessionId }) => {

  const [metrics, setMetrics] = useState<MetricsData | null>(null);
  const [loading, setLoading] = useState(false);

  const generateMetrics = async () => {

    if (!sessionId) {
      alert("Session is not available.");
      return;
    }

    try {

      setLoading(true);

      const response = await fetch(
        `${API_BASE_URL}/metrics?session_id=${encodeURIComponent(sessionId)}`
      );

      const result = await response.json();

      console.log("Metrics data:", result);

      if (!response.ok || !result.success) {
        throw new Error(
          result.message || "Failed to fetch metrics"
        );
      }

      setMetrics(result.data);

    } catch (error) {

      console.error("Failed to fetch metrics:", error);

      alert("Failed to generate metrics.");

    } finally {

      setLoading(false);

    }
  };

  const completionTime =
    metrics?.completion_time
      ? Math.max(
          ...Object.values(metrics.completion_time).map(Number)
        )
      : null;

  return (
    <div className="metrics-section">

      <div className="metrics-section__title">
        METRICS
      </div>

      <button
        className="metrics-section__button"
        onClick={generateMetrics}
        disabled={loading || !sessionId}
      >
        {loading ? "Generating..." : "Generate Metrics"}
      </button>

      <div className="metrics-grid">

        <div className="metric-box">
          <span>Waiting Time</span>
          <strong>
            {metrics?.waiting_time?.average ?? "-"}
          </strong>
        </div>

        <div className="metric-box">
          <span>Turnaround Time</span>
          <strong>
            {metrics?.turnaround_time?.average ?? "-"}
          </strong>
        </div>

        <div className="metric-box">
          <span>Response Time</span>
          <strong>
            {metrics?.response_time?.average ?? "-"}
          </strong>
        </div>

        <div className="metric-box">
          <span>Completion Time</span>
          <strong>
            {completionTime ?? "-"}
          </strong>
        </div>

        <div className="metric-box">
          <span>CPU Utilization</span>
          <strong>
            {metrics?.cpu_utilization != null
              ? `${Number(metrics.cpu_utilization).toFixed(2)}%`
              : "-"}
          </strong>
        </div>

      </div>

    </div>
  );
};

export default Metrics;