import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import './Pages.css';

const Page1 = () => {
    const navigate = useNavigate();

    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        const deckList = document.getElementById('decklist').value;
        const commander = document.getElementById('commander').value;
        const partner = document.getElementById('partner').value;

        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:5000/api/submit-deck', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ deckList, commander, partner })
            });

            const result = await response.json();

            // Navigate with state
            navigate('/page2', { state: { data: result } });
        } catch (err) {
            console.error("Error submitting deck:", err);
            alert("Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page1">
            <div className="title-text">
                <h1>LandFill</h1>

                <p>LandFill is an automatic manabase generator for EDH decks.</p>
                <p>Start by pasting in the nonland cards from your deck, plus any utility lands. You can copy+paste direct from TappedOut</p>
            </div>

            <div>
                <p>DeckList</p>
                <div>
                    <i className="hint">HINT: LandFill only gives you lands that'll help you with color fixing. If you've got utility lands,
                req towers, etc, add them now.</i>
                </div>
                <textarea id="decklist" cols="40" rows="20"></textarea>
            </div>
            <div>
                <p>Commander</p>
                <textarea id="commander" cols="40" rows="1"></textarea>
            </div>

            <div>
                <p>Partner</p>
                <textarea id="partner" cols="40" rows="1"></textarea>
            </div>

            <button onClick={handleSubmit}>Start {loading && <i>Loading... 🌀</i>}</button>
        </div>
    );
};

export default Page1;