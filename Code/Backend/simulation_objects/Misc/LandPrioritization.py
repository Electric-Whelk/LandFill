from collections import defaultdict, deque

from simulation_objects.GameCards import ShockLand, CommandTower, BondLand, PainLand, DualLand, Triome, TriTap, \
    BattleLand, SlowLand, FastLand, RevealLand, CheckLand, SurveilLand, BicycleLand, TypedDualLand, ArtifactTapLand, \
    ScryLand, GainLand
from simulation_objects.GameCards.TappedCycles.GuildGate import GuildGate

stdprioritization = {
    "BasicLand": [],
    "FetchLand": [],
    "BondLand": [ShockLand, CommandTower],
    "DualFacedLand": [BondLand],
    "DualLand": [],
    "BattleLand": [ShockLand],
    "FastLand": [BondLand],
    "SlowLand": [BondLand],
    "PainLand": [BondLand],
    "HorizonLand": [PainLand], #"Horizon Lands"
    "ShockLand": [DualLand],
    "Triome": [],
    "TriTap": [Triome],
    "FilterLand": [],
    "Verge": [BondLand],
    "CheckLand": [BondLand],
    "RevealLand": [BondLand],
    "CommandTower": [],
    "SurveilLand": [BattleLand, Triome],
    "BicycleLand": [BattleLand, Triome],
    "TypedDualLand": [BattleLand, Triome],

    "GuildGate": [TriTap, SlowLand, FastLand, RevealLand, CheckLand, SurveilLand, BicycleLand,
                  TypedDualLand], #Guildgate
    "ScryLand": [TriTap, SlowLand, FastLand, RevealLand, CheckLand, SurveilLand, BicycleLand,
                  TypedDualLand],
    "ArtifactTapLand": [TriTap, SlowLand, FastLand, RevealLand, CheckLand, SurveilLand, BicycleLand,
                  TypedDualLand],
    "GainLand": [TriTap, SlowLand, FastLand, RevealLand, CheckLand, SurveilLand, BicycleLand,
                        TypedDualLand]


}

class LandPrioritization:
    def __init__(self, base_prioritization):
        # Maps cycle name → list of superior cycle names (strings)
        self.superior_cycles = defaultdict(list, base_prioritization)
        self.class_registry = {}

        # Build reverse graph
        self.inferior_cycles = defaultdict(list)
        for cycle, superiors in base_prioritization.items():
            self.class_registry[cycle] = base_prioritization.get(cycle, None)
            print(f"Cycle: {cycle}, superiors: {superiors}")
            for sup in superiors:
                self.inferior_cycles[sup.__name__].append(cycle)
                self.class_registry[sup.__name__] = sup

        bottomtier = {
            "ArtifactTapLand": ArtifactTapLand,
            "GuildGate": GuildGate,
            "ScryLand": ScryLand,
            "GainLand": GainLand
        }

        for item in bottomtier:
            self.class_registry[item] = bottomtier.get(item, None)

        # Maps cycle name → list of actual land instances
        self.cycle_to_lands = defaultdict(list)

    def reset(self):
        self.cycle_to_lands = defaultdict(list)




    def register_land(self, land):
        #cycle_name = land.__class__.__name__
        #self.cycle_to_lands[cycle_name].append(land)

        cycle_name = land.__class__.__name__

        # Set superior classes directly on the land instance
        if not land._superior_classes:
            superior_classes = self.superior_cycles.get(cycle_name, [])
            land._superior_classes = superior_classes

        self.cycle_to_lands[cycle_name].append(land)

    def cascade_superiors(self, land, deck):
        """
        Given a land instance, return all *actual* land cards that are strict superiors,
        including cascading through missing intermediate cycles.
        """
        visited = set()
        resolved_superiors = set()
        queue = deque()

        initial_superior_classes = [cls.__name__ for cls in land._superior_classes]

        queue.extend(initial_superior_classes)

        while queue:
            current_cycle = queue.popleft()
            if current_cycle in visited:
                continue
            visited.add(current_cycle)

            for superior_land in self.cycle_to_lands.get(current_cycle, []):
                if self._is_strict_superior(land, superior_land, deck):
                    resolved_superiors.add(superior_land)

            # If no suitable land exists in this cycle, cascade upward
            if not any(self._is_strict_superior(land, l, deck) for l in self.cycle_to_lands.get(current_cycle, [])):
                for sup in self.superior_cycles.get(current_cycle, []):
                    queue.append(sup.__name__)

        return list(resolved_superiors)

    def _is_strict_superior(self, inferior, superior, deck):
        """
        Returns True if the superior land produces all colors the inferior does (or more).
        """
        inf_colors = set(inferior.heap_prod(deck))  # You may need to pass deck here
        sup_colors = set(superior.heap_prod(deck))
        return inf_colors.issubset(sup_colors)

    def remove_cycle(self, cycle_name):
        """
        Forbid an entire land cycle (e.g., 'Bond Lands'), useful for user customization.
        """
        if cycle_name in self.cycle_to_lands:
            del self.cycle_to_lands[cycle_name]

    def remove_land(self, land):
        """
        Remove an individual land instance from its cycle.
        """
        if land._cycle in self.cycle_to_lands:
            self.cycle_to_lands[land._cycle] = [
                l for l in self.cycle_to_lands[land._cycle] if l != land
            ]

    def apply_player_rankings(self, ranking_sets):
        """
        Takes a list of rankings (list of lists of cycle names, highest priority first)
        and rewires superior_cycles & inferior_cycles accordingly,
        preserving class object references.
        """

        def resolve_class(cycle_name):
            """Try to get a class object for this cycle name."""
            # Check registry
            cls = self.class_registry.get(cycle_name)
            if cls:
                return cls
            # Check registered lands
            if self.cycle_to_lands.get(cycle_name):
                return self.cycle_to_lands[cycle_name][0].__class__
            # Check globals
            cls = globals().get(cycle_name)
            if cls:
                self.class_registry[cycle_name] = cls  # cache for future
                return cls
            # Not found
            raise ValueError(f"Unknown cycle name '{cycle_name}' in rankings.")

        for ranking in ranking_sets:
            if not ranking:
                continue

            # Step 1: preserve original superiors for the top-ranked cycle
            top_cycle = ranking[0]
            original_superiors = self.superior_cycles.get(top_cycle, [])
            self.superior_cycles[top_cycle] = original_superiors[:]  # shallow copy

            # Step 2: rewire all lower-ranked cycles
            for i in range(1, len(ranking)):
                above_name = ranking[i - 1]
                current_name = ranking[i]

                above_cls = resolve_class(above_name)
                self.superior_cycles[current_name] = [above_cls]

        # Step 3: rebuild inferior_cycles with updated relationships
        self.inferior_cycles.clear()
        for cycle, superiors in self.superior_cycles.items():
            #print(f"{cycle}")
            for sup in superiors:
                #print(f"\t{sup}")
                sup_name = sup.__name__
                self.inferior_cycles[sup_name].append(cycle)


