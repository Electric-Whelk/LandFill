import React from "react"
import { useState, useEffect } from "react"
import Cycle from "./Cycle"

const CyclePanel = ({ cycles }) => {

    return (
        <>
            {cycles.map((cycle) => (
                <Cycle key={cycle.id} cycle={cycle}/>
            ))}
        </>
    )
}

export default CyclePanel