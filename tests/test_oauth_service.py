"""
Unit tests for OAuthService and PKCE flow.
"""

import pytest
import requests
from src.auth.oauth_service import generate_pkce_pair, OAuthService

def test_pkce_generation():
    verifier, challenge = generate_pkce_pair()
    assert len(verifier) >= 43
    assert len(challenge) >= 43
    assert verifier != challenge

def test_token_exchange_mock(monkeypatch):
    class MockResponse:
        status_code = 200
        def json(self):
            return {
                "access_token": "mock-access-token",
                "refresh_token": "mock-refresh-token",
                "expires_in": 3600
            }

    monkeypatch.setattr(requests, "post", lambda url, data, timeout: MockResponse())

    svc = OAuthService()
    tokens = svc.exchange_code_for_tokens(
        provider="google",
        code="mock-auth-code",
        verifier="mock-verifier",
        redirect_uri="http://127.0.0.1:8080/callback",
        client_id="mock-client-id"
    )

    assert tokens["access_token"] == "mock-access-token"
    assert tokens["refresh_token"] == "mock-refresh-token"

def test_fetch_user_email_google(monkeypatch):
    class MockResponse:
        status_code = 200
        def json(self):
            return {"email": "user@gmail.com"}

    monkeypatch.setattr(requests, "get", lambda url, headers, timeout: MockResponse())

    svc = OAuthService()
    email = svc.fetch_user_email("google", "mock-access-token")
    assert email == "user@gmail.com"
