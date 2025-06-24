import React from "react"
import { useState, useEffect } from "react"


const MonteCarlo = ({ }) => {


    return (
        <div id="montecarlo">
            <div>
                <button type="button">Run</button>
            </div>

            <div>
                <label htmlFor="budget">Budget</label>
                <input type="number" id="budget" name="budget"/>
            </div>

            <div>
                <label htmlFor="perCard">Max Price Per Card</label>
                <input type="number" id="perCard" name="perCard"/>
            </div>

            <div>
                <label htmlFor="currency">Currency</label>
                <select name="currency" id="currency">
                    <option>GBP</option>
                    <option>USD</option>
                    <option>EU</option>
                </select>
            </div>

            <div>
                <label htmlFor="painThresh">Pain Threshold</label>
                <input type="number" id="painThresh" name="painThresh"/>
            </div>

            <div>
                <label htmlFor="minBasics">Minimum Basic Lands</label>
                <input type="number" id="minBasics" name="minBasics"/>
            </div>
        </div>

    )
}

export default MonteCarlo