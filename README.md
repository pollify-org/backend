# Polify

Polify: Um projeto backend para o sistema do projeto integrador da Universidade Evangélica de Goiás, desenvolvido em FastAPI.

## Como começar

```bash
python3 -m venv env
source env/bin/activate
```

Crie um arquivo `.env` seguindo o modelo `example.env`

O arquivo `app/config.py` possui três configurações: Teste, Desenvolvimento e Produção.

```bash
touch .env
```

Execute o comando abaixo para instalar as dependências. O arquivo `runtime.txt` especifica a versão de runtime utilizada.

```bash
bash reset.sh
```

## Executar a aplicação localmente

```bash
python run.py
```

## Executar testes

Utilizamos a configuração `TestConfig` para rodar os testes.

```bash
bash test.sh
```

## Funcionalidades

- **SQLAlchemy Assíncrono**: Utiliza as capacidades assíncronas do SQLAlchemy para operações eficientes com banco de dados.
- **Framework FastAPI**: Leva vantagem do FastAPI para construir APIs de alto desempenho com Python 3.8+.
- **Validação de Dados com Pydantic**: Emprega modelos Pydantic para garantir integridade e validação dos dados.
- **Autenticação OAuth2**: Implementa protocolos OAuth2 para autenticação e autorização seguras.
- **Logging Abrangente**: Inclui logging para monitorar o comportamento da aplicação e facilitar a depuração.
- **Configurações Baseadas em Ambiente**: Suporta várias configurações (Teste, Desenvolvimento, Produção) para se adaptar a diferentes cenários de implantação.

## Estrutura do Projeto

A aplicação modela três principais entidades:

- **User**: Representa os usuários da aplicação.
- **Post**: Denota conteúdo criado pelos usuários.
- **Tag**: Classifica os posts para melhor organização.

As relações entre esses modelos são definidas da seguinte forma:

- Um **Usuário** pode ter várias **Tags**.
- Um **Usuário** pode criar vários **Posts**.
- **Posts** e **Tags** compartilham uma relação muitos-para-muitos, gerida por uma tabela de associação.

Este design facilita a recuperação e manipulação eficientes dos dados, seguindo as melhores práticas de normalização de banco de dados.

## Carregamento Eficiente de Relacionamentos

Para otimizar o desempenho, o framework utiliza estratégias seletivas de carregamento de relacionamentos:

- Ao buscar múltiplos registros de um modelo, entidades relacionadas não são carregadas por padrão, reduzindo consultas desnecessárias ao banco de dados.
- Ao recuperar um único registro, geralmente pelo seu ID, as entidades relacionadas são carregadas antecipadamente para fornecer dados completos em uma única consulta.

Esta abordagem equilibra desempenho com disponibilidade de dados, garantindo uma utilização eficiente dos recursos.

## Classe Base do Modelo

O projeto define uma classe `Base` personalizada da qual todos os modelos herdam. Esta classe inclui configurações e comportamentos comuns, promovendo reutilização de código e consistência nos modelos de dados da aplicação.

## Informações do Projeto

**Autor**: João Victor Guimarães Santos  