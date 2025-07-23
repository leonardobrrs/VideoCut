# ✂️ Cortador de Vídeo Web

![Licença](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask)
![MoviePy](https://img.shields.io/badge/MoviePy-E8D232?logo=python&logoColor=black)

Uma aplicação web simples construída com Python e Flask que permite aos usuários fazer o upload de um vídeo, definir um intervalo de tempo e cortar o clipe correspondente para download.

![Demonstração do Cortador de Vídeo Web](https://cdn-icons-gif.flaticon.com/6172/6172554.gif) ---

## ✨ Funcionalidades

* **Interface Simples:** Faça o upload e defina os tempos de corte em uma única página.
* **Upload de Vídeos:** Suporte para os formatos mais comuns de vídeo (MP4, MOV, AVI, etc.).
* **Corte Preciso:** Defina os segundos de início e fim para extrair o clipe desejado.
* **Processamento no Backend:** Utiliza a poderosa biblioteca **MoviePy** (com FFmpeg) para realizar o corte no servidor.
* **Download Direto:** Baixe o vídeo processado diretamente do navegador.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:**
    * [Python](https://www.python.org/)
    * [Flask](https://flask.palletsprojects.com/) (Framework Web)
    * [MoviePy](https://zulko.github.io/moviepy/) (Biblioteca de edição de vídeo)
* **Dependência Externa:**
    * [FFmpeg](https://ffmpeg.org/)
* **Frontend:**
    * HTML5
    * CSS3

---

## 🚀 Instalação e Execução

Siga os passos abaixo para executar o projeto localmente.

### Pré-requisitos

1.  **Python 3.9+** instalado.
2.  **FFmpeg** instalado e adicionado ao PATH do seu sistema. (Instruções de instalação em [ffmpeg.org](https://ffmpeg.org/download.html)).
3.  **Git** para clonar o repositório.

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```
    2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o ambiente
    python -m venv venv

    # Ativar no Windows
    .\venv\Scripts\activate

    # Ativar no macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    O projeto usa um arquivo `requirements.txt` para gerenciar as dependências.
    ```bash
    pip install -r requirements.txt
    ```
    > **Nota:** Se você adicionar novas bibliotecas ao projeto, não se esqueça de atualizar este arquivo com o comando: `pip freeze > requirements.txt`

### Execução

1.  Com o ambiente virtual ativado, inicie a aplicação Flask:
    ```bash
    python app.py
    ```

2.  Abra seu navegador e acesse:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📝 Lista de Melhorias Futuras (To-Do)

Este é um projeto em desenvolvimento. Algumas ideias para o futuro incluem:

* [ ] Permitir múltiplos intervalos de corte e juntá-los.
* [ ] Adicionar uma pré-visualização do vídeo com marcadores visuais na linha do tempo.
* [ ] Opção para converter o clipe cortado para outros formatos (ex: GIF).
* [ ] Implementar uma fila de processamento assíncrono (com Celery & Redis) para lidar com vídeos longos sem travar o servidor.
* [ ] Melhorar a interface do usuário (UI/UX).
* [ ] Adicionar testes automatizados.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

Feito com ❤️ por **[Seu Nome]**

* **GitHub:** [@leonardobrrs](https://github.com/leonardobrrs)
* **LinkedIn:** [Leonardo Barbosa Barros](https://www.linkedin.com/in/leonardobrrs/)
