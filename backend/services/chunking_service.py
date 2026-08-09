def chunk_transcript(
    transcript: list,
    max_chars: int = 2000,
    overlap_chars: int = 200
):
    chunks = []

    current_parts = []
    current_length = 0

    for part in transcript:
        text = part["text"].strip()

        if not text:
            continue

        # Если добавление следующего subtitle превышает лимит,
        # сначала сохраняем текущий chunk.
        if current_parts and current_length + len(text) > max_chars:
            chunks.append({
                "start": current_parts[0]["start"],
                "end": (
                    current_parts[-1]["start"]
                    + current_parts[-1]["duration"]
                ),
                "text": " ".join(
                    part["text"] for part in current_parts
                )
            })

            # Оставляем небольшой overlap из предыдущего chunk.
            overlap_parts = []
            overlap_length = 0

            for previous_part in reversed(current_parts):
                if overlap_length + len(previous_part["text"]) > overlap_chars:
                    break

                overlap_parts.insert(0, previous_part)
                overlap_length += len(previous_part["text"])

            current_parts = overlap_parts
            current_length = sum(
                len(part["text"]) for part in current_parts
            )

        current_parts.append({
            "text": text,
            "start": part["start"],
            "duration": part["duration"]
        })

        current_length += len(text)

    # Последний chunk
    if current_parts:
        chunks.append({
            "start": current_parts[0]["start"],
            "end": (
                current_parts[-1]["start"]
                + current_parts[-1]["duration"]
            ),
            "text": " ".join(
                part["text"] for part in current_parts
            )
        })

    return chunks