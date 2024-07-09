class MessageParsingError(Exception):
    """Custom exception for errors during message parsing."""


class SendMessageError(Exception):
    """Custom exception for errors during sending messages."""


class WebhookError(Exception):
    """Custom exception for errors during webhook registration."""
