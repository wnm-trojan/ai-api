"""Domain exceptions – raised by domain/application, mapped to HTTP in presentation."""


class DomainError(Exception):
    """Base for all domain errors."""


class ValidationError(DomainError):
    """Input failed a domain rule."""


class AIProviderError(DomainError):
    """The AI provider returned an error."""


class ToolExecutionError(DomainError):
    """A tool call failed during execution."""


class UnauthorizedError(DomainError):
    """API key is missing or invalid."""


class RateLimitError(DomainError):
    """Request rate limit exceeded."""
