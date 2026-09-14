# Evidências para a Defesa — Confirmação ao Vivo (NVDA + axe DevTools)

**Aluno:** Matheus Vitor Lourenço Schionato
**Data da confirmação:** 23/06/2026 | **Ferramentas:** axe DevTools (WCAG 2.1 AA, Best Practices **OFF**) + NVDA (leitor de tela real)

> Estes dados confirmam **ao vivo** os achados do relatório (coletados em 09–10/06/2026). Pequenas variações nos números são esperadas — os portais atualizam conteúdo dinâmico diariamente; a regra de erro permanece a mesma.

---

## SLIDE 1 — A prova da plataforma Atende.net 🔒

**Argumento:** O mesmo erro ARIA aparece **só** nos 3 sites que usam a Atende.net, e **não** nos que não usam. Logo, o defeito é da plataforma, não das prefeituras.

| Município | Plataforma | "permitted ARIA attributes" | Confirmado ao vivo |
|---|---|---|---|
| **Colombo** | Atende.net | **27** | ✅ |
| **Araucária** | Atende.net | **34** | ✅ |
| **Pinhais** | Atende.net | **34** | ✅ |
| Curitiba | Própria | — (não tem) | grupo de controle |
| São José dos Pinhais | Própria | — (não tem) | grupo de controle |

**Conclusão:** uma única correção do fornecedor (Atende.net / IPM Sistemas) melhoraria os 3 municípios de uma vez → importância de exigir acessibilidade em **contratos públicos de TI**.

---

## SLIDE 2 — Os 5 tipos de erro vistos no código

| # | Erro (axe) | Critério WCAG | O que é | Quem sofre |
|---|---|---|---|---|
| 1 | Elements must only use permitted ARIA attributes | 4.1.2 | etiqueta ARIA num elemento que não a aceita | cego |
| 2 | Elements must meet minimum color contrast | 1.4.3 | texto e fundo com cores parecidas | baixa visão |
| 3 | Buttons must have discernible text | 4.1.2 | botão só com ícone, sem nome | cego |
| 4 | Images must have alternative text | 1.1.1 | imagem sem descrição (`alt`) | cego |
| 5 | Links must have discernible text | 2.4.4 | link sem texto | cego |

> **"must"** = critério obrigatório do WCAG = exigência da Lei (Art. 63 da LBI). Não é estética, é conformidade legal.

---

## SLIDE 3 — Provas técnicas capturadas (o código exato)

**Erro 1 — ARIA proibido** (botão de compartilhar, Colombo):
```html
<a title="Menu de Compartilhamento" aria-label="Menu de Compartilhamento"
   tabindex="0" class="social-ativo share fa-share-alt"></a>
```
→ Erro do axe: *"aria-label attribute cannot be used on a `<a>` with no valid role attribute."*
→ É um link **sem `href`** (não leva a lugar nenhum) com etiqueta proibida.

**Erro 3 — Botão sem nome** (carrossel, Colombo):
```html
<button><i class="fas fa-ellipsis"></i></button>
```
→ Painel do axe: **Accessible Text: `empty`** (vazio).

**Erro 2 — Contraste** (data de notícia, Colombo):
```
contraste de 2,95:1 (texto #969696 cinza / fundo #ffffff branco) — exigido: 4,5:1
```

---

## SLIDE 4 — A experiência real (NVDA) ⭐

**O ponto alto:** não é simulação. O **NVDA** é o leitor de tela gratuito mais usado por pessoas cegas no Brasil — a mesma ferramenta do cidadão real.

**O que o NVDA narrou no site de Colombo:**
> "Menu de Compartilhamento, link"
> "Menu de Compartilhamento, link"
> "Menu de Compartilhamento, link" *(repetido dezenas de vezes)*

**O problema na prática:** todo botão de compartilhar é anunciado **igual**, sem dizer **qual notícia**. O usuário cego não tem como saber o que está compartilhando — e o "link" sequer tem destino.

> **Frase de defesa:** *"O leitor de tela lê 'Menu de Compartilhamento, link' repetido sem contexto. Para um usuário cego, é impossível saber o que cada botão faz. É a tradução prática do erro `aria-prohibited-attr` que a auditoria automática apontou."*

---

## SLIDE 5 — Por que duas ferramentas (rigor metodológico)

| Tipo de erro | axe (automático) | NVDA (experiência) |
|---|---|---|
| ARIA proibido | ✅ aponta o código | ✅ mostra a confusão |
| Botão/link sem nome | ✅ "Accessible Text: empty" | ✅ fala só "botão"/"link" |
| **Contraste** | ✅ mede 2,95:1 | ❌ não vê cor |
| **Armadilha de teclado** | ❌ não detecta | ✅ teste de teclado |

**Conclusão:** nenhuma ferramenta sozinha cobre tudo. As duas se complementam — por isso a metodologia combinou auditoria automática + testes manuais.

---

## SLIDE 6 — O achado mais grave (Araucária)

**Armadilha de teclado** (critério 2.1.2, **nível A** — o mínimo):
- Um modal "Avisos do Portal do Cidadão" (IPTU 2026) prende o foco do teclado num **ciclo de 6 elementos**.
- Quem usa só teclado **nunca chega** ao menu nem ao conteúdo → site **inutilizável**.
- Nenhuma ferramenta automática detecta isso — só o teste manual de teclado.

> Demonstrar isto ao vivo na defesa é o momento mais impactante da apresentação.

---

## Checklist de evidências a anexar

- [ ] Print axe — Colombo (ARIA 27, Best Practices OFF)
- [ ] Print axe — Araucária (ARIA 34)
- [ ] Print axe — Pinhais (ARIA 34)
- [ ] Print do código `<a>` com aria-label proibido
- [ ] Print do `<button>` com Accessible Text: empty
- [ ] Print do contraste 2,95:1
- [ ] Print do NVDA narrando "Menu de Compartilhamento" repetido
- [ ] (Opcional) Vídeo/print da armadilha de teclado em Araucária
