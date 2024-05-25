import { useState } from 'react'
import './App.css'
import Welcome from './components/welcome'
import RecordScreen from './components/recordPage'
import { TranscriptProvider } from './context/TranscriptContext'

function App() {
  const [isWelcome, setIsWelcome] = useState(true)

  return (
    <>
    <TranscriptProvider>
    {
      isWelcome? (<Welcome setWelcome={setIsWelcome}></Welcome>) : (<RecordScreen></RecordScreen>)
    }
    </TranscriptProvider>
    </>
  )
}

export default App
