#!/usr/bin/env python3
"""
week1_specs.py — Gera os 7 carrosséis do dia 2 ao dia 8 (dia 1 = painel
financeiro, já na fila) e monta a fila.json completa da semana.

Todos seguem a estrutura fixa de 8 slides e o DNA documentado em
design/LAYOUT.md: foto real full-bleed no slide 1 (tag em pílula sólida +
card de prova), slide 2 de autoridade (case próprio, nunca terceiro),
3 prompts práticos e copiáveis, resultado, CTA com palavra específica.

Uso:
    python3 design/week1_specs.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build_carousel import build_html, export_slides  # noqa: E402
import asyncio

PHOTO = "assets/thiago_perfil.jpg"

SPECS = [
    # DIA 2 — Atendimento no WhatsApp (já validado antes, refinado)
    {
        "slug": "prompt-atendimento-whatsapp",
        "caption": (
            "Você demora 20 minutos pra responder e o cliente já comprou no concorrente.\n\n"
            "3 prompts prontos resolvem isso hoje — cola no ChatGPT ou Claude e adapta pro seu negócio em 2 minutos.\n\n"
            "Comenta \"ATENDIMENTO\" que eu te mando os 3 completos no direct 👇\n\n"
            "#inteligenciaartificial #atendimentoaocliente #automacao #chatgpt #pequenosnegocios"
        ),
        "slides": [
            {"kind": "capa", "use_photo": False, "tag": "CASE PRÓPRIO",
             "headline": ["VOCÊ DEMORA 20 MIN", "PRA RESPONDER.", "O CLIENTE SOME"],
             "subtitle": "3 prompts prontos resolvem isso hoje.",
             "proof": {"type": "checklist", "label": "WHATSAPP BUSINESS", "items": [
                 [True, "Responder dúvida de preço"],
                 [True, "Follow-up de carrinho parado"],
                 [False, "Resposta pra reclamação"],
             ]}},
            {"kind": "capa2", "tag": "O QUE MUDOU",
             "headline": ["PAREI DE PARAR", "TUDO PRA RESPONDER", "PERGUNTA REPETIDA"],
             "body": "3 prompts fixos resolvem 80% do que chega no meu WhatsApp.",
             "stat_items": [["80%", "das perguntas são repetidas"], ["3", "prompts cobrem quase tudo"], ["0", "app novo pra instalar"]]},
            {"kind": "dor", "tag": "O PROBLEMA", "headline": ["A MESMA PERGUNTA,", "TODO DIA"],
             "pain_lines": [
                 "Você para o que está fazendo pra responder preço",
                 "O cliente some e você nem sabe se comprou em outro lugar",
                 "Reclamação chega e a resposta sai emocional, não estratégica",
             ]},
            {"kind": "prompt", "tag": "PROMPT 1 DE 3", "headline": ["RESPONDER PREÇO", "SEM PARECER ROBÔ"],
             "body": "Cole isso no ChatGPT ou Claude:",
             "prompt": "\"Aja como atendente da minha loja de [nicho]. Cliente perguntou o preço de [produto]. Responda de forma calorosa, cite o valor R$[valor] e ofereça 1 produto complementar.\""},
            {"kind": "prompt", "tag": "PROMPT 2 DE 3", "headline": ["FOLLOW-UP DE", "CARRINHO PARADO"],
             "body": "Prompt pronto:",
             "prompt": "\"Escreva uma mensagem casual perguntando se o cliente ainda tem interesse em [produto], sem soar insistente, com 1 gatilho de urgência real.\""},
            {"kind": "prompt", "tag": "PROMPT 3 DE 3", "headline": ["RESPOSTA PRA", "RECLAMAÇÃO"],
             "body": "Prompt pronto:",
             "prompt": "\"Reescreva essa reclamação do cliente [colar reclamação] como resposta empática, assumindo o erro quando for o caso, e oferecendo solução em até 2 frases.\""},
            {"kind": "resultado", "tag": "O RESULTADO", "headline": ["O QUE MUDA NA", "PRÁTICA"],
             "body": "Com os 3 prompts rodando no seu WhatsApp:",
             "items": [["⚡", "Resposta em segundos", "Sem parar o que você está fazendo"],
                       ["✅", "Tom consistente", "Sempre no seu jeito de atender"],
                       ["💰", "Menos venda perdida", "Follow-up automático de quem sumiu"]]},
            {"kind": "cta", "cta_word": "ATENDIMENTO"},
        ],
    },
    # DIA 3 — Proposta comercial rápida (vender mais)
    {
        "slug": "prompt-proposta-comercial",
        "caption": (
            "Eu levava 40 minutos pra montar uma proposta comercial. Agora levo 4.\n\n"
            "O prompt que uso pra transformar uma conversa de WhatsApp numa proposta profissional em minutos.\n\n"
            "Comenta \"PROPOSTA\" que eu te mando o prompt completo no direct 👇\n\n"
            "#inteligenciaartificial #vendas #propostacomercial #ia #automacao"
        ),
        "slides": [
            {"kind": "capa", "use_photo": False, "tag": "CASE PRÓPRIO",
             "headline": ["MINHA PROPOSTA", "LEVAVA 40 MIN.", "AGORA LEVA 4"],
             "subtitle": "O prompt que fecha o texto pra mim.",
             "proof": {"type": "stats", "label": "PROPOSTA COMERCIAL", "items": [
                 ["Cliente", "Loja XPTO"], ["Valor", "R$ 3.400"], ["Prazo", "5 dias úteis"],
             ]}},
            {"kind": "capa2", "tag": "O QUE MUDOU",
             "headline": ["A DEMORA NÃO ERA", "FALTA DE VONTADE.", "ERA FALTA DE MODELO"],
             "body": "Com um prompt fixo, a proposta sai formatada e convincente na hora.",
             "stat_items": [["4 MIN", "tempo médio agora"], ["0", "modelo pra abrir e editar"], ["100%", "personalizada pro cliente"]]},
            {"kind": "dor", "tag": "O PROBLEMA", "headline": ["VOCÊ DEIXA VENDA", "NA MESA"],
             "pain_lines": [
                 "Cliente pede orçamento e você demora, ele já foi no concorrente",
                 "Proposta feita correndo sai com erro ou informação faltando",
                 "Cada proposta parece diferente, sem cara de profissional",
             ]},
            {"kind": "prompt", "tag": "PASSO 1 DE 3", "headline": ["ESTRUTURAR A", "PROPOSTA"],
             "body": "Cole isso com os dados da conversa:",
             "prompt": "\"Aja como consultor comercial. Com base nessa conversa com o cliente [colar conversa], monte uma proposta comercial profissional: escopo, valor, prazo e forma de pagamento. Tom confiante, sem ser robótico.\""},
            {"kind": "prompt", "tag": "PASSO 2 DE 3", "headline": ["QUEBRAR OBJEÇÃO", "DE PREÇO"],
             "body": "Prompt pronto:",
             "prompt": "\"O cliente achou o valor alto. Escreva uma resposta que reforça o valor entregue sem baixar o preço, oferecendo no máximo 1 condição de pagamento facilitada.\""},
            {"kind": "prompt", "tag": "PASSO 3 DE 3", "headline": ["FOLLOW-UP DE", "PROPOSTA ENVIADA"],
             "body": "Cole isso 2 dias depois:",
             "prompt": "\"Escreva uma mensagem de follow-up pra proposta enviada há 2 dias, sem soar desesperado, perguntando se ficou alguma dúvida.\""},
            {"kind": "resultado", "tag": "O RESULTADO", "headline": ["O QUE MUDA NA", "PRÁTICA"],
             "body": "Com os 3 prompts rodando nas suas vendas:",
             "items": [["⚡", "Proposta em minutos", "Antes de o cliente esfriar"],
                       ["✅", "Padrão profissional", "Toda proposta com a mesma qualidade"],
                       ["📈", "Mais fechamento", "Objeção de preço tratada certo"]]},
            {"kind": "cta", "cta_word": "PROPOSTA"},
        ],
    },
    # DIA 4 — Negociação com fornecedor (reduzir custo)
    {
        "slug": "prompt-negociar-fornecedor",
        "caption": (
            "Consegui 12% de desconto do meu fornecedor com uma mensagem que a IA escreveu.\n\n"
            "O prompt que uso pra negociar preço sem parecer que estou implorando.\n\n"
            "Comenta \"FORNECEDOR\" que eu te mando o prompt completo no direct 👇\n\n"
            "#inteligenciaartificial #reducaodecustos #negociacao #ia #gestao"
        ),
        "slides": [
            {"kind": "capa", "use_photo": False, "tag": "CASE PRÓPRIO",
             "headline": ["CONSEGUI 12%", "DE DESCONTO COM", "UMA MENSAGEM"],
             "subtitle": "A IA escreveu, eu só mandei.",
             "proof": {"type": "stats", "label": "NEGOCIAÇÃO FORNECEDOR", "items": [
                 ["Antes", "R$ 8.200/mês"], ["Depois", "R$ 7.210/mês"], ["Economia", "12%"],
             ]}},
            {"kind": "capa2", "tag": "O QUE MUDOU",
             "headline": ["NEGOCIAR NÃO É", "SOBRE PEDIR.", "É SOBRE ARGUMENTAR"],
             "body": "O prompt monta o argumento certo — volume, prazo, concorrência — antes de eu mandar.",
             "stat_items": [["12%", "de desconto conseguido"], ["1", "mensagem, sem ida e volta"], ["0", "constrangimento"]]},
            {"kind": "dor", "tag": "O PROBLEMA", "headline": ["VOCÊ PAGA O MESMO", "PREÇO HÁ ANOS"],
             "pain_lines": [
                 "Você não sabe como pedir desconto sem parecer chato",
                 "Fornecedor sobe preço e você só aceita",
                 "Falta argumento na hora de negociar prazo ou condição",
             ]},
            {"kind": "prompt", "tag": "PASSO 1 DE 3", "headline": ["PEDIR DESCONTO", "COM ARGUMENTO"],
             "body": "Cole isso com os dados do seu contrato:",
             "prompt": "\"Aja como negociador comercial. Sou cliente há [tempo] do fornecedor [nome], compro [volume] por mês. Escreva uma mensagem pedindo desconto de [X]%, citando fidelidade e volume, sem soar ameaçador.\""},
            {"kind": "prompt", "tag": "PASSO 2 DE 3", "headline": ["RESPONDER UM", "'NÃO' INICIAL"],
             "body": "Prompt pronto:",
             "prompt": "\"O fornecedor recusou o desconto. Escreva uma contraproposta oferecendo pagamento antecipado ou aumento de volume em troca de uma condição melhor.\""},
            {"kind": "prompt", "tag": "PASSO 3 DE 3", "headline": ["RENEGOCIAR", "PRAZO DE PAGAMENTO"],
             "body": "Cole isso quando precisar de fôlego de caixa:",
             "prompt": "\"Escreva uma mensagem pedindo pra estender o prazo de pagamento de [X] pra [Y] dias, explicando o motivo de forma transparente e profissional.\""},
            {"kind": "resultado", "tag": "O RESULTADO", "headline": ["O QUE MUDA NA", "PRÁTICA"],
             "body": "Com os 3 prompts na sua próxima negociação:",
             "items": [["💰", "Menos custo fixo", "Sem cortar qualidade"],
                       ["✅", "Argumento pronto", "Não trava na hora de pedir"],
                       ["🤝", "Relação preservada", "Negocia sem parecer ameaça"]]},
            {"kind": "cta", "cta_word": "FORNECEDOR"},
        ],
    },
    # DIA 5 — Fluxo de caixa / inadimplência
    {
        "slug": "prompt-fluxo-de-caixa",
        "caption": (
            "Descobri quais 3 clientes estavam prestes a me deixar no vermelho — antes de acontecer.\n\n"
            "O prompt que transforma sua planilha de vendas num alerta de fluxo de caixa.\n\n"
            "Comenta \"CAIXA\" que eu te mando o prompt completo no direct 👇\n\n"
            "#inteligenciaartificial #fluxodecaixa #gestaofinanceira #ia #pequenosnegocios"
        ),
        "slides": [
            {"kind": "capa", "use_photo": False, "tag": "CASE PRÓPRIO",
             "headline": ["ACHEI 3 CLIENTES", "QUE IAM ME DEIXAR", "NO VERMELHO"],
             "subtitle": "Antes de acontecer, não depois.",
             "proof": {"type": "stats", "label": "ALERTA DE CAIXA", "items": [
                 ["Risco", "3 clientes"], ["Valor exposto", "R$ 6.100"], ["Ação", "cobrança antecipada"],
             ]}},
            {"kind": "capa2", "tag": "O QUE MUDOU",
             "headline": ["EU NÃO PRECISO", "OLHAR A PLANILHA", "TODO DIA MAIS"],
             "body": "O prompt lê os dados e me avisa só quando tem risco real.",
             "stat_items": [["3", "clientes de risco identificados"], ["1x", "por semana eu rodo"], ["0", "surpresa no caixa"]]},
            {"kind": "dor", "tag": "O PROBLEMA", "headline": ["VOCÊ SÓ VÊ O", "PROBLEMA DEPOIS"],
             "pain_lines": [
                 "Cliente atrasa e você só percebe quando falta dinheiro pra pagar conta",
                 "Planilha de vendas tem os dados, mas ninguém olha com atenção",
                 "Decisão de cobrar ou não fica no feeling, não no número",
             ]},
            {"kind": "prompt", "tag": "PASSO 1 DE 3", "headline": ["MAPEAR RISCO DE", "INADIMPLÊNCIA"],
             "body": "Cole isso com sua planilha de vendas/recebimentos:",
             "prompt": "\"Aja como analista financeiro. Analise esses dados de recebimento [colar planilha/dados] e liste os clientes com maior risco de atraso, com base no histórico. Traga os 3 mais urgentes.\""},
            {"kind": "prompt", "tag": "PASSO 2 DE 3", "headline": ["PROJETAR O CAIXA", "DAS PRÓXIMAS 4 SEMANAS"],
             "body": "Prompt pronto:",
             "prompt": "\"Com base nesses dados de entrada e saída [colar dados], projete meu saldo de caixa das próximas 4 semanas e aponte a semana mais crítica.\""},
            {"kind": "prompt", "tag": "PASSO 3 DE 3", "headline": ["COBRANÇA SEM", "SOAR AGRESSIVA"],
             "body": "Cole isso pro cliente em atraso:",
             "prompt": "\"Escreva uma mensagem de cobrança pro cliente [nome], atraso de [X] dias, valor [R$], educada mas direta, com 1 opção de parcelamento.\""},
            {"kind": "resultado", "tag": "O RESULTADO", "headline": ["O QUE MUDA NA", "PRÁTICA"],
             "body": "Com os 3 prompts rodando no seu financeiro:",
             "items": [["🔍", "Risco visível cedo", "Antes de virar problema de caixa"],
                       ["📊", "Decisão com dado", "Não no feeling"],
                       ["💬", "Cobrança sem climão", "Educada e eficaz"]]},
            {"kind": "cta", "cta_word": "CAIXA"},
        ],
    },
    # DIA 6 — Contrato/documento simples (reduzir custo jurídico)
    {
        "slug": "prompt-contrato-simples",
        "caption": (
            "Economizei uma consulta com advogado montando o rascunho de um contrato simples com IA.\n\n"
            "O prompt que gera a base de um contrato de prestação de serviço em minutos (você ainda revisa com um advogado antes de assinar).\n\n"
            "Comenta \"CONTRATO\" que eu te mando o prompt completo no direct 👇\n\n"
            "#inteligenciaartificial #reducaodecustos #contratos #ia #pequenosnegocios"
        ),
        "slides": [
            {"kind": "capa", "use_photo": False, "tag": "CASE PRÓPRIO",
             "headline": ["POUPEI UMA CONSULTA", "COM ADVOGADO", "USANDO ISSO"],
             "subtitle": "Rascunho pronto, revisão rápida, assina depois.",
             "proof": {"type": "checklist", "label": "CONTRATO DE SERVIÇO", "items": [
                 [True, "Escopo do serviço"], [True, "Valor e forma de pagamento"], [False, "Revisão do advogado"],
             ]}},
            {"kind": "capa2", "tag": "O QUE MUDOU",
             "headline": ["A IA NÃO SUBSTITUI", "O ADVOGADO.", "ADIANTA O TRABALHO"],
             "body": "Ela monta a base — cláusula por cláusula — pra revisão sair rápida e barata.",
             "stat_items": [["80%", "do rascunho pronto na hora"], ["1", "revisão jurídica ainda necessária"], ["R$", "menos horas cobradas"]]},
            {"kind": "dor", "tag": "O PROBLEMA", "headline": ["CONTRATO CARO", "OU CONTRATO", "NENHUM"],
             "pain_lines": [
                 "Advogado cobra caro só pra redigir o básico do zero",
                 "Sem contrato, cliente contesta prazo e escopo depois",
                 "Modelo genérico da internet não cobre seu caso",
             ]},
            {"kind": "prompt", "tag": "PASSO 1 DE 3", "headline": ["RASCUNHO DE", "CONTRATO"],
             "body": "Cole isso com os detalhes do serviço:",
             "prompt": "\"Aja como assistente jurídico. Monte um rascunho de contrato de prestação de serviço entre [sua empresa] e [cliente], para [descrição do serviço], valor R$[valor], prazo [prazo]. Deixe claro que precisa de revisão de um advogado antes de assinar.\""},
            {"kind": "prompt", "tag": "PASSO 2 DE 3", "headline": ["CLÁUSULA DE", "CANCELAMENTO"],
             "body": "Prompt pronto:",
             "prompt": "\"Escreva uma cláusula de cancelamento justa pros dois lados, prevendo aviso prévio de [X] dias e multa proporcional ao que já foi entregue.\""},
            {"kind": "prompt", "tag": "PASSO 3 DE 3", "headline": ["EXPLICAR O CONTRATO", "PRO CLIENTE"],
             "body": "Cole isso antes de enviar:",
             "prompt": "\"Resuma esse contrato [colar contrato] em linguagem simples, em 5 bullets, pra eu explicar pro cliente antes de ele assinar.\""},
            {"kind": "resultado", "tag": "O RESULTADO", "headline": ["O QUE MUDA NA", "PRÁTICA"],
             "body": "Com os 3 prompts no seu próximo contrato:",
             "items": [["💰", "Menos hora cobrada", "Advogado só revisa, não redige do zero"],
                       ["✅", "Menos contestação", "Escopo e prazo claros desde o início"],
                       ["⚡", "Fecha mais rápido", "Contrato pronto no mesmo dia"]]},
            {"kind": "cta", "cta_word": "CONTRATO"},
        ],
    },
    # DIA 7 — Relatório semanal automático de vendas
    {
        "slug": "prompt-relatorio-vendas",
        "caption": (
            "Todo domingo à noite eu tinha 1h de trabalho pra fechar o relatório da semana. Agora são 5 minutos.\n\n"
            "O prompt que transforma a planilha de vendas num relatório pronto pra decisão.\n\n"
            "Comenta \"RELATORIO\" que eu te mando o prompt completo no direct 👇\n\n"
            "#inteligenciaartificial #automacao #vendas #gestao #ia"
        ),
        "slides": [
            {"kind": "capa", "use_photo": False, "tag": "CASE PRÓPRIO",
             "headline": ["MEU RELATÓRIO", "LEVAVA 1H.", "AGORA LEVA 5 MIN"],
             "subtitle": "Toda semana, sem esforço.",
             "proof": {"type": "stats", "label": "RELATÓRIO SEMANAL", "items": [
                 ["Vendas", "R$ 18.400"], ["Top produto", "Kit Essencial"], ["Queda", "categoria C"],
             ]}},
            {"kind": "capa2", "tag": "O QUE MUDOU",
             "headline": ["EU NÃO PRECISO", "MONTAR GRÁFICO", "PRA ENTENDER A SEMANA"],
             "body": "O prompt lê a planilha e devolve o que realmente importa, em texto direto.",
             "stat_items": [["5 MIN", "tempo do relatório agora"], ["1x", "por semana"], ["0", "planilha nova pra montar"]]},
            {"kind": "dor", "tag": "O PROBLEMA", "headline": ["VOCÊ TEM DADO,", "NÃO TEM TEMPO"],
             "pain_lines": [
                 "A planilha de vendas existe, mas ninguém tem tempo de analisar direito",
                 "Decisão de compra/estoque sai no chute, não no número",
                 "Fechamento de semana vira tarefa de domingo à noite",
             ]},
            {"kind": "prompt", "tag": "PASSO 1 DE 3", "headline": ["RESUMO DA", "SEMANA"],
             "body": "Cole isso com sua planilha de vendas:",
             "prompt": "\"Aja como analista de vendas. Resuma essa planilha da semana [colar dados]: faturamento total, produto mais vendido, produto que mais caiu, e uma recomendação prática pra semana que vem.\""},
            {"kind": "prompt", "tag": "PASSO 2 DE 3", "headline": ["COMPARAR COM", "A SEMANA ANTERIOR"],
             "body": "Prompt pronto:",
             "prompt": "\"Compare esses dois períodos de vendas [colar semana atual e anterior] e aponte o que mudou pra melhor e pra pior, em 3 bullets cada.\""},
            {"kind": "prompt", "tag": "PASSO 3 DE 3", "headline": ["TRANSFORMAR EM", "MENSAGEM PRO TIME"],
             "body": "Cole isso antes de enviar pro grupo:",
             "prompt": "\"Transforme esse resumo de vendas [colar resumo] numa mensagem curta e motivadora pra enviar no grupo do time, destacando o que foi bem.\""},
            {"kind": "resultado", "tag": "O RESULTADO", "headline": ["O QUE MUDA NA", "PRÁTICA"],
             "body": "Com os 3 prompts no seu fechamento semanal:",
             "items": [["⚡", "5 minutos, não 1 hora", "Todo domingo de volta pra você"],
                       ["📊", "Decisão com dado", "Não no chute"],
                       ["🗣️", "Time informado", "Sem trabalho extra de comunicação"]]},
            {"kind": "cta", "cta_word": "RELATORIO"},
        ],
    },
    # DIA 8 — FAQ automático de dúvidas do produto
    {
        "slug": "prompt-faq-automatico",
        "caption": (
            "Parei de responder a mesma dúvida sobre o produto 15 vezes por semana.\n\n"
            "O prompt que transforma suas perguntas mais frequentes num FAQ pronto pra colar no seu site ou bio.\n\n"
            "Comenta \"FAQ\" que eu te mando o prompt completo no direct 👇\n\n"
            "#inteligenciaartificial #automacao #atendimento #ia #pequenosnegocios"
        ),
        "slides": [
            {"kind": "capa", "use_photo": False, "tag": "CASE PRÓPRIO",
             "headline": ["PAREI DE RESPONDER", "A MESMA DÚVIDA", "15X POR SEMANA"],
             "subtitle": "Um FAQ resolveu o que eu repetia toda hora.",
             "proof": {"type": "checklist", "label": "FAQ DO PRODUTO", "items": [
                 [True, "Como funciona a entrega"], [True, "Formas de pagamento"], [True, "Política de troca"],
             ]}},
            {"kind": "capa2", "tag": "O QUE MUDOU",
             "headline": ["A DÚVIDA CONTINUA", "A MESMA.", "EU QUE PAREI DE REPETIR"],
             "body": "O prompt junta as perguntas que mais chegam e já devolve a resposta pronta.",
             "stat_items": [["15x", "por semana era repetido"], ["1", "FAQ resolve quase tudo"], ["0", "copy-paste manual"]]},
            {"kind": "dor", "tag": "O PROBLEMA", "headline": ["VOCÊ VIROU UM", "DISCO RISCADO"],
             "pain_lines": [
                 "Mesma pergunta chega todo dia, de gente diferente",
                 "Você responde igual, mas gasta tempo digitando de novo",
                 "Cliente novo não acha a resposta sozinho em lugar nenhum",
             ]},
            {"kind": "prompt", "tag": "PASSO 1 DE 3", "headline": ["MONTAR O FAQ", "A PARTIR DAS DÚVIDAS"],
             "body": "Cole isso com as perguntas que mais recebe:",
             "prompt": "\"Aja como especialista em atendimento. Com base nessas perguntas frequentes que eu recebo [listar perguntas], monte um FAQ com respostas curtas, claras e no meu tom de voz.\""},
            {"kind": "prompt", "tag": "PASSO 2 DE 3", "headline": ["RESPOSTA PADRÃO", "PRA DÚVIDA REPETIDA"],
             "body": "Prompt pronto:",
             "prompt": "\"Escreva uma resposta padrão e calorosa pra pergunta '[pergunta mais comum]', que eu possa copiar e colar sem parecer automática.\""},
            {"kind": "prompt", "tag": "PASSO 3 DE 3", "headline": ["ATUALIZAR O FAQ", "COM DÚVIDA NOVA"],
             "body": "Cole isso quando surgir uma pergunta nova recorrente:",
             "prompt": "\"Essa pergunta nova está aparecendo bastante: '[pergunta]'. Escreva a resposta no mesmo tom do FAQ que já tenho [colar FAQ atual] e me diga onde encaixar ela.\""},
            {"kind": "resultado", "tag": "O RESULTADO", "headline": ["O QUE MUDA NA", "PRÁTICA"],
             "body": "Com os 3 prompts no seu atendimento:",
             "items": [["⚡", "Resposta instantânea", "Copia e cola, sem reescrever"],
                       ["✅", "Cliente se resolve sozinho", "Se o FAQ estiver visível"],
                       ["🧠", "Menos desgaste seu", "Sem repetir a mesma explicação"]]},
            {"kind": "cta", "cta_word": "FAQ"},
        ],
    },
]


def main():
    fila_entries = []
    for spec in SPECS:
        spec["photo"] = PHOTO
        html = build_html(spec)
        preview_dir = ROOT / "preview"
        preview_dir.mkdir(exist_ok=True)
        (preview_dir / f"{spec['slug']}.html").write_text(html, encoding="utf-8")

        out_dir = ROOT / "images" / spec["slug"]
        asyncio.run(export_slides(html, out_dir, len(spec["slides"])))
        print(f"Gerado: {spec['slug']} ({len(spec['slides'])} slides)")

        fila_entries.append({
            "titulo": spec["slides"][0]["headline"][0] + " " + " ".join(spec["slides"][0]["headline"][1:]),
            "images": [f"images/{spec['slug']}/slide_{i+1}.png" for i in range(len(spec["slides"]))],
            "caption": spec["caption"],
            "postado": False,
        })

    out_path = ROOT / "design" / "week1_fila_entries.json"
    out_path.write_text(json.dumps(fila_entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nEntradas de fila salvas em {out_path}")


if __name__ == "__main__":
    main()
