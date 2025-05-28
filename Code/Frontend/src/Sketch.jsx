import { useState } from 'react'
import './sketch.css'


const Sketch = () => {

  const [nonLands, setNonLands] = useState("")

  const monteCarlo = async (e) => {
    e.preventDefault()

    const url = "http://127.0.0.1:5000/test_input"
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({nonLands})
    }

    const response = await fetch(url, options)
    const info = await response.json()
    console.log(info.message)
    let result = document.getElementById("lands")
    result.innerText = info.message

    
  }

  return (
     <div class="container">
        <div id ="playerInput">
            <textarea id="nonLands"
                cols="40"
                rows="20"
                onChange={(e) => setNonLands(e.target.value)}> 
            </textarea>
            <div>
            <label for="formats">Format:</label>
            <select name="formats" id="formats">
            <option value="standard">Standard</option>
            <option value="modern">Modern</option>
            <option value="legacy">Legacy</option>
            <option value="EDH">EDH</option>
            </select> 
            </div>
            <div>
            <label for="quantity">Lands to fill:</label>
            <input type="number" id="quantity" name="quantity"/> 
            </div>
        </div>


        <div id="HitItMonte">
            <div>
            <button onClick={monteCarlo}type="button">Run</button>
            </div>

            <div>
            <label for="budget">Budget</label>
            <input type="number" id="budget" name="budget"/>
            </div>

            <div>
            <label for="perCard">Max Price Per Card</label>
            <input type="number" id="perCard" name="perCard"/>
            </div>

            <div>
            <label for="painThresh">Pain Threshold</label>
            <input type="number" id="painThresh" name="painThresh"/>
            </div>

            <div>
            <label for="minBasics">Minimum Basic Lands</label>
            <input type="number" id="minBasics" name="minBasics"/>
            </div>

            <div>
            <h2>Metrics:</h2>
            </div>

        </div>
        
        <div id="output">
            <textarea id="lands"
                cols="40"
                rows="20">
            </textarea>
            <div>
                <label for="outputStyle">Output Style:</label>
                <select name="outputStyle" id="outputStyle">
                <option value="match input">Match Input</option>
                <option value="modern">Moxfield</option>
                <option value="legacy">Tappedout</option>
                </select>
            </div>
            <div>
                <input type="checkbox" id="includeNonLands" name="includeNonLands"/>
                <label for="includeNonLands"> Include nonlands</label>
            </div>
        </div>

        <div class="landOptions">
            <div>
                <div class="cycleName">
                    <input type="checkbox" id="Shocks" name="Shocks"/>
                    <label for="Shocks"> ShockLands</label>
                </div>
                <div class="cycle">
                    <input type="checkbox" id="Steam Vents" name="Steam Vents"/>
                    <label for="Steam Vents">Steam Vents</label><br />
                    
                    <input type="checkbox" id="Sacred Foundry" name="Sacred Foundry"/>
                    <label for="Sacred Foundry">Sacred Foundry</label><br />

                    <input type="checkbox" id="shockEtc" name="shockEtc"/>
                    <label for="shockEtc">etc...</label><br />
                </div>
            </div>

            <div>
                <div class="cycleName">
                    <input type="checkbox" id="Fetches" name="Fetches"/>
                    <label for="Fetches"> Fetch Lands</label>
                </div>
                <div class="cycle">
                    <input type="checkbox" id="Scalding Tarn" name="Scalding Tarn"/>
                    <label for="Scalding Tarn">Scalding Tarn</label><br />
                    
                    <input type="checkbox" id="Arid Mesa" name="Arid Mesa"/>
                    <label for="Arid Mesa">Arid Mesa</label><br />

                    <input type="checkbox" id="fetchEtc" name="fetchEtc"/>
                    <label for="fetchEtc">etc...</label><br />
                </div>
            </div>
        </div>

    </div>

  )
}

export default Sketch
