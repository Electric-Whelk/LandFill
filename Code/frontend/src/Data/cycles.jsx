

const ShockLands = {
    displayName: 'Shock Lands',
    description: "Has basic landtypes, enters tapped unless you pay 2 life",
    image: "/cyclesamples/ShockLand.jpg",
    maxPriceInDollars: 15.43,
    maxPriceInEuros: 17.94,
    maxPriceInGBP: 13.54,
    alwaysTapped: false,
    fetchable: true,
    suggestAutoInclude: true,
    rank: null
}

const FilterLands = {
    displayName: 'Filter Lands',
    description: "No basic landtypes, taps for colorless, or you tap and pay hybrid to add two mana in any combination of those two colours",
    image: "/cyclesamples/FilterLand.jpg",
    maxPriceInDollars: 15.43,
    maxPriceInEuros: 17.94,
    maxPriceInGBP: 13.54,
    alwaysTapped: false,
    fetchable: false,
    suggestAutoInclude: false,
    rank: null
}

const SurveilLands = {
    displayName: 'Surveil Lands',
    description: "Has basic landtypes, enters tapped, surveils 1 on entry",
    image: "/cyclesamples/ShockLand.jpg",
    maxPriceInDollars: 15.43,
    maxPriceInEuros: 17.94,
    maxPriceInGBP: 13.54,
    alwaysTapped: true,
    fetchable: true,
    suggestAutoInclude: false,
    rank: 0
}

const BicycleLands = {
    displayName: 'Bicycle Lands',
    description: "Has basic landtypes, enters tapped, can be cycled for 2 mana",
    image: "/cyclesamples/ShockLand.jpg",
    maxPriceInDollars: 15.43,
    maxPriceInEuros: 17.94,
    maxPriceInGBP: 13.54,
    alwaysTapped: true,
    fetchable: true,
    suggestAutoInclude: false,
    rank: 1
}

const GuildGates = {
    displayName: 'GuildGates',
    description: "No basic landtypes, enters tapped",
    image: "/cyclesamples/ShockLand.jpg",
    maxPriceInDollars: 15.43,
    maxPriceInEuros: 17.94,
    maxPriceInGBP: 13.54,
    alwaysTapped: true,
    fetchable: false,
    suggestAutoInclude: false,
    rank: 2
}

const ScryLands = {
    displayName: 'Scry Lands',
    description: "No basic landtypes, scries on entry",
    image: "/cyclesamples/ShockLand.jpg",
    maxPriceInDollars: 15.43,
    maxPriceInEuros: 17.94,
    maxPriceInGBP: 13.54,
    alwaysTapped: true,
    fetchable: false,
    suggestAutoInclude: false,
    rank: 1
}



const cyclesData = [ShockLands, FilterLands, SurveilLands, GuildGates, ScryLands]

export default cyclesData;