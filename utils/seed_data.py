#Perguntas de exemplo para popular o quiz



from sqlalchemy import insert
from utils.storage import session, questions, answers

def seed_questions():
    sample_questions = [
        {
            "text": "O que significa a sigla SQL?",
            "answers": [
                ("Structured Query Language", True),
                ("Simple Question Line", False),
                ("Strong Query Logic", False),
                ("Standard Quick Language", False),
            ],
        },
        {
            "text": "Qual a saída de print(2 ** 3) em Python?",
            "answers": [
                ("5", False),
                ("6", False),
                ("8", True),
                ("9", False),
            ],
        },
        {
            "text": "Qual empresa desenvolveu o sistema operacional Windows?",
            "answers": [
                ("Apple", False),
                ("Microsoft", True),
                ("IBM", False),
                ("Google", False),
            ],
        },
        {
            "text": "O que é um algoritmo?",
            "answers": [
                ("Um hardware de computador", False),
                ("Uma sequência de instruções para resolver um problema", True),
                ("Um tipo de banco de dados", False),
                ("Um sistema operacional", False),
            ],
        },
        {
            "text": "Qual protocolo é usado para transferir páginas web?",
            "answers": [
                ("FTP", False),
                ("HTTP", True),
                ("SMTP", False),
                ("SSH", False),
            ],
        },
        {
            "text": "Qual destas é uma linguagem de programação?",
            "answers": [
                ("HTML", False),
                ("CSS", False),
                ("Python", True),
                ("HTTP", False),
            ],
        },
        {
            "text": "O que significa a sigla CPU?",
            "answers": [
                ("Central Processing Unit", True),
                ("Computer Personal Unit", False),
                ("Central Program Utility", False),
                ("Control Processing Usage", False),
            ],
        },
        {
            "text": "Qual banco de dados é relacional?",
            "answers": [
                ("MongoDB", False),
                ("PostgreSQL", True),
                ("Redis", False),
                ("Elasticsearch", False),
            ],
        },
        {
            "text": "Quem é considerado o criador da World Wide Web?",
            "answers": [
                ("Bill Gates", False),
                ("Tim Berners-Lee", True),
                ("Steve Jobs", False),
                ("Larry Page", False),
            ],
        },
        {
            "text": "Qual destas é uma tecnologia de versionamento de código?",
            "answers": [
                ("Docker", False),
                ("Git", True),
                ("Kubernetes", False),
                ("Nginx", False),
            ],
        },
    ]

    for q in sample_questions:
        q_stmt = insert(questions).values(text=q["text"])
        result = session.execute(q_stmt)
        q_id = result.inserted_primary_key[0]

        for ans_text, is_correct in q["answers"]:
            session.execute(
                insert(answers).values(
                    question_id=q_id, text=ans_text, is_correct=is_correct
                )
            )

    session.commit()
    print("✅ 10 perguntas de exemplo foram adicionadas ao banco de dados!")
