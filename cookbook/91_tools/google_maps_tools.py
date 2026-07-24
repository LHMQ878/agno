"""
Google Maps Tools - Directions, Geocoding, and Distance Agent

This example demonstrates various Google Maps API functionalities including
directions, geocoding, address validation, and more. Shows how to use include_tools and
exclude_tools parameters for selective function access.

Prerequisites:
- Set the environment variable `GOOGLE_MAPS_API_KEY` with your Google Maps API key.
  You can obtain the API key from the Google Cloud Console:
  https://console.cloud.google.com/projectselector2/google/maps-apis/credentials

- You also need to activate the Address Validation API for your project:
  https://console.developers.google.com/apis/api/addressvalidation.googleapis.com

Note: For place search functionality, use GooglePlacesTools instead.
"""

from agno.agent import Agent
from agno.tools.google.maps import GoogleMapsTools

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------


# Example 1: All functions available (default behavior)
agent_full = Agent(
    name="Full Maps API Agent",
    tools=[
        GoogleMapsTools(all=True),  # All functions enabled
    ],
    description="You are a location and navigation specialist with full Google Maps access.",
    instructions=[
        "Use any Google Maps function as needed for location-based queries",
        "Format responses clearly and provide relevant details",
        "Handle errors gracefully and provide meaningful feedback",
    ],
    markdown=True,
)

# Example 2: Include only specific functions
agent_directions = Agent(
    name="Directions-focused Maps Agent",
    tools=[
        GoogleMapsTools(
            include_tools=[
                "get_directions",
                "get_distance_matrix",
            ]
        ),
    ],
    description="You are a navigation specialist focused only on directions and distances.",
    instructions=[
        "Focus on providing directions between locations",
        "Use get_directions for route planning",
        "Use get_distance_matrix for comparing multiple routes",
    ],
    markdown=True,
)

# Example 3: Exclude potentially expensive operations
agent_safe = Agent(
    name="Safe Maps API Agent",
    tools=[
        GoogleMapsTools(
            exclude_tools=[
                "get_distance_matrix",  # Can be expensive with many origins/destinations
                "get_directions",  # Excludes detailed route calculations
            ]
        ),
    ],
    description="You are a location specialist with restricted access to expensive operations.",
    instructions=[
        "Provide location information without detailed routing",
        "Use geocoding and address validation freely",
        "For directions, provide general guidance only",
    ],
    markdown=True,
)

# Using the full-featured agent for examples
agent = agent_full

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Example 1: Directions (default - runs when you execute this file)
    print("\n=== Example 1: Directions ===")
    agent.print_response(
        """Get driving directions from 'Phoenix Sky Harbor Airport' to 'Desert Botanical Garden',
        avoiding highways if possible""",
        stream=True,
    )

    # Uncomment any example below to run it:

    # # Example 2: Address Validation and Geocoding
    # print("\n=== Example 2: Address Validation and Geocoding ===")
    # agent.print_response(
    #     """Please validate and geocode this address:
    #     '1600 Amphitheatre Parkway, Mountain View, CA'""",
    #     stream=True,
    # )

    # # Example 3: Distance Matrix
    # print("\n=== Example 3: Distance Matrix ===")
    # agent.print_response(
    #     """Calculate the travel time and distance between these locations in Phoenix:
    #     Origins: ['Phoenix Sky Harbor Airport', 'Downtown Phoenix']
    #     Destinations: ['Desert Botanical Garden', 'Phoenix Zoo']""",
    #     stream=True,
    # )

    # # Example 4: Reverse Geocoding and Timezone
    # print("\n=== Example 4: Reverse Geocoding and Timezone ===")
    # agent.print_response(
    #     """Get the address and timezone information for these coordinates:
    #     Latitude: 33.4484, Longitude: -112.0740 (Phoenix)""",
    #     stream=True,
    # )

    # # Example 5: Multi-step Route Planning
    # print("\n=== Example 5: Multi-step Route Planning ===")
    # agent.print_response(
    #     """Plan a route with multiple stops in Phoenix:
    #     Start: Phoenix Sky Harbor Airport
    #     Stops:
    #     1. Arizona Science Center
    #     2. Heard Museum
    #     3. Desert Botanical Garden
    #     End: Return to Airport
    #     Please include estimated travel times between each stop.""",
    #     stream=True,
    # )

    # # Example 6: Location Analysis
    # print("\n=== Example 6: Location Analysis ===")
    # agent.print_response(
    #     """Analyze this location in Phoenix:
    #     Address: '2301 N Central Ave, Phoenix, AZ 85004'
    #     Please provide:
    #     1. Exact coordinates
    #     2. Elevation data
    #     3. Local timezone""",
    #     stream=True,
    # )

    # # Example 7: Transit Options
    # print("\n=== Example 7: Transit Options ===")
    # agent.print_response(
    #     """Compare different travel modes from 'Phoenix Convention Center' to 'Phoenix Art Museum':
    #     1. Driving
    #     2. Walking
    #     3. Transit (if available)
    #     Include estimated time and distance for each option.""",
    #     stream=True,
    # )
