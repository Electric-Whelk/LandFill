import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'


const Initializer = () => {
  const [nonLands, setNonLands] = useState("")

  const submitCards = async (e) => {
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
    let result = document.getElementById("output")
    result.innerText = info.message

    
}

  return (
    <>
    <form onSubmit={submitCards}>
      <textarea
        cols="40"
        rows="5"
        id="nonLands"
        value={nonLands}
        onChange={(e) => {setNonLands(e.target.value); console.log("ch ch ch ch changes")}}>     

        </textarea>
      <div>
      <button type="submit">Submit</button>
      </div>
    </form>
         <p id="output"></p>
    </>
  )
}

export default Initializer
