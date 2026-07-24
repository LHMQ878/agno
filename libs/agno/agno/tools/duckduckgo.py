from typing import Literal, Optional

from agno.tools.websearch import WebSearchTools


class DuckDuckGoTools(WebSearchTools):
    """Convenience wrapper around WebSearchTools with backend defaulting to "duckduckgo".

    Args:
        search: Enable web search function.
        news: Enable news search function.
        modifier: Modifier to prepend to search queries.
        fixed_max_results: Fixed number of maximum results.
        proxy: Proxy for requests.
        timeout: Maximum seconds to wait for a response.
        verify_ssl: Whether to verify SSL certificates.
        timelimit: Time limit for results ("d", "w", "m", "y").
        region: Region for results (e.g., "us-en", "uk-en").
        backend: Backend for searching. Defaults to "duckduckgo".
        all: Enable all tools.
    """

    def __init__(
        self,
        search: bool = True,
        news: bool = True,
        modifier: Optional[str] = None,
        fixed_max_results: Optional[int] = None,
        proxy: Optional[str] = None,
        timeout: Optional[int] = 10,
        verify_ssl: bool = True,
        timelimit: Optional[Literal["d", "w", "m", "y"]] = None,
        region: Optional[str] = None,
        backend: Optional[str] = None,
        all: bool = False,
        **kwargs,
    ):
        super().__init__(
            search=search,
            news=news,
            backend=backend or "duckduckgo",
            modifier=modifier,
            fixed_max_results=fixed_max_results,
            proxy=proxy,
            timeout=timeout,
            verify_ssl=verify_ssl,
            timelimit=timelimit,
            region=region,
            all=all,
            **kwargs,
        )

        # Backward compatibility aliases for old method names
        self.duckduckgo_search = self.web_search
        self.duckduckgo_news = self.search_news
