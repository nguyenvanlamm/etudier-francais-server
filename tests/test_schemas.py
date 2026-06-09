from app.schemas.exam import ExamSubmitRequest, ExamResponse, ExamReviewResponse
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse,
    LoginRequest, RegisterRequest, GoogleLoginRequest,
    RefreshTokenRequest, LogoutRequest,
)
import pytest


class TestExamSchemas:
    def test_exam_submit_request_valid(self):
        req = ExamSubmitRequest(answers={"q1": "answer text"}, timeSpent=120)
        assert req.answers == {"q1": "answer text"}
        assert req.timeSpent == 120

    def test_exam_submit_request_empty_answers(self):
        req = ExamSubmitRequest(answers={}, timeSpent=0)
        assert req.answers == {}

    def test_exam_submit_request_long_answer_raises(self):
        with pytest.raises(ValueError, match="exceeds 10000 characters"):
            ExamSubmitRequest(answers={"q1": "x" * 10001}, timeSpent=120)

    def test_exam_submit_request_strips_control_chars(self):
        req = ExamSubmitRequest(answers={"q1": "hello\x00world\x01test"}, timeSpent=120)
        assert req.answers == {"q1": "helloworldtest"}

    def test_exam_submit_request_control_chars_only(self):
        req = ExamSubmitRequest(answers={"q1": "\x00\x01\x02"}, timeSpent=120)
        assert req.answers == {"q1": ""}

    def test_exam_response_model(self):
        resp = ExamResponse(
            id="exam-1", courseSlug="delf-a1", name="Test",
            duration=60, questionCount=10, skills={"writing": 2},
        )
        assert resp.id == "exam-1"
        assert resp.status is None
        assert resp.attempts == 0

    def test_exam_response_with_optional_fields(self):
        resp = ExamResponse(
            id="exam-1", courseSlug="delf-a1", name="Test",
            duration=60, questionCount=10, skills={"writing": 2},
            status="active", attempts=3, highestScore=85.5,
        )
        assert resp.status == "active"
        assert resp.attempts == 3
        assert resp.highestScore == 85.5

    def test_exam_review_response(self):
        resp = ExamReviewResponse(
            exam={"id": "e1"}, result={"score": 80},
            questions=[{"id": "q1"}], userAnswers={"q1": "ans"},
        )
        assert resp.exam["id"] == "e1"
        assert resp.userAnswers == {"q1": "ans"}


class TestUserSchemas:
    def test_user_create_valid(self):
        u = UserCreate(email="test@example.com", password="secret123", name="Test")
        assert u.email == "test@example.com"
        assert u.password == "secret123"
        assert u.name == "Test"

    def test_user_create_no_name(self):
        u = UserCreate(email="test@example.com", password="secret123")
        assert u.name is None

    def test_user_create_invalid_email(self):
        with pytest.raises(ValueError):
            UserCreate(email="not-an-email", password="secret123")

    def test_user_update_empty(self):
        u = UserUpdate()
        assert u.name is None
        assert u.image is None

    def test_user_update_partial(self):
        u = UserUpdate(name="New Name")
        assert u.name == "New Name"
        assert u.image is None

    def test_user_response(self):
        u = UserResponse(
            id=1, email="user@example.com", name="User",
            is_pro=False, is_verified=True,
        )
        assert u.id == 1
        assert u.is_pro is False
        assert u.is_verified is True

    def test_login_request_valid(self):
        req = LoginRequest(email="a@b.com", password="pwd")
        assert req.email == "a@b.com"

    def test_login_request_invalid_email(self):
        with pytest.raises(ValueError):
            LoginRequest(email="bad", password="pwd")

    def test_register_request(self):
        req = RegisterRequest(name="A", email="a@b.com", password="pwd")
        assert req.name == "A"

    def test_google_login_request(self):
        req = GoogleLoginRequest(idToken="token123")
        assert req.idToken == "token123"

    def test_refresh_token_request(self):
        req = RefreshTokenRequest(refreshToken="rtoken")
        assert req.refreshToken == "rtoken"

    def test_logout_request(self):
        req = LogoutRequest(refreshToken="rtoken")
        assert req.refreshToken == "rtoken"
