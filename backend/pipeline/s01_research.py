"""
Step 01: Subject Research
Uses LLM to generate a biological/lore profile for the subject.
Input: Subject name + theme
Output: 01_research.md
"""

from backend.models import StepName
from backend.pipeline.base import PipelineStep


class ResearchStep(PipelineStep):
    step_name = StepName.RESEARCH
    requires_llm = True

    # Primary authoritative sites per theme (searched first)
    THEME_PRIMARY_SITES = {
        "pokemon": [
            "bulbapedia.bulbagarden.net",
            "serebii.net",
            "pokemondb.net",
        ],
        "harry_potter": [
            "harrypotter.fandom.com",
            "wizardingworld.com",
        ],
        "ancient_creatures": [
            "en.wikipedia.org",
            "nhm.ac.uk",
            "smithsonianmag.com",
            "britannica.com",
        ],
        "deep_sea": [
            "en.wikipedia.org",
            "oceanexplorer.noaa.gov",
            "mbari.org",
            "marinespecies.org",
        ],
    }

    # Search instructions per theme
    THEME_SEARCH_HINTS = {
        "pokemon": (
            "Search for all Pokédex entries, abilities, evolution details, "
            "base stats, and notable anime/game appearances."
        ),
        "harry_potter": (
            "Search for all canonical descriptions, behaviors, magical properties, "
            "Ministry of Magic classifications (X-XXXXX), and notable appearances "
            "in the books/films. Check the creature list and individual creature pages."
        ),
        "ancient_creatures": (
            "Search for fossil evidence, anatomical reconstructions, habitat, diet, "
            "predator-prey relationships, geological period, and evolutionary history."
        ),
        "deep_sea": (
            "Search for documented observations, bioluminescence data, depth range, "
            "feeding behavior, reproductive strategies, and pressure adaptations."
        ),
    }

    def execute(self) -> bool:
        subject = self.state.subject_name
        theme = self.state.theme
        self.log(f"Researching {subject} (theme: {theme})...")

        # Load SOP 01 prompt
        system_prompt = self.load_sop_prompt("1_research.md")

        # Remove the saving instructions (we handle file saving ourselves)
        if "## Saving Instructions" in system_prompt:
            system_prompt = system_prompt[:system_prompt.index("## Saving Instructions")].strip()

        primary_sites = self.THEME_PRIMARY_SITES.get(theme, [])
        search_hint = self.THEME_SEARCH_HINTS.get(theme, self.THEME_SEARCH_HINTS["pokemon"])

        # Phase 1: Targeted search on authoritative sites
        site_queries = " OR ".join(f"site:{s}" for s in primary_sites) if primary_sites else ""
        targeted_query = f"{subject} ({site_queries})" if site_queries else subject

        user_message = (
            f"Target Subject: {subject}\n\n"
            f"SEARCH PRIORITY:\n"
            f"1. First search these authoritative sources: {', '.join(primary_sites)}\n"
            f"   Suggested query: {targeted_query}\n"
            f"2. Then supplement with general web search if needed.\n\n"
            f"{search_hint}"
        )

        # Call LLM with web search enabled to ground research in real data
        self.log(f"Calling LLM with web search (primary sites: {', '.join(primary_sites)})...")
        result = self.llm.generate_with_continuation(
            system_prompt=system_prompt,
            user_message=user_message,
            plugins=[{"id": "web", "max_results": 5}],
        )

        if not result:
            self.log("LLM returned empty response", level="error")
            return False

        # Save output
        self.write_file("01_research.md", result)
        self.step_state.output = result
        self.log(f"Research complete: {len(result)} characters")
        return True
