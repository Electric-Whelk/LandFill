const Cycle = ({ cycle }) => {

    const cards = cycle.cards

    const selectAll = async () => {
        const title = document.getElementById(cycle.id)
        const status = title.checked
        for (const card of cards) {
            const element = document.getElementById(card.id)
            element.checked = status
        }

    }

    return (
        <>
            <div class="cycle">
                <div class="cycleName">
                    <input type="checkbox" key={cycle.id} id = {cycle.id} name={cycle.name} onChange={selectAll} defaultChecked/>
                    <label for={cycle.id}>{cycle.name}</label>
                </div>


                {cards.map((card) => (
                    <div class="cardList" key = {card.id}>
                        <input type="checkbox" id={card.id} name={card.name} class="card" defaultChecked/>
                        <label for={card.id}>{card.name}</label><br />
                    </div>

                ))}
            </div>
        </>
    )
}

export default Cycle