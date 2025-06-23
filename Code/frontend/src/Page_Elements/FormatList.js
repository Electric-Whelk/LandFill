import React from "react"

const FormatList = ({ formats }) => {


    return (
        <>
            {formats.map((format) => (
                <option key={format.id}>{format.display_name}</option>
            ))}
        </>
    )
}

export default FormatList