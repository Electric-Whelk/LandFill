import React from "react"
import { useState, useEffect } from "react"


const Output = ({ }) => {


    return (
        <div id="output">
            <textarea id="lands"
                      cols="40"
                      rows="20">
            </textarea>
            <div>
                <label htmlFor="outputStyle">Output Style:</label>
                <select name="outputStyle" id="outputStyle">
                    <option value="match input">Match Input</option>
                    <option value="modern">Moxfield</option>
                    <option value="legacy">Tappedout</option>
                </select>
            </div>
            <div>
                <input type="checkbox" id="includeNonLands" name="includeNonLands"/>
                <label htmlFor="includeNonLands"> Include nonlands</label>
            </div>
        </div>

    )
}

export default Output