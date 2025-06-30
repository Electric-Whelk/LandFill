import FormatList from './FormatList'
import React from "react"
import { useState, useEffect } from "react"


const PlayerInput = ({ lock, setInputCards, inputCards, setFormat, format, setRequestedQuantity, requestedQuantity }) => {
    const [allFormats, setAllFormats] = useState([]);


    useEffect(() => {
        fetchFormats()
    }, []);

    const estimate_req = (cardList, formatToUse) => {
        const size = formatToUse.deck_size
        const len = cardList.length
        setRequestedQuantity(size - len)
    }


    const fetchFormats = async() => {
        const response = await fetch("http://127.0.0.1:5000/fetch_formats")
        const data = await response.json()
        setFormat(data.formats[0])
        setAllFormats(data.formats)
    }

    const handleFormatChange = (e) => {
        const newFormat = allFormats.find((f) =>
            f.display_name === e.target.value)
        setFormat(newFormat)
        const asList = inputCards.split('\n');
        estimate_req(asList, newFormat)
    }

    const handleInputChange = (e) => {
        const cards = e.target.value
        setInputCards(cards)
        const asList = cards.split('\n')
        estimate_req(asList, format)
    }




    return (
        <div id="playerinput">
            <textarea id="inputCards"
                      cols="40"
                      rows="20"
                      onChange={e => handleInputChange(e)}>
            </textarea>
            <div>
                <label htmlFor="formats">Format:</label>
                <select name="formats" id="formats" onChange={(e) => handleFormatChange(e)}>
                    <FormatList formats={allFormats}/>
                </select>
            </div>
            <div>
                <label htmlFor="quantity">Lands to fill:</label>
                <input type="number"
                       id="quantity"
                       name="quantity"
                       value={requestedQuantity}
                       onChange={(e) => setRequestedQuantity(e.target.value)}/>
            </div>
            <div>
                <button onClick={lock} type="button">Confirm Decklist</button>
            </div>
        </div>

    )
}

export default PlayerInput