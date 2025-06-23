import FormatList from './FormatList'
import React from "react"
import { useState, useEffect } from "react"


const PlayerInput = ({ lock, setInputCards, setFormat, setRequestedQuantity }) => {
    const [allFormats, setAllFormats] = useState([]);

    useEffect(() => {
        fetchFormats()
    }, []);

    const fetchFormats = async() => {
        const response = await fetch("http://127.0.0.1:5000/fetch_formats")
        const data = await response.json()
        setFormat(data.formats[0])
        setAllFormats(data.formats)
    }

    const handleFormatChange = (e) => {
        setFormat(allFormats.find((f) =>
            f.display_name === e.target.value))
    }



    return (
        <div>
            <textarea id="inputCards"
                      cols="40"
                      rows="20"
                      onChange={e => setInputCards(e.target.value)}>
            </textarea>
            <div>
                <label htmlFor="formats">Format:</label>
                <select name="formats" id="formats" onChange={(e) => handleFormatChange(e)}>
                    <FormatList formats={allFormats}/>
                </select>
            </div>
            <div>
                <label htmlFor="quantity">Lands to fill:</label>
                <input type="number" id="quantity" name="quantity" onChange={(e) => setRequestedQuantity(e.target.value)}/>
            </div>
            <div>
                <button onClick={lock} type="button">Confirm Decklist</button>
            </div>
        </div>

    )
}

export default PlayerInput