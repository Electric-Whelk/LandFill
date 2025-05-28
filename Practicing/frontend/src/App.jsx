import { useState, useEffect} from 'react'
import ContactList from "./ContactList"
import ContactForm from "./ContactForm"
import './App.css'

function App() {
  const [contacts, setContacts] = useState([]) //an empty list, what we'll have for the contacts
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentContact, setCurrentContact] = useState({}) //stores the contact we're currently editing

  useEffect(() => {
    fetchContacts()
  }, [])

  const fetchContacts = async () => { //sends a request to the backend to get the contexts
    const response = await fetch("http://127.0.0.1:5000/contacts") //sending a get request to our backend server
    const data = await response.json()
    setContacts(data.contacts) //not entirely sure what is happening here
  }

  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentContact({}) //sets current contact to be equal to an empty object
  }

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true)  }

  const openEditModal = () => {
    if (isModalOpen) return
    setCurrentContact(contact)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchContacts()
  }


  return (
    <>
      <ContactList contacts={contacts} updateContact={openEditModal}/>
      <button onClick={openCreateModal}>Create New Contact</button>
      {isModalOpen && <div className="modal">
        <div className='modal-content'>
          <span className="close" onClick={closeModal}>&times;</span>
          <ContactForm existingContact={currentContact}/>
        </div>
      </div>
      }
      </>
  )

}

export default App
