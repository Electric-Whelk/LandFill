import React, {useState} from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Pages.css';
import cardsData from '../Data/cards';
import page2 from "./Page2";

const Page3Dev = () => {

    const navigate = useNavigate();
    const location = useLocation();

    const [tmpLands, setTmpLands] = useState(() => {

        const data = location.state?.data
        data.cards.forEach((card) => {console.log(card.name + ":" + card.permitted)})
        return data.cards;
    });

    const [viewedCard, setViewedCard] = useState(null)





    return(
        <div className="page3">
            <div>
            <h2>Mandatory</h2>
            {tmpLands.map((land, index) => {
                if (land.mandatory) {
                    return(<p>{land.name}</p>)
                }
            })}</div>

            <div>
            <h2>Excluded</h2>
            {tmpLands.map((land, index) => {
                if (!land.permitted) {
                    return(<p>{land.name}</p>)
                }
            })}</div>


            <div>
            <h2>Permitted</h2>
            {tmpLands.map((land, index) => {
                if ((!land.mandatory) && land.permitted) {
                    return(<p>{land.name}</p>)
                }
            })}</div>

            {/*<div className = "main-content" id="page3-main">
            <div className="card-outputs">
                <h3>Lands We've Added (ranked by performance)</h3>
                <i>HINT: If you don't like some of these, remove them and hit "re-run optimizer"</i>

                {tmpLands.map((land, index) => (
                    <CardRankPanel land={land}
                                   index={index}
                                   setViewedCard={setViewedCard}
                                   key={land.displayName || index}
                    />
                ))}
            </div>



            <div className="admin-outputs">


            <div>
                <h3>Metrics</h3>
                <p>Percentage of wasteless games: 99</p>
                <p>Percentage of games where you cast your commander on curve: 99</p>
                <p>Deck cost: 50</p>
                <p>Lands cost: 10</p>

            </div>

            <div>
                <h3>Format Output</h3>
                <textarea cols="40" rows="20"></textarea>
            </div>

                <div>
                    <label htmlFor="outputStyle">Output Style:</label>
                    <select name="outputStyle" id="outputStyle">
                        <option value="match input">Match Input</option>
                        <option value="moxfield">Moxfield</option>
                        <option value="tappedout">Tappedout</option>
                    </select>
                </div>
                <div>
                    <input type="checkbox" id="includeNonLands" name="includeNonLands"/>
                    <label htmlFor="includeNonLands"> Include nonlands</label>
                </div>



            </div>

        </div>
        <div className = "side-panel">
            <CardInfoPanel card={viewedCard}/>

            <div className="nav-buttons">
                <button onClick={() => navigate('/page2')}>⬅ Back to Cycles</button>
                <button onClick={() => navigate('/page3')}>Re-Run Optimizer</button>
            </div>
        </div>*/}
        </div>
    );
}

const CardRankPanel = ({ land, index, setViewedCard }) => {
    return (

        <div
            className = "cycle-card"
            land={land}
            index={index}
            onMouseOver={() => setViewedCard(land)}>
            <Remover hey={"hey"}/>
            {land.name} {land.mandatory && <i>MANDATORY</i>} {land.permitted && <i>PERMITTED</i>}
        </div>
                );
};

const Remover = ({ hey }) => {
    return(
        <span> X </span>
    )
}

const CardInfoPanel = ({ card }) => {

    if (card === null) return <div className="card-info-panel">sploop</div>

    return (

        <div className="card-info-panel">
            <img src={card.image} />
            <div className="card-text-info">
                <p>Name: {card.displayName}</p>
                <p>Performance: {card.performance}</p>
            </div>

        </div>);
}

export default Page3Dev;