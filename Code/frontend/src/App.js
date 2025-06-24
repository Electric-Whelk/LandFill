import CyclePanel from "./Page_Elements/CyclePanel"
import MonteCarlo from "./Page_Elements/MonteCarlo"
import Output from "./Page_Elements/Output"
import PlayerInput from "./Page_Elements/PlayerInput"
import React, { useState, useEffect } from "react";

import './App.css';


const App = () => {
    const [allCycles, setAllCycles] = useState([])
    const [format, setFormat] = useState({})
    const [requestedQuantity, setRequestedQuantity] = useState(0)
    const [inputCards, setInputCards] = useState([])

    useEffect(() => {
        fetchCycles()
    }, []);


    const fetchCycles = async() => {
        const response = await fetch("http://127.0.0.1:5000/fetch_cycles")
        const data = await response.json()
        setAllCycles(data.cycles)
    }



    const lock = async (e) => {
        e.preventDefault()
        const url = "http://127.0.0.1:5000/lock"


        const options = {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({format, requestedQuantity, inputCards}),
        }

        const response = await fetch(url, options)
        const info = await response.json()
    }

    return (
        <div className="container">
            <PlayerInput lock={lock}
                         setFormat={setFormat}
                         setRequestedQuantity={setRequestedQuantity}
                         setInputCards={setInputCards}/>
            <MonteCarlo/>
            <Output/>
            <div className="landOptions">
                <CyclePanel cycles={allCycles}/>
            </div>
        </div>
    );
}

export default App;
