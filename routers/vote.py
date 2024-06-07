from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import schema
import models
import database
import oauth2


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def get_vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user=Depends(oauth2.get_curr_user)):

    # Check if post exist
    post = db.query(models.BlogPost).filter(models.BlogPost.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does not exist")

    # Query to find if current user has already made a vote on input post id
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,
                                               models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    # If direction is 1 it means we want to upvote the post, means add vote in table
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already "
                                                                             f"voted on post {vote.post_id}")
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    # Direction 0 means delete vote so delete vote from table
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}
