from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
 
app = FastAPI()
 
class Feedback(BaseModel):
    feedback: str
 
 
@app.post("/feedback", response_model=Feedback, status_code=201)
def leave_feedback(feedback: Feedback):
    feedback_text = feedback.feedback.strip()
 
    # Проверяем наличие комментария
    if len(feedback_text) == 0:
        raise HTTPException(status_code=400, detail="Комментарий не может быть пустым.")
 
    # Проверяем длину комментария
    if len(feedback_text) < 2:
        raise HTTPException(status_code=400, detail="Комментарий должен содержать не менее 2 символов.")
 
    # Проверяем запрещенную фразу
    if "я молодец" in feedback_text.lower():
        raise HTTPException(status_code=400, detail="Запрещено использовать фразу 'я молодец'.")
 
    return {"message": "Спасибо за комментарий!", "feedback": "Спасибо за комментарий!", "status": "ok"}
 