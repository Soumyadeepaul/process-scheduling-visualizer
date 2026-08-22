import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

export type SimulationSpeed = 1 | 2 | 5;

export interface SimulationSegment {
  type?: string;
  process_id: number;
  start: number;
  end: number;
  state: "ready" | "completed";
}

const WS_BASE_URL =
  import.meta.env.VITE_WS_BASE_URL ||
  "ws://127.0.0.1:8000/api/v1";

export const useSimulation = (sessionId: string) => {

  const socketRef =
    useRef<WebSocket | null>(null);

  /*
   * --------------------------------
   * CONNECTION STATE
   * --------------------------------
   */

  const [connected, setConnected] =
    useState(false);

  const [simulationStarted, setSimulationStarted] =
    useState(false);

  const [paused, setPaused] =
    useState(false);


  /*
   * --------------------------------
   * SIMULATION SPEED
   * --------------------------------
   */

  const [speed, setSpeed] =
    useState<SimulationSpeed>(1);


  /*
   * --------------------------------
   * SIMULATION DATA
   * --------------------------------
   */

  const [messages, setMessages] =
    useState<SimulationSegment[]>([]);


  /*
   * --------------------------------
   * SIMULATION CLOCK
   * --------------------------------
   *
   * simulationTime is the frontend
   * simulation clock.
   *
   * It represents CPU simulation time,
   * NOT real wall-clock time.
   */

  const [simulationTime, setSimulationTime] =
    useState(0);


  /*
   * Keep the current simulation time
   * in a ref as well.
   *
   * This allows the animation clock to
   * update without depending on stale
   * state values.
   */

  const simulationTimeRef =
    useRef(0);


  /*
   * Timestamp of the previous animation
   * frame.
   */

  const lastFrameTimeRef =
    useRef<number | null>(null);


  /*
   * --------------------------------
   * CONNECT
   * --------------------------------
   */

  const connect = useCallback(() => {

    if (
      !sessionId ||
      socketRef.current
    ) {
      return;
    }

    const socket = new WebSocket(
      `${WS_BASE_URL}/ws/${sessionId}`
    );


    socket.onopen = () => {

      setConnected(true);

    };


    socket.onmessage = (event) => {

      try {

        const message =
          JSON.parse(event.data);


        /*
         * --------------------------------
         * PROCESS START
         * --------------------------------
         */

        if (
          message.type ===
          "PROCESS_START"
        ) {

          const segment =
            message.data as SimulationSegment;


          /*
           * Store the segment.
           */

          setMessages(
            (previous) => [
              ...previous,
              segment,
            ]
          );


          setSimulationStarted(true);


          /*
           * --------------------------------
           * SYNCHRONIZE CLOCK
           * --------------------------------
           *
           * The backend tells us that this
           * process starts at `segment.start`.
           *
           * Never move the frontend clock
           * backwards.
           *
           * This is important during:
           *
           *     IDLE -> PROCESS
           *
           * transition.
           */

          const currentTime =
            simulationTimeRef.current;


          if (
            segment.start >
            currentTime
          ) {

            simulationTimeRef.current =
              segment.start;

            setSimulationTime(
              segment.start
            );

          }

        }


        /*
         * --------------------------------
         * SIMULATION COMPLETE
         * --------------------------------
         */

        if (
          message.type ===
          "SIMULATION_COMPLETE"
        ) {

          /*
           * Make sure the clock reaches
           * the end of the final segment.
           */

          setMessages(
            (previous) => {

              if (
                previous.length === 0
              ) {
                return previous;
              }

              const finalSegment =
                previous[
                  previous.length - 1
                ];

              const finalTime =
                finalSegment.end;


              if (
                simulationTimeRef.current <
                finalTime
              ) {

                simulationTimeRef.current =
                  finalTime;

                setSimulationTime(
                  finalTime
                );

              }

              return previous;

            }
          );


          setSimulationStarted(false);

          setPaused(false);

          lastFrameTimeRef.current =
            null;

        }

      } catch (error) {

        console.error(
          "Invalid WebSocket message:",
          error
        );

      }

    };


    socket.onclose = () => {

      socketRef.current = null;

      setConnected(false);

      lastFrameTimeRef.current =
        null;

    };


    socket.onerror = (error) => {

      console.error(
        "WebSocket error:",
        error
      );

    };


    socketRef.current = socket;

  }, [sessionId]);


  /*
   * --------------------------------
   * DISCONNECT
   * --------------------------------
   */

  const disconnect = useCallback(() => {

    socketRef.current?.close();

    socketRef.current = null;

    setConnected(false);

    lastFrameTimeRef.current =
      null;

  }, []);


  /*
   * --------------------------------
   * SEND ACTION
   * --------------------------------
   */

  const sendAction = useCallback(
    (
      action: string,
      extra: Record<string, unknown> = {}
    ) => {

      if (
        !socketRef.current ||
        socketRef.current.readyState !==
          WebSocket.OPEN
      ) {
        return;
      }

      socketRef.current.send(
        JSON.stringify({
          action,
          ...extra,
        })
      );

    },
    []
  );


  /*
   * --------------------------------
   * PLAY
   * --------------------------------
   */

  const play = useCallback(() => {

    if (!connected) {
      return;
    }

    setSimulationStarted(true);

    setPaused(false);

    /*
     * Start a fresh frame interval.
     *
     * We intentionally do not reset
     * simulationTime here because PLAY
     * may be used after a previous pause.
     */

    lastFrameTimeRef.current =
      null;

    sendAction("PLAY");

  }, [
    connected,
    sendAction,
  ]);


  /*
   * --------------------------------
   * PAUSE
   * --------------------------------
   */

  const pause = useCallback(() => {

    if (!connected) {
      return;
    }

    setPaused(true);

    /*
     * Stop measuring elapsed wall time.
     */

    lastFrameTimeRef.current =
      null;

    sendAction("PAUSE");

  }, [
    connected,
    sendAction,
  ]);


  /*
   * --------------------------------
   * RESUME
   * --------------------------------
   */

  const resume = useCallback(() => {

    if (!connected) {
      return;
    }

    setPaused(false);

    /*
     * Start measuring elapsed time
     * again from the moment of resume.
     */

    lastFrameTimeRef.current =
      null;

    sendAction("RESUME");

  }, [
    connected,
    sendAction,
  ]);


  /*
   * --------------------------------
   * RESET
   * --------------------------------
   */

  const reset = useCallback(() => {

    if (!connected) {
      return;
    }

    sendAction("RESET");


    /*
     * Clear all received segments.
     */

    setMessages([]);


    /*
     * Stop simulation.
     */

    setSimulationStarted(false);

    setPaused(false);


    /*
     * Reset simulation clock.
     */

    simulationTimeRef.current = 0;

    setSimulationTime(0);


    /*
     * Reset animation timing.
     */

    lastFrameTimeRef.current =
      null;

  }, [
    connected,
    sendAction,
  ]);


  /*
   * --------------------------------
   * SPEED
   * --------------------------------
   */

  const changeSpeed = useCallback(
    (
      newSpeed: SimulationSpeed
    ) => {

      setSpeed(newSpeed);

      /*
       * Reset frame timestamp so changing
       * speed does not create a large jump
       * in simulation time.
       */

      lastFrameTimeRef.current =
        null;

      sendAction(
        "SPEED",
        {
          speed: newSpeed,
        }
      );

    },
    [sendAction]
  );


  /*
   * --------------------------------
   * SIMULATION CLOCK
   * --------------------------------
   *
   * This is the important part.
   *
   * The clock runs independently of
   * WebSocket messages.
   *
   * Therefore it can represent:
   *
   *     PROCESS
   *     IDLE
   *     PROCESS
   *     IDLE
   *
   * even though the backend sends
   * no message for IDLE.
   */

  useEffect(() => {

    if (
      !simulationStarted ||
      paused
    ) {

      lastFrameTimeRef.current =
        null;

      return;

    }


    let animationFrameId:
      number;


    const updateClock = (
      currentFrameTime: number
    ) => {

      /*
       * First frame after PLAY/RESUME/
       * SPEED CHANGE.
       */

      if (
        lastFrameTimeRef.current ===
        null
      ) {

        lastFrameTimeRef.current =
          currentFrameTime;

      } else {

        /*
         * Real elapsed time in seconds.
         */

        const elapsedSeconds =
          (
            currentFrameTime -
            lastFrameTimeRef.current
          ) / 1000;


        lastFrameTimeRef.current =
          currentFrameTime;


        /*
         * Convert real time into
         * simulation time.
         *
         * 1x -> 1 simulation second
         *       per real second
         *
         * 2x -> 2 simulation seconds
         *       per real second
         *
         * 5x -> 5 simulation seconds
         *       per real second
         */

        const simulationIncrement =
          elapsedSeconds * speed;


        const nextTime =
          simulationTimeRef.current +
          simulationIncrement;


        simulationTimeRef.current =
          nextTime;

        setSimulationTime(
          nextTime
        );

      }


      animationFrameId =
        window.requestAnimationFrame(
          updateClock
        );

    };


    animationFrameId =
      window.requestAnimationFrame(
        updateClock
      );


    return () => {

      window.cancelAnimationFrame(
        animationFrameId
      );

      lastFrameTimeRef.current =
        null;

    };

  }, [
    simulationStarted,
    paused,
    speed,
  ]);


  /*
   * --------------------------------
   * CLEANUP
   * --------------------------------
   */

  useEffect(() => {

    return () => {

      socketRef.current?.close();

      socketRef.current = null;

      lastFrameTimeRef.current =
        null;

    };

  }, []);


  /*
   * --------------------------------
   * RETURN
   * --------------------------------
   */

  return {

    connected,

    simulationStarted,

    paused,

    speed,

    messages,

    simulationTime,

    connect,

    disconnect,

    play,

    pause,

    resume,

    reset,

    setSpeed: changeSpeed,

  };

};