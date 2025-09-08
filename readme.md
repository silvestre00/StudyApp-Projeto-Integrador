# 📚 Aplicativo de Estudos com Streamlit

Este projeto faz parte de um trabalho acadêmico e tem como objetivo o desenvolvimento de um **aplicativo web para organização de estudos**, utilizando **Python, Streamlit e SQLite**.

A aplicação é modular e conta com diferentes funcionalidades para auxiliar estudantes no planejamento e acompanhamento das suas rotinas de estudo.

---

## 🚀 Funcionalidades Implementadas

- **Planner de Estudos Interativo**
  - Cadastro de disciplinas
  - Definição de horas e minutos semanais para cada disciplina
  - Armazenamento em banco SQLite
  - Visualização de cronogramas em tabelas e gráficos (pizza e barras)

*(Outros módulos como Quiz, Flashcards e Resumos ainda serão adicionados futuramente.)*

---

## 🛠️ Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [SQLite (via SQLAlchemy)](https://www.sqlalchemy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)

---

## 📂 Estrutura do Projeto

```
StudyApp/
│── app.py                  # Arquivo principal do Streamlit
│── modules/
│   └── planner.py          # Módulo de Planner de Estudos
│── utils/
│   ├── storage.py          # Conexão com o banco SQLite
│   └── helpers.py          # Funções auxiliares (conversão de horas/minutos)
│── data/
│   └── estudos.db          # Banco de dados SQLite (ignorado pelo Git)
│── .gitignore              # Arquivos e pastas ignorados pelo Git
└── requirements.txt        # Dependências do projeto
```

---

## ⚙️ Como Executar o Projeto

1. **Clone este repositório**
   ```bash
   git clone https://github.com/seu-usuario/studyapp.git
   cd studyapp
   ```

2. **Crie um ambiente virtual e ative-o**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```
   *(se ainda não existir requirements.txt, você pode gerar com `pip freeze > requirements.txt`)*

4. **Execute a aplicação**
   ```bash
   streamlit run app.py
   ```

5. **Acesse no navegador**
   ```
   http://localhost:8501
   ```

---

## 🎯 Próximos Passos

- Implementar módulo de **Quiz/Simulados**
- Criar **Flashcards Digitais**
- Adicionar **Resumo Inteligente** com integração de IA
- Expandir **Gestor de Provas e Trabalhos**
- Criar **Dashboard de Estatísticas de Estudo**
- Implementar **Modo Foco (Pomodoro)**

---

## 👥 Equipe do Projeto

Projeto desenvolvido pelos seguintes integrantes como parte do Projeto Integrador Senac Grupo 39:

- **Silvestre Alves**
- **Valter Paulino**
- **Vinicius Luscri**
- **Vitor Alves**
- **Tiago Sampaio**

---

## 📄 Licença

Este projeto é de uso acadêmico.
Sinta-se livre para clonar e melhorar.