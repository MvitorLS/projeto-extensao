# Resumo da Conversa — Projeto Acessibilidade (Práticas de Extensão II)

> Arquivo de referência rápida. Tudo que foi discutido e decidido, em um só lugar.
> **Aluno:** Matheus Vitor Lourenço Schionato | **Orientador:** Prof. Guilherme Werneck | IFPR Pinhais, 2026.

---

## 1. Status do projeto: PRONTO para entrega ✅

O relatório está completo. Faltam só ações manuais:
- **Entregar:** usar o **`Relatorio-Final-Matheus`** (segue modelo oficial IFPR, com logos IFPR/MEC). O `relatorio.pdf` (LaTeX) é só o rascunho técnico.
- **Antes de entregar:** abrir o `.docx` e apertar **F9** no sumário (atualiza números de página).

---

## 2. Dúvidas resolvidas

- **IBGE 2023 vs 2022:** dado é do **Censo 2022**, publicado em **2023**. Na citação ABNT usa-se o ano de publicação (2023). Correto.
- **IBGE 2026 não existe:** dado mais recente é o Censo 2022. O "(2026)" na fonte é o ano em que o autor elaborou a tabela — não é dado do IBGE.
- **Best Practices ON/OFF (axe):** ON soma regras "should" (recomendações, não-WCAG). Para bater com o relatório, usar **OFF** (conta só WCAG A/AA = exigido por lei). Diferença "must" (obrigatório/WCAG) vs "should" (recomendado).
- **Por que números ao vivo ≠ relatório:** os portais mudam conteúdo diariamente. A auditoria é uma "foto" da data (09–10/06/2026). Variação pequena é normal.

---

## 3. O argumento principal: a plataforma Atende.net 🔒

Mesmo erro ARIA (`aria-prohibited-attr` = "Elements must only use permitted ARIA attributes") só nos 3 sites Atende.net:

| Município | Plataforma | ARIA proibido (confirmado 23/06) |
|---|---|---|
| Colombo | Atende.net | 27 ✅ |
| Araucária | Atende.net | 34 ✅ |
| Pinhais | Atende.net | 34 ✅ |
| Curitiba | própria | não tem (controle) |
| SJP | própria | não tem (controle) |

→ Defeito é da plataforma, não das prefeituras. Uma correção do fornecedor resolve os 3. Mostra importância de exigir acessibilidade em contratos públicos de TI.

---

## 4. Os 5 tipos de erro (vistos ao vivo no código)

| Erro (axe) | WCAG | O que é | Quem sofre |
|---|---|---|---|
| permitted ARIA attributes | 4.1.2 | etiqueta ARIA em elemento que não aceita | cego |
| color contrast | 1.4.3 | texto/fundo com cores parecidas (ex: 2,95:1, exige 4,5:1) | baixa visão |
| buttons discernible text | 4.1.2 | botão só com ícone, sem nome ("Accessible Text: empty") | cego |
| images alternative text | 1.1.1 | imagem sem `alt` | cego |
| links discernible text | 2.4.4 | link sem texto | cego |

**Códigos exatos capturados:**
- ARIA proibido: `<a aria-label="Menu de Compartilhamento" class="social-ativo share fa-share-alt"></a>` (link sem href + etiqueta proibida)
- Botão sem nome: `<button><i class="fas fa-ellipsis"></i></button>` (Accessible Text: empty)
- Contraste: texto #969696 / fundo #ffffff = 2,95:1

---

## 5. Confirmação com NVDA (a pendência crítica — RESOLVIDA ✅)

- **NVDA = leitor de tela real**, gratuito, o mais usado por cegos no Brasil. Não é simulação.
- No site de Colombo, narrou **"Menu de Compartilhamento, link"** repetido dezenas de vezes, sem dizer qual notícia → cego não sabe o que compartilha.
- **Importante:** "ler algumas coisas certo" não significa "sem erro". O botão de compartilhar tem etiqueta proibida/repetida e link sem destino = inacessível de forma inconsistente.

---

## 6. Achado mais grave: armadilha de teclado (Araucária)

- Critério **2.1.2, nível A** (o mínimo). Modal de avisos (IPTU 2026) prende o foco do teclado em ciclo de 6 elementos.
- Quem usa só teclado nunca chega ao conteúdo → site inutilizável.
- Nenhuma ferramenta automática detecta — só teste manual de teclado.
- **Demonstrar ao vivo na defesa** = momento mais impactante.

---

## 7. Arquivos de apoio criados

- **GUIA-APRESENTACAO.md** — roteiro de fala (5–7 min) + respostas a perguntas difíceis.
- **EVIDENCIAS-DEFESA.md** — 6 slides prontos + checklist de prints.
- **RESUMO-CONVERSA.md** — este arquivo.
- **PENDENCIAS.md** — pendências originais (NVDA já resolvido).

---

## 8. Por que duas ferramentas (rigor metodológico)

axe vê o **código** (contraste, ARIA). NVDA vê a **experiência** (mas não vê cor). Teclado vê a **armadilha** (que nenhuma ferramenta automática pega). As três se complementam.
