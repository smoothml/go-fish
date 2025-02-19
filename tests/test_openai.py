"""Test the make_request function.

- Use pytest.
- Mock the OpenAI client.
- Test the happy path logs the response and the correct response is returned.
- Test that when the model name starts with "o`" or "o3", the temperature is ignored.
- Test that the function logs an error and returns an empty string when an exception is raised.
"""

import json
from unittest.mock import Mock, patch

import pytest
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion, Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from go_fish.openai import make_request


@patch("go_fish.openai.client")
def test_make_request(mock_client: OpenAI):
    """Test the make_request function.

    Args:
        mock_client: Mocked OpenAI client.
    """
    # Arrange
    mock_response = ChatCompletion(
        id="id",
        object="chat.completion",
        created=0,
        model="model",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(content="Response content", role="assistant"),
            )
        ],
    )
    mock_client.chat.completions.create.return_value = mock_response

    # Act
    response = make_request("Prompt")

    # Assert
    assert response == "Response content"
    mock_client.chat.completions.create.assert_called_once_with(
        messages=[{"role": "user", "content": "Prompt"}], model="gpt-4o-2024-08-06", temperature=0.7
    )
    mock_client.chat.completions.create.assert_called_once()
    mock_client.chat.completions.create.assert_called_once_with(
        messages=[{"role": "user", "content": "Prompt"}], model="gpt-4o-2024-08-06", temperature=0.7
    )


@patch("go_fish.openai.client")
def test_make_request_reasoning_model(mock_client: OpenAI, caplog: pytest.LogCaptureFixture) -> None:
    """Test the make_request function with a reasoning model.

    The temperature setting should be ignored.

    Args:
        mock_client: Mocked OpenAI client.
        caplog: Pytest fixture to capture logs.
    """
    # Arrange
    mock_response = ChatCompletion(
        id="id",
        object="chat.completion",
        created=0,
        model="model",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(content="Response content", role="assistant"),
            )
        ],
    )
    mock_client.chat.completions.create.return_value = mock_response

    # Act
    response = make_request("Prompt", model="o1-2024-08-06")

    # Assert
    assert response == "Response content"
    mock_client.chat.completions.create.assert_called_once_with(
        messages=[{"role": "user", "content": "Prompt"}], model="o1-2024-08-06"
    )
    assert "Using a reasoning model, ignoring temperature setting." in caplog.text


@patch("go_fish.openai.client")
def test_make_request_exception(mock_client: OpenAI, caplog: pytest.LogCaptureFixture) -> None:
    """Test the make_request function with an exception.

    The function should log an error and return an empty string.

    Args:
        mock_client: Mocked OpenAI client.
        caplog: Pytest fixture to capture logs.
    """
    # Arrange
    mock_client.chat.completions.create.side_effect = Exception("Error")

    # Act
    response = make_request("Prompt")

    # Assert
    assert response == ""
    assert "Error making request to OpenAI: Error" in caplog.text
    mock_client.chat.completions.create.assert_called_once_with(
        messages=[{"role": "user", "content": "Prompt"}], model="gpt-4o-2024-08-06", temperature=0.7
    )
    mock_client.chat.completions.create.assert_called_once()
    mock_client.chat.completions.create.assert_called_once_with(
        messages=[{"role": "user", "content": "Prompt"}], model="gpt-4o-2024-08-06", temperature=0.7
    )
