# 3 Slides de Evidência (prints essenciais)

Recriar no mesmo estilo azul da apresentação. Inserir após o slide correspondente.

---

## SLIDE A — inserir DEPOIS do slide 8 (Armadilha de Teclado)

**Título:** Evidência: A Armadilha em Ação

**Layout:** título em cima, print grande centralizado, legenda embaixo.

[ COLAR AQUI: print/GIF do pop-up de Araucária prendendo o foco do teclado ]

**Legenda:** "Portal de Araucária — modal de IPTU 2026 prende o foco num ciclo de 6 elementos. Navegando só com Tab, o usuário nunca alcança o menu nem o conteúdo. Critério WCAG 2.1.2 (Nível A)."

---

## SLIDE B — inserir DEPOIS do slide 9 (Plataformas Terceirizadas)

**Título:** A Prova: O Mesmo Bug, Três Cidades

**Layout:** tabela à esquerda + 1 print do axe à direita.

| Município | Plataforma | Erros ARIA (axe) |
|---|---|---|
| Colombo | Atende.net | 27 |
| Araucária | Atende.net | 34 |
| Pinhais | Atende.net | 34 |
| Curitiba | Própria | 0 |
| São José dos Pinhais | Própria | 0 |

[ COLAR AQUI: print do axe DevTools mostrando "permitted ARIA attributes" ]

**Frase de impacto (rodapé):** "O erro existe SÓ nos 3 sites Atende.net e em NENHUM dos outros → o defeito é da plataforma, não da prefeitura. Uma correção do fornecedor resolve as três."

---

## SLIDE C — inserir DEPOIS do slide 9 ou perto do paradoxo (slide 7)

**Título:** O Que o Usuário Cego Ouve (NVDA)

**Layout:** print à esquerda, texto à direita.

[ COLAR AQUI: print do NVDA narrando os links ]

**Texto:**
- O NVDA (leitor de tela real, gratuito, mais usado por cegos no Brasil) narrou em Colombo:
  > "Menu de Compartilhamento, link"
  > "Menu de Compartilhamento, link" *(repetido dezenas de vezes)*
- Todo botão de compartilhar é anunciado igual, sem dizer QUAL notícia.
- É a tradução prática do erro `aria-prohibited-attr` que o axe apontou.

---

## Dica de execução
- Prints grandes e legíveis (testar no projetor).
- Ordem de impacto na fala: Armadilha (A) → Atende.net (B) → NVDA (C).
- Demais prints (código, contraste 2,95:1) ficam numa pasta aberta, como evidência extra sob demanda.
