from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from agents import orchestrator
from database import Comment, Vendor, get_db, init_db

app = FastAPI(title="Vendor Reviews API")


@app.on_event("startup")
def startup():
    init_db()


class VendorCreate(BaseModel):
    name: str


class CommentCreate(BaseModel):
    content: str


@app.post("/vendors")
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    if db.query(Vendor).filter(Vendor.name == vendor.name).first():
        raise HTTPException(status_code=400, detail="Vendor already exists")
    db_vendor = Vendor(name=vendor.name)
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor


@app.get("/vendors")
def list_vendors(db: Session = Depends(get_db)):
    return db.query(Vendor).all()


@app.post("/vendors/{vendor_id}/comments")
def add_comment(vendor_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    result = orchestrator("intake", comment=comment.content, vendor_name=vendor.name)

    if not result["valid"]:
        raise HTTPException(status_code=400, detail=f"Comment rejected: {result['reason']}")

    db_comment = Comment(
        vendor_id=vendor_id,
        content=result["cleaned_comment"],
        sentiment=result["sentiment"],
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return {
        "message": "Comment added",
        "sentiment": result["sentiment"],
        "comment": result["cleaned_comment"],
    }


@app.get("/vendors/{vendor_id}/comments")
def get_comments(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db.query(Comment).filter(Comment.vendor_id == vendor_id).all()


@app.get("/vendors/{vendor_id}/summary")
def get_summary(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    comments = db.query(Comment).filter(Comment.vendor_id == vendor_id).all()
    comments_data = [{"content": c.content, "sentiment": c.sentiment} for c in comments]
    summary = orchestrator("summarize", comments=comments_data, vendor_name=vendor.name)

    return {"vendor": vendor.name, "summary": summary, "total_comments": len(comments)}
