from fastapi import APIRouter, Depends
from typing import List, Dict, Any

router = APIRouter(prefix="/courses", tags=["courses"])

MOCK_COURSES = {
    "delf-a1": {
        "id": "delf-a1",
        "name": "DELF A1",
        "fullName": "Diplôme d'Études en Langue Française - A1",
        "level": "Sơ cấp",
        "description": "Chứng chỉ tiếng Pháp trình độ sơ cấp dành cho người mới bắt đầu",
        "longDescription": "DELF A1 là chứng chỉ đầu tiên trong hệ thống DELF/DALF, dành cho những người mới bắt đầu học tiếng Pháp.",
        "icon": "🌱",
        "color": "text-green-500",
        "bgColor": "bg-green-500",
        "questions": 450,
        "duration": "1h20",
        "skills": [
            {"name": "Nghe", "nameFr": "Compréhension orale", "questions": 120, "description": "Nghe và trả lời câu hỏi", "slug": "listening"},
            {"name": "Ngữ pháp & Từ vựng", "nameFr": "Maîtrise des structures de la langue", "questions": 80, "description": "Ngữ pháp và từ vựng cơ bản", "slug": "language_structure"},
            {"name": "Đọc", "nameFr": "Compréhension écrite", "questions": 200, "description": "Đọc hiểu các văn bản đơn giản", "slug": "reading"},
            {"name": "Viết", "nameFr": "Production écrite", "questions": 30, "description": "Viết form điền thông tin", "slug": "writing"},
            {"name": "Nói", "nameFr": "Production orale", "questions": 20, "description": "Giới thiệu bản thân", "slug": "speaking"}
        ]
    },
    "delf-a2": {
        "id": "delf-a2",
        "name": "DELF A2",
        "fullName": "Diplôme d'Études en Langue Française - A2",
        "level": "Sơ cấp",
        "description": "Giao tiếp trong các tình huống đơn giản và quen thuộc",
        "longDescription": "DELF A2 chứng nhận khả năng giao tiếp trong các tình huống đơn giản hàng ngày.",
        "icon": "🌿",
        "color": "text-green-600",
        "bgColor": "bg-green-600",
        "questions": 450,
        "duration": "1h40",
        "skills": [
            {"name": "Nghe", "nameFr": "Compréhension orale", "questions": 120, "description": "Hiểu thông báo, hướng dẫn", "slug": "listening"},
            {"name": "Ngữ pháp & Từ vựng", "nameFr": "Maîtrise des structures de la langue", "questions": 80, "description": "Ngữ pháp và từ vựng sơ cấp", "slug": "language_structure"},
            {"name": "Đọc", "nameFr": "Compréhension écrite", "questions": 200, "description": "Đọc thư từ, quảng cáo", "slug": "reading"},
            {"name": "Viết", "nameFr": "Production écrite", "questions": 30, "description": "Viết tin nhắn, email", "slug": "writing"},
            {"name": "Nói", "nameFr": "Production orale", "questions": 20, "description": "Mô tả thói quen, sở thích", "slug": "speaking"}
        ]
    },
    "delf-b1": {
        "id": "delf-b1",
        "name": "DELF B1",
        "fullName": "Diplôme d'Études en Langue Française - B1",
        "level": "Trung cấp",
        "description": "Độc lập trong giao tiếp, diễn đạt ý kiến cá nhân",
        "longDescription": "DELF B1 đánh dấu ngưỡng người dùng độc lập.",
        "icon": "🌳",
        "color": "text-blue-500",
        "bgColor": "bg-blue-500",
        "questions": 380,
        "duration": "1h55",
        "skills": [
            {"name": "Nghe", "nameFr": "Compréhension orale", "questions": 100, "description": "Hiểu các cuộc hội thoại", "slug": "listening"},
            {"name": "Ngữ pháp & Từ vựng", "nameFr": "Maîtrise des structures de la langue", "questions": 70, "description": "Ngữ pháp và từ vựng trung cấp", "slug": "language_structure"},
            {"name": "Đọc", "nameFr": "Compréhension écrite", "questions": 170, "description": "Đọc báo, blog", "slug": "reading"},
            {"name": "Viết", "nameFr": "Production écrite", "questions": 25, "description": "Viết essay ngắn", "slug": "writing"},
            {"name": "Nói", "nameFr": "Production orale", "questions": 15, "description": "Thuyết trình, tranh luận", "slug": "speaking"}
        ]
    },
    "delf-b2": {
        "id": "delf-b2",
        "name": "DELF B2",
        "fullName": "Diplôme d'Études en Langue Française - B2",
        "level": "Trung cấp cao",
        "description": "Độc lập hoàn toàn, lập luận phức tạp",
        "longDescription": "DELF B2 là trình độ yêu cầu để đăng ký vào đại học Pháp.",
        "icon": "🌲",
        "color": "text-blue-600",
        "bgColor": "bg-blue-600",
        "questions": 380,
        "duration": "2h30",
        "skills": [
            {"name": "Nghe", "nameFr": "Compréhension orale", "questions": 100, "description": "Hiểu bài giảng, phóng sự", "slug": "listening"},
            {"name": "Ngữ pháp & Từ vựng", "nameFr": "Maîtrise des structures de la langue", "questions": 70, "description": "Ngữ pháp và từ vựng trung cấp cao", "slug": "language_structure"},
            {"name": "Đọc", "nameFr": "Compréhension écrite", "questions": 170, "description": "Đọc báo, bài nghị luận", "slug": "reading"},
            {"name": "Viết", "nameFr": "Production écrite", "questions": 25, "description": "Viết thư trang trọng", "slug": "writing"},
            {"name": "Nói", "nameFr": "Production orale", "questions": 15, "description": "Tranh luận, thuyết trình", "slug": "speaking"}
        ]
    },
    "dalf-c1": {
        "id": "dalf-c1",
        "name": "DALF C1",
        "fullName": "Diplôme Approfondi de Langue Française - C1",
        "level": "Cao cấp",
        "description": "Thành thạo ngôn ngữ trong môi trường học thuật và chuyên nghiệp",
        "longDescription": "DALF C1 chứng nhận khả năng sử dụng tiếng Pháp thành thạo.",
        "icon": "🏔️",
        "color": "text-purple-500",
        "bgColor": "bg-purple-500",
        "questions": 315,
        "duration": "4h",
        "skills": [
            {"name": "Nghe", "nameFr": "Compréhension orale", "questions": 80, "description": "Hiểu bài giảng, hội thảo", "slug": "listening"},
            {"name": "Ngữ pháp & Từ vựng", "nameFr": "Maîtrise des structures de la langue", "questions": 60, "description": "Ngữ pháp và từ vựng cao cấp", "slug": "language_structure"},
            {"name": "Đọc", "nameFr": "Compréhension écrite", "questions": 140, "description": "Đọc văn bản học thuật", "slug": "reading"},
            {"name": "Viết", "nameFr": "Production écrite", "questions": 20, "description": "Viết tổng hợp tài liệu", "slug": "writing"},
            {"name": "Nói", "nameFr": "Production orale", "questions": 15, "description": "Thuyết trình học thuật", "slug": "speaking"}
        ]
    },
    "dalf-c2": {
        "id": "dalf-c2",
        "name": "DALF C2",
        "fullName": "Diplôme Approfondi de Langue Française - C2",
        "level": "Tinh thông",
        "description": "Tinh thông như người bản ngữ",
        "longDescription": "DALF C2 là cấp độ cao nhất.",
        "icon": "🏆",
        "color": "text-purple-600",
        "bgColor": "bg-purple-600",
        "questions": 315,
        "duration": "3h30",
        "skills": [
            {"name": "Nghe", "nameFr": "Compréhension orale", "questions": 80, "description": "Nghe tài liệu phức tạp", "slug": "listening"},
            {"name": "Ngữ pháp & Từ vựng", "nameFr": "Maîtrise des structures de la langue", "questions": 60, "description": "Ngữ pháp và từ vựng tinh thông", "slug": "language_structure"},
            {"name": "Đọc", "nameFr": "Compréhension écrite", "questions": 140, "description": "Phân tích văn bản học thuật", "slug": "reading"},
            {"name": "Viết", "nameFr": "Production écrite", "questions": 20, "description": "Viết bài nghị luận", "slug": "writing"},
            {"name": "Nói", "nameFr": "Production orale", "questions": 15, "description": "Thuyết trình học thuật", "slug": "speaking"}
        ]
    },
    "tcf": {
        "id": "tcf",
        "name": "TCF",
        "fullName": "Test de Connaissance du Français",
        "level": "Mọi trình độ",
        "description": "Bài test đánh giá trình độ tiếng Pháp",
        "longDescription": "TCF là bài kiểm tra tiếng Pháp được công nhận quốc tế.",
        "icon": "🎓",
        "color": "text-primary-500",
        "bgColor": "bg-primary-500",
        "questions": 380,
        "duration": "2h30",
        "skills": [
            {"name": "Nghe", "nameFr": "Compréhension orale", "questions": 100, "description": "Nghe các đoạn hội thoại", "slug": "listening"},
            {"name": "Ngữ pháp & Từ vựng", "nameFr": "Maîtrise des structures de la langue", "questions": 70, "description": "Ngữ pháp và từ vựng", "slug": "language_structure"},
            {"name": "Đọc", "nameFr": "Compréhension écrite", "questions": 170, "description": "Đọc hiểu các văn bản", "slug": "reading"},
            {"name": "Viết", "nameFr": "Production écrite", "questions": 25, "description": "Viết bài luận ngắn", "slug": "writing"},
            {"name": "Nói", "nameFr": "Production orale", "questions": 15, "description": "Nói theo chủ đề", "slug": "speaking"}
        ]
    }
}


@router.get("")
def get_courses():
    return list(MOCK_COURSES.values())


@router.get("/{slug}")
def get_course(slug: str):
    course = MOCK_COURSES.get(slug)
    if not course:
        return {"error": "Course not found"}
    return course