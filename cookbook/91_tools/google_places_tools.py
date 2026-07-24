"""
Google Places Tools - Place Search and Business Information Agent

This example demonstrates various Google Places API (New) functionalities including
place search, nearby search, place details, and autocomplete. Shows how to use include_tools
and exclude_tools parameters for selective function access.

Prerequisites:
- Set the environment variable `GOOGLE_PLACES_API_KEY` or `GOOGLE_MAPS_API_KEY`.
  You can obtain the API key from the Google Cloud Console:
  https://console.cloud.google.com/projectselector2/google/maps-apis/credentials

- Enable the Places API (New) for your project:
  https://console.cloud.google.com/apis/library/places.googleapis.com

Note: For directions and geocoding, use GoogleMapsTools instead.
"""

from agno.agent import Agent
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.google.places import GooglePlacesTools

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------


# Example 1: All functions available with web scraping
agent_full = Agent(
    name="Full Places API Agent",
    tools=[
        GooglePlacesTools(all=True),  # All functions enabled
        Crawl4aiTools(max_length=5000),  # Scrape business websites for menus, details
    ],
    description="You are a business and location information specialist with full Google Places access.",
    instructions=[
        "Use any Google Places function as needed for location-based queries",
        "Combine Places data with website data when available",
        "Format responses clearly and provide relevant details",
        "Handle errors gracefully and provide meaningful feedback",
    ],
    markdown=True,
)

# Example 2: Include only specific functions
agent_search = Agent(
    name="Search-focused Places Agent",
    tools=[
        GooglePlacesTools(
            include_tools=[
                "search_places",
                "search_nearby",
            ]
        ),
    ],
    description="You are a location search specialist focused only on finding places.",
    instructions=[
        "Focus on place searches and nearby searches",
        "Use search_places for general queries",
        "Use search_nearby for proximity searches",
    ],
    markdown=True,
)

# Example 3: Exclude potentially expensive operations
agent_safe = Agent(
    name="Safe Places API Agent",
    tools=[
        GooglePlacesTools(
            exclude_tools=[
                "get_place_details",  # Extra API call per place
                "autocomplete",  # Usually for interactive UIs
            ]
        ),
        Crawl4aiTools(max_length=3000),
    ],
    description="You are a location specialist with restricted access to expensive operations.",
    instructions=[
        "Provide location information using search functions",
        "Use search_places and search_nearby freely",
        "Scrape websites for additional details instead of place details API",
    ],
    markdown=True,
)

# Using the full-featured agent for examples
agent = agent_full

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Example 1: Business Search (default - runs when you execute this file)
    print("\n=== Example 1: Business Search ===")
    agent.print_response(
        "Find me highly rated Chinese restaurants in Phoenix, AZ with their contact details",
        stream=True,
    )

    # Uncomment any example below to run it:

    # # Example 2: Nearby Places
    # print("\n=== Example 2: Nearby Places ===")
    # agent.print_response(
    #     """Find coffee shops near Arizona State University Tempe campus.
    #     Include ratings and opening hours if available.""",
    #     stream=True,
    # )

    # # Example 3: Place Details with Website Scraping
    # print("\n=== Example 3: Place Details with Website ===")
    # agent.print_response(
    #     """Find information about 'Pizzeria Bianco' in Phoenix.
    #     Get their menu from their website if available.""",
    #     stream=True,
    # )

    # # Example 4: Nearby Search with Type Filter
    # print("\n=== Example 4: Nearby Search with Type Filter ===")
    # agent.print_response(
    #     """Find hospitals within 2km of coordinates 33.4484, -112.0740 (Downtown Phoenix).
    #     Include contact information and ratings.""",
    #     stream=True,
    # )

    # # Example 5: Business Hours and Accessibility
    # print("\n=== Example 5: Business Hours and Accessibility ===")
    # agent.print_response(
    #     """Find museums in Phoenix that are:
    #     1. Open on Mondays
    #     2. Have wheelchair accessibility
    #     3. Within 5 miles of downtown
    #     Include their opening hours and contact information.""",
    #     stream=True,
    # )

    # # Example 6: Autocomplete Search
    # print("\n=== Example 6: Autocomplete ===")
    # agent.print_response(
    #     """I'm typing 'star' in Phoenix - what place suggestions would come up?
    #     Show me the top autocomplete results.""",
    #     stream=True,
    # )

    # # Example 7: Comparative Search
    # print("\n=== Example 7: Comparative Search ===")
    # agent.print_response(
    #     """Compare the top 3 Italian restaurants in Scottsdale, AZ.
    #     Include ratings, price level, and what makes each one unique.
    #     Check their websites for current specials if available.""",
    #     stream=True,
    # )
