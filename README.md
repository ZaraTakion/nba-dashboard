# 🏀 NBA Dashboard – Python + Streamlit

Dashboard interativo desenvolvido em **Python** para análise de desempenho de times da NBA (2000–2023).  
Combina visualização de dados, interatividade e design moderno com **Streamlit** e **Plotly**.

---

## 🚀 Tecnologias Utilizadas
- **Python 3.10+**
- **Streamlit** – interface interativa
- **Pandas** – manipulação e limpeza de dados
- **Plotly Express** – gráficos dinâmicos e responsivos
- **Dataset:** [Kaggle – NBA Team Stats (2000–2023)](https://www.kaggle.com/datasets/bluedreamv1b3/nba-teams-stat-2000-2023)

---

## 🧠 Funcionalidades
- Filtros dinâmicos por **time**, **temporada** e **métrica**  
- KPIs automáticos: Pontos, Assistências e Rebotes  
- Gráficos interativos:
  - Linha: evolução da métrica ao longo dos anos  
  - Barras: comparativo entre times em uma temporada  
- Layout **dark mode** estilizado com CSS customizado  
- Estatísticas descritivas em tempo real

---

## 💻 Como Rodar Localmente

```bash
# Clonar o repositório
git clone https://github.com/<seu-usuario>/nba-dashboard.git
cd nba-dashboard

# Instalar dependências
pip install -r requirements.txt

# Executar o dashboard
streamlit run app/app.py

````

---

## ☁️ Deploy

O projeto pode ser publicado gratuitamente via [Streamlit Cloud](https://streamlit.io/cloud).
Basta conectar o repositório do GitHub e definir o caminho do arquivo principal:

```
app/app.py
```

## 📸 Preview

*(Adicione aqui uma captura de tela do dashboard após o deploy)*
Exemplo:
![NBA Dashboard Preview](./screenshot.png)

## 🧩 Estrutura do Projeto

```
nba-dashboard/
│
├── app/
│   └── app.py
│
├── data/
│   └── nba_clean.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```

## ✨ Autor

**Zara Takion**
Estudante de Sistemas para Internet • Foco em Dados e Web Design
📫 [LinkedIn](https://www.linkedin.com) | [GitHub](https://github.com/<seu-usuario>)


