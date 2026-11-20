from flask import Flask

app = Flask(__name__)

JOGO_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Aventura do Maguinho</title>
  <style>
    * { box-sizing: border-box; user-select: none; -webkit-user-select: none; -webkit-tap-highlight-color: transparent; }
    body {
      margin: 0;
      background: #120d1d;
      color: #f3e9ff;
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 8px;
      touch-action: manipulation;
    }
    .topo {
      width: 100%;
      max-width: 680px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 8px;
    }
    h2 { margin: 0; font-size: 16px; color: #d8b4fe; }
    canvas {
      background: linear-gradient(#1b1230, #2b1947);
      border: 3px solid #6b46c1;
      border-radius: 10px;
      width: 100%;
      max-width: 680px;
      height: auto;
      display: block;
    }
    .controles {
      margin-top: 12px;
      width: 100%;
      max-width: 680px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
    }
    .grupo {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    .grupo-acao {
      flex-direction: row-reverse;
    }
    button {
      background: #4c1d95;
      color: white;
      border: 2px solid #8b5cf6;
      border-radius: 12px;
      padding: 14px 16px;
      min-width: 56px;
      min-height: 54px;
      font-size: 16px;
      font-weight: bold;
      cursor: pointer;
      touch-action: none;
    }
    #btnReiniciar {
      padding: 6px 10px;
      min-width: auto;
      min-height: auto;
      font-size: 12px;
      border-radius: 8px;
      background: #2e1065;
    }
    button:active { background: #7c3aed; transform: scale(0.97); }
    .dica { margin-top: 8px; font-size: 12px; color: #a78bfa; text-align: center; }

    @media (max-width: 600px) {
      h2 { font-size: 14px; }
      button {
        padding: 15px 13px;
        min-width: 52px;
        min-height: 56px;
        font-size: 15px;
      }
      #btnAgachar { padding: 15px 10px; font-size: 13px; }
      #btnPular, #btnMagia { padding: 15px 12px; font-size: 14px; }
      .dica { display: none; }
    }
  </style>
</head>
<body>
  <div class="topo">
    <h2 id="tituloFase">Aventura do Maguinho — Fase 1: Floresta Dark</h2>
    <button id="btnReiniciar">↻ Reiniciar</button>
  </div>
  <canvas id="tela" width="640" height="320"></canvas>

  <div class="controles">
    <div class="grupo">
      <button id="btnEsq">◀</button>
      <button id="btnDir">▶</button>
      <button id="btnAgachar">▼ Agachar</button>
    </div>
    <div class="grupo grupo-acao">
      <button id="btnMagia">✦ Magia</button>
      <button id="btnPular">▲ Pular</button>
    </div>
  </div>

  <div class="dica">PC: Setas ou WASD para mover/pular/agachar | Espaço para magia | R para reiniciar</div>

  <script>
    const canvas = document.getElementById("tela");
    const ctx = canvas.getContext("2d");

    const chaoY = 270;
    const gravidade = 0.6;
    const larguraMundo = 1600;

    const FASES = [
      {
        numero: 1,
        nome: "Floresta Dark",
        tema: "floresta",
        plataformas: [
          { x: 240, y: 198, largura: 135, altura: 16 },
          { x: 650, y: 190, largura: 145, altura: 16 },
          { x: 1120, y: 185, largura: 150, altura: 16 }
        ],
        espinhos: [
          { x: 195, y: chaoY - 18, largura: 28, altura: 18 },
          { x: 560, y: chaoY - 18, largura: 32, altura: 18 },
          { x: 1030, y: chaoY - 18, largura: 30, altura: 18 },
          { x: 1360, y: chaoY - 18, largura: 32, altura: 18 }
        ],
        moedas: [
          { x: 140, y: chaoY - 22 },
          { x: 285, y: 175 },
          { x: 330, y: 175 },
          { x: 451, y: chaoY - 22 },
          { x: 700, y: 166 },
          { x: 745, y: 166 },
          { x: 914, y: chaoY - 22 },
          { x: 1170, y: 162 },
          { x: 1220, y: 162 },
          { x: 1445, y: chaoY - 22 }
        ],
        bichinhos: [
          { x: 485, y: chaoY - 26, largura: 30, altura: 26, vx: -1.4, minX: 465, maxX: 545, tipo: "chifrudo" },
          { x: 945, y: chaoY - 26, largura: 30, altura: 26, vx: 1.5, minX: 925, maxX: 1015, tipo: "peludo" },
          { x: 1255, y: chaoY - 26, largura: 30, altura: 26, vx: -1.6, minX: 1235, maxX: 1345, tipo: "chifrudo" }
        ]
      },
      {
        numero: 2,
        nome: "Caverna dos Cristais",
        tema: "caverna",
        plataformas: [
          { x: 210, y: 205, largura: 120, altura: 16 },
          { x: 470, y: 175, largura: 125, altura: 16 },
          { x: 780, y: 200, largura: 130, altura: 16 },
          { x: 1150, y: 170, largura: 140, altura: 16 }
        ],
        espinhos: [
          { x: 170, y: chaoY - 18, largura: 28, altura: 18 },
          { x: 390, y: chaoY - 18, largura: 34, altura: 18 },
          { x: 660, y: chaoY - 18, largura: 32, altura: 18 },
          { x: 980, y: chaoY - 18, largura: 34, altura: 18 },
          { x: 1330, y: chaoY - 18, largura: 34, altura: 18 }
        ],
        moedas: [
          { x: 250, y: 180 },
          { x: 290, y: 180 },
          { x: 510, y: 150 },
          { x: 555, y: 150 },
          { x: 820, y: 175 },
          { x: 865, y: 175 },
          { x: 1185, y: 145 },
          { x: 1235, y: 145 },
          { x: 1430, y: chaoY - 22 }
        ],
        bichinhos: [
          { x: 425, y: chaoY - 26, largura: 30, altura: 26, vx: -1.8, minX: 420, maxX: 520, tipo: "peludo" },
          { x: 705, y: chaoY - 26, largura: 30, altura: 26, vx: 1.9, minX: 695, maxX: 775, tipo: "chifrudo" },
          { x: 1030, y: chaoY - 26, largura: 30, altura: 26, vx: -2.0, minX: 1015, maxX: 1125, tipo: "peludo" },
          { x: 1380, y: chaoY - 26, largura: 30, altura: 26, vx: 2.0, minX: 1365, maxX: 1465, tipo: "chifrudo" }
        ]
      },
      {
        numero: 3,
        nome: "Ruínas do Castelo",
        tema: "ruinas",
        plataformas: [
          { x: 220, y: 195, largura: 115, altura: 16 },
          { x: 520, y: 175, largura: 120, altura: 16 },
          { x: 840, y: 190, largura: 125, altura: 16 },
          { x: 1180, y: 165, largura: 135, altura: 16 }
        ],
        espinhos: [
          { x: 180, y: chaoY - 18, largura: 30, altura: 18 },
          { x: 380, y: chaoY - 18, largura: 36, altura: 18 },
          { x: 710, y: chaoY - 18, largura: 36, altura: 18 },
          { x: 1020, y: chaoY - 18, largura: 36, altura: 18 },
          { x: 1360, y: chaoY - 18, largura: 38, altura: 18 }
        ],
        moedas: [
          { x: 255, y: 170 },
          { x: 295, y: 170 },
          { x: 560, y: 150 },
          { x: 600, y: 150 },
          { x: 880, y: 165 },
          { x: 925, y: 165 },
          { x: 1225, y: 140 },
          { x: 1270, y: 140 },
          { x: 1445, y: chaoY - 22 }
        ],
        bichinhos: [
          { x: 430, y: chaoY - 26, largura: 30, altura: 26, vx: -2.1, minX: 418, maxX: 515, tipo: "chifrudo" },
          { x: 760, y: chaoY - 26, largura: 30, altura: 26, vx: 2.2, minX: 748, maxX: 835, tipo: "peludo" },
          { x: 1070, y: chaoY - 26, largura: 30, altura: 26, vx: -2.3, minX: 1058, maxX: 1165, tipo: "chifrudo" },
          { x: 1410, y: chaoY - 26, largura: 30, altura: 26, vx: 2.3, minX: 1398, maxX: 1480, tipo: "peludo" }
        ]
      }
    ];

    const portal = { x: larguraMundo - 95, y: chaoY - 56, largura: 34, altura: 56 };

    let faseAtualIdx = 0;
    let pontos = 0;
    let mago, magias, moedas, bichinhos, cameraX, vidas, statusJogo;

    function atualizarTitulo() {
      const fase = FASES[faseAtualIdx];
      document.getElementById("tituloFase").textContent =
        `Aventura do Maguinho — Fase ${fase.numero}: ${fase.nome}`;
    }

    function carregarFase(indice, manterPontos = false) {
      faseAtualIdx = indice;
      if (!manterPontos) pontos = 0;
      const fase = FASES[faseAtualIdx];
      atualizarTitulo();

      mago = {
        x: 40,
        y: chaoY - 48,
        largura: 28,
        alturaNormal: 48,
        alturaAgachado: 28,
        altura: 48,
        vx: 0,
        vy: 0,
        velocidade: 4.4,
        forcaPulo: -12.2,
        noChao: true,
        agachado: false,
        direcao: 1,
        invulneravel: 0
      };

      cameraX = 0;
      magias = [];
      vidas = 3;
      statusJogo = "jogando";

      moedas = fase.moedas.map((m) => ({
        x: m.x,
        y: m.y,
        raio: 9,
        pega: false
      }));

      bichinhos = fase.bichinhos.map((b) => ({
        ...b,
        vivo: true
      }));
    }

    carregarFase(0, false);

    const teclas = { esq: false, dir: false, baixo: false };

    function pular() {
      if (statusJogo !== "jogando") return;
      if (mago.noChao && !mago.agachado) {
        mago.vy = mago.forcaPulo;
        mago.noChao = false;
      }
    }

    function lancarMagia() {
      if (statusJogo !== "jogando") return;
      magias.push({
        x: mago.direcao === 1 ? mago.x + mago.largura + 4 : mago.x - 10,
        y: mago.y + mago.altura * 0.45,
        vx: 7.5 * mago.direcao,
        raio: 6
      });
    }

    function acaoReiniciar() {
      if (statusJogo === "fim_jogo") {
        carregarFase(0, false);
      } else {
        carregarFase(faseAtualIdx, faseAtualIdx > 0);
      }
    }

    function colideRetangulos(a, b) {
      return (
        a.x < b.x + b.largura &&
        a.x + a.largura > b.x &&
        a.y < b.y + b.altura &&
        a.y + a.altura > b.y
      );
    }

    function tomarDano() {
      if (mago.invulneravel > 0 || statusJogo !== "jogando") return;
      vidas -= 1;
      mago.invulneravel = 60;
      mago.x = Math.max(15, mago.x - 28);
      if (vidas <= 0) {
        vidas = 0;
        statusJogo = "gameover";
      }
    }

    window.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") teclas.esq = true;
      if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") teclas.dir = true;
      if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") teclas.baixo = true;
      if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") pular();
      if (e.code === "Space") { e.preventDefault(); lancarMagia(); }
      if (e.key === "r" || e.key === "R") acaoReiniciar();
    });

    window.addEventListener("keyup", (e) => {
      if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") teclas.esq = false;
      if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") teclas.dir = false;
      if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") teclas.baixo = false;
    });

    function ligarBotaoSegurar(id, prop) {
      const btn = document.getElementById(id);
      const ativar = (e) => { e.preventDefault(); teclas[prop] = true; };
      const desativar = (e) => { e.preventDefault(); teclas[prop] = false; };
      btn.addEventListener("mousedown", ativar);
      btn.addEventListener("mouseup", desativar);
      btn.addEventListener("mouseleave", desativar);
      btn.addEventListener("touchstart", ativar, { passive: false });
      btn.addEventListener("touchend", desativar, { passive: false });
      btn.addEventListener("touchcancel", desativar, { passive: false });
    }

    function ligarBotaoToque(id, acao) {
      const btn = document.getElementById(id);
      btn.addEventListener("touchstart", (e) => {
        e.preventDefault();
        acao();
      }, { passive: false });
      btn.addEventListener("click", (e) => {
        if (e.detail === 0) return;
        acao();
      });
    }

    ligarBotaoSegurar("btnEsq", "esq");
    ligarBotaoSegurar("btnDir", "dir");
    ligarBotaoSegurar("btnAgachar", "baixo");

    ligarBotaoToque("btnPular", pular);
    ligarBotaoToque("btnMagia", lancarMagia);
    document.getElementById("btnReiniciar").addEventListener("click", acaoReiniciar);

    function atualizar() {
      if (statusJogo !== "jogando") return;
      const fase = FASES[faseAtualIdx];

      if (mago.invulneravel > 0) mago.invulneravel -= 1;

      if (teclas.baixo && mago.noChao) {
        if (!mago.agachado) {
          mago.agachado = true;
          mago.y += (mago.alturaNormal - mago.alturaAgachado);
          mago.altura = mago.alturaAgachado;
        }
      } else if (mago.agachado) {
        mago.agachado = false;
        mago.y -= (mago.alturaNormal - mago.alturaAgachado);
        mago.altura = mago.alturaNormal;
      }

      mago.vx = 0;
      if (!mago.agachado) {
        if (teclas.esq) { mago.vx = -mago.velocidade; mago.direcao = -1; }
        if (teclas.dir) { mago.vx = mago.velocidade; mago.direcao = 1; }
      }
      mago.x += mago.vx;

      if (mago.x < 10) mago.x = 10;
      if (mago.x + mago.largura > larguraMundo - 10) {
        mago.x = larguraMundo - 10 - mago.largura;
      }

      mago.vy += gravidade;
      mago.y += mago.vy;
      mago.noChao = false;

      const pesAntes = mago.y + mago.altura - mago.vy;
      for (const plat of fase.plataformas) {
        const dentroX = mago.x + mago.largura > plat.x && mago.x < plat.x + plat.largura;
        if (dentroX && pesAntes <= plat.y && mago.y + mago.altura >= plat.y && mago.vy >= 0) {
          mago.y = plat.y - mago.altura;
          mago.vy = 0;
          mago.noChao = true;
        }
      }

      if (mago.y + mago.altura >= chaoY) {
        mago.y = chaoY - mago.altura;
        mago.vy = 0;
        mago.noChao = true;
      }

      for (const esp of fase.espinhos) {
        if (colideRetangulos(mago, esp)) {
          tomarDano();
        }
      }

      for (const m of moedas) {
        if (!m.pega) {
          const dx = (mago.x + mago.largura / 2) - m.x;
          const dy = (mago.y + mago.altura / 2) - m.y;
          if (Math.hypot(dx, dy) < m.raio + 16) {
            m.pega = true;
            pontos += 10;
          }
        }
      }

      for (const b of bichinhos) {
        if (!b.vivo) continue;
        b.x += b.vx;
        if (b.x <= b.minX) {
          b.x = b.minX;
          b.vx = Math.abs(b.vx);
        } else if (b.x + b.largura >= b.maxX) {
          b.x = b.maxX - b.largura;
          b.vx = -Math.abs(b.vx);
        }

        if (colideRetangulos(mago, b)) {
          tomarDano();
        }
      }

      for (let i = magias.length - 1; i >= 0; i--) {
        magias[i].x += magias[i].vx;
        let acertou = false;

        for (const b of bichinhos) {
          if (!b.vivo) continue;
          const hitBoxMagia = {
            x: magias[i].x - magias[i].raio,
            y: magias[i].y - magias[i].raio,
            largura: magias[i].raio * 2,
            altura: magias[i].raio * 2
          };
          if (colideRetangulos(hitBoxMagia, b)) {
            b.vivo = false;
            pontos += 25;
            acertou = true;
            break;
          }
        }

        if (acertou || magias[i].x < cameraX - 20 || magias[i].x > cameraX + canvas.width + 20) {
          magias.splice(i, 1);
        }
      }

      if (colideRetangulos(mago, portal)) {
        if (faseAtualIdx < FASES.length - 1) {
          carregarFase(faseAtualIdx + 1, true);
          return;
        } else {
          statusJogo = "fim_jogo";
        }
      }

      const alvoCamera = mago.x - canvas.width * 0.35;
      const maxCamera = larguraMundo - canvas.width;
      cameraX = Math.max(0, Math.min(maxCamera, alvoCamera));
    }

    function desenharEstrelinha(x, y, raio) {
      ctx.save();
      ctx.translate(x, y);
      ctx.fillStyle = "#fef9c3";
      ctx.beginPath();
      ctx.moveTo(0, -raio);
      ctx.quadraticCurveTo(0, 0, raio, 0);
      ctx.quadraticCurveTo(0, 0, 0, raio);
      ctx.quadraticCurveTo(0, 0, -raio, 0);
      ctx.quadraticCurveTo(0, 0, 0, -raio);
      ctx.fill();
      ctx.restore();
    }

    function desenharEspeto(esp) {
      const qtd = 3;
      const passoX = esp.largura / qtd;

      for (let i = 0; i < qtd; i++) {
        const x0 = esp.x + i * passoX;
        const xMeio = x0 + passoX / 2;
        const x1 = x0 + passoX;
        const topoY = esp.y + (i % 2 === 1 ? 2 : 0);

        const grad = ctx.createLinearGradient(xMeio, topoY, xMeio, chaoY);
        grad.addColorStop(0, "#fda4af");
        grad.addColorStop(0.35, "#e11d48");
        grad.addColorStop(1, "#4c0519");

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.moveTo(x0, chaoY);
        ctx.lineTo(xMeio, topoY);
        ctx.lineTo(x1, chaoY);
        ctx.closePath();
        ctx.fill();

        ctx.strokeStyle = "#fecdd3";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(xMeio, topoY + 1);
        ctx.lineTo(x0 + 2, chaoY - 1);
        ctx.stroke();
      }
    }

    function desenharCenario() {
      const fase = FASES[faseAtualIdx];

      const ceu = ctx.createLinearGradient(0, 0, 0, chaoY);
      if (fase.tema === "floresta") {
        ceu.addColorStop(0, "#070510");
        ceu.addColorStop(0.6, "#120a24");
        ceu.addColorStop(1, "#1d1033");
      } else if (fase.tema === "caverna") {
        ceu.addColorStop(0, "#060b14");
        ceu.addColorStop(0.6, "#0c192c");
        ceu.addColorStop(1, "#152238");
      } else {
        ceu.addColorStop(0, "#0d0612");
        ceu.addColorStop(0.6, "#210c26");
        ceu.addColorStop(1, "#331230");
      }
      ctx.fillStyle = ceu;
      ctx.fillRect(0, 0, canvas.width, chaoY);

      const estrelas = [
        [45, 35, 1.4], [110, 70, 1.1], [175, 30, 1.6], [230, 85, 1.0],
        [310, 42, 1.5], [385, 65, 1.2], [455, 28, 1.4], [595, 45, 1.3],
        [615, 95, 1.0], [85, 120, 1.1], [275, 115, 1.2], [490, 105, 1.1]
      ];
      const brilho = 0.65 + Math.sin(Date.now() * 0.003) * 0.25;
      for (const [ex, ey, er] of estrelas) {
        const px = ((ex - cameraX * 0.15) % canvas.width + canvas.width) % canvas.width;
        ctx.fillStyle = fase.tema === "caverna"
          ? `rgba(125, 211, 252, ${brilho * 0.85})`
          : `rgba(233, 213, 255, ${brilho})`;
        ctx.beginPath();
        ctx.arc(px, ey, er, 0, Math.PI * 2);
        ctx.fill();
      }

      if (fase.tema !== "caverna") {
        ctx.fillStyle = fase.tema === "ruinas" ? "#fbcfe8" : "#e2d9f3";
        ctx.beginPath();
        ctx.arc(540, 62, 20, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.save();
      ctx.translate(-cameraX, 0);

      if (fase.tema === "floresta") {
        for (let ax = 25; ax < larguraMundo - 40; ax += 68) {
          const w = 22 + ((ax * 7) % 14);
          const h = 95 + ((ax * 13) % 62);
          const topoY = chaoY - h;

          ctx.fillStyle = "#140e1f";
          ctx.fillRect(ax - w * 0.14, topoY + h * 0.35, w * 0.28, h * 0.65);

          ctx.fillStyle = "#191129";
          ctx.beginPath();
          ctx.moveTo(ax, topoY);
          ctx.lineTo(ax - w * 0.65, topoY + h * 0.45);
          ctx.lineTo(ax + w * 0.65, topoY + h * 0.45);
          ctx.closePath();
          ctx.fill();

          ctx.beginPath();
          ctx.moveTo(ax, topoY + h * 0.22);
          ctx.lineTo(ax - w * 0.8, topoY + h * 0.72);
          ctx.lineTo(ax + w * 0.8, topoY + h * 0.72);
          ctx.closePath();
          ctx.fill();
        }
      } else if (fase.tema === "caverna") {
        for (let rx = 30; rx < larguraMundo - 30; rx += 64) {
          const h = 28 + ((rx * 11) % 36);
          ctx.fillStyle = "#0b1524";
          ctx.beginPath();
          ctx.moveTo(rx - 14, 0);
          ctx.lineTo(rx + 14, 0);
          ctx.lineTo(rx, h);
          ctx.closePath();
          ctx.fill();

          if (rx % 128 === 30) {
            ctx.fillStyle = "rgba(56, 189, 248, 0.32)";
            ctx.beginPath();
            ctx.moveTo(rx + 20, chaoY);
            ctx.lineTo(rx + 28, chaoY - 26);
            ctx.lineTo(rx + 36, chaoY);
            ctx.closePath();
            ctx.fill();
          }
        }
      } else {
        for (let cx = 40; cx < larguraMundo - 50; cx += 95) {
          const h = 75 + ((cx * 9) % 55);
          const topoY = chaoY - h;
          ctx.fillStyle = "#26102b";
          ctx.fillRect(cx, topoY, 24, h);
          ctx.fillRect(cx - 4, topoY, 32, 8);
          ctx.fillStyle = "#17091b";
          ctx.fillRect(cx + 8, topoY + 18, 8, 6);
        }
      }

      const nevoa = ctx.createLinearGradient(0, chaoY - 35, 0, chaoY);
      nevoa.addColorStop(0, "rgba(30, 18, 54, 0)");
      nevoa.addColorStop(1, fase.tema === "caverna" ? "rgba(14, 116, 144, 0.16)" : "rgba(76, 29, 149, 0.16)");
      ctx.fillStyle = nevoa;
      ctx.fillRect(0, chaoY - 35, larguraMundo, 35);

      if (fase.tema === "floresta") {
        ctx.fillStyle = "#17111e";
        ctx.fillRect(0, chaoY, larguraMundo, canvas.height - chaoY);
        ctx.fillStyle = "#291d38";
        ctx.fillRect(0, chaoY + 8, larguraMundo, 10);
        ctx.fillStyle = "#2d2a4a";
        ctx.fillRect(0, chaoY, larguraMundo, 6);
        ctx.fillStyle = "#3b3561";
        for (let mx = 12; mx < larguraMundo - 12; mx += 28) {
          ctx.fillRect(mx, chaoY - 3, 10, 3);
        }
      } else if (fase.tema === "caverna") {
        ctx.fillStyle = "#09111d";
        ctx.fillRect(0, chaoY, larguraMundo, canvas.height - chaoY);
        ctx.fillStyle = "#13233a";
        ctx.fillRect(0, chaoY + 8, larguraMundo, 10);
        ctx.fillStyle = "#1e3a5f";
        ctx.fillRect(0, chaoY, larguraMundo, 6);
        ctx.fillStyle = "#38bdf8";
        for (let mx = 18; mx < larguraMundo - 18; mx += 44) {
          ctx.fillRect(mx, chaoY + 2, 8, 2);
        }
      } else {
        ctx.fillStyle = "#180b1c";
        ctx.fillRect(0, chaoY, larguraMundo, canvas.height - chaoY);
        ctx.fillStyle = "#2d1433";
        ctx.fillRect(0, chaoY + 8, larguraMundo, 10);
        ctx.fillStyle = "#4c1d57";
        ctx.fillRect(0, chaoY, larguraMundo, 6);
        ctx.fillStyle = "#6b21a8";
        for (let mx = 10; mx < larguraMundo - 10; mx += 32) {
          ctx.fillRect(mx, chaoY + 11, 18, 3);
        }
      }

      for (const plat of fase.plataformas) {
        ctx.fillStyle = fase.tema === "caverna" ? "#162942" : "#2e2042";
        ctx.fillRect(plat.x, plat.y, plat.largura, plat.altura);
        ctx.fillStyle = fase.tema === "caverna" ? "#38bdf8" : "#5b3e7a";
        ctx.fillRect(plat.x, plat.y, plat.largura, 3);
      }

      for (const esp of fase.espinhos) {
        desenharEspeto(esp);
      }

      ctx.fillStyle = "#38bdf8";
      ctx.beginPath();
      ctx.ellipse(portal.x + portal.largura / 2, portal.y + portal.altura / 2, portal.largura / 2, portal.altura / 2, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#e0f2fe";
      ctx.beginPath();
      ctx.ellipse(portal.x + portal.largura / 2, portal.y + portal.altura / 2, portal.largura * 0.25, portal.altura * 0.35, 0, 0, Math.PI * 2);
      ctx.fill();
    }

    function desenharMoedas() {
      for (const m of moedas) {
        if (m.pega) continue;
        ctx.fillStyle = "#facc15";
        ctx.beginPath();
        ctx.arc(m.x, m.y, m.raio, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = "#fef08a";
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }
    }

    function desenharBichinhos() {
      const balanco = Math.sin(Date.now() * 0.01) * 2;

      for (const b of bichinhos) {
        if (!b.vivo) continue;
        const bx = b.x;
        const by = b.y;
        const bw = b.largura;
        const bh = b.altura;
        const cx = bx + bw / 2;
        const dir = b.vx >= 0 ? 1 : -1;

        if (b.tipo === "chifrudo") {
          ctx.fillStyle = "#f43f5e";
          ctx.beginPath();
          ctx.moveTo(cx - 8, by + 8);
          ctx.lineTo(cx - 13, by - 3);
          ctx.lineTo(cx - 3, by + 5);
          ctx.closePath();
          ctx.fill();

          ctx.beginPath();
          ctx.moveTo(cx + 8, by + 8);
          ctx.lineTo(cx + 13, by - 3);
          ctx.lineTo(cx + 3, by + 5);
          ctx.closePath();
          ctx.fill();

          ctx.fillStyle = "#be185d";
          ctx.beginPath();
          ctx.moveTo(bx + 2, by + bh);
          ctx.quadraticCurveTo(bx - 2, by + bh * 0.35, cx, by + 5);
          ctx.quadraticCurveTo(bx + bw + 2, by + bh * 0.35, bx + bw - 2, by + bh);
          ctx.lineTo(bx + bw * 0.72, by + bh - 4 + balanco * 0.4);
          ctx.lineTo(cx, by + bh);
          ctx.lineTo(bx + bw * 0.28, by + bh - 4 - balanco * 0.4);
          ctx.closePath();
          ctx.fill();

          ctx.fillStyle = "#fef08a";
          ctx.beginPath();
          ctx.arc(cx - 5 + dir * 2, by + bh * 0.52, 2.7, 0, Math.PI * 2);
          ctx.arc(cx + 5 + dir * 2, by + bh * 0.52, 2.7, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = "#1f0716";
          ctx.fillRect(cx - 5.8 + dir * 2.5, by + bh * 0.52 - 0.8, 1.6, 1.8);
          ctx.fillRect(cx + 4.2 + dir * 2.5, by + bh * 0.52 - 0.8, 1.6, 1.8);
        } else {
          ctx.fillStyle = "#65a30d";
          ctx.beginPath();
          ctx.moveTo(bx + 2, by + bh);
          ctx.lineTo(bx, by + bh * 0.55);
          ctx.lineTo(bx + 6, by + 6);
          ctx.lineTo(cx - 2, by + 11);
          ctx.lineTo(cx + 3, by + 2);
          ctx.lineTo(bx + bw - 6, by + 7);
          ctx.lineTo(bx + bw, by + bh * 0.55);
          ctx.lineTo(bx + bw - 2, by + bh);
          ctx.lineTo(bx + bw * 0.75, by + bh - 3 - balanco * 0.4);
          ctx.lineTo(cx, by + bh);
          ctx.lineTo(bx + bw * 0.25, by + bh - 3 + balanco * 0.4);
          ctx.closePath();
          ctx.fill();

          ctx.fillStyle = "#fef9c3";
          ctx.beginPath();
          ctx.arc(cx - 3 + dir * 3, by + bh * 0.55, 3.2, 0, Math.PI * 2);
          ctx.arc(cx + 6 + dir * 3, by + bh * 0.5, 2.2, 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = "#1a2e05";
          ctx.beginPath();
          ctx.arc(cx - 2.5 + dir * 3.5, by + bh * 0.55, 1.3, 0, Math.PI * 2);
          ctx.arc(cx + 6.5 + dir * 3.5, by + bh * 0.5, 1.0, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }

    function desenharMago() {
      if (mago.invulneravel > 0 && Math.floor(mago.invulneravel / 4) % 2 === 0) {
        return;
      }

      const cx = mago.x + mago.largura / 2;
      const andando = (teclas.esq || teclas.dir) && mago.noChao && !mago.agachado;
      const passo = andando ? Math.sin(Date.now() * 0.015) * 3 : 0;

      ctx.fillStyle = "rgba(0, 0, 0, 0.25)";
      ctx.beginPath();
      ctx.ellipse(cx, mago.y + mago.altura + 1, mago.largura * 0.55, 4, 0, 0, Math.PI * 2);
      ctx.fill();

      if (!mago.agachado) {
        ctx.fillStyle = "#5b21b6";
        ctx.beginPath();
        ctx.arc(cx - 6, mago.y + mago.altura - 3 + passo, 5, 0, Math.PI * 2);
        ctx.arc(cx + 6, mago.y + mago.altura - 3 - passo, 5, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.fillStyle = "#7c3aed";
      ctx.beginPath();
      ctx.moveTo(mago.x + 3, mago.y + mago.altura - 4);
      ctx.quadraticCurveTo(cx, mago.y + 8, mago.x + mago.largura - 3, mago.y + mago.altura - 4);
      ctx.quadraticCurveTo(cx, mago.y + mago.altura + 2, mago.x + 3, mago.y + mago.altura - 4);
      ctx.fill();

      ctx.fillStyle = "#c4b5fd";
      ctx.fillRect(mago.x + 4, mago.y + mago.altura * 0.62, mago.largura - 8, 4);

      const cabecaY = mago.y + (mago.agachado ? 13 : 14);
      const raioCabeca = mago.agachado ? 10 : 12;
      ctx.fillStyle = "#fde68a";
      ctx.beginPath();
      ctx.arc(cx, cabecaY, raioCabeca, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#f472b6";
      const offsetOlhar = mago.direcao * 2.5;
      ctx.beginPath();
      ctx.arc(cx - 5 + offsetOlhar, cabecaY + 2.5, 2.5, 0, Math.PI * 2);
      ctx.arc(cx + 5 + offsetOlhar, cabecaY + 2.5, 2.5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#1e1b4b";
      ctx.beginPath();
      ctx.arc(cx - 4 + offsetOlhar, cabecaY - 0.5, 2.3, 0, Math.PI * 2);
      ctx.arc(cx + 4 + offsetOlhar, cabecaY - 0.5, 2.3, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(cx - 4.7 + offsetOlhar, cabecaY - 1.3, 0.9, 0, Math.PI * 2);
      ctx.arc(cx + 3.3 + offsetOlhar, cabecaY - 1.3, 0.9, 0, Math.PI * 2);
      ctx.fill();

      const topoChapeuY = mago.agachado ? mago.y - 8 : mago.y - 21;
      const pontaChapeuX = cx + mago.direcao * 5;
      const baseChapeuY = cabecaY - raioCabeca + 3;

      const gradChapeu = ctx.createLinearGradient(cx, topoChapeuY, cx, baseChapeuY);
      gradChapeu.addColorStop(0, "#4f46e5");
      gradChapeu.addColorStop(1, "#5b21b6");

      ctx.fillStyle = gradChapeu;
      ctx.beginPath();
      ctx.moveTo(cx - 15, baseChapeuY);
      ctx.quadraticCurveTo(cx, baseChapeuY - 3, cx + 15, baseChapeuY);
      ctx.lineTo(pontaChapeuX, topoChapeuY);
      ctx.lineTo(cx - 15, baseChapeuY);
      ctx.closePath();
      ctx.fill();

      ctx.strokeStyle = "#ddd6fe";
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(cx - 10, baseChapeuY - 1.5);
      ctx.lineTo(cx + 10, baseChapeuY - 1.5);
      ctx.stroke();

      const pisca = 0.8 + Math.sin(Date.now() * 0.008) * 0.2;
      desenharEstrelinha(cx - 4, baseChapeuY - 7, 2.8 * pisca);
      desenharEstrelinha(cx + 3, baseChapeuY - 11, 2.3 * pisca);
      desenharEstrelinha(pontaChapeuX - mago.direcao * 2, topoChapeuY + 6, 2.0 * pisca);

      const cajadoX = mago.direcao === 1 ? mago.x + mago.largura + 2 : mago.x - 2;
      const baseCajadoY = mago.y + mago.altura - 12;
      const topoCajadoY = mago.y + 13;
      ctx.strokeStyle = "#b45309";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(cajadoX, baseCajadoY);
      ctx.lineTo(cajadoX, topoCajadoY);
      ctx.stroke();

      ctx.fillStyle = "#f3e8ff";
      ctx.beginPath();
      ctx.arc(cajadoX, topoCajadoY - 2, 4.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#d8b4fe";
      ctx.lineWidth = 1.2;
      ctx.stroke();
    }

    function desenharMagias() {
      for (const m of magias) {
        ctx.fillStyle = "#e9d5ff";
        ctx.beginPath();
        ctx.arc(m.x, m.y, m.raio, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    function desenharHUD() {
      ctx.restore();

      ctx.fillStyle = "#f3e9ff";
      ctx.font = "bold 14px Arial";
      ctx.fillText(`Pontos: ${pontos}`, 16, 24);
      ctx.fillText(`Vidas: ${"♥".repeat(vidas)}`, 120, 24);

      const progresso = Math.min(100, Math.round((mago.x / (portal.x - 40)) * 100));
      ctx.fillText(`Fase ${faseAtualIdx + 1}/3 (${progresso}%)`, 225, 24);

      if (statusJogo === "fim_jogo") {
        ctx.fillStyle = "rgba(10, 6, 20, 0.82)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#d8b4fe";
        ctx.font = "bold 24px Arial";
        ctx.textAlign = "center";
        ctx.fillText("Você concluiu as 3 fases!", canvas.width / 2, 138);
        ctx.font = "16px Arial";
        ctx.fillStyle = "#f3e9ff";
        ctx.fillText(`Pontuação total: ${pontos}`, canvas.width / 2, 168);
        ctx.font = "14px Arial";
        ctx.fillStyle = "#c4b5fd";
        ctx.fillText("Aperte R ou Reiniciar para jogar novamente", canvas.width / 2, 196);
        ctx.textAlign = "left";
      } else if (statusJogo === "gameover") {
        ctx.fillStyle = "rgba(10, 6, 20, 0.78)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#fda4af";
        ctx.font = "bold 24px Arial";
        ctx.textAlign = "center";
        ctx.fillText("O maguinho caiu!", canvas.width / 2, 145);
        ctx.font = "16px Arial";
        ctx.fillStyle = "#f3e9ff";
        ctx.fillText("Aperte R ou Reiniciar para tentar de novo", canvas.width / 2, 178);
        ctx.textAlign = "left";
      }
    }

    function loop() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      desenharCenario();
      atualizar();
      desenharMoedas();
      desenharBichinhos();
      desenharMago();
      desenharMagias();
      desenharHUD();
      requestAnimationFrame(loop);
    }

    loop();
  </script>
</body>
</html>
"""

@app.route("/")
def inicio():
    return JOGO_HTML

if __name__ == "__main__":
    app.run(debug=True)