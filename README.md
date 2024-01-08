[![Python application](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/application.yml/badge.svg)](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/application.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/psgrigoletti/margemliquida-streamlit/badge)](https://www.codefactor.io/repository/github/psgrigoletti/margemliquida-streamlit)
[![Codecov](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/codecov.yml/badge.svg)](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/codecov.yml)
[![codecov](https://codecov.io/gh/psgrigoletti/margemliquida-streamlit/graph/badge.svg?token=8XSEKSF7WE)](https://codecov.io/gh/psgrigoletti/margemliquida-streamlit)
[![CodeQL](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/github-code-scanning/codeql)
[![Pylint](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/pylint.yml/badge.svg)](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/pylint.yml)
[![Pyre](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/pyre.yml/badge.svg)](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/pyre.yml)
[![Pysa](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/pysa.yml/badge.svg)](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/pysa.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Snyk Security](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/snyk-security.yml/badge.svg)](https://github.com/psgrigoletti/margemliquida-streamlit/actions/workflows/snyk-security.yml)

# margemliquida-streamlit (eternamente versão: 0.0.1)

# :bulb: Aplicação criada para:
- Exercitar os aprendizados do curso [Python para Mercado Financeiro](https://hotmart.com/pt-br/marketplace/produtos/python-para-mercado-financeiro/) da [Trading com Dados](https://tradingcomdados.com/).
- Aprender a usar a biblioteca [Streamlit](https://streamlit.io/), bem como o ambiente [Streamlit Cloud](https://streamlit.io/cloud).

# :computer: Para você rodar localmente:

- Clonar o repositório:
  - ```git clone git@github.com:psgrigoletti/margemliquida-streamlit.git``` 
- Entrar na pasta margemliquida-streamlit
- Se quiser, crie um env para isolar as dependências desta aplicação
- Baixar as dependências:
  - ```$ pip install -r requirements.txt ```
- Executar o comando para iniciar o streamlit:
  - ```$ streamlit run src/streamlit_app.py```
- Acessar no navegador a url [http://localhost:8501](http://localhost:8501/):
  - para logar use ```usuário: guest | senha: guest```

# :computer: Para você acessar na [Streamlit Cloud](https://streamlit.io/cloud):
- Acessar no navegador a url [https://margemliquida.streamlit.app/](https://margemliquida.streamlit.app/)
  - para logar use ```usuário: guest | senha: guest```

# :construction_worker_man: Para você criar seus próprios usuários:
- Ajuste o arquivo config.yaml de acordo com as [instruções](https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/).

# :bug: Issues para bugs ou features:
- Encontrou bugs ou deseja novas funcionalidades? [Clique aqui](https://github.com/psgrigoletti/margemliquida-streamlit/issues/new) e abra uma issue.

# :computer: Ambiente dev sugerido:
- [VS Code](https://code.visualstudio.com/)
- Extensões:
  - Pylint	https://marketplace.visualstudio.com/items?itemName=ms-python.pylint
  - flake8	https://marketplace.visualstudio.com/items?itemName=ms-python.flake8
  - mypy	https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker

# :test_tube: Pylint
- pylint ./src/ | pylint_report > report.html
- [Último report gerado](https://htmlpreview.github.io/?https://raw.githubusercontent.com/psgrigoletti/margemliquida-streamlit/main/report.html)

# :construction: Todo list:
- Em construção
- Separar melhor a "camada da lógica de negócio" da "camada de apresentação", de forma que seja possível reutilizar as implementações com outros frontend
- Usar https://pypi.org/project/pyettj/
- Usar https://riskfolio-lib.readthedocs.io/
- Usar https://shields.io/
- Definir um fluxo de trabalho https://www.atlassian.com/br/git

# :pill: Links úteis:
- [Streamlit - Site oficial](http://streamlit.io) 
- [Streamlit - Documentação](http://docs.streamlit.io) 
- [Streamlit - Comunidade](http://discuss.streamlit.io) 
- [Projeto Awesome Streamlit](http://awesome-streamlit.org)
- [Trading com Dados](https://www.tradingcomdados.com.br/)

# :bookmark: Links que usei e me ajudaram:
- https://wkrzywiec.medium.com/how-to-write-good-quality-python-code-with-github-actions-2f635a2ab09a
- https://code.visualstudio.com/docs/python/python-tutorial
- https://code.visualstudio.com/docs/python/linting
- https://www.atlassian.com/br/git

# :email: Contato:
- Quer contribuir neste projeto?
- Apenas trocar ideias?
- Realizar novos projetos juntos?

Entre em contato!

**Pablo Souza Grigoletti** - ```psgrigoletti@gmail.com```
