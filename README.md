##VisionGuardHome 🛡️

Sistema de vigilância em tempo real com reconhecimento facial, gravação inteligente detecção de anomalias, upload automático e notificação.

🎯 Objetivo

Fornecer uma solução completa para monitoramento automático com visão computacional, capaz de detectar e reconhecer faces específicas, movimentações, armazenar 30 segundos antes e depois da detecção, e enviar o vídeo gravado para um endpoint via API.

🧩 Funcionalidades

Detecção e reconhecimento de faces e objetos.

Reconhecimento de pessoas com base em fotos de referência em known_faces/.

Buffer circular para armazenar os últimos 30 segundos antes da detecção.

Gravação automática de 30 segundos antes + 30 segundos depois da detecção da situação anormal.

Upload automático do vídeo capturado para o endpoint HTTP configurado.

Disparo de notificaçao para o WhatsApp

Logs detalhados para fácil monitoramento e debugging.

🚀 Pré-requisitos

Python ≥ 3.8

macOS ARM (M1/M2/M3) ou Linux/Windows

Bibliotecas:

face_recognition (com dlib)

opencv-python

imutils

requests

Instalação recomendada via venv:

bash
Copiar
Editar
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install face_recognition opencv-python imutils requests
pip install git+https://github.com/ageitgey/face_recognition_models

🗂️ Estrutura do repositório

(```)
VisionGuardHome/
├── known_faces/
│   └── faces.png        ← Fotos de referência
├── face_recognition_live.py ← Script principal
├── requirements.txt        ← Dependências (facultativo)
└── README.md               ← Este arquivo
(```)

⚙️ Como usar

Configurar rostos de referência em known_faces/.

Ative o venv:

bash
source venv/bin/activate
Execute o script:

bash

python face_recognition_live.py
O script:

Detecta "faces" no feed.

Escreve um arquivo face_detected_<timestamp>.mp4.

Faz upload automático para: http://localhost:7071/api/UploadVideo (que armazena na auzure).

Exibe logs no terminal (FPS, buffer, upload, etc.).

Pressione q dentro da janela de vídeo para encerrar o programa.

📌 Principais parâmetros

Parâmetro	Descrição	Valor padrão
buffer_seconds	Tempo antes e depois da detecção para gravar	30 segundos
fps	Frames por segundo (detectado automaticamente)	10 (fallback)

endpoint_url	URL para upload de vídeo	LocalHost:7071

Você pode alterar esses valores diretamente no script conforme suas necessidades.

🛠️ Logs e Debug
O script imprime logs como:

[DEBUG] FPS: 30

[INFO] Detected 'vinicius'. Saving...

[INFO] post_frames_remaining: ...

[INFO] Finished saving 30s after detection.

[UPLOAD] Status Code: 200

Esses logs ajudam a acompanhar o estado interno do buffer, gravação e upload.

✅ Melhoria e Considerações

Cooldown: Evitar regravação contínua se a mesma pessoa aparecer repetidamente em poucos segundos.

Interface web/live stream: Mostrar o feed em tempo real com overlay de caixas e nomes via Flask ou FastAPI.

Notificações: Enviar e-mails, SMS ou mensagens via Telegram quando houver detecção.

📞 Suporte

Se encontrar erros como falhas na instalação do dlib, face_recognition_models ou do VideoWriter, revise se:

O ambiente virtual está ativo.

Sua instalação com pip list inclui todos os pacotes necessários.

A URL do endpoint está acessível e suportando multipart/form-data.

📄 Licença

GPL

👤 Sobre o Autor

Vinicius Carvalho – desenvolvedor 👨‍💻
