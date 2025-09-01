import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const Page2p5 = () => {
    const [status, setStatus] = useState("running");
    const [logs, setLogs] = useState([]);
    const location = useLocation();
    const navigate = useNavigate();
    const { task_id } = location.state;  // must be passed from previous page

    useEffect(() => {
        if (!task_id) return;

        const interval = setInterval(async () => {
            try {
                const res = await fetch(`/status/${task_id}`);
                const { status, logs } = await res.json();

                setLogs(logs || []);   // keep frontend logs in sync
                setStatus(status);

                if (status === "done") {
                    clearInterval(interval);
                    const resultRes = await fetch(`/result/${task_id}`);
                    const result = await resultRes.json();
                    navigate("/page3", { state: { data: result } });
                }
            } catch (err) {
                console.error("Polling error:", err);
            }
        }, 1000);

        return () => clearInterval(interval);
    }, [task_id, navigate]);

    return (
        <div>
            <h2>Simulation running...</h2>
            <pre>{logs.join("\n")}</pre>
        </div>
    );
};

export default Page2p5;
