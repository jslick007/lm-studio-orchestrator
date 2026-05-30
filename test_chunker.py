from app.services.chunker import chunk_text


def test_chunker():
    # Create a long text
    text = "Hello world! " * 200  # roughly 400 tokens

    # Test splitting into 3 chunks with 50 token overlap
    # Since it's small, I'll use smaller chunk sizes
    chunks = chunk_text(text, chunk_size=100, overlap=20)

    print(f"Total chunks: {len(chunks)}")
    for chunk in chunks:
        print(
            f"Chunk {chunk['chunk_id']}: {chunk['start_token']} to {chunk['end_token']}"
        )

    # Check overlap
    if len(chunks) > 1:
        # End of chunk 0 should be > start of chunk 1
        if chunks[0]["end_token"] > chunks[1]["start_token"]:
            print("Overlap detected!")
        else:
            print("No overlap detected!")


if __name__ == "__main__":
    test_chunker()
