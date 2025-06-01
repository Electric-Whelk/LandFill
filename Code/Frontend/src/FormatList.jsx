import React from "react"
import { useState, useEffect } from "react"

const FormatList = ({ formats }) => {
    /*const [formats, setFormats] = useState([]);

    useEffect(() => {
    fetchFormats()
    }, []);


    const fetchFormats = async() => {
        const response = await fetch("http://127.0.0.1:5000/fetch_formats")
        const data = await response.json()
        setFormats(data.formats)
    }*/

    return (
        <>
            {formats.map((format) => (
                <option id={format.id}>{format.name}</option>
            ))}
        </>
    )
}

export default FormatList