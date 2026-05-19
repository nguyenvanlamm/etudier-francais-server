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
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Marie: Salut Pierre! Qu'est-ce que tu fais ce week-end? Pierre: Je vais au cinéma voir un nouveau film. Et toi? Marie: Moi, je fais du shopping avec mes amies. On va au centre commercial. Pierre: Amusant! Bonne chance!", "instruction": "Qu'est-ce que Marie fait ce week-end?", "options": ["Elle va au cinéma", "Elle fait du shopping", "Elle rencontre des amis", "Elle reste chez elle"], "correctAnswer": "Elle fait du shopping", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-1/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Attention! Le train pour Paris partira à dix heures trente du quai numéro cinq. Ce train s'arrête à Lyon et à Dijon. Les voyageurs sont priés de valider leur billet avant l'embarquement. Merci de votre attention.", "instruction": "A quelle heure part le train?", "options": ["10h00", "10h15", "10h30", "10h45"], "correctAnswer": "10h30", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-1/q2.mp3"},
        {"id": "q3", "skill": "listening", "type": "multiple_choice", "content": "Paul: Bonjour Madame Martin! Comment allez-vous? Madame Martin: Très bien merci! Et vous? Paul: Bien aussi. Je m'appelle Paul, je suis le nouveau voisin. Madame Martin: Enchantée! Bienvenue dans l'immeuble!", "instruction": "Comment s'appelle le personnage?", "options": ["Pierre", "Paul", "Jean", "Luc"], "correctAnswer": "Paul", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-1/q3.mp3"},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez le texte et répondez.", "instruction": "De quelle couleur est la robe?", "options": ["Rouge", "Bleue", "Verte", "Jaune"], "correctAnswer": "Bleue", "points": 1},
        {"id": "q5", "skill": "reading", "type": "true_false", "content": "Lisez l'email et dites si c'est vrai ou faux.", "instruction": "Le rendez-vous est à 14h.", "correctAnswer": "true", "points": 1},
        {"id": "q6", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article.", "instruction": "Quel est le thème principal?", "options": ["Voyage", "Travail", "Famille", "Loisirs"], "correctAnswer": "Voyage", "points": 1},
        {"id": "q7", "skill": "writing", "type": "short_answer", "content": "Ecrivez une phrase pour présenter votre famille.", "instruction": "Utilisez au moins 3 mots.", "correctAnswer": "", "points": 5},
        {"id": "q8", "skill": "writing", "type": "short_answer", "content": "Décrivez votre journée idéale.", "instruction": "Ecrivez 5-10 mots.", "correctAnswer": "", "points": 5},
        {"id": "q9", "skill": "speaking", "type": "short_answer", "content": "Présentez-vous en quelques phrases.", "instruction": "Parlez de votre nom, votre âge et votre origine.", "correctAnswer": "", "points": 5},
        {"id": "q10", "skill": "speaking", "type": "short_answer", "content": "Décrivez votre lieu de vie.", "instruction": "Où habitez-vous? Combien de pièces?", "correctAnswer": "", "points": 5},
    ],
    "delf-a1-full-2": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Sophie: Qu'est-ce que tu fais maintenant Jean? Jean: Je travaille sur mon ordinateur. Je dois préparer un rapport pour demain. Sophie: Tu es toujours occupé! Tu veux prendre une pause? Jean: Peut-être plus tard, merci.", "instruction": "Que fait le personnage?", "options": ["Mange", "Dort", "Travaille", "Lis"], "correctAnswer": "Travaille", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-2/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Information importante: une exposition de peinture aura lieu ce mercredi de quatorze heures à dix-huit heures à la bibliothèque municipale. L'entrée est gratuite pour tous. Venez nombreux découvrir les œuvres d'artistes locaux!", "instruction": "Quel jour a lieu l'événement?", "options": ["Lundi", "Mardi", "Mercredi", "Jeudi"], "correctAnswer": "Mercredi", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-2/q2.mp3"},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez la carte.", "instruction": "Quel restaurant est recommandé?", "options": ["Le Paris", "La Maison", "Le Jardin", "La Terrace"], "correctAnswer": "Le Paris", "points": 1},
        {"id": "q4", "skill": "reading", "type": "true_false", "content": "Lisez le message.", "instruction": "Le message est urgent.", "correctAnswer": "true", "points": 1},
        {"id": "q5", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article.", "instruction": "De quoi parle l'article?", "options": ["Météo", "Sport", "Politique", "Culture"], "correctAnswer": "Culture", "points": 1},
        {"id": "q6", "skill": "writing", "type": "short_answer", "content": "Twrivez une carte postale.", "instruction": "Décrivez où vous êtes.", "correctAnswer": "", "points": 5},
        {"id": "q7", "skill": "writing", "type": "short_answer", "content": "Twrivez vos coordonnées.", "instruction": "Donnez votre adresse et téléphone.", "correctAnswer": "", "points": 5},
        {"id": "q8", "skill": "speaking", "type": "short_answer", "content": "Décrivez votre ami.", "instruction": "Comment est-il/elle?", "correctAnswer": "", "points": 5},
        {"id": "q9", "skill": "speaking", "type": "short_answer", "content": "Parlez de vos activités.", "instruction": "Qu'aimez-vous faire?", "correctAnswer": "", "points": 5},
    ],
    "delf-a2-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Marie: Tu veux aller au cinéma ce soir? Luc: Pourquoi pas! Quel film veux-tu voir? Marie: Il y a un bon film d'action au Rex. Luc: D'accord! On se retrouve à dix-huit heures devant le cinéma? Marie: Parfait! A tout à l'heure!", "instruction": "Où vont les personnages?", "options": ["Au cinéma", "Au restaurant", "Au musée", "A la gare"], "correctAnswer": "Au cinéma", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-1/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Bonjour! Voici les informations météo pour aujourd'hui. Le soleil brille sur tout le pays ce matin. Cet après-midi, quelques nuages apparaissent dans le nord, mais pas de pluie prévue. Les températures varient entre vingt et vingt-cinq degrés. C'est une belle journée pour sortir!", "instruction": "Quel temps fait-il?", "options": ["Beau", "Mauvais", "Pluieux", "Neige"], "correctAnswer": "Beau", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-1/q2.mp3"},
        {"id": "q3", "skill": "listening", "type": "true_false", "content": "Pierre:-allô Marie? Marie: Oui allô! Pierre: C'est Pierre. Je t'appelle pour confirmer notre rendez-vous demain à quatorze heures au café de la place. Marie: Oui, je serai là. A demain! Pierre: D'accord, à demain!", "instruction": "Le rendez-vous est confirmé.", "correctAnswer": "true", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-1/q3.mp3"},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article de journal.", "instruction": "Quel est l'événement?", "options": ["Fête", "Concert", "Exhibition", "Competition"], "correctAnswer": "Concert", "points": 1},
        {"id": "q5", "skill": "reading", "type": "multiple_choice", "content": "Lisez la publicité.", "instruction": "Quel est le prix?", "options": ["50€", "75€", "100€", "150€"], "correctAnswer": "75€", "points": 1},
        {"id": "q6", "skill": "reading", "type": "true_false", "content": "Lisez la lettre.", "instruction": "L'expéditeur est content.", "correctAnswer": "false", "points": 1},
        {"id": "q7", "skill": "writing", "type": "short_answer", "content": "Twrivez un message à un ami.", "instruction": "Parlez de vos projets pour le week-end.", "correctAnswer": "", "points": 5},
        {"id": "q8", "skill": "writing", "type": "short_answer", "content": "Twrivez un email professionnel.", "instruction": "Demandez des informations sur un produit.", "correctAnswer": "", "points": 5},
        {"id": "q9", "skill": "speaking", "type": "short_answer", "content": "Présentez un sujet qui vous passionne.", "instruction": "Expliquez pourquoi cela vous interesse.", "correctAnswer": "", "points": 5},
        {"id": "q10", "skill": "speaking", "type": "short_answer", "content": "Décrivez votre lieu de travail.", "instruction": "Parlez de votre environnement professionnel.", "correctAnswer": "", "points": 5},
    ],
    "delf-b1-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Bonsoir à tous! Ce soir, nous parlons du problème du logement chez les jeunes en France. Selon une étude récente, plus de soixante pour cent des jeunes de vingt-cinq à trente ans ont des difficultés à trouver un appartement. Les prix élevés et le manque de logements disponibles sont les principales causes. Le gouvernement annonce de nouvelles mesures pour aider cette génération.", "instruction": "Quel est le sujet principal?", "options": ["Economie", "Politique", "Société", "Culture"], "correctAnswer": "Société", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-1/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Journaliste: Monsieur Dubois, pouvez-vous vous présenter? Dubois: Bien sûr! Je m'appelle Michel Dubois, j'enseigne le français depuis vingt ans dans un lycée de Lyon. J'aime beaucoup mon métier, car j'ai quotidiennement contacto avec des élèves motivés. Journaliste: Quels sont les défis de votre profession? Dubois: Former les citoyens de demain, c'est une grande responsabilité.", "instruction": "Quel métier exerce la personne?", "options": ["Médecin", "Avocat", "Professeur", "Ingénieur"], "correctAnswer": "Professeur", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-1/q2.mp3"},
        {"id": "q3", "skill": "listening", "type": "true_false", "content": "Animateur: Aujourd'hui, nous débatons sur l'utilisation des réseaux sociaux chez les adolescents. Marie: Je pense que les réseaux sociaux sont dangereux car ils créent une dépendance et isolent les jeunes. Pierre: Je ne suis pas d'accord! Ils permettent de communiquer facilement et de développer des compétences numériques. Marie: Mais il y a des risques de cyber-harcèlement! Pierre: Avec une bonne éducation, les avantages dépassent les inconvénients.", "instruction": "Les participants sont d'accord.", "correctAnswer": "false", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-1/q3.mp3"},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article scientifique.", "instruction": "Quelle est la conclusion?", "options": ["Positive", "Négative", "Neutre", "Inconnue"], "correctAnswer": "Positive", "points": 1},
        {"id": "q5", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'essai.", "instruction": "Quel est l'argument principal?", "options": ["Environnement", "Education", "Santé", "Technologie"], "correctAnswer": "Education", "points": 1},
        {"id": "q6", "skill": "reading", "type": "multiple_choice", "content": "Lisez le roman.", "instruction": "Quel est le sentiment dominant?", "options": ["Joie", "Tristesse", "Peur", "Espoir"], "correctAnswer": "Espoir", "points": 1},
        {"id": "q7", "skill": "writing", "type": "essay", "content": "Twrivez une dissertation.", "instruction": "Les réseaux sociaux sont-ils utiles?", "correctAnswer": "", "points": 10},
        {"id": "q8", "skill": "writing", "type": "essay", "content": "Twrivez une lettre formelle.", "instruction": "Postulez pour un emploi.", "correctAnswer": "", "points": 10},
        {"id": "q9", "skill": "speaking", "type": "short_answer", "content": "Présentez un sujet d'actualité.", "instruction": "Expliquez votre point de vue.", "correctAnswer": "", "points": 10},
        {"id": "q10", "skill": "speaking", "type": "short_answer", "content": "Participez à un débat.", "instruction": "Argumentez pour ou contre.", "correctAnswer": "", "points": 10},
    ],
    "delf-b2-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Chers collègues, aujourd'hui je vais vous presenter une these sur l'intelligence artificielle et son impact sur le marché du travail. Selon mes recherches, l'automatisation pourrait remplacer trente pour cent des emplois d'ici vingt ans. Cependant, de nouveaux métiers vont émerger dans les domaines de la data science et de la robotique. Il est essentiel de former la population aux compétences numériques pour face a cette transformation.", "instruction": "Quelle est la thèse présentée?", "options": ["A", "B", "C", "D"], "correctAnswer": "A", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-1/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Ce documentaire explore les avancées récentes dans le domaine de la médecine personnalisée. Grâce aux progrès de la génomique, les médecins peuvent maintenant adapter les traitements selon le profil génétique de chaque patient. Cette approche révolu-tionnaire permet de traiter certaines maladies auparavant incurables. Les chercheurs espé-rent que d'ici dix ans, cette technologie sera accessible à tous les patients.", "instruction": "Quel aspect est développé?", "options": ["Historique", "Scientifique", "Culturel", "Social"], "correctAnswer": "Scientifique", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-1/q2.mp3"},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article académique.", "instruction": "Quelle méthodologie est utilisée?", "options": ["Quantitative", "Qualitative", "Mixte", "Autre"], "correctAnswer": "Mixte", "points": 1},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'éditorial.", "instruction": "Quelle position défend l'auteur?", "options": ["Conservatrice", "Libérale", "Neutre", "Extrémiste"], "correctAnswer": "Libérale", "points": 1},
        {"id": "q5", "skill": "writing", "type": "essay", "content": "Twrivez un essai argumenté.", "instruction": "La technologie améliore-t-elle la vie?", "correctAnswer": "", "points": 15},
        {"id": "q6", "skill": "writing", "type": "essay", "content": "Twrivez un article de presse.", "instruction": "Sujets d'actualité au choix.", "correctAnswer": "", "points": 15},
        {"id": "q7", "skill": "speaking", "type": "short_answer", "content": "Présentez un exposé.", "instruction": "Sujet libre de 3 minutes.", "correctAnswer": "", "points": 15},
    ],
    "dalf-c1-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Bienvenue dans notre emission littéraire de ce soir. Aujourd'hui, nous analysons 'Les Misérables' de Victor Hugo,这部伟大的法国文学作品。Dans ce roman publié en mil huit cent soixante-deux, Hugo dépeint la société française du dix-neuvième siècle à travers le parcours de Jean Valjean. L'auteur aborde des thèmes universels comme la rédemption, la justice sociale et l'amour. Cette œuvre reste l'une des plus lues au monde.", "instruction": "Quel obra est analysée?", "options": ["Roman", "Poésie", "Théâtre", "Essai"], "correctAnswer": "Roman", "points": 1, "audioUrl": "/assets/audio/dalf-c1-full-1/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Mesdames et Messieurs, honorables invités, c'est avec une profonde émotion que je prends la parole aujourd'hui pour célébrER le cinquantième anniversaire de notre académie. Depuis sa fondation, notre institution s'est engagée à promouvoir l'excellence académique et à fostering la recherche innovative. Nous devons Collectivement préservER cet héritage pour les générations futures. Je vous remercie de votre attention.", "instruction": "Quel est le registre de langue?", "options": ["Familier", "Courant", "Soutenu", "Littéraire"], "correctAnswer": "Soutenu", "points": 1, "audioUrl": "/assets/audio/dalf-c1-full-1/q2.mp3"},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'extrait littéraire.", "instruction": "Identifiez le style de l'auteur.", "options": ["Réalisme", "Romantisme", "Naturalisme", "Symbolisme"], "correctAnswer": "Réalisme", "points": 1},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article philosophique.", "instruction": "Quelle école de pensée?", "options": ["Existentialisme", "Matérialisme", "Idéalisme", "Positivisme"], "correctAnswer": "Existentialisme", "points": 1},
        {"id": "q5", "skill": "writing", "type": "essay", "content": "Twrivez une dissertation littéraire.", "instruction": "Analysez un oeuvre au choix.", "correctAnswer": "", "points": 20},
        {"id": "q6", "skill": "writing", "type": "essay", "content": "Twrivez un essai philosophique.", "instruction": "Réflexion sur un concept au choix.", "correctAnswer": "", "points": 20},
        {"id": "q7", "skill": "speaking", "type": "short_answer", "content": "Exposé avancé.", "instruction": "Sujet complexe avec argumentation.", "correctAnswer": "", "points": 20},
    ],
    "dalf-c2-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Professeur Martin: Le positivisme du dix-neuvième siècle a profondément influencé les sciences humaines, mais cette approche présente des limites épistémologiques que nous devons reconnaître. Le sujet percevant n'est pas aussi objectif qu'on le pensait. Professor Dubois: Cependant, n'est-il pas prématuré de rejeter entièrement cette méthodologie? Les données quantitatives restent indispensables. Professor Martin: Je vous accCord partiellement, mais la subjectivité du chercheur doit être intégrée comme variable, non comme bruit à éliminer.", "instruction": "Identifiez les nuances du discours.", "options": ["A", "B", "C", "D"], "correctAnswer": "C", "points": 1, "audioUrl": "/assets/audio/dalf-c2-full-1/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Cette conférence présente les résultats d'une recherche longitudinale menée pendant quinze ans sur l'évolution des comportements linguistiques chez les locuteurs bilingues. Nous avons observe que le changement de code entre deux langues dépend non seulement du contexte social, mais aussi de facteurs cognitifs comme la charge mémorielle. Les données démontrent une correlation significative entre la proficiency et la fréquence de commutation. Ces résultats suggèrent des applications pédagogiques potentielles.", "instruction": "Synthétisez les idées principales.", "options": ["1", "2", "3", "4"], "correctAnswer": "2", "points": 1, "audioUrl": "/assets/audio/dalf-c2-full-1/q2.mp3"},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'article de recherche.", "instruction": "Critiquez la méthodologie.", "options": ["Forte", "Faible", "Moyenne", "Insufficient"], "correctAnswer": "Faible", "points": 1},
        {"id": "q4", "skill": "writing", "type": "essay", "content": "Twrivez une note de synthèse.", "instruction": "Synthétisez plusieurs documents.", "correctAnswer": "", "points": 25},
        {"id": "q5", "skill": "writing", "type": "essay", "content": "Twrivez un article critique.", "instruction": "Analyse approfondie d'un sujet.", "correctAnswer": "", "points": 25},
        {"id": "q6", "skill": "speaking", "type": "short_answer", "content": "Exposé de recherche.", "instruction": "Présentez et défendez votre thèse.", "correctAnswer": "", "points": 25},
    ],
    "tcf-full-1": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Aujourd'hui, nous annonçons l'ouverture d'un nouveau centre commercial dans le quartier nord de la ville. Ce centre proposera plus de cinquante boutiques, un cinéma multiplexe et plusieurs restaurants. L'ouverture est prévue pour le mois prochain. Les travaux de construction avancent conformément au calendrier prévu. C'est une nouvelle importante pour l'économie locale.", "instruction": "Quelle est la nature du texte?", "options": ["Publicitaire", "Informatif", "Persuasif", "Narratif"], "correctAnswer": "Informatif", "points": 1, "audioUrl": "/assets/audio/tcf-full-1/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Message vocal: Bonjour Marie! C'est Pierre. Je t'appel pour te dire que le réunion est reportée à demain à cause d'un problème technique. Désolé pour le dérangement. Rappelle-moi si tu as des questions. Merci! A bientôt!", "instruction": "Quel est le niveau de langue?", "options": ["A1", "A2", "B1", "B2"], "correctAnswer": "A2", "points": 1, "audioUrl": "/assets/audio/tcf-full-1/q2.mp3"},
        {"id": "q3", "skill": "listening", "type": "multiple_choice", "content": "Offre spéciale! Venez découvrir notre nouvelle collection d'été! Profits de trente pour cent de réduction sur tous les articles pendant cette semaine seulement. Venez vite en magasin! Offre válida jusqu'au trente juin. Ne manquez pas cette opportunité exceptionnelle!", "instruction": "Identifiez le type de document.", "options": ["Official", "Commercial", "Personnel", "Médiatique"], "correctAnswer": "Commercial", "points": 1, "audioUrl": "/assets/audio/tcf-full-1/q3.mp3"},
        {"id": "q4", "skill": "reading", "type": "multiple_choice", "content": "Lisez le texte.", "instruction": "Quel est le registre?", "options": ["Familier", "Standard", "Soutenu", "Littéraire"], "correctAnswer": "Standard", "points": 1},
        {"id": "q5", "skill": "reading", "type": "multiple_choice", "content": "Lisez la lettre.", "instruction": "Quel niveau de compétence?", "options": ["A1", "A2", "B1", "B2"], "correctAnswer": "B1", "points": 1},
        {"id": "q6", "skill": "speaking", "type": "short_answer", "content": "Réponse à des questions.", "instruction": "Demontrer la maîtrise des niveaux.", "correctAnswer": "", "points": 5},
    ],
    "delf-a1-full-3": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Bonjour! Bienvenue chez Le Petit Café. Voulez-vous un café ou un thé? Merci beaucoup! Voici votre commande. Bonne journée!", "instruction": "Que commande le client?", "options": ["Un café", "Un thé", "Un jus", "De l'eau"], "correctAnswer": "Un café", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-3/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Attention aux voyageurs! Le train pour Lyon partira dans dix minutes sur le quai numéro trois. Veuillez valider votre billet avant de monter à bord.", "instruction": "Pour quelle destination part le train?", "options": ["Paris", "Lyon", "Marseille", "Nice"], "correctAnswer": "Lyon", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-3/q2.mp3"},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez l'annonce.", "instruction": "Quel est l'événement?", "options": ["Concert", "Exposition", "Match de foot", "Fête"], "correctAnswer": "Concert", "points": 1},
    ],
    "delf-a1-full-4": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Salut! Je m'appelle Sophie. J'ai vingt-cinq ans et je suis estudiante en français. J'habite à Paris avec ma famille.", "instruction": "Comment s'appelle la personne?", "options": ["Marie", "Sophie", "Julie", "Emma"], "correctAnswer": "Sophie", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-4/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Le musée ferme à dix-huit heures aujourd'hui. Dernière entrée à dix-sept heures trente. Merci de votre visite!", "instruction": "A quelle heure ferme le musée?", "options": ["17h", "18h", "19h", "20h"], "correctAnswer": "18h", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-4/q2.mp3"},
    ],
    "delf-a1-full-5": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Allô? C'est moi! Je suis à la gare. Le train arrive dans cinq minutes. À tout à l'heure!", "instruction": "Où est la personne?", "options": ["A la maison", "A la gare", "Au travail", "A l'école"], "correctAnswer": "A la gare", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-5/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Il fait beau aujourd'hui. Le soleil brille et il fait vingt-cinq degrés. C'est parfait pour aller à la plage!", "instruction": "Quel temps fait-il?", "options": ["Il pleut", "Il fait froid", "Il fait beau", "Il neige"], "correctAnswer": "Il fait beau", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-5/q2.mp3"},
        {"id": "q3", "skill": "reading", "type": "multiple_choice", "content": "Lisez le menu.", "instruction": "Combien coûte le burger?", "options": ["8€", "10€", "12€", "15€"], "correctAnswer": "10€", "points": 1},
    ],
    "delf-a1-full-6": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Mardi prochain, il y a un cours de français à dix heures. Le professeur s'appelle Monsieur Dupont. N'oubliez pas votre livre!", "instruction": "Quel jour a lieu le cours?", "options": ["Lundi", "Mardi", "Mercredi", "Jeudi"], "correctAnswer": "Mardi", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-6/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Je voudrais réserver une chambre pour deux personnes, du vendredi au dimanche. C'est possible? Bien sûr! Quel type de chambre préférez-vous?", "instruction": "Pour combien de nuits?", "options": ["Une nuit", "Deux nuits", "Trois nuits", "Une semaine"], "correctAnswer": "Deux nuits", "points": 1, "audioUrl": "/assets/audio/delf-a1-full-6/q2.mp3"},
    ],
    "delf-a2-full-2": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Hier, je suis allé au cinéma avec mes amis. Nous avons regardé un film très intéressant sur l'histoire de France. Le film durait deux heures.", "instruction": "Qu'est-ce que le narrateur a fait hier?", "options": ["Aller au cinéma", "Aller au musée", "Aller au restaurant", "Aller à la plage"], "correctAnswer": "Aller au cinéma", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-2/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Météo France annonce du soleil pour toute la semaine. Les températures maximales seront autour de vingt-huit degrés dans le sud.", "instruction": "Quelle est la prévisions météo?", "options": ["Pluie", "Neige", "Soleil", "Vent"], "correctAnswer": "Soleil", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-2/q2.mp3"},
        {"id": "q3", "skill": "listening", "type": "true_false", "content": "Le train de seize heures trente pour Bordeaux est retardé de quinze minutes. Les voyageurs sont priés de patienter en salle d'attente.", "instruction": "Le train est à l'heure.", "correctAnswer": "false", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-2/q3.mp3"},
    ],
    "delf-a2-full-3": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Selon une étude récente, les jeunes Français passent en moyenne trois heures par jour sur les réseaux sociaux. C'est beaucoup plus qu'il y a dix ans.", "instruction": "Combien de temps passent les jeunes sur les réseaux sociaux?", "options": ["1 heure", "2 heures", "3 heures", "4 heures"], "correctAnswer": "3 heures", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-3/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Journaliste: Quels sont vos projets pour l'avenir? Candidat: Je voudrais devenir développeur informatique. J'aime la programmation et je suis motivé pour apprendre.", "instruction": "Quel métier le candidat veut-il faire?", "options": ["Médecin", "Avocat", "Développeur", "Professeur"], "correctAnswer": "Développeur", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-3/q2.mp3"},
    ],
    "delf-a2-full-4": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "La nouvelle ligne de métro sera inaugurée demain matin à huit heures. Elle permettra de relier le centre-ville à l'aéroport en seulement trente minutes.", "instruction": "Quand sera inaugurée la nouvelle ligne?", "options": ["Aujourd'hui", "Demain", "La semaine prochaine", "Le mois prochain"], "correctAnswer": "Demain", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-4/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Publicité: Notre nouveau produit est maintenant disponible dans tous les magasins! Profitez de vingt pour cent de réduction cette semaine seulement.", "instruction": "Quelle est l'offre spéciale?", "options": ["50% de réduction", "30% de réduction", "20% de réduction", "10% de réduction"], "correctAnswer": "20% de réduction", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-4/q2.mp3"},
    ],
    "delf-a2-full-5": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Annonce radio: Ce soir, concert gratuit dans le parc municipal à partir de vingt heures. Plusieurs artistes seront présents. Venez nombreux!", "instruction": "Où aura lieu le concert?", "options": ["Au théâtre", "Dans le parc", "Au stade", "A la bibliothèque"], "correctAnswer": "Dans le parc", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-5/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "true_false", "content": "Message: Allô Marie? C'est Pierre. Je ne pourrai pas venir demain, je suis malade. Désolé! Rappelle-moi quand tu auras ce message.", "instruction": "Pierre viendra demain.", "correctAnswer": "false", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-5/q2.mp3"},
    ],
    "delf-a2-full-6": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Emission culturelle: Ce semaine, nous parlons de la littérature française du dix-neuvième siècle. Les grands auteurs comme Hugo, Flaubert et Zola seront analysés.", "instruction": "De quelle période parle l'émission?", "options": ["18ème siècle", "19ème siècle", "20ème siècle", "21ème siècle"], "correctAnswer": "19ème siècle", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-6/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Interview: Comment avez-vous appris le français? J'ai vécu trois ans à Paris. C'était difficile au début mais maintenant je parle couramment.", "instruction": "Où la personne a-t-elle vécu?", "options": ["Londres", "Paris", "Berlin", "Madrid"], "correctAnswer": "Paris", "points": 1, "audioUrl": "/assets/audio/delf-a2-full-6/q2.mp3"},
    ],
    "delf-b1-full-2": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Reportage: En France, le taux de chômage a diminué de deux pour cent cette année. C'est une bonne nouvelle pour l'économie du pays. Le gouvernement se félicite de ces résultats.", "instruction": "Quel est le taux de chômage?", "options": ["En augmentation", "En diminution", "Stable", "Inconnu"], "correctAnswer": "En diminution", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-2/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Débat电视: Faut-il interdire les téléphones portables à l'école? Certains disent oui pour protéger les enfants. D'autres disent non car c'est utile pour l'apprentissage.", "instruction": "Quel est le sujet du débat?", "options": ["Les examens", "Les uniformes", "Les téléphones", "Les transports"], "correctAnswer": "Les téléphone", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-2/q2.mp3"},
        {"id": "q3", "skill": "listening", "type": "true_false", "content": "Journaliste: Monsieur, quels sont vos objectifs? Citoyen: Je voudrais trouver un emploi stable et Buying une maison. C'est mon rêve.", "instruction": "Le citoyen a un emploi stable.", "correctAnswer": "false", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-2/q3.mp3"},
    ],
    "delf-b1-full-3": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Documentaire: La pollution de l'air est un problème majeur dans les grandes villes. Selon les scientifiques, elle cause des maladies respiratoires chez des millions de personnes.", "instruction": "Quel est le problème décrit?", "options": ["Le bruit", "La pollution", "Le trafic", "Les déchets"], "correctAnswer": "La pollution", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-3/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Interview: Pourquoi avez-vous choisi ce métier? J'ai toujours voulu aider les gens. C'est pour ça que je suis infirmière depuis vingt ans.", "instruction": "Quel est le métier de la personne?", "options": ["Médecin", "Infirmière", "Avocat", "Professeur"], "correctAnswer": "Infirmière", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-3/q2.mp3"},
    ],
    "delf-b1-full-4": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Actualités: Le président a annoncé today de nouvelles mesures pour protéger l'environnement. Les entreprises devront réduire leurs émissions de carbone de trente pour cent d'ici dix ans.", "instruction": "Quel est le sujet principal?", "options": ["L'économie", "L'éducation", "L'environnement", "La santé"], "correctAnswer": "L'environnement", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-4/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Reportage: Les Françaisisent de plus en plus vers les villes. Plus de soixante-dix pour cent de la population vit désormais dans les zones urbaines.", "instruction": "Quel pourcentage vit en ville?", "options": ["50%", "60%", "70%", "80%"], "correctAnswer": "70%", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-4/q2.mp3"},
    ],
    "delf-b1-full-5": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Débat: La peine de mort devrait-elle être abolie? Pour certains, c'est une question de justice. Pour d'autres, c'est toujours une violation des droits de l'homme.", "instruction": "De quoi parle le débat?", "options": ["L'immigration", "La peine de mort", "L'euthanasie", "L'avortement"], "correctAnswer": "La peine de mort", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-5/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "true_false", "content": "Interview: Quels sont vos loisirs? J'aime la lecture, le vélo et parfois le tennis. Mais je n'ai pas beaucoup de temps libre.", "instruction": "La personne fait du sport.", "correctAnswer": "true", "points": 1, "audioUrl": "/assets/audio/delf-b1-full-5/q2.mp3"},
    ],
    "delf-b2-full-2": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Conférence: Les avancées technologiques transforment notre société. L'intelligence artificielle, la robotique et les biotechnologies révolutionnent de nombreux secteurs.", "instruction": "Quel thème est abordé?", "options": ["La politique", "La technologie", "La religion", "L'art"], "correctAnswer": "La technologie", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-2/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Documentaire: Le changement climatique est l'un des plus grands défis de notre époque. Les conséquences sont déjà visibles: montée des eaux, événements météorologiques extrêmes, perte de biodiversité.", "instruction": "Quel est le problème principal?", "options": ["La déforestation", "Le changement climatique", "La surexploitation", "L'urbanisation"], "correctAnswer": "Le changement climatique", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-2/q2.mp3"},
    ],
    "delf-b2-full-3": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Editorial: Face à la crise économique, le gouvernement doit prendre des mesures courageuses. Il faut réduire les dépenses publiques et augmenter les impôts.", "instruction": "Quelle est la position de l'éditorial?", "options": ["Maintenir les dépenses", "Réduire les dépenses", "Augmenter les investissements", "Aucune mesure"], "correctAnswer": "Réduire les dépenses", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-3/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Interview: Comment voyez-vous l'avenir de l'Europe? L'Europe doit rester unie pour faire face aux défis globaux. Sinon, nousperdrons notre influence.", "instruction": "Quelle est l'opinion sur l'Europe?", "options": ["Elle doit se diviser", "Elle doit être unie", "Elle doit quitter l'ONU", "Elle doit se désarmer"], "correctAnswer": "Elle doit être unie", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-3/q2.mp3"},
    ],
    "delf-b2-full-4": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Discours politique: Mesdames et Messieurs, nous devons agir maintenant pour l'avenir de nos enfants. L'éducation est la priorité absolue de ce gouvernement.", "instruction": "Quel est le thème du discours?", "options": ["L'économie", "L'éducation", "La défense", "La culture"], "correctAnswer": "L'éducation", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-4/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "true_false", "content": "Débat télévisé: La mondialisation est-elle beneficiosse? Pour certains pays, oui. Pour d'autres, elle cause des inégalités.", "instruction": "Les participants sont d'accord.", "correctAnswer": "false", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-4/q2.mp3"},
    ],
    "delf-b2-full-5": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Émission scientifique: Les recherches sur le cerveauprogressent rapidly. Grâce aux nouvelles technologies, nous comprenons mieux comment fonctionne la mémoire.", "instruction": "Quel sujet est évoqué?", "options": ["Le cœur", "Le cerveau", "Les poumons", "Le foie"], "correctAnswer": "Le cerveau", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-5/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Rapport: Le nombre de chômeurs a augmenté de cinq pour cent cette année. Les secteurs les plus touchés sont l'industrie et la construction.", "instruction": "Quel secteur est le plus touché?", "options": ["Les services", "L'industrie", "L'agriculture", "Le tourisme"], "correctAnswer": "L'industrie", "points": 1, "audioUrl": "/assets/audio/delf-b2-full-5/q2.mp3"},
    ],
    "dalf-c1-full-2": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Analyse littéraire: L'œuvre de Camus illustre parfaitement l'absurde. L'homme cherche un sens dans un univers qui n'en offre pas. Cette pensée philosophersque reste d'actualité.", "instruction": "Quel thème est analysé?", "options": ["Le romantisme", "Le réalisme", "L'existentialisme", "Le surréalisme"], "correctAnswer": "L'existentialisme", "points": 1, "audioUrl": "/assets/audio/dalf-c1-full-2/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Conférence académique: Les sciences humaines ont connu une transformación majeure au vingtième siècle. Le structuralisme, puis le post-structuralisme ont profondément modifié notre approche.", "instruction": "Quel mouvement est mentionné?", "options": ["Le positivisme", "Le structuralisme", "Le marxisme", "Le cartésianisme"], "correctAnswer": "Le structuralisme", "points": 1, "audioUrl": "/assets/audio/dalf-c1-full-2/q2.mp3"},
    ],
    "dalf-c1-full-3": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Émission philosophique: Qu'est-ce que la conscience? Cette question intrigue les philosophes depuis des siècles. Les neurosciences apporter-elles enfin une réponse?", "instruction": "Quel est le sujet?", "options": ["L'inconscient", "La conscience", "Le subconscient", "La mémoire"], "correctAnswer": "La conscience", "points": 1, "audioUrl": "/assets/audio/dalf-c1-full-3/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Discours solenNEl: C'est avec une profonde gratitude que je reçois aujourd'hui cette distinction. Ce prix revient à toute mon équipe qui a travaillé sans relâche.", "instruction": "Quel est le registre de langue?", "options": ["Familier", "Courant", "Soutenu", "Littéraire"], "correctAnswer": "Soutenu", "points": 1, "audioUrl": "/assets/audio/dalf-c1-full-3/q2.mp3"},
    ],
    "dalf-c1-full-4": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Débat intellectuel: La morale peut-elle être séparée de la religion? Certains philosophes défendent une morale autonome. D'autres estiment qu'elle découle nécessairement du divin.", "instruction": "De quoi traite le débat?", "options": ["La politique", "La morale et la religion", "La science", "L'art"], "correctAnswer": "La morale et la religion", "points": 1, "audioUrl": "/assets/audio/dalf-c1-full-4/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Analyse sociologique: Les nouvelles technologies ont profondément transformé les relations sociales. Les liens virtuels remplacent progressivement les interactions directes.", "instruction": "Quel sujet est analysé?", "options": ["La famille", "Les nouvelles technologies", "Le travail", "L'éducation"], "correctAnswer": "Les nouvelles technologies", "points": 1, "audioUrl": "/assets/audio/dalf-c1-full-4/q2.mp3"},
    ],
    "dalf-c2-full-2": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Professeur: La méthode scientifique classique présente des limites évidentes. Nous devons adopter une approche plus interdisciplinaire pour comprendre les phénomènes complexes.", "instruction": "Quelle méthode est critiquée?", "options": ["La méthode qualitative", "La méthode scientifique classique", "La méthode comparative", "La méthode historique"], "correctAnswer": "La méthode scientifique classique", "points": 1, "audioUrl": "/assets/audio/dalf-c2-full-2/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Conférence de recherche: Nos résultats démontrent une corrélation significative entre les variables indépendantes et dépendantes. Toutefois, des études supplémentaires sont nécessaires.", "instruction": "Synthétisez la conclusion.", "options": ["Résultats définitifs", "Résultats partiels avec besoin d'études", "Résultats négatifs", "Résultats impossibles à interpréter"], "correctAnswer": "Résultats partiels avec besoin d'études", "points": 1, "audioUrl": "/assets/audio/dalf-c2-full-2/q2.mp3"},
    ],
    "dalf-c2-full-3": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Débat académique: L'éthique de l'intelligence artificielle soulève des questions fondamentales. jusqu'où peut-on laisser une machine prendre des décisions autonomes?", "instruction": "Identifiez les nuances du discours.", "options": ["Problème technique", "Problème éthique", "Problème juridique", "Problème économique"], "correctAnswer": "Problème éthique", "points": 1, "audioUrl": "/assets/audio/dalf-c2-full-3/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Séminaire: Le concept de posthumanisme Question les frontières traditionnelles entre l'humain et la machine. Cette évolutionsoulève des défis philosophiques majeurs.", "instruction": "Quel concept est étudié?", "options": ["Le transhumanisme", "Le posthumanisme", "Le humanisme", "L'humanitarisme"], "correctAnswer": "Le posthumanisme", "points": 1, "audioUrl": "/assets/audio/dalf-c2-full-3/q2.mp3"},
    ],
    "dalf-c2-full-4": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Colloque: Les approches méthodologiques actuelles en sciences sociales présentent des biais épistémologiques. Une reflexion sur les fondements théoriques s'impose.", "instruction": "Quel est le thème principal?", "options": ["Les résultats", "La méthodologie", "Le financement", "La publication"], "correctAnswer": "La méthodologie", "points": 1, "audioUrl": "/assets/audio/dalf-c2-full-4/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Table ronde: Face aux défis environnementaux, une approche holistique est nécessaire. Les solutions sectorielles ne suffisent plus.", "instruction": "Quelle approche est recommandée?", "options": ["Sectorielle", "Holistique", "Partielle", "Limitée"], "correctAnswer": "Holistique", "points": 1, "audioUrl": "/assets/audio/dalf-c2-full-4/q2.mp3"},
    ],
    "tcf-full-2": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Annonce dans le métro: Prochaine station: Opéra. Correspondance avec les lignes un, deux et huit. Attention à la fermeture des portes.", "instruction": "Quelle est la prochaine station?", "options": ["Bastille", "Opéra", "République", "Châtelet"], "correctAnswer": "Opéra", "points": 1, "audioUrl": "/assets/audio/tcf-full-2/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Message automatique: Votre nouveau code secret est le deux quatre zéro sept. Veuillez le changer lors de votre prochaine connexion.", "instruction": "Quel est le code?", "options": ["2407", "2704", "2047", "2470"], "correctAnswer": "2407", "points": 1, "audioUrl": "/assets/audio/tcf-full-2/q2.mp3"},
        {"id": "q3", "skill": "listening", "type": "multiple_choice", "content": "Publicité radio: Opération soldes! Tous les articles à moins trente pour cent ce week-end uniquement. Ne manquez pas cette offre exceptionnelle!", "instruction": "Quel est le discount?", "options": ["20%", "30%", "40%", "50%"], "correctAnswer": "30%", "points": 1, "audioUrl": "/assets/audio/tcf-full-2/q3.mp3"},
    ],
    "tcf-full-3": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Information météorologique: Le temps sera variable demain. Soleil le matin, nuages l'après-midi et возможно дождь le soir. Températures entre quinze et vingt degrés.", "instruction": "Quel temps prévu pour demain?", "options": ["Pluie toute la journée", "Soleil toute la journée", "Variable avec possibles averses", "Neige"], "correctAnswer": "Variable avec possibles averses", "points": 1, "audioUrl": "/assets/audio/tcf-full-3/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Conversation: Tu as vu le nouveau film de Tarantino? Oui, c'est incroyable! Les dialogues sont exceptionnels et la musique est parfaite.", "instruction": "De quoi parlent-ils?", "options": ["Un livre", "Un film", "Un concert", "Une exposition"], "correctAnswer": "Un film", "points": 1, "audioUrl": "/assets/audio/tcf-full-3/q2.mp3"},
    ],
    "tcf-full-4": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Journal radio: La crise financière de deux mille huit a profondément changé l'économie mondiale. Les Banques ont du se réformer radicalement.", "instruction": "De quelle crise parle-t-on?", "options": ["2000", "2008", "2015", "2020"], "correctAnswer": "2008", "points": 1, "audioUrl": "/assets/audio/tcf-full-4/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "multiple_choice", "content": "Interview: Quel est votre projet professionnel? Je veux créer ma propre entreprise dans le domaine du développement durable. C'est mon ambition.", "instruction": "Que veut faire la personne?", "options": ["Travailler en entreprise", "Créer une entreprise", "Devenir fonctionnaire", "Faire des études"], "correctAnswer": "Créer une entreprise", "points": 1, "audioUrl": "/assets/audio/tcf-full-4/q2.mp3"},
    ],
    "tcf-full-5": [
        {"id": "q1", "skill": "listening", "type": "multiple_choice", "content": "Annonce officielle: Le président de la République s'exprimera ce soir à vingt heures sur les chaînes de télévision nationales. Il abordera la question du changement climatique.", "instruction": "Quand aura lieu le discours?", "options": ["Ce matin", "Cet après-midi", "Ce soir", "Demain"], "correctAnswer": "Ce soir", "points": 1, "audioUrl": "/assets/audio/tcf-full-5/q1.mp3"},
        {"id": "q2", "skill": "listening", "type": "true_false", "content": "Message professionnel: Bonjour Monsieur. Je vous appelle au sujet de notre réunion de demain. Je ne pourrai pas être présent. Pouvons-nous la reprogrammer?", "instruction": "La réunion est maintenue.", "correctAnswer": "false", "points": 1, "audioUrl": "/assets/audio/tcf-full-5/q2.mp3"},
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
    from app.config import settings
    
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
    
    # Add full URL for audio files
    base_url = "http://localhost:5000"
    for q in questions:
        if q.get("audioUrl") and q["audioUrl"].startswith("/assets"):
            q["audioUrl"] = f"{base_url}{q['audioUrl']}"

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