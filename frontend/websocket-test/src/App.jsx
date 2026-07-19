import { useState, useRef } from "react";

const API = "http://127.0.0.1:8000/api/v1";
const WS = "ws://127.0.0.1:8000/api/v1";

function App() {

    const socketRef = useRef(null);

    // -------------------------
    // Session
    // -------------------------

    const [sessionId, setSessionId] = useState("");

    const generateSession = async () => {

        try {

            const response = await fetch(`${API}/session`, {
                method: "POST",
            });

            const result = await response.json();

            console.log(result);

            if (result.success) {

                setSessionId(result.data.session_id);

                setProcesses([]);

                setMessages([]);

                setProcessUploaded(false);

                setSchedulerUploaded(false);

                setConnected(false);

                setSimulationStarted(false);

                setPaused(false);

            }

        }
        catch (err) {

            console.error(err);

        }

    };

    // -------------------------
    // Scheduler
    // -------------------------

    const [algorithm, setAlgorithm] = useState("FCFS");

    const [timeQuantum, setTimeQuantum] = useState(2);

    // -------------------------
    // Processes
    // -------------------------

    const [processes, setProcesses] = useState([]);        // All processes
    const [sentProcesses, setSentProcesses] = useState([]); // Already uploaded

    const addProcess = () => {

        setProcesses([
            ...processes,
            {
                id: processes.length + 1,
                arrival_time: 0,
                burst_time: 1,
                priority: 1
            }
        ]);

    };

    const removeProcess = (index) => {

        setProcesses(
            processes.filter((_, i) => i !== index)
        );

    };

    const updateProcess = (index, field, value) => {

        const copy = [...processes];

        copy[index][field] = Number(value);

        setProcesses(copy);

    };

    // -------------------------
    // Upload Flags
    // -------------------------

    const [processUploaded, setProcessUploaded] = useState(false);

    const [schedulerUploaded, setSchedulerUploaded] = useState(false);

    // -------------------------
    // Send Processes
    // -------------------------

    const sendProcesses = async () => {
        // Only send processes that haven't been sent yet
        const unsentProcesses = processes.filter(
            p => !sentProcesses.some(sp => sp.id === p.id)
        );

        if (unsentProcesses.length === 0) {
            alert("No new processes to upload");
            return;
        }

        try {
            const response = await fetch(`${API}/processes`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    data: unsentProcesses,
                }),
            });

            const result = await response.json();

            if (result.success) {
                alert("New Processes Uploaded");

                // Mark these processes as sent
                setSentProcesses(prev => [...prev, ...unsentProcesses]);

                setProcessUploaded(true);
            }
        } catch (err) {
            console.error(err);
        }
    };

    // -------------------------
    // Send Scheduler
    // -------------------------

    const sendScheduler = async () => {

        try {

            const response = await fetch(`${API}/scheduler`, {

                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    session_id: sessionId,

                    data: {

                        algorithm,

                        time_quantum: timeQuantum

                    }

                })

            });

            const result = await response.json();

            console.log(result);

            if (result.success) {

                alert("Scheduler Updated");

                setSchedulerUploaded(true);

            }

        }

        catch (err) {

            console.error(err);

        }

    };
        // -------------------------
    // WebSocket State
    // -------------------------

    const [connected, setConnected] = useState(false);

    const [simulationStarted, setSimulationStarted] = useState(false);

    const [paused, setPaused] = useState(false);

    const [messages, setMessages] = useState([]);

    const [speed, setSpeed] = useState(1);

    const changeSpeed = (newSpeed) => {

        setSpeed(newSpeed);

        if (!socketRef.current) return;

        socketRef.current.send(
            JSON.stringify({
                action: "SPEED",
                speed: newSpeed
            })
        );

    };

    // -------------------------
    // Connect
    // -------------------------

    const connect = () => {

        if (sessionId === "") {

            alert("Generate Session First");

            return;

        }

        const socket = new WebSocket(

            `${WS}/ws/${sessionId}`

        );

        socket.onopen = () => {

            console.log("Connected");

            setConnected(true);

        };

        socket.onmessage = (event) => {

            console.log(event.data);

            try {

                const msg = JSON.parse(event.data);

                setMessages((prev) => [...prev, msg]);

            }

            catch {

                setMessages((prev) => [...prev, event.data]);

            }

        };

        socket.onclose = () => {

            console.log("Disconnected");

            setConnected(false);

            socketRef.current = null;

        };

        socket.onerror = (err) => {

            console.error(err);

        };

        socketRef.current = socket;

    };

    // -------------------------
    // Disconnect
    // -------------------------

    const disconnect = () => {

        socketRef.current?.close();

    };

    // -------------------------
    // Send Action
    // -------------------------

    const sendAction = (action) => {

        if (!socketRef.current) return;

        socketRef.current.send(

            JSON.stringify({

                action

            })

        );

    };

    // -------------------------
    // PLAY
    // -------------------------

    const play = () => {

        sendAction("PLAY");

        setSimulationStarted(true);

        setPaused(false);

    };

    // -------------------------
    // PAUSE
    // -------------------------

    const pause = () => {

        sendAction("PAUSE");

        setPaused(true);

    };

    // -------------------------
    // RESUME
    // -------------------------

    const resume = () => {

        sendAction("RESUME");

        setPaused(false);

    };

    // -------------------------
    // RESET
    // -------------------------

    const reset = () => {

        sendAction("RESET");

        setSimulationStarted(false);

        setPaused(false);

        setMessages([]);

    };

    const [metrics, setMetrics] = useState(null);

    const fetchMetrics = async () => {

    try {

        const response = await fetch(
            `${API}/metrics?session_id=${sessionId}`
        );

        const result = await response.json();

        if (result.success) {
            setMetrics(result.data);
        }
        else {
            alert("Failed to fetch metrics.");
        }

    }
    catch (err) {

        console.error(err);

    }

};

    return (

<div
    style={{
        padding: "30px",
        maxWidth: "1100px",
        margin: "auto",
        fontFamily: "Arial"
    }}
>

    <h1>Scheduling Visualizer Tester</h1>

    <hr />

    {/* ---------------- Session ---------------- */}

    <h2>Session</h2>

    <button onClick={generateSession}>
        Generate Session
    </button>

    <input
        style={{
            marginLeft: "15px",
            width: "400px",
            padding: "6px"
        }}
        value={sessionId}
        readOnly
    />

    <hr />

    {/* ---------------- Scheduler ---------------- */}

    <h2>Scheduler</h2>

    <label>

        Algorithm

    </label>

    <select

        value={algorithm}

        onChange={(e) => setAlgorithm(e.target.value)}

        style={{ marginLeft: "10px" }}

    >

        <option value="FCFS">FCFS</option>

        <option value="SJF">SJF</option>

        <option value="SRTF">SRTF</option>

        <option value="PRIORITY">Priority</option>

        <option value="PRIORITY_PREEMPTIVE">
            Priority Preemptive
        </option>

        <option value="ROUND_ROBIN">
            Round Robin
        </option>

    </select>

    {

        algorithm === "ROUND_ROBIN" &&

        <>

            <span style={{ marginLeft: "20px" }}>

                Time Quantum

            </span>

            <input

                type="number"

                value={timeQuantum}

                onChange={(e) =>
                    setTimeQuantum(Number(e.target.value))
                }

                style={{
                    width: "80px",
                    marginLeft: "10px"
                }}

            />

        </>

    }

    <button

        onClick={sendScheduler}

        disabled={sessionId === ""}

        style={{ marginLeft: "20px" }}

    >

        Send Scheduler

    </button>

    <hr />

    {/* ---------------- Processes ---------------- */}

    <h2>Processes</h2>

    <button

        onClick={addProcess}

        disabled={sessionId === ""}

    >

        Add Process

    </button>

    <table

        border="1"

        cellPadding="8"

        style={{

            width: "100%",

            marginTop: "20px",

            borderCollapse: "collapse"

        }}

    >

        <thead>

            <tr>

                <th>PID</th>

                <th>Arrival Time</th>

                <th>Burst Time</th>

                <th>Priority</th>

                <th>Delete</th>

            </tr>

        </thead>

        <tbody>

        {

            processes.map((process, index) => (

                <tr key={index}>

                    <td>

                        <input

                            type="number"

                            value={process.id}

                            onChange={(e) =>
                                updateProcess(
                                    index,
                                    "id",
                                    e.target.value
                                )
                            }

                        />

                    </td>

                    <td>

                        <input

                            type="number"

                            value={process.arrival_time}

                            onChange={(e) =>
                                updateProcess(
                                    index,
                                    "arrival_time",
                                    e.target.value
                                )
                            }

                        />

                    </td>

                    <td>

                        <input

                            type="number"

                            value={process.burst_time}

                            onChange={(e) =>
                                updateProcess(
                                    index,
                                    "burst_time",
                                    e.target.value
                                )
                            }

                        />

                    </td>

                    <td>

                        <input

                            type="number"

                            value={process.priority}

                            onChange={(e) =>
                                updateProcess(
                                    index,
                                    "priority",
                                    e.target.value
                                )
                            }

                        />

                    </td>

                    <td>

                        <button

                            onClick={() =>
                                removeProcess(index)
                            }

                        >

                            Remove

                        </button>

                    </td>

                </tr>

            ))

        }

        </tbody>

    </table>

    <br />

    <button

        onClick={sendProcesses}

        disabled={

            sessionId === "" ||

            processes.length === 0

        }

    >

        Send Processes

    </button>

    <hr />

        {/* ---------------- Connection ---------------- */}

    <h2>Connection</h2>

    <button

        onClick={connect}

        disabled={

            connected ||

            !processUploaded ||

            !schedulerUploaded

        }

    >

        Connect

    </button>

    <button

        onClick={disconnect}

        disabled={!connected}

        style={{ marginLeft: "10px" }}

    >

        Disconnect

    </button>

    <p>

        <strong>Status : </strong>

        {

            connected ?

            "🟢 Connected"

            :

            "🔴 Disconnected"

        }

    </p>

    <hr />

    {/* ---------------- Controls ---------------- */}

    <h2>Simulation Controls</h2>

    <button

        onClick={play}

        disabled={

            !connected ||

            simulationStarted

        }

    >

        PLAY

    </button>

    <button

        onClick={pause}

        disabled={

            !connected ||

            paused ||

            !simulationStarted

        }

        style={{ marginLeft: "10px" }}

    >

        PAUSE

    </button>

    <button

        onClick={resume}

        disabled={

            !connected ||

            !paused

        }

        style={{ marginLeft: "10px" }}

    >

        RESUME

    </button>

    <button

        onClick={reset}

        disabled={!connected}

        style={{ marginLeft: "10px" }}

    >

        RESET

    </button>

    <hr />

    {/* ---------------- Messages ---------------- */}
    

    <h2>Speed</h2>

    <button
        onClick={() => changeSpeed(1)}
        disabled={!connected || speed === 1}
    >
        1×
    </button>

    <button
        onClick={() => changeSpeed(2)}
        disabled={!connected || speed === 2}
        style={{ marginLeft: "10px" }}
    >
        2×
    </button>

    <button
        onClick={() => changeSpeed(5)}
        disabled={!connected || speed === 5}
        style={{ marginLeft: "10px" }}
    >
        5×
    </button>

    <p>
        Current Speed : <strong>{speed}×</strong>
    </p>
    <hr />
    <h2>Messages</h2>

    <div

        style={{

            border: "1px solid #888",

            borderRadius: "6px",

            minHeight: "300px",

            maxHeight: "300px",

            overflowY: "auto",

            padding: "10px",

            background: "#f5f5f5"

        }}

    >

        {

            messages.length === 0 ?

            <p>No Messages Received</p>

            :

            messages.map((msg, index) => (

                <pre

                    key={index}

                    style={{

                        background: "white",

                        padding: "10px",

                        marginBottom: "10px",

                        borderRadius: "4px"

                    }}

                >

                    {

                        typeof msg === "object"

                        ?

                        JSON.stringify(msg, null, 2)

                        :

                        msg

                    }

                </pre>

            ))

        }

    </div>
    <button
        onClick={fetchMetrics}
        disabled={!connected}
        style={{ marginLeft: "10px" }}
    >
        SHOW METRICS
    </button>

    {
metrics && (

<>
    <hr />

    <h2>Metrics</h2>

    <table
        border="1"
        cellPadding="8"
        style={{
            width: "100%",
            borderCollapse: "collapse"
        }}
    >

        <thead>
            <tr>
                <th>PID</th>
                <th>Waiting</th>
                <th>Turnaround</th>
                <th>Response</th>
                <th>Completion</th>
            </tr>
        </thead>

        <tbody>

        {
            Object.keys(metrics.waiting_time.per_process).map(pid => (

                <tr key={pid}>
                    <td>{pid}</td>
                    <td>{metrics.waiting_time.per_process[pid]}</td>
                    <td>{metrics.turnaround_time.per_process[pid]}</td>
                    <td>{metrics.response_time.per_process[pid]}</td>
                    <td>{metrics.completion_time[pid]}</td>
                </tr>

            ))
        }

        </tbody>

    </table>

    <br />

    <table
        border="1"
        cellPadding="8"
        style={{
            width: "450px",
            borderCollapse: "collapse"
        }}
    >
        <tbody>

            <tr>
                <td><b>Average Waiting Time</b></td>
                <td>{metrics.waiting_time.average}</td>
            </tr>

            <tr>
                <td><b>Average Turnaround Time</b></td>
                <td>{metrics.turnaround_time.average}</td>
            </tr>

            <tr>
                <td><b>Average Response Time</b></td>
                <td>{metrics.response_time.average}</td>
            </tr>

            <tr>
                <td><b>CPU Utilization</b></td>
                <td>{metrics.cpu_utilization}%</td>
            </tr>

        </tbody>
    </table>

</>

)}

</div>

);

}

export default App;