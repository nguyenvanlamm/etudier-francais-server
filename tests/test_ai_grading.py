from app.services.ai_grading import (
    _sanitize_input,
    _get_level_from_exam_id,
    build_system_prompt,
    parse_response,
)


class TestSanitizeInput:
    def test_clean_text_passes_through(self):
        result = _sanitize_input("Bonjour, je m'appelle Pierre.")
        assert result == "Bonjour, je m'appelle Pierre."

    def test_removes_control_characters(self):
        result = _sanitize_input("hello\x00world\x01test")
        assert result == "helloworldtest"

    def test_removes_null_bytes(self):
        result = _sanitize_input("\x00\x01\x02")
        assert result == ""

    def test_truncates_long_text(self):
        long_text = "a" * 6000
        result = _sanitize_input(long_text)
        assert len(result) == 5003  # max_length + "..."
        assert result.endswith("...")

    def test_preserves_newlines(self):
        result = _sanitize_input("line1\nline2\nline3")
        assert result == "line1\nline2\nline3"

    def test_preserves_tabs(self):
        # \t is 0x09, which is NOT in the stripped range \x00-\x08 \x0b\x0c\x0e-\x1f
        result = _sanitize_input("col1\tcol2")
        assert result == "col1\tcol2"


class TestGetLevelFromExamId:
    def test_delf_a1(self):
        assert _get_level_from_exam_id("delf-a1-2024") == "A1"

    def test_delf_a2(self):
        assert _get_level_from_exam_id("delf-a2-sample") == "A2"

    def test_delf_b1(self):
        assert _get_level_from_exam_id("delf-b1-test") == "B1"

    def test_delf_b2(self):
        assert _get_level_from_exam_id("delf-b2-exam") == "B2"

    def test_dalf_c1(self):
        assert _get_level_from_exam_id("dalf-c1-2024") == "C1"

    def test_dalf_c2(self):
        assert _get_level_from_exam_id("dalf-c2-practice") == "C2"

    def test_tcf_returns_b2(self):
        assert _get_level_from_exam_id("tcf-test") == "B2"

    def test_unknown_prefix_returns_b1(self):
        assert _get_level_from_exam_id("unknown-exam") == "B1"

    def test_empty_string_returns_b1(self):
        assert _get_level_from_exam_id("") == "B1"

    def test_exact_match(self):
        assert _get_level_from_exam_id("delf-a1") == "A1"


class TestBuildSystemPrompt:
    def test_returns_string(self):
        prompt = build_system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 100

    def test_contains_key_sections(self):
        prompt = build_system_prompt()
        assert "giám khảo chấm thi viết DELF/DALF" in prompt
        assert "NHIỆM VỤ" in prompt
        assert "YÊU CẦU ĐẦU RA" in prompt
        assert "results" in prompt
        assert "taskCompletion" in prompt
        assert "feedback" in prompt
        assert "improvements" in prompt
        assert "criteria" in prompt


class TestParseResponse:
    def test_valid_json_with_all_fields(self):
        response_text = """{
            "results": {
                "q1": {
                    "score": 15,
                    "feedback": "Bài làm tốt",
                    "improvements": ["Cải thiện từ vựng"],
                    "criteria": {
                        "taskCompletion": 16,
                        "coherence": 14,
                        "grammar": 15,
                        "vocabulary": 13,
                        "relevance": 17
                    }
                }
            }
        }"""
        result = parse_response(response_text, ["q1"])
        assert "q1" in result
        assert result["q1"]["score"] == 15
        assert result["q1"]["feedback"] == "Bài làm tốt"
        assert result["q1"]["improvements"] == ["Cải thiện từ vựng"]
        assert result["q1"]["criteria"]["taskCompletion"] == 16
        assert result["q1"]["criteria"]["coherence"] == 14
        assert result["q1"]["criteria"]["grammar"] == 15
        assert result["q1"]["criteria"]["vocabulary"] == 13
        assert result["q1"]["criteria"]["relevance"] == 17

    def test_missing_question_id_returns_empty(self):
        response_text = '{"results": {}}'
        result = parse_response(response_text, ["q1"])
        assert result["q1"]["score"] == 0
        assert result["q1"]["feedback"] == ""
        assert result["q1"]["improvements"] == []
        assert result["q1"]["criteria"] == {}

    def test_invalid_json_returns_empty_dict(self):
        result = parse_response("not json", ["q1"])
        assert result == {}

    def test_partial_criteria(self):
        response_text = """{
            "results": {
                "q1": {
                    "score": 10,
                    "feedback": "OK",
                    "improvements": [],
                    "criteria": {
                        "taskCompletion": 10
                    }
                }
            }
        }"""
        result = parse_response(response_text, ["q1"])
        assert result["q1"]["score"] == 10
        assert result["q1"]["criteria"]["taskCompletion"] == 10
        assert result["q1"]["criteria"]["coherence"] is None

    def test_multiple_questions(self):
        response_text = """{
            "results": {
                "q1": {"score": 15, "feedback": "A", "improvements": [], "criteria": {}},
                "q2": {"score": 18, "feedback": "B", "improvements": [], "criteria": {}}
            }
        }"""
        result = parse_response(response_text, ["q1", "q2"])
        assert result["q1"]["score"] == 15
        assert result["q2"]["score"] == 18
