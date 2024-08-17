# Análise Avançada de Vídeos com MediaPipe e OpenCV

## Visão Geral

Este projeto é uma solução avançada para a análise e comparação de vídeos, focada em movimentos corporais. Utilizando **MediaPipe** para detecção de pontos-chave e **OpenCV** para visualização, o código é capaz de processar dois vídeos simultaneamente, destacar as diferenças nas trajetórias dos pontos-chave e fornecer uma visualização clara e útil para análise de movimentos.

![Visualização do Projeto](https://your-image-url.com/preview.png)

## Funcionalidades

- **Detecção Precisa de Pontos-Chave**: Utiliza MediaPipe para identificar e rastrear pontos-chave do corpo em cada frame dos vídeos.
- **Comparação de Trajetórias**: Desenha linhas que mostram as diferenças entre os pontos-chave dos dois vídeos, facilitando a análise das variações de movimento.
- **Visualização Interativa**: Mostra os vídeos com as diferenças destacadas e salva os vídeos processados com as análises visuais.
- **Saída de Vídeo**: Gera vídeos de saída com as diferenças e pontos-chave destacados, prontos para revisão e compartilhamento.

## Benefícios

- **Análise Profunda**: Ideal para treinadores, analistas e pesquisadores que precisam comparar técnicas ou movimentos entre vídeos.
- **Visualização Clara**: As diferenças são claramente destacadas, facilitando a identificação de áreas de melhoria ou variações entre os vídeos.
- **Facilidade de Uso**: Simples de configurar e executar, com dependências bem definidas e instruções claras.

## Demonstração

Aqui estão alguns exemplos de vídeos processados:

- [Vídeo 1 com Diferenças](https://your-video-url.com/video1.mp4)
- [Vídeo 2 com Diferenças](https://your-video-url.com/video2.mp4)

## Como Usar

1. **Clone o Repositório**:

   ```bash
   git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
   cd NOME_DO_REPOSITORIO
Instale as Dependências:

bash
Copiar código
pip install opencv-python mediapipe numpy
Prepare seus Vídeos:

Coloque os vídeos a serem comparados no diretório do projeto, nomeando-os como video1.mp4 e video2.mp4, ou ajuste o código para usar outros nomes.
Execute o Script:

bash
Copiar código
python main.py
Os vídeos resultantes com as análises serão salvos como output_video1.mp4 e output_video2.mp4.
