def chunk_transcript(
    transcript: list,
    chunk_duration: float = 60.0,
    overlap_duration: float = 10.0
):
    chunks = []

    if not transcript:
        return chunks

    current_parts = []
    chunk_start = None

    for part in transcript:
        text = part["text"].strip()

        if not text:
            continue

        start = float(part["start"])
        end = start + float(part["duration"])

        if chunk_start is None:
            chunk_start = start

        current_parts.append({
            "text": text,
            "start": start,
            "duration": float(part["duration"])
        })

        # Продолжаем собирать chunk,
        # пока не достигнем примерно 60 секунд.
        if end - chunk_start < chunk_duration:
            continue

        chunks.append({
            "start": chunk_start,
            "end": end,
            "text": " ".join(
                part["text"] for part in current_parts
            )
        })

        # Начинаем следующий chunk с overlap.
        overlap_start = end - overlap_duration

        current_parts = [
            part
            for part in current_parts
            if part["start"] >= overlap_start
        ]

        if current_parts:
            chunk_start = current_parts[0]["start"]
        else:
            chunk_start = None

    # Добавляем остаток transcript.
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