import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'


function App() {
  const [nonLands, setNonLands] = useState("")

  const submitCards = async (e) => {
    e.preventDefault()

    const url = "http://127.0.0.1:5000/general_test"
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({nonLands})
    }

    response = await fetch(url, options)
    console.log(response.json().message)

}

  return (
    <>
    <form onSubmit={submitCards}>
      <div>
        <label htmlFor="nonLands">nonLands</label>
        <input
          type="text"
          id="nonLands"
          value={nonLands}
          onChange={(e) => setNonLands(e.target.value)}
        />
      </div>
      <button type="submit">Submit</button>

    </form>
    </>
  )
}

export default App
