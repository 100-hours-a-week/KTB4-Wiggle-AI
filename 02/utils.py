from fastapi import HTTPException, status


def check_author_identity(a, b) -> bool:
    if a != b:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit/delete your own posts"
        )
    else:
        return True
    
