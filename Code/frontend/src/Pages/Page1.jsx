import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import { useDeck } from '../DeckContext';
import './Pages.css';



const Page1 = () => {

    const { deckList, setDeckList, commander, setCommander, partner, setPartner, currency, setCurrency } = useDeck();
    const navigate = useNavigate();

    const [loading, setLoading] = useState(false);
    const [removeLands, setRemoveLands] = useState(false);
    //const [currency, setCurrency] = useState('GBP');

    const handleSubmit = async () => {
        /*const deckList = document.getElementById('decklist').value;
        const commander = document.getElementById('commander').value;
        const partner = document.getElementById('partner').value;*/
        const host = "http://127.0.0.1:5000";
        const url = "/submit-deck"


        setLoading(true);

        try {
            const response = await fetch('/submit-deck', {
                method: 'POST',
                credentials: "include",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ deckList, commander, partner, currency, removeLands })
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
                <p>Start by pasting in the nonland cards from your deck. You can copy+paste direct from TappedOut, Deckbox, Moxfield or Archidekt</p>
            </div>

            <div>
                <div>
                    <i className="hint">HINT: LandFill only gives you lands that'll help you with color fixing. If you've got utility lands,
                req towers, etc, add them too.</i>
                </div>
                <textarea id="decklist"
                          cols="40"
                          rows="20"
                          value={deckList}
                          onChange={(e) => setDeckList(e.target.value)}
                ></textarea>
            </div>
            <div>
                <label>
                <input type="checkbox" name="removelands" onChange={(e) => setRemoveLands(e.target.value)}/>
                Ignore all land cards currently in decklist (ie, remove them and replace them with a totally new manabase)
                </label>

            </div>

            <div>
                <p>Commander</p>
                <textarea id="commander"
                          cols="40"
                          rows="1"
                          value={commander}
                          onChange={(e) => setCommander(e.target.value)}
                ></textarea>
            </div>

            <div>
                <p>Partner (leave blank if none)</p>
                <textarea id="partner"
                          cols="40"
                          rows="1"
                          value={partner}
                          onChange={(e) => setPartner(e.target.value)}
                ></textarea>
            </div>

            <div>
                <label>Display card prices in: </label>
            <select name="currency"
                    value={currency}
                    onChange= {(e) => {setCurrency(e.target.value)}}>
                <option value="USD">USD</option>
                <option value="Euros">Euros</option>
                <option value="GBP">GBP</option>
            </select>
            </div>
        <div>                <button id="pageOneStart" onClick={handleSubmit}>Start {loading && <i>Loading... 🌀</i>}</button>
        </div>

        </div>
    );
};

export default Page1;
