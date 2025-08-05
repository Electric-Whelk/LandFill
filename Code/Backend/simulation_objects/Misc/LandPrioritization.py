from collections import defaultdict, deque

from simulation_objects.GameCards import ShockLand, CommandTower, BondLand, PainLand, DualLand, Triome, TriTap, \
    BattleLand, SlowLand, FastLand, RevealLand, CheckLand

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
    "Horizon Lands": [PainLand],
    "ShockLand": [DualLand],
    "Triome": [],
    "TriTap": [Triome],
    "Guildgate": [TriTap, BattleLand, SlowLand, FastLand, RevealLand, CheckLand], #swap battleland for surveil and stuff when you add these
    "FilterLand": [],
    "Verge": [BondLand],
    "CheckLand": [BondLand],
    "RevealLand": [BondLand],
    "CommandTower": []
}

class LandPrioritization:
    def __init__(self, base_prioritization):
        # Maps cycle name → list of superior cycle names (strings)
        self.superior_cycles = defaultdict(list, base_prioritization)

        # Build reverse graph
        self.inferior_cycles = defaultdict(list)
        for cycle, superiors in base_prioritization.items():
            for sup in superiors:
                self.inferior_cycles[sup.__name__].append(cycle)

        # Maps cycle name → list of actual land instances
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

    def reprioritize(self, cycle_name, new_superiors):
        """
        Dynamically change the superiority chain of a land cycle.
        """
        self.superior_cycles[cycle_name] = [cls.__name__ for cls in new_superiors]