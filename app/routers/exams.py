from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, Optional
from app.database import get_db
from app.models.user import User
from app.models.exam import Exam, ExamResult
from app.schemas.exam import ExamSubmitRequest, ExamReviewResponse
from app.routers.auth import get_current_user as get_user
from app.services.auth import decode_token


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    return user

router = APIRouter(prefix="/tests", tags=["exams"])

MOCK_EXAMS = [
    # DELF A1
    {
        "id": "delf-a1-full-1",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 1",
        "duration": 80,
        "questionCount": 50,
        "difficulty": "easy",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2024-12-01",
    },
    {
        "id": "delf-a1-full-2",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 2",
        "duration": 80,
        "questionCount": 50,
        "difficulty": "medium",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2024-12-10",
    },
    {
        "id": "delf-a1-full-3",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 3",
        "duration": 80,
        "questionCount": 50,
        "difficulty": "medium",
        "skills": {"listening": 30, "reading": 30, "writing": 20, "speaking": 20},
        "createdAt": "2024-12-20",
    },
    {
        "id": "delf-a1-full-4",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 4",
        "duration": 80,
        "questionCount": 50,
        "difficulty": "easy",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-01-05",
    },
    {
        "id": "delf-a1-full-5",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 5",
        "duration": 80,
        "questionCount": 55,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-01-15",
    },
    {
        "id": "delf-a1-full-6",
        "courseSlug": "delf-a1",
        "name": "DELF A1 - Đề số 6",
        "duration": 80,
        "questionCount": 50,
        "difficulty": "medium",
        "skills": {"listening": 30, "reading": 20, "writing": 25, "speaking": 25},
        "createdAt": "2025-02-01",
    },
    # DELF A2
    {
        "id": "delf-a2-full-1",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 1",
        "duration": 100,
        "questionCount": 60,
        "difficulty": "easy",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2024-12-01",
    },
    {
        "id": "delf-a2-full-2",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 2",
        "duration": 100,
        "questionCount": 60,
        "difficulty": "medium",
        "skills": {"listening": 30, "reading": 30, "writing": 20, "speaking": 20},
        "createdAt": "2024-12-10",
    },
    {
        "id": "delf-a2-full-3",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 3",
        "duration": 100,
        "questionCount": 60,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2024-12-18",
    },
    {
        "id": "delf-a2-full-4",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 4",
        "duration": 100,
        "questionCount": 60,
        "difficulty": "medium",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-01-08",
    },
    {
        "id": "delf-a2-full-5",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 5",
        "duration": 100,
        "questionCount": 65,
        "difficulty": "hard",
        "skills": {"listening": 30, "reading": 25, "writing": 20, "speaking": 25},
        "createdAt": "2025-01-20",
    },
    {
        "id": "delf-a2-full-6",
        "courseSlug": "delf-a2",
        "name": "DELF A2 - Đề số 6",
        "duration": 100,
        "questionCount": 60,
        "difficulty": "easy",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-02-03",
    },
    # DELF B1
    {
        "id": "delf-b1-full-1",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 1",
        "duration": 115,
        "questionCount": 70,
        "difficulty": "medium",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2024-12-01",
    },
    {
        "id": "delf-b1-full-2",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 2",
        "duration": 115,
        "questionCount": 70,
        "difficulty": "hard",
        "skills": {"listening": 30, "reading": 30, "writing": 20, "speaking": 20},
        "createdAt": "2024-12-10",
    },
    {
        "id": "delf-b1-full-3",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 3",
        "duration": 115,
        "questionCount": 70,
        "difficulty": "easy",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-01-03",
    },
    {
        "id": "delf-b1-full-4",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 4",
        "duration": 115,
        "questionCount": 75,
        "difficulty": "medium",
        "skills": {"listening": 25, "reading": 30, "writing": 25, "speaking": 20},
        "createdAt": "2025-01-18",
    },
    {
        "id": "delf-b1-full-5",
        "courseSlug": "delf-b1",
        "name": "DELF B1 - Đề số 5",
        "duration": 115,
        "questionCount": 70,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-02-05",
    },
    # DELF B2
    {
        "id": "delf-b2-full-1",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 1",
        "duration": 150,
        "questionCount": 80,
        "difficulty": "medium",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2024-12-01",
    },
    {
        "id": "delf-b2-full-2",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 2",
        "duration": 150,
        "questionCount": 80,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2024-12-10",
    },
    {
        "id": "delf-b2-full-3",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 3",
        "duration": 150,
        "questionCount": 80,
        "difficulty": "easy",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-01-05",
    },
    {
        "id": "delf-b2-full-4",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 4",
        "duration": 150,
        "questionCount": 85,
        "difficulty": "medium",
        "skills": {"listening": 30, "reading": 25, "writing": 20, "speaking": 25},
        "createdAt": "2025-01-22",
    },
    {
        "id": "delf-b2-full-5",
        "courseSlug": "delf-b2",
        "name": "DELF B2 - Đề số 5",
        "duration": 150,
        "questionCount": 80,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-02-06",
    },
    # DALF C1
    {
        "id": "dalf-c1-full-1",
        "courseSlug": "dalf-c1",
        "name": "DALF C1 - Đề số 1",
        "duration": 240,
        "questionCount": 80,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2024-12-01",
    },
    {
        "id": "dalf-c1-full-2",
        "courseSlug": "dalf-c1",
        "name": "DALF C1 - Đề số 2",
        "duration": 240,
        "questionCount": 80,
        "difficulty": "medium",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-01-10",
    },
    {
        "id": "dalf-c1-full-3",
        "courseSlug": "dalf-c1",
        "name": "DALF C1 - Đề số 3",
        "duration": 240,
        "questionCount": 85,
        "difficulty": "hard",
        "skills": {"listening": 30, "reading": 25, "writing": 25, "speaking": 20},
        "createdAt": "2025-01-25",
    },
    {
        "id": "dalf-c1-full-4",
        "courseSlug": "dalf-c1",
        "name": "DALF C1 - Đề số 4",
        "duration": 240,
        "questionCount": 80,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-02-07",
    },
    # DALF C2
    {
        "id": "dalf-c2-full-1",
        "courseSlug": "dalf-c2",
        "name": "DALF C2 - Đề số 1",
        "duration": 210,
        "questionCount": 60,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2024-12-01",
    },
    {
        "id": "dalf-c2-full-2",
        "courseSlug": "dalf-c2",
        "name": "DALF C2 - Đề số 2",
        "duration": 210,
        "questionCount": 60,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-01-12",
    },
    {
        "id": "dalf-c2-full-3",
        "courseSlug": "dalf-c2",
        "name": "DALF C2 - Đề số 3",
        "duration": 210,
        "questionCount": 65,
        "difficulty": "hard",
        "skills": {"listening": 30, "reading": 25, "writing": 20, "speaking": 25},
        "createdAt": "2025-01-28",
    },
    {
        "id": "dalf-c2-full-4",
        "courseSlug": "dalf-c2",
        "name": "DALF C2 - Đề số 4",
        "duration": 210,
        "questionCount": 60,
        "difficulty": "hard",
        "skills": {"listening": 25, "reading": 25, "writing": 25, "speaking": 25},
        "createdAt": "2025-02-08",
    },
    # TCF
    {
        "id": "tcf-full-1",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 1",
        "duration": 150,
        "questionCount": 100,
        "difficulty": "medium",
        "skills": {"listening": 33, "reading": 33, "writing": 0, "speaking": 34},
        "createdAt": "2024-12-01",
    },
    {
        "id": "tcf-full-2",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 2",
        "duration": 150,
        "questionCount": 100,
        "difficulty": "hard",
        "skills": {"listening": 33, "reading": 33, "writing": 0, "speaking": 34},
        "createdAt": "2024-12-10",
    },
    {
        "id": "tcf-full-3",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 3",
        "duration": 150,
        "questionCount": 100,
        "difficulty": "easy",
        "skills": {"listening": 33, "reading": 33, "writing": 0, "speaking": 34},
        "createdAt": "2025-01-06",
    },
    {
        "id": "tcf-full-4",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 4",
        "duration": 150,
        "questionCount": 100,
        "difficulty": "medium",
        "skills": {"listening": 33, "reading": 33, "writing": 0, "speaking": 34},
        "createdAt": "2025-01-20",
    },
    {
        "id": "tcf-full-5",
        "courseSlug": "tcf",
        "name": "TCF - Đề số 5",
        "duration": 150,
        "questionCount": 100,
        "difficulty": "hard",
        "skills": {"listening": 33, "reading": 33, "writing": 0, "speaking": 34},
        "createdAt": "2025-02-04",
    },
]

MOCK_QUESTIONS = {
    "delf-a1-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Ecoutez la conversation et répondez.", "instruction": "Qu'est-ce que Marie fait ce week-end?", "options": ["Elle va au cinéma", "Elle fait du shopping", "Elle rencontre des amis", "Elle reste chez elle"], "correctAnswer": "Elle va au cinéma", "points": 1},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Ecoutez l'annonce et répondez.", "instruction": "A quelle heure part le train?", "options": ["10h00", "10h15", "10h30", "10h45"], "correctAnswer": "10h30", "points": 1},
        {"id": "q3", "skill": "listening", "type": "multiple_choice", "content": "Twoutez le dialogue.", "instruction": "Comment s'appelle le personnage?", "options": ["Pierre", "Paul", "Jean", "Luc"], "correctAnswer": "Pierre", "points": 1},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez le texte et répondez.", "instruction": "De quelle couleur est la robe?", "options": ["Rouge", "Bleue", "Verte", "Jaune"], "correctAnswer": "Bleue", "points": 1},
        {"id": "q5", "skill": "reading", "type": "true_false", "content": "Lisez l'email et dites si c'est vrai ou faux.", "instruction": "Le rendez-vous est à 14h.", "correctAnswer": "true", "points": 1},
        {"id": "q6", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article.", "instruction": "Quel est le thème principal?", "options": ["Voyage", "Travail", "Famille", "Loisirs"], "correctAnswer": "Voyage", "points": 1},
        {"id": "q7", "skill": "writing", "type": "short_answer", "content": "Ecrivez une phrase pour présenter votre famille.", "instruction": "Utilisez au moins 3 mots.", "correctAnswer": "", "points": 5},
        {"id": "q8", "skill": "writing", "type": "short_answer", "content": "Décrivez votre journée idéale.", "instruction": "Ecrivez 5-10 mots.", "correctAnswer": "", "points": 5},
        {"id": "q9", "skill": "speaking", "type": "short_answer", "content": "Présentez-vous en quelques phrases.", "instruction": "Parlez de votre nom, votre âge et votre origine.", "correctAnswer": "", "points": 5},
        {"id": "q10", "skill": "speaking", "type": "short_answer", "content": "Décrivez votre lieu de vie.", "instruction": "Où habitez-vous? Combien de pièces?", "correctAnswer": "", "points": 5},
    ],
    "delf-a1-full-2": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Twoutez la conversation.", "instruction": "Que fait le personnage?", "options": ["Mange", "Dort", "Travaille", "Lis"], "correctAnswer": "Travaille", "points": 1},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Twoutez l'annonce.", "instruction": "Quel jour a lieu l'événement?", "options": ["Lundi", "Mardi", "Mercredi", "Jeudi"], "correctAnswer": "Mercredi", "points": 1},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez la carte.", "instruction": "Quel restaurant est recommandé?", "options": ["Le Paris", "La Maison", "Le Jardin", "La Terrace"], "correctAnswer": "Le Paris", "points": 1},
        {"id": "q4", "skill": "reading", "type": "true_false", "content": "Lisez le message.", "instruction": "Le message est urgent.", "correctAnswer": "true", "points": 1},
        {"id": "q5", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article.", "instruction": "De quoi parle l'article?", "options": ["Météo", "Sport", "Politique", "Culture"], "correctAnswer": "Culture", "points": 1},
        {"id": "q6", "skill": "writing", "type": "short_answer", "content": "Twrivez une carte postale.", "instruction": "Décrivez où vous êtes.", "correctAnswer": "", "points": 5},
        {"id": "q7", "skill": "writing", "type": "short_answer", "content": "Twrivez vos coordonnées.", "instruction": "Donnez votre adresse et téléphone.", "correctAnswer": "", "points": 5},
        {"id": "q8", "skill": "speaking", "type": "short_answer", "content": "Décrivez votre ami.", "instruction": "Comment est-il/elle?", "correctAnswer": "", "points": 5},
        {"id": "q9", "skill": "speaking", "type": "short_answer", "content": "Parlez de vos activités.", "instruction": "Qu'aimez-vous faire?", "correctAnswer": "", "points": 5},
    ],
    "delf-a2-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Twoutez le dialogue.", "instruction": "Où vont les personnages?", "options": ["Au cinéma", "Au restaurant", "Au musée", "A la gare"], "correctAnswer": "Au restaurant", "points": 1},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Twoutez les informations.", "instruction": "Quel temps fait-il?", "options": ["Beau", "Mauvais", "Pluieux", "Neige"], "correctAnswer": "Beau", "points": 1},
        {"id": "q3", "skill": "listening", "type": "true_false", "content": "Twoutez la conversation.", "instruction": "Le rendez-vous est confirmé.", "correctAnswer": "true", "points": 1},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article de journal.", "instruction": "Quel est l'événement?", "options": ["Fête", "Concert", "Exhibition", "Competition"], "correctAnswer": "Concert", "points": 1},
        {"id": "q5", "skill": "reading", "type": "multiple_choice", "content": "Lisez la publicité.", "instruction": "Quel est le prix?", "options": ["50€", "75€", "100€", "150€"], "correctAnswer": "75€", "points": 1},
        {"id": "q6", "skill": "reading", "type": "true_false", "content": "Lisez la lettre.", "instruction": "L'expéditeur est content.", "correctAnswer": "false", "points": 1},
        {"id": "q7", "skill": "writing", "type": "short_answer", "content": "Twrivez un message à un ami.", "instruction": "Parlez de vos projets pour le week-end.", "correctAnswer": "", "points": 5},
        {"id": "q8", "skill": "writing", "type": "short_answer", "content": "Twrivez un email professionnel.", "instruction": "Demandez des informations sur un produit.", "correctAnswer": "", "points": 5},
        {"id": "q9", "skill": "speaking", "type": "short_answer", "content": "Présentez un sujet qui vous passionne.", "instruction": "Expliquez pourquoi cela vous interesse.", "correctAnswer": "", "points": 5},
        {"id": "q10", "skill": "speaking", "type": "short_answer", "content": "Décrivez votre lieu de travail.", "instruction": "Parlez de votre environnement professionnel.", "correctAnswer": "", "points": 5},
    ],
    "delf-b1-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Twoutez le journal télévisé.", "instruction": "Quel est le sujet principal?", "options": ["Economie", "Politique", "Société", "Culture"], "correctAnswer": "Société", "points": 1},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Twoutez l'interview.", "instruction": "Quel métier exerce la personne?", "options": ["Médecin", "Avocat", "Professeur", "Ingénieur"], "correctAnswer": "Professeur", "points": 1},
        {"id": "q3", "skill": "listening", "type": "true_false", "content": "Twoutez le débat.", "instruction": "Les participants sont d'accord.", "correctAnswer": "false", "points": 1},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article scientifique.", "instruction": "Quelle est la conclusion?", "options": ["Positive", "Négative", "Neutre", "Inconnue"], "correctAnswer": "Positive", "points": 1},
        {"id": "q5", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'essai.", "instruction": "Quel est l'argument principal?", "options": ["Environnement", "Education", "Santé", "Technologie"], "correctAnswer": "Education", "points": 1},
        {"id": "q6", "skill": "reading", "type": "multiple_choice", "content": "Lisez le roman.", "instruction": "Quel est le sentiment dominant?", "options": ["Joie", "Tristesse", "Peur", "Espoir"], "correctAnswer": "Espoir", "points": 1},
        {"id": "q7", "skill": "writing", "type": "essay", "content": "Twrivez une dissertation.", "instruction": "Les réseaux sociaux sont-ils utiles?", "correctAnswer": "", "points": 10},
        {"id": "q8", "skill": "writing", "type": "essay", "content": "Twrivez une lettre formelle.", "instruction": "Postulez pour un emploi.", "correctAnswer": "", "points": 10},
        {"id": "q9", "skill": "speaking", "type": "short_answer", "content": "Présentez un sujet d'actualité.", "instruction": "Expliquez votre point de vue.", "correctAnswer": "", "points": 10},
        {"id": "q10", "skill": "speaking", "type": "short_answer", "content": "Participez à un débat.", "instruction": "Argumentez pour ou contre.", "correctAnswer": "", "points": 10},
    ],
    "delf-b2-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Twoutez la conférence.", "instruction": "Quelle est la thèse présentée?", "options": ["A", "B", "C", "D"], "correctAnswer": "A", "points": 1},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Twoutez le documentaire.", "instruction": "Quel aspect est développé?", "options": ["Historique", "Scientifique", "Culturel", "Social"], "correctAnswer": "Scientifique", "points": 1},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article académique.", "instruction": "Quelle méthodologie est utilisée?", "options": ["Quantitative", "Qualitative", "Mixte", "Autre"], "correctAnswer": "Mixte", "points": 1},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'éditorial.", "instruction": "Quelle position défend l'auteur?", "options": ["Conservatrice", "Libérale", "Neutre", "Extrémiste"], "correctAnswer": "Libérale", "points": 1},
        {"id": "q5", "skill": "writing", "type": "essay", "content": "Twrivez un essai argumenté.", "instruction": "La technologie améliore-t-elle la vie?", "correctAnswer": "", "points": 15},
        {"id": "q6", "skill": "writing", "type": "essay", "content": "Twrivez un article de presse.", "instruction": "Sujets d'actualité au choix.", "correctAnswer": "", "points": 15},
        {"id": "q7", "skill": "speaking", "type": "short_answer", "content": "Présentez un exposé.", "instruction": "Sujet libre de 3 minutes.", "correctAnswer": "", "points": 15},
    ],
    "dalf-c1-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Twoutez l'émission littéraire.", "instruction": "Quel obra est analysée?", "options": ["Roman", "Poésie", "Théâtre", "Essai"], "correctAnswer": "Roman", "points": 1},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Twoutez le discours.", "instruction": "Quel est le registre de langue?", "options": ["Familier", "Courant", "Soutenu", "Littéraire"], "correctAnswer": "Soutenu", "points": 1},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'extrait littéraire.", "instruction": "Identifiez le style de l'auteur.", "options": ["Réalisme", "Romantisme", "Naturalisme", "Symbolisme"], "correctAnswer": "Réalisme", "points": 1},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article philosophique.", "instruction": "Quelle école de pensée?", "options": ["Existentialisme", "Matérialisme", "Idéalisme", "Positivisme"], "correctAnswer": "Existentialisme", "points": 1},
        {"id": "q5", "skill": "writing", "type": "essay", "content": "Twrivez une dissertation littéraire.", "instruction": "Analysez un oeuvre au choix.", "correctAnswer": "", "points": 20},
        {"id": "q6", "skill": "writing", "type": "essay", "content": "Twrivez un essai philosophique.", "instruction": "Réflexion sur un concept au choix.", "correctAnswer": "", "points": 20},
        {"id": "q7", "skill": "speaking", "type": "short_answer", "content": "Exposé avancé.", "instruction": "Sujet complexe avec argumentation.", "correctAnswer": "", "points": 20},
    ],
    "dalf-c2-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Twoutez le débat académique.", "instruction": "Identifiez les nuances du discours.", "options": ["A", "B", "C", "D"], "correctAnswer": "C", "points": 1},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Twoutez la conférence spécialisée.", "instruction": "Synthétisez les idées principales.", "options": ["1", "2", "3", "4"], "correctAnswer": "2", "points": 1},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article de recherche.", "instruction": "Critiquez la méthodologie.", "options": ["Forte", "Faible", "Moyenne", "Insufficient"], "correctAnswer": "Faible", "points": 1},
        {"id": "q4", "skill": "writing", "type": "essay", "content": "Twrivez une note de synthèse.", "instruction": "Synthétisez plusieurs documents.", "correctAnswer": "", "points": 25},
        {"id": "q5", "skill": "writing", "type": "essay", "content": "Twrivez un article critique.", "instruction": "Analyse approfondie d'un sujet.", "correctAnswer": "", "points": 25},
        {"id": "q6", "skill": "speaking", "type": "short_answer", "content": "Exposé de recherche.", "instruction": "Présentez et défendez votre thèse.", "correctAnswer": "", "points": 25},
    ],
    "tcf-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Twoutez la conversation.", "instruction": "Quelle est la nature du texte?", "options": ["Publicitaire", "Informatif", "Persuasif", "Narratif"], "correctAnswer": "Informatif", "points": 1},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Twoutez le message.", "instruction": "Quel est le niveau de langue?", "options": ["A1", "A2", "B1", "B2"], "correctAnswer": "A2", "points": 1},
        {"id": "q3", "skill": "listening", "type": "multiple_choice", "content": "Twoutez l'annonce.", "instruction": "Identifiez le type de document.", "options": ["Official", "Commercial", "Personnel", "Médiatique"], "correctAnswer": "Commercial", "points": 1},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez le texte.", "instruction": "Quel est le registre?", "options": ["Familier", "Standard", "Soutenu", "Littéraire"], "correctAnswer": "Standard", "points": 1},
        {"id": "q5", "skill": "reading", "type": "multiple_choice", "content": "Lisez la lettre.", "instruction": "Quel niveau de compétence?", "options": ["A1", "A2", "B1", "B2"], "correctAnswer": "B1", "points": 1},
        {"id": "q6", "skill": "speaking", "type": "short_answer", "content": "Réponse à des questions.", "instruction": "Demontrer la maîtrise des niveaux.", "correctAnswer": "", "points": 5},
    ],
}


def generate_sample_questions(exam_id: str, skills: dict) -> list:
    """Generate sample questions based on exam skills."""
    questions = []
    question_types = ["multiple_choice", "true_false", "short_answer"]
    
    skill_map = {
        "listening": "listening",
        "reading": "reading", 
        "writing": "writing",
        "speaking": "speaking"
    }
    
    question_id = 1
    for skill, count in skills.items():
        if count == 0:
            continue
        for i in range(min(count, 5)):
            questions.append({
                "id": f"{exam_id}-q{question_id}",
                "skill": skill_map.get(skill, "reading"),
                "type": question_types[i % len(question_types)],
                "content": f"Sample {skill} question {i+1}",
                "instruction": f"Répondez à la question {i+1}",
                "options": ["A", "B", "C", "D"] if question_types[i % len(question_types)] == "multiple_choice" else [],
                "correctAnswer": "A",
                "points": 1
            })
            question_id += 1
    
    return questions


def exam_to_dict(exam: Exam) -> dict:
    """Convert Exam database object to dictionary."""
    return {
        "id": exam.id,
        "courseSlug": exam.course_slug,
        "name": exam.name,
        "duration": exam.duration,
        "questionCount": exam.question_count,
        "difficulty": exam.difficulty,
        "skills": exam.skills,
        "createdAt": exam.created_at.isoformat() if exam.created_at else None,
    }


@router.get("")
def get_exams(
    courseSlug: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Exam)
    if courseSlug:
        query = query.filter(Exam.course_slug == courseSlug)
    
    exams_db = query.all()
    exams = [exam_to_dict(e) for e in exams_db]

    # Only fetch user progress if user is authenticated
    if current_user:
        user_results = db.query(ExamResult).filter(
            ExamResult.user_id == current_user.id
        ).all()

        result_map = {r.exam_id: r for r in user_results}

        for exam in exams:
            if exam["id"] in result_map:
                exam["status"] = "completed"
                exam["attempts"] = result_map[exam["id"]].percentage

    return exams


@router.get("/{examId}")
def get_exam(
    examId: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exam = db.query(Exam).filter(Exam.id == examId).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )

    exam_dict = exam_to_dict(exam)
    
    questions = MOCK_QUESTIONS.get(examId, [])
    if not questions and exam.skills:
        questions = generate_sample_questions(examId, exam.skills)

    return {
        **exam_dict,
        "questions": questions
    }


@router.post("/{examId}/submit")
def submit_exam(
    examId: str,
    request: ExamSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to submit exam"
        )

    exam = db.query(Exam).filter(Exam.id == examId).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )

    questions = MOCK_QUESTIONS.get(examId, [])
    if not questions and exam.skills:
        questions = generate_sample_questions(examId, exam.skills)
    
    correct_count = 0
    total_points = 0

    for q in questions:
        total_points += q.get("points", 1)
        user_answer = request.answers.get(q["id"], "")
        if q.get("type") in ["short_answer", "essay"]:
            correct_count += q.get("points", 1)
        elif user_answer.lower() == q.get("correctAnswer", "").lower():
            correct_count += q.get("points", 1)

    score = correct_count
    max_score = total_points
    percentage = (score / max_score * 100) if max_score > 0 else 0
    passed = percentage >= 50

    result = ExamResult(
        user_id=current_user.id,
        exam_id=examId,
        score=score,
        max_score=max_score,
        percentage=percentage,
        passed=str(passed).lower(),
        answers=request.answers,
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow()
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return {
        "resultId": str(result.id),
        "score": score,
        "maxScore": max_score,
        "percentage": round(percentage, 1),
        "passed": passed
    }


@router.get("/{examId}/results/{resultId}/review")
def get_exam_review(
    examId: str,
    resultId: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.query(ExamResult).filter(
        ExamResult.id == int(resultId),
        ExamResult.user_id == current_user.id,
        ExamResult.exam_id == examId
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )

    exam = db.query(Exam).filter(Exam.id == examId).first()
    questions = MOCK_QUESTIONS.get(examId, [])
    if not questions and exam and exam.skills:
        questions = generate_sample_questions(examId, exam.skills)

    course_names = {
        "delf-a1": "DELF A1",
        "delf-a2": "DELF A2",
        "delf-b1": "DELF B1",
        "delf-b2": "DELF B2",
        "dalf-c1": "DALF C1",
        "dalf-c2": "DALF C2",
        "tcf": "TCF"
    }

    review_questions = []
    for q in questions:
        user_answer = result.answers.get(q["id"], "")
        is_correct = user_answer.lower() == q.get("correctAnswer", "").lower() if q.get("correctAnswer") else False

        review_questions.append({
            "id": q["id"],
            "skill": q["skill"],
            "type": q["type"],
            "content": q.get("content", ""),
            "instruction": q.get("instruction", ""),
            "options": q.get("options", []),
            "answer": q.get("correctAnswer", ""),
            "explanation": None,
            "audioUrl": None,
            "imageUrl": None,
            "userAnswer": user_answer,
            "isCorrect": is_correct,
            "points": q.get("points", 1)
        })

    return {
        "exam": {
            "id": examId,
            "name": exam.name if exam else examId,
            "courseSlug": exam.course_slug if exam else "",
            "courseName": course_names.get(exam.course_slug, "") if exam else "",
            "duration": exam.duration if exam else 0,
            "totalScore": result.score,
            "maxScore": result.max_score,
            "percentage": result.percentage,
            "passed": result.passed == "true",
            "timeSpent": 0
        },
        "result": {
            "score": result.score,
            "maxScore": result.max_score,
            "percentage": result.percentage,
            "passed": result.passed == "true",
            "details": {
                "listening": {"correct": 2, "total": 2},
                "reading": {"correct": 2, "total": 2},
                "writing": {"correct": 1, "total": 1}
            },
            "startedAt": result.started_at.isoformat() if result.started_at else "",
            "completedAt": result.completed_at.isoformat() if result.completed_at else ""
        },
        "questions": review_questions,
        "userAnswers": result.answers
    }