import CyclePanel from "./Page_Elements/CyclePanel"
import MonteCarlo from "./Page_Elements/MonteCarlo"
import Output from "./Page_Elements/Output"
import PlayerInput from "./Page_Elements/PlayerInput"
import React, { useState, useEffect } from "react";

import './App.css';


const App = () => {
    //used on the homepage
    const [allCycles, setAllCycles] = useState([])

    //passed to PlayerInput
    const [format, setFormat] = useState({})
    const [requestedQuantity, setRequestedQuantity] = useState(0)
    const [inputCards, setInputCards] = useState("")

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

    //passed to MonteCarlo
    const [budget, setBudget] = useState(0                                                  )
    const [maxPricePerCard, setMaxPricePerCard] = useState(0)
    const [currency, setCurrency] = useState("GBP")
    const [painThreshold, setPainThreshold] = useState(0)
    const [minBasics, setMinBasics] = useState(0)

    const run = async (e) => {
        console.log("Currency: " + currency)
        e.preventDefault()
        const url = "http://127.0.0.1:5000/run"

        const options = {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({budget,
                maxPricePerCard,
                currency,
                painThreshold,
                minBasics}),
        }

        const response = await fetch(url, options)
        const data = await response.json()
        setOutputCards(data.response.cards)
        console.log(outputCards)
    }

    const options = {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({format, requestedQuantity, inputCards}),
    }

    //passed to output
    const [outputCards, setOutputCards] = useState([])




    //used here
    useEffect(() => {
        fetchCycles()
    }, []);


    const fetchCycles = async() => {
        const response = await fetch("http://127.0.0.1:5000/fetch_cycles")
        const data = await response.json()
        setAllCycles(data.cycles)
    }

    return (
        <div className="container">
            <PlayerInput lock={lock}
                         setFormat={setFormat}
                         format = {format}
                         setRequestedQuantity={setRequestedQuantity}
                         setInputCards={setInputCards}
                         inputCards = {inputCards}
                         requestedQuantity={requestedQuantity}/>
            <MonteCarlo run={run}
                        setBudget={setBudget}
                        setMaxPricePerCard={setMaxPricePerCard}
                        setCurrency={setCurrency}
                        setPainThreshold={setPainThreshold}
                        setMinBasics={setMinBasics}/>
            <Output outputCards = { outputCards }/>
            <div className="landOptions">
                <CyclePanel cycles={allCycles}/>
            </div>
        </div>
    );
}

export default App;
