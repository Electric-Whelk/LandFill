import { createContext, useContext, useState } from 'react';

const DeckContext = createContext();

export const DeckProvider = ({ children }) => {
    //Page 1 Details
    const [deckList, setDeckList] = useState('');
    const [commander, setCommander] = useState('');
    const [partner, setPartner] = useState('');
    const [currency, setCurrency] = useState("GBP")

    //page2 Details
    const [cycles, setCycles] = useState([]);

    return (
        <DeckContext.Provider value={{
            deckList, setDeckList,
            commander, setCommander,
            partner, setPartner,
            currency, setCurrency,
            cycles, setCycles
        }}>
            {children}
        </DeckContext.Provider>
    );
};

export const useDeck = () => useContext(DeckContext);
