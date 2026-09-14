# Padrão de watchdog via cron (referência do monitor do site cuidar.vc)

Job `b66e74eee96a` (every 15m, no_agent=True, deliver=origin), script `scripts/watchdog-site.py` no workspace `/home/hermes/cuidarvc`. Testa `https://cuidar.vc` esperando HTTP 200 (o `www` responde 302 e também conta como OK).

## Regras de alerta (comportamento validado 14/09)
1. Site OK = stdout vazio = silêncio absoluto (cron no_agent só fala com output não vazio).
2. 1ª falha = silêncio (evita alarme por blip de rede).
3. 2ª falha SEGUIDA = 1 ÚNICO alerta no DM do Rob ("SITE FORA DO AR... verificar hospedagem (Lovable) urgente"); não repete a cada tick enquanto continuar fora.
4. Volta do ar = 1 aviso de recuperação ("SITE DE VOLTA") e reseta o estado.

## Estado e overrides
Estado em arquivo JSON no workspace (contador de falhas consecutivas + flag de alertado). Overrides por env: `WATCHDOG_URL`, `WATCHDOG_STATE` (usados nos testes e se a URL mudar).

## Receita de teste (4 cenários, ~5 min)
Rodar o script 4x variando URL/estado: (1) URL real OK = exit 0 e ZERO output; (2) URL inválida, 1ª vez = silêncio; (3) mesma falha, 2ª vez seguida = sai o alerta ÚNICO; (4) URL real de volta = sai a RECUPERAÇÃO e o estado reseta. Validado 14/09 com os 4 cenários passando em sequência.

## Quando reaproveitar este padrão
Qualquer monitor recorrente (site, API, webhook, fila) que rodaria a cada 15-30m: NUNCA alertar a cada tick, apenas em transição de estado (OK→fora e fora→OK) com deduplicação por arquivo de estado. Alertas no_agent vão no DM do Rob; o briefing não duplica, só menciona incidente em curso.
