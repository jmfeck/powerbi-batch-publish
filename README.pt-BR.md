# Power BI Batch Publisher

[![Assista ao tutorial no YouTube](https://img.shields.io/badge/YouTube-Assistir%20Tutorial-red?logo=youtube)](https://www.youtube.com/watch?v=s6eXtUX6FL8)

> 📺 Um passo a passo completo desta ferramenta está disponível no YouTube. Clique acima para assistir.

---

Este repositório contém uma ferramenta baseada em Python e PowerShell que automatiza a publicação de arquivos `.pbix` no Power BI Service utilizando comandos do PowerShell.

A ferramenta foi desenvolvida para Windows e é ideal para cenários em que você publica vários relatórios regularmente e quer evitar etapas manuais repetitivas.

## Visão Geral

- Coloque seus arquivos `.pbix` na pasta `input/`.
- Defina o workspace do Power BI no arquivo `config/config.yaml`.
- Execute a ferramenta usando o arquivo `.bat` ou diretamente via Python.
- O script realiza o login pelo navegador (não utiliza conta de serviço).
- Cada arquivo `.pbix` é publicado usando seu nome como nome do relatório.
- Os arquivos publicados são movidos para a pasta `output/`.

## Estrutura de Pastas

    powerbi-batch-publisher/
    ├── input/                              Coloque os arquivos PBIX aqui
    ├── output/                             Arquivos publicados serão movidos para cá
    ├── logs/                               Logs da execução
    ├── scripts/
    │   └── main.py                         Script principal
    ├── config/
    │   └── config.yaml                     Defina o nome do workspace aqui
    ├── run_powerbi_batch_publish.bat    Atalho para execução
    ├── requirements.txt
    └── README.md

## Instruções de Instalação

### 1. Clone o repositório e instale as dependências do Python

    git clone https://github.com/jmfeck/powerbi-batch-publisher.git
    cd powerbi-batch-publisher
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

### 2. Instale o módulo PowerShell do Power BI

Abra o **PowerShell como Administrador** e execute:

    Install-Module -Name MicrosoftPowerBIMgmt -Scope CurrentUser

Durante a instalação, você pode ser solicitado a:

- **Instalar o NuGet** — responda com `Y` (Yes) para continuar.
- **Confiar no repositório PSGallery** — responda com `Y` (Yes) para confirmar.

> Esse módulo é necessário para publicar arquivos `.pbix` via script com o PowerShell.

### 3. Verifique a instalação

Para confirmar que o módulo foi instalado corretamente, execute:

    Get-Module -ListAvailable MicrosoftPowerBIMgmt

Você deve ver uma saída como esta:

    ModuleType Version    Name                      ExportedCommands
    ---------- -------    ----                      ----------------
    Script     1.X.X      MicrosoftPowerBIMgmt      {Connect-PowerBIServiceAccount, ...}

Se nada for exibido, a instalação falhou. Tente novamente como administrador.

### 4. Defina o nome do workspace

Edite o arquivo `config/config.yaml` e defina o nome do workspace de destino:

    workspace_name: "NOME_DO_SEU_WORKSPACE"

Você pode encontrar esse nome na URL ou interface do Power BI Service. Ele deve corresponder exatamente.

### 5. Adicione os arquivos PBIX

Coloque todos os arquivos `.pbix` que deseja publicar dentro da pasta `input/`.  
Cada relatório será publicado com **o nome exato do arquivo**, então escolha nomes claros e consistentes.

### 6. Execute o script

Você pode executar a ferramenta de duas formas:

Usando o arquivo `.bat`:

    run_powerbi_batch_publish.bat

Ou diretamente via Python:

    python scripts/main.py

## O Que o Script Faz

- Lê a pasta `input/` e encontra os arquivos `.pbix`.
- Monta uma sequência de comandos PowerShell que:
  - Define a política de execução como `Bypass` (necessário em alguns ambientes corporativos).
  - Faz login no Power BI via navegador (você será solicitado a se autenticar).
  - Publica cada arquivo `.pbix` no workspace definido.
- Após a publicação:
  - O script imprime no console os links dos relatórios publicados.
  - Cada arquivo publicado é movido para a pasta `output/`.
- Relatórios com o mesmo nome serão **sobrescritos**.

## Notas Finais

- Esta ferramenta foi testada apenas no **Windows**.
- A autenticação é feita via navegador usando sua conta pessoal do Power BI — **não usa conta de serviço**.
- O nome do relatório publicado será **exatamente o mesmo do arquivo `.pbix`**.
- Na prática, essa ferramenta reduziu um processo manual de 30 a 60 minutos (para 12 relatórios) para **menos de 3 minutos**.
