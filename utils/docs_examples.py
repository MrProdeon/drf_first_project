example_course_dict = {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "lessons": [
                {
                    "id": 0,
                    "video_url": "string",
                    "title": "string",
                    "preview": "string",
                    "description": "string",
                    "course": 0,
                    "owner": 0
                }
            ],
            "count_lessons": "string",
            "is_signed": "string",
            "title": "string",
            "preview": "string",
            "description": "string",
            "owner": 0
        }]
}

example_lesson_dict = {
    'count': 10,
    'next': 'http://...',
    'previous': None,
    'results': [
        {
            'id': 1,
            'title': 'Введение в Python',
            'owner': 5,
            'created_at': '2024-01-01T12:00:00Z'
        }
    ]
}

example_user_dict = {
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "password": "string",
      "last_login": "2026-05-15T08:20:31.439Z",
      "is_superuser": True,
      "first_name": "string",
      "last_name": "string",
      "is_staff": True,
      "is_active": True,
      "date_joined": "2026-05-15T08:20:31.439Z",
      "phone_number": "string",
      "city": "string",
      "avatar": "string",
      "email": "user@example.com",
      "groups": [
        0
      ],
      "user_permissions": [
        0
      ]
    }
  ]
}

example_payments_dict = {
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "payment_date": "2026-05-15",
      "payment_amount": 2147483647,
      "session_id": "string",
      "payment_link": "string",
      "payment_method": "cash",
      "user": 0,
      "course": 0,
      "lesson": 0
    }
  ]
}
