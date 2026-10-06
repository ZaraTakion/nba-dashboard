# NBA Team Dashboard

Painel interativo para explorar estatísticas históricas de equipes da NBA, temporada por temporada, entre 2000 e 2023. O projeto usa Python, Streamlit, Pandas e Plotly.

> Este projeto é independente e não é afiliado à NBA. Os dados são um arquivo estático; não há atualização em tempo real.

## O que o painel oferece

- Seleção de franquia, temporada e indicador estatístico.
- Evolução histórica da franquia e comparação com as equipes da temporada escolhida.
- Média da liga somente nas temporadas em que a fonte inclui essa linha.
- Marcador `*` da fonte preservado e opção para filtrar equipes com esse marcador.
- Nomes históricos agrupados sob a franquia atual, com o nome original da fonte visível nos detalhes.
- Percentuais formatados como porcentagem, embora sejam armazenados como proporções decimais no CSV.
- Tabela com as estatísticas e identificação da franquia selecionada.

## Dados e limites

O CSV incluído em `app/nba_clean.csv` foi obtido do conjunto [NBA Teams Stat 2000–2023 no Kaggle](https://www.kaggle.com/datasets/bluedreamv1b3/nba-teams-stat-2000-2023). O painel não consulta uma API e não verifica os números contra uma fonte oficial em tempo real. A cobertura observada no arquivo é de 739 linhas e 24 temporadas rotuladas de 2000 a 2023. A linha “League Average” não existe em todas as temporadas.

Os rótulos históricos presentes no arquivo são normalizados para permitir acompanhar a mesma franquia ao longo do tempo: Charlotte Bobcats → Charlotte Hornets; New Jersey Nets → Brooklyn Nets; New Orleans Hornets e New Orleans/Oklahoma City Hornets → New Orleans Pelicans; Seattle SuperSonics → Oklahoma City Thunder; Vancouver Grizzlies → Memphis Grizzlies. O campo “Nome na fonte” conserva o rótulo original para auditoria e contexto histórico. A normalização acompanha a continuidade da franquia; não afirma que a marca ou a cidade fossem as mesmas naquela época.

O asterisco é apresentado como marcador da fonte e pode ser usado como filtro. O Basketball-Reference descreve `*` como marcador de equipes que chegaram aos playoffs; como o conjunto intermediário do Kaggle não informa proveniência detalhada por linha, o painel preserva o símbolo em vez de inferir outros significados. Consulte a [convenção do Basketball-Reference](https://www.basketball-reference.com/).

A licença de redistribuição do conjunto de dados não pôde ser confirmada. Por esse motivo, este repositório não declara uma licença própria nem atribui uma licença ao CSV. Verifique os termos do conjunto original antes de redistribuir os dados.

## Executar localmente

Requer Python 3.11 ou superior. No Windows 10, abra o terminal na pasta clonada e execute:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app/app.py
```

No macOS ou Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app/app.py
```

O Streamlit abrirá o endereço local no navegador, normalmente `http://localhost:8501`.

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes verificam a estrutura e as regras dos dados, os aliases históricos, a escala dos percentuais e uma inicialização do painel via Streamlit AppTest. O GitHub Actions executa compilação e testes em Python 3.11 em cada push ou pull request para `main`.

## Estrutura

```text
app/
  app.py             # interface Streamlit e gráficos Plotly
  data_utils.py      # validação, normalização e leitura do CSV
  nba_clean.csv      # recorte estático do Kaggle
.streamlit/
  config.toml        # tema do painel
 tests/              # testes de dados e smoke test do app
```

## Tecnologias

- Python 3.11+
- Streamlit
- Pandas
- Plotly
