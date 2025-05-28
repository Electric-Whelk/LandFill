import { useState } from "react"

const ContactForm = ({ existingContact = {}, updateCallback }) => {
    const [firstName, setFirstName] = useState("existingContact.firstName" || "")
    const [lastName, setLastName] = useState("existingContact.lastName" || "")
    const [email, setEmail] = useState("existingContact.email" || "")

    const updating = Object.entries(existingContact).length !== 0 //"if there is at least one entry matching the data, you are updating."

    const onSubmit = async (e) => {
        e.preventDefault() //stops from refreshing page automatically
        
        const data = {
            firstName,
            lastName,
            email
        }
        const url = "http://127.0.0.1:5000/" + (updating ? `update_contact/${existingContact.id}` : "create_contact")
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json" //confirms we are sending json data
            },
            body: JSON.stringify(data)
        }
        const response = await fetch(url, options)
        if (response.status !== 201 && response.status !== 200){
            const message = await response.json()
            alert(message.message)
        } else {
            updateCallback() //closes the modal and udpates the data


        }
    }

    return (
        <form onSubmit={onSubmit}> 
            <div>
                <label htmlFor="firstName">First Name:</label>
                <input
                    type="text"
                    id="firstName"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="lastName">Last Name:</label>
                <input
                    type="text"
                    id="lastName"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="email">Email:</label>
                <input
                    type="text"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <button type="submit">Create Contact</button>
        </form>
    );
}

export default ContactForm