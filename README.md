# Polify

Polify é um projeto de backend desenvolvido com FastAPI, originado de um projeto maior da Universidade Evangélica de Goiás. O módulo de usuário foi transportado para esta versão com o objetivo de demonstrar a aplicação dos conceitos abordados na disciplina de API Backend. A estrutura foi mantida de forma anônima, preservando o código fonte original dos desenvolvedores, mas permitindo a demonstração das boas práticas e conceitos como SOLID.

Este projeto foi projetado para ser executado **únicamente em distribuições Linux**.

## Como Começar

1. Clone o repositório e entre no diretório do projeto.

2. Execute o script de setup para configurar o ambiente e instalar as dependências:

   ```bash
   ./setup.sh
   ```

   Durante o processo, o script irá:
   - Preencher as dependências no arquivo `.env`, baseado no modelo fornecido.
   - Instalar as dependências necessárias.

3. O arquivo `app/config.py` contém três configurações principais: **Teste**, **Desenvolvimento** e **Produção**. Escolha a configuração desejada.

4. Para rodar a aplicação localmente, execute:

   ```bash
   python run.py
   ```

## Executar os Testes

O ambiente de testes está configurado com o `TestConfig`. Para rodar os testes, execute:

```bash
bash test.sh
```

## Funcionalidades

- **SQLAlchemy Assíncrono**: Aproveita a performance assíncrona do SQLAlchemy para operações eficientes com o banco de dados.
- **FastAPI**: A estrutura FastAPI é utilizada para garantir alta performance e rapidez na construção das APIs.
- **Validação de Dados com Pydantic**: Utiliza modelos Pydantic para garantir que os dados sejam validados e integros.
- **Autenticação OAuth2**: Implementa OAuth2 para autenticação e autorização seguras.
- **Logging Abrangente**: Logging detalhado para monitoramento e depuração da aplicação.
- **Configurações Baseadas em Ambiente**: Suporta múltiplas configurações de ambiente (Teste, Desenvolvimento, Produção) para adaptação a diferentes cenários de implantação.

## Estrutura do Projeto

Este projeto foca no módulo de **Usuário**, o qual é o único componente transportado para demonstrar os conceitos abordados. A estrutura do banco de dados é otimizada para garantir uma manipulação eficiente dos dados.

### Carregamento Eficiente de Relacionamentos

A aplicação implementa técnicas de carregamento eficiente de relacionamentos:

- **Carregamento Seletivo**: Quando múltiplos registros são recuperados, as entidades relacionadas não são carregadas automaticamente, evitando consultas desnecessárias ao banco de dados.
- **Carregamento Antecipado**: Quando um único registro é recuperado, as entidades relacionadas são carregadas junto para evitar múltiplas consultas.

Essas estratégias ajudam a balancear desempenho e disponibilidade de dados, otimizando o uso de recursos.

## Classe Base do Modelo

A aplicação utiliza uma classe base personalizada, da qual todos os modelos herdam. Isso facilita a reutilização de código e garante consistência no comportamento dos modelos de dados.

## Informações do Projeto

**Autor**: João Victor Guimarães Santos