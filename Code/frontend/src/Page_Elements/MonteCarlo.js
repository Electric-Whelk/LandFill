import React from "react"
import { useState, useEffect } from "react"


const MonteCarlo = ({ run, setBudget, setMaxPricePerCard, setCurrency, setPainThreshold, setMinBasics }) => {


    return (
        <div id="montecarlo">
            <div>
                <button type="button" onClick={run}>Run</button>
            </div>

            <div>
                <label htmlFor="budget">Budget</label>
                <input type="number" id="budget" name="budget"
                onChange={(e) => setBudget(e.target.value)}/>
            </div>

            <div>
                <label htmlFor="perCard">Max Price Per Card</label>
                <input type="number" id="perCard" name="perCard"
                onChange={(e) => setMaxPricePerCard(e.currentTarget.value)}/>
            </div>

            <div>
                <label htmlFor="currency">Currency</label>
                <select name="currency" id="currency"
                onChange={(e) => setCurrency(e.currentTarget.value)}>
                    <option>GBP</option>
                    <option>USD</option>
                    <option>EU</option>
                </select>
            </div>

            <div>
                <label htmlFor="painThresh">Pain Threshold</label>
                <input type="number" id="painThresh" name="painThresh"
                onChange={(e) => setPainThreshold(e.target.value)}/>
            </div>

            <div>
                <label htmlFor="minBasics">Minimum Basic Lands</label>
                <input type="number" id="minBasics" name="minBasics"
                onChange={(e) => setMinBasics(e.target.value)}/>
            </div>
        </div>

    )
}

export default MonteCarlo