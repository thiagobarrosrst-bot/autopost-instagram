#!/usr/bin/env node
/**
 * post_next.js — Lê fila.json, pega o próximo carrossel não-postado,
 * chama publish_instagram.py e marca como postado.
 *
 * Exit codes:
 *   0 = sucesso (postou) OU fila vazia (nada a fazer)
 *   1 = erro na publicação
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const FILA_PATH = path.join(ROOT, 'fila.json');
const PUBLISH_SCRIPT = path.join(__dirname, 'publish_instagram.py');

// Evita post duplicado se o mesmo horário disparar 2x seguidas.
const JANELA_MIN = 50;

function log(msg) {
  console.log(`[post_next] ${msg}`);
}

function lerFila() {
  return JSON.parse(fs.readFileSync(FILA_PATH, 'utf-8'));
}

function salvarFila(dados) {
  fs.writeFileSync(FILA_PATH, JSON.stringify(dados, null, 2) + '\n', 'utf-8');
}

function resolverImagens(images) {
  return images.map((img) => {
    if (img.startsWith('http://') || img.startsWith('https://')) return img;
    return path.isAbsolute(img) ? img : path.join(ROOT, img);
  });
}

function main() {
  if (!fs.existsSync(FILA_PATH)) {
    log(`ERRO: ${FILA_PATH} não existe.`);
    process.exit(1);
  }

  const fila = lerFila();
  const ehManual = process.env.MANUAL_POST === '1';

  const agora = Date.now();
  const postadoRecente = fila.carrosseis.some((c) => {
    if (!c.postado || !c.postadoEm) return false;
    const diffMin = (agora - new Date(c.postadoEm).getTime()) / 60000;
    return diffMin >= 0 && diffMin < JANELA_MIN;
  });
  if (postadoRecente && !ehManual) {
    log(`Já houve post nos últimos ${JANELA_MIN} min. Evitando duplicação. Saindo.`);
    process.exit(0);
  }

  const proximo = fila.carrosseis.find((c) => !c.postado);
  if (!proximo) {
    log('Fila vazia — nenhum carrossel pendente. Saindo com sucesso.');
    process.exit(0);
  }

  if (!proximo.images || proximo.images.length === 0) {
    log(`AVISO: carrossel #${proximo.id} não tem imagens. Marcando como ignorado.`);
    proximo.postado = true;
    proximo.ignorado = true;
    salvarFila(fila);
    process.exit(0);
  }

  const imagens = resolverImagens(proximo.images);
  for (const img of imagens) {
    if (!img.startsWith('http') && !fs.existsSync(img)) {
      log(`ERRO: imagem não encontrada: ${img}`);
      process.exit(1);
    }
  }

  log(`Publicando carrossel #${proximo.id}: "${proximo.titulo}"`);

  const resultado = spawnSync(
    'python3',
    [PUBLISH_SCRIPT, '--images', ...imagens, '--caption', proximo.caption],
    { encoding: 'utf-8', stdio: 'inherit', timeout: 600000 },
  );

  if (resultado.status !== 0) {
    log(`Falha na publicação (exit ${resultado.status}).`);
    process.exit(1);
  }

  proximo.postado = true;
  proximo.postadoEm = new Date().toISOString();
  salvarFila(fila);

  const pendentes = fila.carrosseis.filter((c) => !c.postado).length;
  log(`Sucesso! Carrossel #${proximo.id} marcado como postado. ${pendentes} pendente(s) na fila.`);
  process.exit(0);
}

main();
