"""SMS Messaging class utilizing Bird API"""

from typing import Any, Dict, Optional, cast
import requests
from ..utils.logger import logger
from src.messaging.basemessaging import BaseMessaging
from src.messaging.models import (
    SendMessageError,
    BirdConfig,
    WebhookError,
    Message,
    MessageMedium,
    MessageType,
    MessageParsingError,
    BirdMessage
)
from pydantic import ValidationError


class BirdSMSProvider(BaseMessaging):
    def __init__(
        self,
        bird_url: str,
        organization_id: str,
        workspace_id: str,
        api_key: str,
        signing_key: str,
        user_phone: str,
        channel_id: str,
    ):
        """Initialize Bird credentials."""
        self._api_url = bird_url
        self._api_header = {
            "Authorization": f"AccessKey {api_key}",
            "Content-Type": "application/json",
        }
        self._signing_key = signing_key
        self._organization_id = organization_id
        self._workspace_id = workspace_id
        self._user_phone = user_phone
        self._channel_id = channel_id

    @classmethod
    def from_config(cls, config: BirdConfig, user_phone: Optional[str] = None, channel_id: Optional[str] = None) -> "BirdSMSProvider":
        """Instantiate and return a BirdSMSProvider object."""
        bird_url = config.BIRD_API_URL
        organization_id = config.BIRD_ORGANIZATION_ID
        workspace_id = config.BIRD_WORKSPACE_ID
        api_key = config.BIRD_API_KEY
        signing_key = config.BIRD_SIGNING_KEY
        channel_id = config.BIRD_CHANNEL_ID

        return cls(
            bird_url, organization_id, workspace_id, api_key, signing_key, user_phone, channel_id
        )
    
    # TODO: Handle images and files
    @classmethod
    async def receive_message(self, request_body: dict) -> Message:
        """Handle an incoming message from a Bird SMS sender."""
        try:
            bird_message = BirdMessage(**request_body['payload'])
        except ValidationError as e:
            print(f"Error parsing Bird message data: {e}")
            raise MessageParsingError("Invalid Bird message format.") from e

        try:
            user_phone = bird_message.sender['contact']['identifierValue']
            channel_id = bird_message.channelId
            message_text = bird_message.body['text']['text']

            user_name = f"Bird User {user_phone[-4:]}"  # Last 4 digits of phone number

            message_type = MessageType.TEXT

            return Message(
                content=message_text,
                uid=user_phone,  # Using phone number as UID
                user_name=user_name,
                medium=MessageMedium.BIRD,
                type=message_type,
                raw_data=request_body
            )
        except KeyError as e:
            print(f"Error extracting data from Bird message: {e}")
            raise MessageParsingError(f"Missing key in Bird message: {e}") from e
    
    # TODO: Get verification that message was actually sent
    async def send_message(self, message: str) -> bool:
        """Send a Bird SMS message to the recipient."""
        try:
            url = f"{self._api_url}/workspaces/{self._workspace_id}/channels/{self._channel_id}/messages"
            payload = {
                "receiver": {
                    "contacts": [{"identifierValue": self._user_phone}]
                },
                "body": {"type": "text", "text": {"text": message}},
            }

            requests.post(url, headers=self._api_header, json=payload)
        except Exception as e:
            raise SendMessageError(f"Error sending message: {e}") from e

    async def register_webhook(self, event: str, webhook_url: str) -> None:
        """Register a webhook URL for receiving text events from Bird API."""
        url = (
            f"{self._api_url}/organizations/{self._organization_id}"
            f"/workspaces/{self._workspace_id}/webhook-subscriptions"
        )
        body = {
            "service": "channels",
            "event": event,
            "url": webhook_url,
            "signingKey": self._signing_key,
            "eventFilters": [{"key": "channelId", "value": self._channel_id}],
        }

        try:
            # List webhooks and delete if already existing
            webhooks = self._get_existing_webhooks()
            for webhook in webhooks["results"]:
                if ".ngrok-free.app" in webhook["url"]:
                    self._delete_webhook(webhook["id"])

            requests.post(url, headers=self._api_header, json=body)
        except Exception as e:
            raise WebhookError(f"Error registering Bird webhook: {e}") from e

    def _get_existing_webhooks(self) -> Optional[Dict]:
        """Retrieves the list of subscribed webhooks."""
        url = (
            f"{self._api_url}/organizations/{self._organization_id}"
            f"/workspaces/{self._workspace_id}/webhook-subscriptions"
        )
        try:
            response = requests.get(url, headers=self._api_header)
            return response.json()
        except Exception as e:
            raise WebhookError(f"Error getting existing Bird webhooks: {e}") from e

    def _delete_webhook(self, webhook_id: str) -> None:
        """Deletes a Bird webhook given a webhook id."""
        url = (
            f"{self._api_url}/organizations/{self._organization_id}"
            f"/workspaces/{self._workspace_id}/webhook-subscriptions/{webhook_id}"
        )
        try:
            requests.delete(url, headers=self._api_header)
        except Exception as e:
            raise WebhookError(f"Error deleting Bird webhook: {e}") from e
