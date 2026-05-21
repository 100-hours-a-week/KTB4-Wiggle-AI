from typing import Type
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import PostModel, CommentModel

def check_id_existence(db: Session,
                       model_cls: Type[PostModel]|Type[CommentModel],
                       id: int):
      if not model_cls.is_id_exists(db, id):
            entity_name = model_cls.__tablename__.capitalize()[:-1]
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{entity_name} not found"
            )

    
def check_author_identity(db: Session,
                          model_cls: Type[PostModel]|Type[CommentModel],
                          id: int,
                          author: str):
      
      return