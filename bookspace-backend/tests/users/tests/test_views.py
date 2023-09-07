import pytest
from django.urls import reverse
from rest_framework import status

from users.models import *
from main.models import *


@pytest.mark.django_db
def test_user_flow(client):
    # Register a new user
    register_data = {
        "username": "test@example.com",
        "password": "testpassword",
        "first_name": "Peter",
        "last_name": "Evance",
        "phone_number": "+254712345699",
        "sex": SexChoices.MALE,
    }

    response = client.post("/auth/users/", register_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "username" in response.data
    user_id = response.data["id"]

    # Access user details (without authentication)
    response = client.get("/auth/users/me", follow=True)
    assert response.data["detail"] == "Authentication credentials were not provided."
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Log in
    login_data = {
        "username": "test@example.com",
        "password": "testpassword",
    }
    response = client.post(reverse("users:login"), login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "auth_token" in response.data
    token = response.data["auth_token"]

    # Access user details (with authentication)
    headers = {"Authorization": f"Token {token}"}
    response = client.get(
        "/auth/users/me", HTTP_AUTHORIZATION=f"Token {token}", follow=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert "username" in response.data
    assert response.data["username"] == "test@example.com"

    # Log out
    response = client.post(
        reverse("users:logout"),
        data={"token": token},
        HTTP_AUTHORIZATION=f"Token {token}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Attempt to access user details after logout
    headers = {"Authorization": f"Token {token}"}
    response = client.get(
        "/auth/users/me", HTTP_AUTHORIZATION=f"Token {token}", follow=True
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data
    assert response.data["detail"] == "Invalid token."


@pytest.mark.django_db
class TestRoleAssignments:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.regular_user_id = setup_users["regular_user_id"]
        self.regular_user_token = setup_users["regular_user_token"]
        self.regular_user_username = setup_users["regular_user_username"]

        self.bookspace_owner_token = setup_users["bookspace_owner_token"]
        self.bookspace_owner_user_id = setup_users["bookspace_owner_user_id"]
        self.bookspace_owner_user_username = setup_users["bookspace_owner_user_username"]

        self.bookspace_manager_token = setup_users["bookspace_manager_token"]
        self.bookspace_manager_user_id = setup_users["bookspace_manager_user_id"]
        self.bookspace_manager_user_username = setup_users["bookspace_manager_user_username"]

        self.asst_bookspace_manager_token = setup_users["asst_bookspace_manager_token"]
        self.asst_bookspace_manager_user_id = setup_users["asst_bookspace_manager_user_id"]
        self.asst_bookspace_manager_user_username = setup_users[
            "asst_bookspace_manager_user_username"
        ]

        self.bookspace_worker_token = setup_users["bookspace_worker_token"]
        self.bookspace_worker_user_id = setup_users["bookspace_worker_user_id"]
        self.bookspace_worker_user_username = setup_users["bookspace_worker_user_username"]

    def test_assign_to_self(self):
        # Assigning the role to oneself should be restricted
        user_ids = [self.bookspace_owner_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == "Cannot assign roles to yourself."

    def test_assign_bookspace_owner(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-owner"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been assigned as a bookspace owner."
        )

    def test_assign_bookspace_manager(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been assigned as a bookspace manager."
        )

    def test_assign_asst_bookspace_manager(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-assistant-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been assigned as an assistant bookspace manager."
        )

    def test_assign_bookspace_worker(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been assigned as a bookspace worker."
        )

    def test_assign_bookspace_manager_permission_denied(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
                response.data["message"]
                == "Only bookspace owners have permission to perform this action."
        )

    def test_assign_assistant_bookspace_manager_permission_denied(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-assistant-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
                response.data["message"]
                == "Only bookspace owners have permission to perform this action."
        )

    def test_assign_bookspace_worker_permission_denied(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-bookspace-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.asst_bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
                response.data["message"]
                == "Only bookspace owners and managers have permission to perform this action."
        )

    def test_dismiss_bookspace_manager(self):
        user_ids = [self.asst_bookspace_manager_user_id]
        response = self.client.post(
            reverse("users:dismiss-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.asst_bookspace_manager_user_username} has been dismissed as a bookspace manager."
        )

    def test_dismiss_asst_bookspace_manager(self):
        user_ids = [self.asst_bookspace_manager_user_id]
        response = self.client.post(
            reverse("users:dismiss-assistant-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.asst_bookspace_manager_user_username} has been dismissed as an "
                   f"assistant bookspace manager."
        )

    def test_dismiss_bookspace_worker(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:dismiss-bookspace-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
                response.data["message"]
                == f"User {self.regular_user_username} has been dismissed as a bookspace worker."
        )

    def test_dismiss_user_not_found(self):
        user_ids = ["99"]
        response = self.client.post(
            reverse("users:dismiss-bookspace-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.bookspace_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["error"] == "User with ID '99' was not found."


