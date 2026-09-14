import pytest
from services.chunking_service import chunk_transcript


class TestChunkingService:
    def test_empty_transcript_returns_empty_list(self):
        assert chunk_transcript([]) == []
        assert chunk_transcript(None) == []

    def test_ignores_whitespace_and_empty_text(self):
        transcript = [
            {"text": "", "start": 0.0, "duration": 2.0},
            {"text": "   ", "start": 2.0, "duration": 2.0},
            {"text": "Valid speech", "start": 4.0, "duration": 3.0},
            {"text": "\n\t", "start": 7.0, "duration": 1.0},
        ]
        chunks = chunk_transcript(transcript, chunk_duration=60.0)
        assert len(chunks) == 1
        assert chunks[0]["text"] == "Valid speech"
        assert chunks[0]["start"] == 4.0
        assert chunks[0]["end"] == 7.0

    def test_single_chunk_under_duration(self, sample_transcript):
        # Total duration is 16.5s, default chunk_duration is 60s
        chunks = chunk_transcript(sample_transcript, chunk_duration=60.0)
        assert len(chunks) == 1
        chunk = chunks[0]
        assert chunk["start"] == 0.0
        assert chunk["end"] == 16.5
        expected_text = "Hello world and welcome to the video. Today we are learning Python testing. Unit tests are very important. They prevent regressions."
        assert chunk["text"] == expected_text

    def test_multiple_chunks_with_overlap(self):
        transcript = [
            {"text": f"Sentence {i}.", "start": float(i * 10), "duration": 10.0}
            for i in range(10)  # 0s to 100s, each 10s
        ]
        # chunk_duration=30s, overlap_duration=10s
        # 1st chunk covers Sentence 0, 1, 2 (end = 30s)
        # overlap_start = 30 - 10 = 20s -> keeps Sentence 2 (start 20 >= 20)
        chunks = chunk_transcript(transcript, chunk_duration=30.0, overlap_duration=10.0)

        assert len(chunks) >= 3
        # Verify first chunk
        assert chunks[0]["start"] == 0.0
        assert chunks[0]["end"] == 30.0
        assert "Sentence 0." in chunks[0]["text"]
        assert "Sentence 1." in chunks[0]["text"]
        assert "Sentence 2." in chunks[0]["text"]

        # Verify overlap: Sentence 2 should be at the beginning of chunk 2
        assert "Sentence 2." in chunks[1]["text"]
        assert chunks[1]["start"] == 20.0

    def test_custom_chunk_and_overlap_duration(self):
        transcript = [
            {"text": "Part A", "start": 0.0, "duration": 5.0},
            {"text": "Part B", "start": 5.0, "duration": 5.0},
            {"text": "Part C", "start": 10.0, "duration": 5.0},
        ]
        # chunk_duration=10s, overlap_duration=5s
        # 1st chunk: Part A + Part B (0 to 10s)
        # 2nd chunk: Part B + Part C (5 to 15s)
        # Remainder chunk: Part C (10 to 15s) from final overlap window
        chunks = chunk_transcript(transcript, chunk_duration=10.0, overlap_duration=5.0)
        assert len(chunks) == 3

        # Chunk 1: Part A + Part B (0 to 10s)
        assert chunks[0]["start"] == 0.0
        assert chunks[0]["end"] == 10.0
        assert chunks[0]["text"] == "Part A Part B"

        # Chunk 2: Part B + Part C (5 to 15s)
        assert chunks[1]["start"] == 5.0
        assert chunks[1]["end"] == 15.0
        assert chunks[1]["text"] == "Part B Part C"

        # Remainder Chunk 3: Part C (10 to 15s)
        assert chunks[2]["start"] == 10.0
        assert chunks[2]["end"] == 15.0
        assert chunks[2]["text"] == "Part C"

    def test_all_empty_entries_returns_empty_list(self):
        transcript = [
            {"text": "", "start": 0.0, "duration": 5.0},
            {"text": "   ", "start": 5.0, "duration": 5.0},
        ]
        chunks = chunk_transcript(transcript)
        assert chunks == []
