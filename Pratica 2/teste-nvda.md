# Registro do Teste com NVDA

**Aluno:** Matheus Vitor Lourenço Schionato
**Data do teste:** ___/___/2026
**Leitor de tela:** NVDA (nvaccess.org) — versão: ________

> Marque **[x]** em "Confirmado?" se o NVDA reproduziu o problema que o relatório aponta.
> Tecla NVDA = **Insert** (desktop) ou **Caps Lock** (notebook). `Ctrl` interrompe a fala.

---

## ⚠️ PRIORIDADE — Araucária (`https://araucaria.atende.net/`)

| # | O que testar | Resultado esperado | Confirmado? | Observações |
|---|---|---|---|---|
| 1 | Tab 12+ vezes **sem usar o mouse** | Foco preso em ciclo de ~6 itens no modal "Avisos"; nunca chega ao menu/conteúdo | [ ] | |
| 2 | Fechar o modal só com teclado (Enter/Espaço em "Fechar Avisos") | Saída existe, mas é difícil de descobrir | [ ] | |
| 3 | Ícones de anexo em `.../subportal/ouvidoria-subportal` | NVDA anuncia "Anexo: undefined" | [ ] | |

**Achado principal:** armadilha de teclado — critério **2.1.2 (nível A)**.

---

## Demais municípios (opcional)

| Município | O que testar | Esperado | Confirmado? | Obs. |
|---|---|---|---|---|
| **Curitiba** (`curitiba.pr.gov.br`) | `NVDA+F7` → Links; Tab 11x até "Ir para o conteúdo" | Links do logo/busca sem nome; skip link é o 11º item | [ ] | |
| **SJP** (`sjp.pr.gov.br`) | Tab na barra de acessibilidade (A+, A-, contraste); `NVDA+F7` → Cabeçalhos | Botões anunciam só "link/botão"; sem H1 | [ ] | |
| **Colombo** (`prefeitura.colombo.pr.gov.br`) | 1º Tab; tecla `K` nos links | 1º Tab foca "Pular para o conteúdo" (correto); vários "Clique aqui, link" | [ ] | |
| **Pinhais** (`atendenet.pinhais.pr.gov.br`) | Tab nos cards de destaque e botão "Acessar no Sistema" | Anunciados sem texto / só "botão" | [ ] | |

---

## Conclusão (para a defesa)

_Escreva 1 parágrafo:_ "O teste com o leitor de tela NVDA em uso real confirmou ________________________________________ (ex.: a armadilha de teclado no modal de avisos de Araucária), validando os achados obtidos via extração automatizada da árvore de acessibilidade."
