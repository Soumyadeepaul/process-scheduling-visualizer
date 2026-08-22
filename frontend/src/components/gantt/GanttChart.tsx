import React, { useEffect, useMemo, useState } from "react";
import type {
  SimulationSegment,
  SimulationSpeed,
} from "../../hooks/useSimulation";
import "./GanttChart.css";

interface GanttChartProps {
  messages: SimulationSegment[];
  simulationTime: number;
  speed: SimulationSpeed;
  paused: boolean;
  simulationStarted: boolean;
  resetKey: number;
}

interface TimelineSegment {
  processId: number | null;
  start: number;
  end: number;
}

const GanttChart: React.FC<GanttChartProps> = ({
  messages,
  simulationTime,
  paused,
  resetKey,
}) => {
  const [visibleTime, setVisibleTime] = useState(0);

  /*
   * --------------------------------
   * RESET
   * --------------------------------
   */
  useEffect(() => {
    setVisibleTime(0);
  }, [resetKey]);

  /*
   * --------------------------------
   * FOLLOW SIMULATION CLOCK
   * --------------------------------
   *
   * Gantt uses the same simulation clock
   * as the SimulationVisualization.
   *
   * When paused, do not update the Gantt
   * from a changing clock.
   */
  useEffect(() => {
    if (!paused) {
      setVisibleTime(simulationTime);
    }
  }, [simulationTime, paused]);

  /*
   * --------------------------------
   * SORT MESSAGES
   * --------------------------------
   */
  const sortedMessages = useMemo(() => {
    return [...messages].sort(
      (a, b) => a.start - b.start
    );
  }, [messages]);

  /*
   * --------------------------------
   * BUILD VISIBLE TIMELINE
   * --------------------------------
   *
   * Backend sends only PROCESS_START.
   *
   * Therefore IDLE is generated from:
   *
   * 0 -> first process
   * process end -> next process
   * last process end -> current clock
   */
  const timeline = useMemo<TimelineSegment[]>(() => {
    const result: TimelineSegment[] = [];

    /*
     * No process message has arrived yet.
     *
     * If simulation time has started,
     * everything is currently IDLE.
     */
    if (sortedMessages.length === 0) {
      if (visibleTime > 0) {
        result.push({
          processId: null,
          start: 0,
          end: visibleTime,
        });
      }

      return result;
    }

    let previousEnd = 0;

    for (const message of sortedMessages) {
      /*
       * This process has not started yet.
       */
      if (message.start > visibleTime) {
        break;
      }

      /*
       * --------------------------------
       * IDLE BEFORE PROCESS
       * --------------------------------
       */
      if (message.start > previousEnd) {
        const idleEnd = Math.min(
          message.start,
          visibleTime
        );

        if (idleEnd > previousEnd) {
          result.push({
            processId: null,
            start: previousEnd,
            end: idleEnd,
          });
        }

        /*
         * Clock is currently inside
         * this idle period.
         */
        if (visibleTime < message.start) {
          return result;
        }
      }

      /*
       * --------------------------------
       * PROCESS
       * --------------------------------
       */
      const processEnd = Math.min(
        message.end,
        visibleTime
      );

      if (processEnd > message.start) {
        result.push({
          processId: message.process_id,
          start: message.start,
          end: processEnd,
        });
      }

      /*
       * Keep the REAL backend end time.
       *
       * This is important for detecting
       * the next idle period.
       */
      previousEnd = Math.max(
        previousEnd,
        message.end
      );

      /*
       * Clock is currently inside this
       * process. Nothing after it should
       * be rendered yet.
       */
      if (visibleTime < message.end) {
        return result;
      }
    }

    /*
     * --------------------------------
     * IDLE AFTER LAST PROCESS
     * --------------------------------
     *
     * Example:
     *
     * P4 ends at 4
     * current clock = 7
     *
     * 4 -> 7 becomes IDLE.
     */
    if (visibleTime > previousEnd) {
      result.push({
        processId: null,
        start: previousEnd,
        end: visibleTime,
      });
    }

    return result;
  }, [
    sortedMessages,
    visibleTime,
  ]);

  /*
   * --------------------------------
   * CURRENT SEGMENT
   * --------------------------------
   */
  const currentSegmentIndex = useMemo(() => {
    return timeline.findIndex(
      (segment) =>
        visibleTime >= segment.start &&
        visibleTime < segment.end
    );
  }, [
    timeline,
    visibleTime,
  ]);

  /*
   * --------------------------------
   * RENDER
   * --------------------------------
   */
  return (
    <div className="gantt-chart">

      <div className="gantt-chart__title">
        LIVE GANTT CHART
      </div>

      {!timeline.length ? (
        <div className="gantt-chart__empty">
          Gantt chart will appear when simulation starts
        </div>
      ) : (
        <>

          {/* --------------------------------
              GANTT TIMELINE
          -------------------------------- */}
          <div className="gantt-chart__timeline">

            {timeline.map(
              (segment, index) => {

                const duration =
                  segment.end -
                  segment.start;

                if (duration <= 0) {
                  return null;
                }

                const isCurrent =
                  index === currentSegmentIndex;

                /*
                 * Completed segments are full.
                 *
                 * Current segment fills according
                 * to the simulation clock.
                 */
                let fillPercentage = 100;

                if (isCurrent) {
                  const elapsed =
                    visibleTime -
                    segment.start;

                  fillPercentage =
                    Math.min(
                      100,
                      Math.max(
                        0,
                        (elapsed / duration) * 100
                      )
                    );
                }

                return (
                  <div
                    className={`gantt-segment ${
                      segment.processId === null
                        ? "gantt-segment--idle"
                        : "gantt-segment--process"
                    }`}
                    key={`${segment.start}-${segment.end}-${index}`}
                    style={{
                      flexGrow: duration,
                    }}
                  >

                    {/* ANIMATION / FILL */}
                    <div
                      className="gantt-segment__fill"
                      style={{
                        width:
                          `${fillPercentage}%`,
                      }}
                    />

                    {/* LABEL */}
                    <div className="gantt-segment__label">
                      {segment.processId === null
                        ? "IDLE"
                        : `P${segment.processId}`}
                    </div>

                  </div>
                );
              }
            )}

          </div>

          {/* --------------------------------
              TIME AXIS
          -------------------------------- */}
          <div className="gantt-chart__time-axis">

            {timeline.map(
              (segment, index) => {

                const totalTime =
                  Math.max(
                    visibleTime,
                    1
                  );

                const position =
                  (segment.start / totalTime) *
                  100;

                /*
                 * Do not render a duplicate
                 * marker at the current end.
                 */
                if (
                  Math.abs(
                    segment.start -
                    visibleTime
                  ) < 0.000001
                ) {
                  return null;
                }

                return (
                  <div
                    className="gantt-time-marker"
                    key={`${segment.start}-${index}`}
                    style={{
                      left: `${position}%`,
                    }}
                  >
                    {segment.start.toFixed(3)}
                  </div>
                );
              }
            )}

            <div
              className="gantt-time-marker gantt-time-marker--end"
              style={{
                left: "100%",
              }}
            >
              {visibleTime.toFixed(3)}
            </div>

          </div>

        </>
      )}

    </div>
  );
};

export default GanttChart;