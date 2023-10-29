def individual_serial(blog) -> dict:
    return {
        "id": str(blog["_id"]),
        "title": blog["title"],
        "content": blog["content"],
        "created_at": blog["created_at"]
    }


def list_serial(blogs) -> list:
    return [individual_serial(blog) for blog in blogs]