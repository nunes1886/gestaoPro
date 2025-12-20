# 🚀 GestãoPro - Sistema de Gestão para Gráficas e Sublimação

Sistema web completo para gestão de pequenas empresas, com foco em controle de produção, financeiro e hierarquia de acessos. Desenvolvido para oferecer personalização total (White Label) pelo próprio usuário administrador.

## 🖼️ Funcionalidades Principais

* **Dashboards Interativos:** Visão geral de faturamento, aniversariantes e O.S. pendentes.
* **Hierarquia Dinâmica:** Controle de permissões granular (quem vê financeiro, quem gerencia equipe, etc.).
* **Personalização do Sistema:** O usuário altera Logo, Nome da Empresa, Produtos e Preços diretamente pelo painel.
* **Gestão de O.S.:** Fluxo de produção com cálculo automático de preços por m².
* **Segurança:** Reset de fábrica protegido por senha e upload de backups.
* **Formatação Inteligente:** Máscaras automáticas para CNPJ, Telefone e Moeda.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.12 + Django 5.0
* **Frontend:** HTML5, Bootstrap 5, JavaScript (Máscaras de Input)
* **Banco de Dados:** SQLite (padrão)
* **Ícones:** FontAwesome 6

## ⚙️ Como rodar o projeto localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/NOME_DO_REPO.git](https://github.com/SEU_USUARIO/NOME_DO_REPO.git)
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install django
    # (Se tiver gerado um requirements.txt, use: pip install -r requirements.txt)
    ```

4.  **Configure o Banco de Dados:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Crie um Superusuário (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Inicie o Servidor:**
    ```bash
    python manage.py runserver
    ```

7.  Acesse: `http://127.0.0.1:8000/`

---
Desenvolvido por **[Seu Nome]**.