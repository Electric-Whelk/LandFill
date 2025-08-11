// Page2.js – Dynamic land cycle selector interface (Refactored)
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { useDeck } from '../DeckContext'
import './Pages.css';

const COLUMN_IDS = {
    include: 'Definitely include these',
    consider: 'Consider these',
    exclude: 'Never include these'
};

const RANK_IDS = {
    fetchable: 'Fetchable Taplands',
    nonFetchable: 'Nonfetchable Taplands'
};

const Page2 = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { cycles, setCycles, currency, setCurrency } = useDeck()

    useEffect(() =>
    {
        if (location.state?.data) {
            const newData = location.state.data
            setCycles(newData.heap || []);
            setCurrency(newData.currency || "GBP")
        }
    }, [location.state, setCycles, setCurrency]);
    /*const data = location.state?.data;
    const cycles = data?.heap || [];
    const currency = data?.currency || "GBP";*/

    // Filters & toggles
    const [loading, setLoading] = useState(false);
    const [minBasics, setMinBasics] = useState(0);
    const [minIndividualBasics, setMinIndividualBasics] = useState(0);
    const [allowOffColorFetches, setAllowOffColorFetches] = useState(true);
    const [viewedCycle, setViewedCycle] = useState(null);
    const [filters, setFilters] = useState({
        tappedNonfetch: false,
        tappedFetchable: false,
        maxPrice: ''
    });

    // Core arrays
    const [excludeArrays, setExcludeArrays] = useState({
        belowMaxPrice: [],
        uncheckedByPlayer: [],
        offColorFetch: [],
        cycleMovedToExclude: [],
        addedBecauseNotTappedButFetchable: [],
        addedBecauseNotTappedAndNotFetchable: []
    });

    const [positiveArrays, setPositiveArrays] = useState({
        include: [],
        consider: []
    });

    // Columns for UI
    const [columns, setColumns] = useState(() => {
        const autoIncluded = [];
        const consider = [];
        const autoincludeList = ["Shock Lands", "Fetch Lands", "OG Dual Lands", "Command Tower"];
        cycles.forEach(cycle => {
            if (autoincludeList.includes(cycle.displayName)) {
                autoIncluded.push(cycle);
                cycle.suggestAutoInclude = true;
            } else {
                consider.push(cycle);
                cycle.suggestAutoInclude = false;
            }
        });
        return { include: autoIncluded, consider, exclude: [] };
    });

    // Rankings for the prioritization panel
    const [rankings, setRankings] = useState(() => {
        const typedTaps = [];
        const untypedTaps = [];
        const nuancedList = ["Triomes", "Bounce Lands", "Tri-Color Taplands"];
        cycles.forEach(cycle => {
            if (cycle.alwaysTapped && !nuancedList.includes(cycle.displayName)) {
                if (cycle.fetchable) typedTaps.push(cycle);
                else untypedTaps.push(cycle);
            }
        });
        return { fetchable: typedTaps, nonFetchable: untypedTaps };
    });

    /** ----------------------------
     * UTILITY: membership checks
     ---------------------------- **/
    const cardInExcludeArray = (card, key) =>
        excludeArrays[key].some(c => c.name === card.name);

    const cardInAnyExcludeArray = (card) =>
        Object.keys(excludeArrays).some(key => cardInExcludeArray(card, key));

    /** ----------------------------
     * UTILITY: update excludeArrays
     ---------------------------- **/
    const addCardToExcludeArray = (card, key) => {
        setExcludeArrays(prev => {
            const newArr = prev[key].some(c => c.name === card.name)
                ? prev[key]
                : [...prev[key], card]
            console.log("Adding " + card.name + " to " + key + " (" + (prev[key].length + 1) + ")");
            return { ...prev, [key]: newArr };
        });
    };

    const removeCardFromExcludeArray = (card, key) => {
        setExcludeArrays(prev => {
            console.log("removing " + card.name + " from " + key + " (" + (prev[key].length - 1) + ")");
            return ({
                ...prev,
                [key]: prev[key].filter(c => c.name !== card.name)
            })
        });
    };


    /** ----------------------------
     * UTILITY: update positiveArrays
     ---------------------------- **/
    const moveCardToPositive = (card, targetKey) => {
        setPositiveArrays(prev => {
            const newState = { ...prev };
            // Remove from other positive array
            Object.keys(newState).forEach(k => {
                newState[k] = newState[k].filter(c => c.name !== card.name);
            });
            // Add to target
            newState[targetKey] = [...newState[targetKey], card];
            return newState;
        });
    };

    const moveCycleToPositive = (cycle, targetKey) => {
        cycle.cards.forEach(card => moveCardToPositive(card, targetKey));
    };

    /** ----------------------------
     * AUTO-MOVE CYCLES TO EXCLUDE
     ---------------------------- **/
    useEffect(() => {
        setColumns(prevCols => {
            const newCols = { include: [], consider: [], exclude: [] };

            // Helper to check if all cards in cycle are excluded
            const allCardsExcluded = (cycle) =>
                cycle.cards.every(card => cardInAnyExcludeArray(card));

            // Rebuild columns based on exclusion status
            [...prevCols.include, ...prevCols.consider, ...prevCols.exclude].forEach(cycle => {
                if (allCardsExcluded(cycle)) {
                    // Move to exclude
                    if (!newCols.exclude.find(c => c.displayName === cycle.displayName)) {
                        newCols.exclude.push(cycle);
                    }
                } else {
                    // Place in column according to positiveArrays
                    const firstCard = cycle.cards[0];
                    if (positiveArrays.include.some(c => c.name === firstCard.name)) {
                        newCols.include.push(cycle);
                    } else {
                        newCols.consider.push(cycle);
                    }
                }
            });

            return newCols;
        });
    }, [excludeArrays, positiveArrays]); // Run whenever excludeArrays or positiveArrays change

    function showErrorMessages(messages){
        console.log(messages);
    }

    function handlePlayerMoveCycleOutOfExclude(cycle) {
        // Step 1: Run exceptions logic
        const { blocked, messages } = checkCycleMoveExceptions(cycle);
        if (blocked) {
            showErrorMessages(messages);
            return;
        }

        // Step 2: Remove cards from cycleMovedToExclude
        removeCardsFromArray(cycle.cards, 'cycleMovedToExclude');

        // Step 3: Remove from tapped arrays
        removeCardsFromArray(cycle.cards, 'addedBecauseNotTappedButFetchable');
        removeCardsFromArray(cycle.cards, 'addedBecauseNotTappedAndNotFetchable');

        // Step 4: Untick relevant filter checkboxes (code-driven)
        setFilters(prev => ({
            ...prev,
            addedBecauseNotTappedButFetchable: false,
            addedBecauseNotTappedAndNotFetchable: false
        }));

        // Step 5: Move cycle to correct positiveArray column
        moveCycleToPositiveByCardMembership(cycle);
    }

    function moveCycleToPositiveByCardMembership(cycle) {
        const firstCard = cycle.cards[0]; // all cards in a cycle should have the same positive array

        if (positiveArrays.include.some(c => c.name === firstCard.name)) {
            setColumns(prev => ({
                ...prev,
                include: [...prev.include, cycle].filter(uniqueByName),
                consider: prev.consider.filter(c => c.displayName !== cycle.displayName),
                exclude: prev.exclude.filter(c => c.displayName !== cycle.displayName)
            }));
        } else {
            setColumns(prev => ({
                ...prev,
                consider: [...prev.consider, cycle].filter(uniqueByName),
                include: prev.include.filter(c => c.displayName !== cycle.displayName),
                exclude: prev.exclude.filter(c => c.displayName !== cycle.displayName)
            }));
        }
    }

// Helper to ensure cycles aren’t duplicated
    function uniqueByName(cycle, index, self) {
        return index === self.findIndex(c => c.displayName === cycle.displayName);
    }


    function removeCardsFromArray(cards, arrayKey) {
        setExcludeArrays(prev => ({
            ...prev,
            [arrayKey]: prev[arrayKey].filter(
                c => !cards.some(card => card.name === c.name)
            )
        }));
    }

    function checkCycleMoveExceptions(cycle) {
        let messages = [];
        const allBelowMaxPrice = cycle.cards.every(card => cardInExcludeArray(card, 'belowMaxPrice'));
        const allOffColorFetch = cycle.cards.every(card => cardInExcludeArray(card, 'offColorFetch'));

        if (allBelowMaxPrice) messages.push("All cards in this cycle are below your maximum price. Please lower it if you wish to edit this cycle’s position");
        if (allOffColorFetch) messages.push("All these cards are offcolor fetches; please untick this option if you wish to edit this cycle’s position");

        const blocked = messages.length > 0;
        return { blocked, messages };
    }




    /** ----------------------------
     * INIT: load positiveArrays from columns
     ---------------------------- **/
    useEffect(() => {
        setPositiveArrays({
            include: columns.include.flatMap(c => c.cards),
            consider: columns.consider.flatMap(c => c.cards)
        });
    }, []); // run once

    /** ----------------------------
     * FILTER APPLICATION
     ---------------------------- **/

    const handleSidePanelTick = (e, card) => {
        const isChecked = e.target.checked;

        if (!isChecked) {
            // Player unchecked → mark as uncheckedByPlayer
            setExcludeArrays(prev => {
                // Avoid duplicate
                if (prev.uncheckedByPlayer.some(c => c.name === card.name)) {
                    return prev;
                }
                return {
                    ...prev,
                    uncheckedByPlayer: [...prev.uncheckedByPlayer, card]
                };
            });
        } else {
            // Player checked → remove from ALL exclude arrays
            setExcludeArrays(prev => {
                const updated = {};
                for (const key in prev) {
                    updated[key] = prev[key].filter(c => c.name !== card.name);
                }
                return updated;
            });
        }
    };

    useEffect(() => {
        // Below max price
        if (filters.maxPrice) {
            cycles.forEach(cycle => {
                cycle.cards.forEach(card => {
                    if (parseFloat(card[currency]) > parseFloat(filters.maxPrice)) {
                        addCardToExcludeArray(card, "belowMaxPrice");
                    } else {
                        removeCardFromExcludeArray(card, "belowMaxPrice");
                    }
                });
            });
        } else {
            // Clear all
            excludeArrays.belowMaxPrice.forEach(card =>
                removeCardFromExcludeArray(card, "belowMaxPrice")
            );
        }
    }, [filters.maxPrice]);

    useEffect(() => {
        // tappedNonfetch
        if (filters.tappedNonfetch) {
            cycles.forEach(cycle => {
                cycle.cards.forEach(card => {
                    if (card.entersTapped && !card.fetchable) {
                        addCardToExcludeArray(card, "addedBecauseNotTappedAndNotFetchable");
                    }
                });
            });
        } else {
            excludeArrays.addedBecauseNotTappedAndNotFetchable.forEach(card =>
                removeCardFromExcludeArray(card, "addedBecauseNotTappedAndNotFetchable")
            );
        }
    }, [filters.tappedNonfetch]);

    useEffect(() => {
        // tappedFetchable
        if (filters.tappedFetchable) {
            cycles.forEach(cycle => {
                cycle.cards.forEach(card => {
                    if (card.entersTapped && card.fetchable) {
                        addCardToExcludeArray(card, "addedBecauseNotTappedButFetchable");
                    }
                });
            });
        } else {
            excludeArrays.addedBecauseNotTappedButFetchable.forEach(card =>
                removeCardFromExcludeArray(card, "addedBecauseNotTappedButFetchable")
            );
        }
    }, [filters.tappedFetchable]);

    useEffect(() => {
        // offColorFetch toggle
        if (!allowOffColorFetches) {
            cycles.forEach(cycle => {
                cycle.cards.forEach(card => {
                    if (card.offColorFetch) addCardToExcludeArray(card, "offColorFetch");
                });
            });
        } else {
            excludeArrays.offColorFetch.forEach(card =>
                removeCardFromExcludeArray(card, "offColorFetch")
            );
        }
    }, [allowOffColorFetches]);

    useEffect(() => {
        console.log("excludeArrays now:", excludeArrays);
    }, [excludeArrays]);

    /** ----------------------------
     * DRAG HANDLERS
     ---------------------------- **/
    const onDragEnd = result => {
        if (!result.destination) return;
        const { source, destination } = result;
        if (source.droppableId === destination.droppableId) return;

        const srcList = Array.from(columns[source.droppableId]);
        const [movedCycle] = srcList.splice(source.index, 1);
        const destList = Array.from(columns[destination.droppableId]);
        destList.splice(destination.index, 0, movedCycle);

        setColumns(prev => ({
            ...prev,
            [source.droppableId]: srcList,
            [destination.droppableId]: destList
        }));

        // Positive array updates
        if (destination.droppableId === "include") {
            moveCycleToPositive(movedCycle, "include");
            if (source.droppableId === "exclude") {handlePlayerMoveCycleOutOfExclude(movedCycle) }
        } else if (destination.droppableId === "consider") {
            moveCycleToPositive(movedCycle, "consider");
            if (source.droppableId === "exclude") {handlePlayerMoveCycleOutOfExclude(movedCycle) }
        } else if (destination.droppableId === "exclude") {
            movedCycle.cards.forEach(card =>
                addCardToExcludeArray(card, "cycleMovedToExclude")
            );
        }

    };

    const onReorder = result => {
        if (!result.destination) return;
        const { source, destination } = result;
        if (source.index === destination.index) return;
        if (source.droppableId !== destination.droppableId) return;

        const newList = Array.from(rankings[source.droppableId]);
        const [movedItem] = newList.splice(source.index, 1);
        newList.splice(destination.index, 0, movedItem);
        setRankings(prev => ({ ...prev, [source.droppableId]: newList }));
        console.log(newList)
    };

    /** ----------------------------
     * FILTER FORM HANDLERS
     ---------------------------- **/
    const handleFilterChange = e => {
        const { name, value, type, checked } = e.target;
        const val = type === 'checkbox' ? checked : value;
        setFilters(prev => ({ ...prev, [name]: val }));
    };

    /** ----------------------------
     * COMPONENTS
     ---------------------------- **/
    const FAQ = ({ label, content }) => {
        const [open, setOpen] = useState(false);
        return (
            <div className="faq" onClick={() => setOpen(!open)}>
                <strong>{label}</strong>
                {open && <div className="faq-content">{content}</div>}
            </div>
        );
    };

    const CycleInfoPanel = ({ cycle }) => {
        if (!cycle) return <div className="card-info-panel">Select a cycle</div>;
        return (
            <div className="card-info-panel">
                <img src={cycle.cards[0].image} alt={cycle.altText} />
                <div className="card-text-info">
                    <p>{cycle.displayName}</p>
                    <table>
                        <thead>
                        <tr><th>Card</th><th>Produces</th><th>Price</th></tr>
                        </thead>
                        <tbody>
                        {cycle.cards.map((card) => (
                            <tr key={card.name}>
                                <td><input type="checkbox"
                                           name={card.name}
                                           checked={!cardInAnyExcludeArray(card)}
                                           onChange = {(e) => handleSidePanelTick(e, card)}
                                            />{card.name}</td>
                                <td>{card.produced}</td>
                                <td>{card[currency]}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    };

    const handleRun = async () => {
        setLoading(true);
        const mandatory = []
        const permitted = []
        const excluded = []


        for(const card of positiveArrays.include){ if (!cardInAnyExcludeArray(card)){mandatory.push(card)}
            else {excluded.push(card)}};
        for(const card of positiveArrays.consider){ if (!cardInAnyExcludeArray(card)){permitted.push(card)}
            else {excluded.push(card)}};

        try {
            const response = await fetch('http://127.0.0.1:5000/api/submit-preferences', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mandatory, permitted, excluded, rankings })
            });

            const result = await response.json();

            // Navigate with state
            navigate('/page3', { state: { data: result } });
        } catch (err) {
            console.error("Error submitting preferences:", err);
            alert("Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    const handleRunDev = async () => {
        setLoading(true);
        const mandatory = []
        const permitted = []
        const excluded = []


        for(const card of positiveArrays.include){ if (!cardInAnyExcludeArray(card)){mandatory.push(card)}
        else {excluded.push(card)}};
        for(const card of positiveArrays.consider){ if (!cardInAnyExcludeArray(card)){permitted.push(card)}
        else {excluded.push(card)}};

        try {
            const response = await fetch('http://127.0.0.1:5000/api/test-preferences', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mandatory, permitted, excluded, rankings })
            });

            const result = await response.json();

            // Navigate with state
            navigate('/page3Dev', { state: { data: result } });
        } catch (err) {
            console.error("Error submitting preferences:", err);
            alert("Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page2">
            <div className="main-content">

                <div className="faq-row">
                    <FAQ label="How will this optimize my manabase?" content="OPTIMIZATON EXPLANATION HERE"/>
                    <FAQ label="How Long Will optimization take?" content="OPTIMIZATION TIME ESTIMATE HERE"/>
                </div>

                <div className="admin">
                    <h1>Land Cycle Preferences</h1>
                    <div className="filters">
                        <label>
                            <input type="checkbox" name="tappedNonfetch" checked={filters.tappedNonfetch} onChange={handleFilterChange} />
                            All lands that are always tapped and aren’t fetchable (eg, GuildGates)
                        </label>
                        <label>
                            <input type="checkbox" name="tappedFetchable" checked={filters.tappedFetchable} onChange={handleFilterChange} />
                            All lands that are always tapped even if they're fetchable (eg, Surveil Lands)
                        </label>
                        <label>
                            All lands that cost more than
                            <input type="number" name="maxPrice" value={filters.maxPrice} onChange={handleFilterChange} placeholder="Amount" /> in {currency}
                        </label>
                    </div>
                    <div className="preciseSpecs">
                        <label>
                            <input type="checkbox" checked={allowOffColorFetches} onChange={(e) => setAllowOffColorFetches(e.target.checked)} />
                            Allow Off-Color Fetches
                        </label>
                    </div>
                </div>

                <DragDropContext onDragEnd={onDragEnd}>
                    <div className="columns">
                        {Object.entries(COLUMN_IDS).map(([key, label]) => (
                            <div key={key}>
                                <h3>{label}</h3>
                                <Droppable droppableId={key}>
                                    {(dropProvided) => (
                                        <div className="column" ref={dropProvided.innerRef} {...dropProvided.droppableProps}>
                                            {columns[key]?.map((cycle, index) => (
                                                <CyclePanel cycle={cycle} index={index} setViewedCycle={setViewedCycle} key={cycle.displayName}/>
                                            ))}
                                            {dropProvided.placeholder}
                                        </div>
                                    )}
                                </Droppable>
                            </div>
                        ))}
                    </div>
                </DragDropContext>

                <div className="prioritization">
                    <h3>Rank Equivalent Lands</h3>
                    <DragDropContext onDragEnd={onReorder}>
                        <div className="columns">
                            {Object.entries(RANK_IDS).map(([key, label]) => (
                                <div key={key}>
                                    <h3>{label}</h3>
                                    <Droppable droppableId={key}>
                                        {(dropProvided) => (
                                            <div className="ranking" ref={dropProvided.innerRef} {...dropProvided.droppableProps}>
                                                {rankings[key]?.map((cycle, index) => (
                                                    <CyclePanel cycle={cycle} index={index} setViewedCycle={setViewedCycle} key={cycle.displayName}/>
                                                ))}
                                                {dropProvided.placeholder}
                                            </div>
                                        )}
                                    </Droppable>
                                </div>
                            ))}
                        </div>
                    </DragDropContext>
                </div>
            </div>

            <div className="side-panel">
                <CycleInfoPanel cycle={viewedCycle} />
                <div className="nav-buttons">
                    <button onClick={() => navigate('/')}>⬅ Back</button>
                    <button onClick={() => handleRun()}>Run Optimizer {loading && <i>Loading... 🌀</i>}</button>
                </div>
                <button onClick={() => handleRunDev()}>RunDev {loading && <i>Loading... 🌀</i>}</button>

            </div>
        </div>
    );
};

const CyclePanel = ({ cycle, index, setViewedCycle }) => (
    <Draggable key={cycle.displayName} draggableId={cycle.displayName} index={index}>
        {(dragProvided) => (
            <div className="cycle-card" ref={dragProvided.innerRef} {...dragProvided.draggableProps} {...dragProvided.dragHandleProps} onMouseOver={() => setViewedCycle(cycle)}>
                <span>{cycle.displayName}</span>
            </div>
        )}
    </Draggable>
);

export default Page2;
