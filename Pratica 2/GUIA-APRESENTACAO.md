# Guia de Apresentação — Tudo sobre o Relatório

**Projeto:** Análise da Acessibilidade Digital nos Sites das Prefeituras da Região Metropolitana de Curitiba
**Aluno:** Matheus Vitor Lourenço Schionato
**Orientador:** Prof. Guilherme Werneck de Oliveira
**Disciplina:** Práticas de Extensão II — IFPR Câmpus Pinhais (2026)

> Este arquivo explica, em ordem, **o que o trabalho fez**, **o que você descobriu** e **o que falar** na defesa. Leia uma vez inteiro; depois use a Seção 8 como roteiro de fala.

---

## 1. Resumo em uma frase (o "elevator pitch")

> "Auditei a acessibilidade digital dos sites das 5 maiores prefeituras da Região Metropolitana de Curitiba, usando ferramentas automáticas (axe-core) e testes manuais de teclado e leitor de tela. Encontrei **472 violações** em 15 páginas, sendo a mais grave uma **armadilha de teclado em Araucária** que impede totalmente o uso do site só com o teclado."

Se só puder dizer uma coisa, é isso.

---

## 2. Por que o tema importa (introdução / motivação)

- Serviços públicos estão cada vez mais **só na internet** (IPTU, certidões, ouvidoria).
- Se o site não é acessível, **a pessoa com deficiência é excluída de um direito**, não de uma conveniência.
- **É lei:** Art. 63 da Lei Brasileira de Inclusão (Lei 13.146/2015) **obriga** sites de governo a serem acessíveis. Logo, site inacessível = ilegal.
- Padrão técnico usado: **WCAG 2.1** (do W3C), níveis A e AA — o mesmo exigido para governo. No Brasil há também o **eMAG** (adaptação para governo).

**Frase pronta:** *"Um cidadão cego que não consegue consultar o IPTU pelo site não está tendo um problema técnico — está sendo impedido de exercer a cidadania. E isso, além de injusto, é ilegal pelo Art. 63 da LBI."*

---

## 3. O que você analisou (escopo)

5 prefeituras, escolhidas pelas **maiores populações** (dado do Censo IBGE 2022, publicado 2023):

| Município | População | Observação importante |
|---|---|---|
| Curitiba | 1.773.733 | Bloqueia robôs (HTTP 403), mas abre normal no navegador |
| São José dos Pinhais | 365.193 | Barra de acessibilidade que é... inacessível |
| Colombo | 256.209 | Único com boa prática de "pular para o conteúdo" |
| Pinhais | 133.105 | Migrou tudo para a Atende.net |
| Araucária | 148.677 | **Armadilha de teclado** (achado mais grave) |

Para **cada** prefeitura, analisou **3 páginas**: inicial, serviço (IPTU/certidões) e contato/ouvidoria. → **15 páginas no total.**

---

## 4. Como você fez (metodologia — 4 etapas)

1. **Avaliação automática** — ferramenta **axe-core** (mesmo motor do Google Lighthouse) rodando num navegador automatizado (Edge + Playwright). Conta violações de contraste, imagens sem texto, botões sem nome, etc.
   - *Por que não só o WAVE (plano original)?* Porque 3 sites bloqueavam acesso simples e vários são "SPA" (carregam por JavaScript). O axe-core num navegador real renderiza tudo e ainda mede contraste automaticamente.
2. **Teste de teclado** — navegar só com **Tab/Enter/Esc**, sem mouse (simula deficiência motora). Parte automatizada: 12 toques de Tab registrando foco e ciclos. É aqui que se acha a **armadilha de teclado**.
3. **Leitor de tela (NVDA)** — simula usuário cego. Por limite do ambiente, foi usado um **proxy técnico**: extração da *árvore de acessibilidade* (mesma estrutura que o NVDA lê). ⚠️ A confirmação com NVDA real é a única pendência (ver Seção 7).
4. **Consolidação** — juntar tudo e classificar pelos 4 princípios do WCAG: **P**erceptível, **O**perável, **C**ompreensível, **R**obusto.

**Termos que podem perguntar:**
- **WCAG:** diretrizes internacionais de acessibilidade web.
- **axe-core:** motor open-source que testa as regras WCAG automaticamente.
- **Árvore de acessibilidade:** "tradução" da página que o leitor de tela usa para narrar.
- **SPA (Single Page Application):** site que monta o conteúdo via JavaScript.
- **ARIA:** atributos HTML que descrevem elementos para tecnologia assistiva.

---

## 5. O que você descobriu (resultados — DECORE ESTES NÚMEROS)

- **472 violações** automáticas em 15 páginas.
- **Contraste insuficiente (critério 1.4.3):** o problema mais universal — **nas 15 páginas, 5/5 municípios**. Atrapalha quem tem baixa visão.
- **Links/botões sem texto (2.4.4 e 4.1.2):** 5/5 municípios. O leitor de tela só fala "link" ou "botão", sem dizer pra quê.
- **Ironia recorrente:** a própria **barra de acessibilidade** (botões A+, A-, alto contraste) é, ela mesma, inacessível em vários sites.

### Os 5 achados que você TEM que saber contar:

1. **Araucária — armadilha de teclado (2.1.2, nível A)** ⭐ O MAIS GRAVE.
   Um modal "Avisos do Portal do Cidadão" (IPTU 2026) **prende o foco do teclado num ciclo de 6 elementos**. Quem usa só teclado **nunca chega ao menu nem ao conteúdo** — o site fica inutilizável. Viola o nível **mínimo** (A) do WCAG.

2. **Plataforma Atende.net (Colombo, Pinhais, Araucária)** — descoberta não planejada.
   3 dos 5 usam a mesma plataforma terceirizada e **repetem o mesmo bug** (`aria-prohibited-attr`): 27/33/38 ocorrências. Conclusão poderosa: **uma única correção do fornecedor consertaria os três** → mostra a importância de exigir acessibilidade em contratos públicos.

3. **Araucária — "Anexo: undefined"** na ouvidoria.
   O leitor de tela lê literalmente a palavra "undefined" — um erro de programação que vaza direto para o usuário cego. Exemplo concreto e didático.

4. **Curitiba — skip link mal posicionado.**
   Tem o link "Ir para o conteúdo", mas é só o **11º** elemento no Tab. Você tem que passar por 10 itens antes de poder "pular" — o que esvazia o recurso.

5. **Colombo — o exemplo positivo.**
   Único com "Pular para o conteúdo" como **1º** elemento e com foco visível. Serve de **referência** para os outros. (Sempre bom mostrar que você sabe reconhecer o que está certo.)

### Condições de acesso (resultado "bônus", impressiona):
- **Araucária:** domínio oficial com **certificado SSL inválido** e site real noutro endereço (`araucaria.atende.net`) — o cidadão não acha o site a partir do oficial.
- **Curitiba:** bloqueia `curl` (403) mas abre no navegador; não tem ouvidoria localizável.
- **Pinhais:** redireciona por JavaScript, sem `<noscript>` de fallback.

---

## 6. Conclusão (o que tudo isso significa)

- A desconformidade é **sistêmica**, não pontual — repete-se entre municípios diferentes.
- Causas: práticas de desenvolvimento que ignoram inclusão **+** plataformas de mercado com defeitos.
- Os portais estão em **desconformidade legal** (Art. 63 da LBI).
- Mais afetados: **cegos** (leitor de tela), **deficiência motora** (só teclado) e **baixa visão/cognitiva** (contraste e estrutura).

**Trabalhos futuros (já no relatório):** ampliar para mais municípios; testes com pessoas com deficiência reais; **reportar os bugs à Atende.net**; criar guia técnico para as prefeituras priorizando a armadilha de Araucária.

---

## 7. Pendências antes de entregar (honestidade na defesa)

1. **NVDA real:** a metodologia previa leitor de tela em uso real; foi substituído por proxy técnico. **Diga isso abertamente** — é uma limitação reconhecida, não um erro escondido. Se der, **demonstre ao vivo a armadilha de Araucária** (é o ponto alto).
2. **Word:** ao abrir `Relatorio-Final-Matheus.docx`, apertar **F9** no sumário para atualizar os números de página.
3. **Entrega:** use o **`Relatorio-Final-Matheus`** (segue o modelo oficial do IFPR, com logos IFPR/MEC). O `relatorio.pdf` (LaTeX) é o rascunho técnico.

---

## 8. Roteiro de fala (5–7 min) — siga esta ordem

1. **Abertura (30s):** "Acessibilidade digital é direito e é lei (Art. 63 da LBI). Sites de prefeitura que excluem pessoas com deficiência estão descumprindo isso."
2. **Objetivo (30s):** medir a conformidade com WCAG 2.1 das 5 maiores prefeituras da RM de Curitiba e achar as barreiras mais comuns.
3. **Como (1 min):** axe-core (automático) + teste de teclado + proxy do leitor de tela; 15 páginas; 4 princípios do WCAG.
4. **Resultados (2 min):** 472 violações. Contraste em 100% das páginas. Conte os **5 achados** da Seção 5 — comece pela **armadilha de Araucária**.
5. **Insight forte (1 min):** a história da **Atende.net** — mesmo bug em 3 cidades, uma correção resolve as três. (Isto te diferencia: você foi além do "achei erros".)
6. **Conclusão (1 min):** problema sistêmico + ilegal + quem sofre. Trabalhos futuros.
7. **Fechamento (30s):** o que aprendeu na formação (aplicar IHC/engenharia de software com impacto social real).

### Se perguntarem...
- *"Por que não usou o NVDA de verdade?"* → "Por limitação do ambiente automatizado; usei a árvore de acessibilidade, que é a mesma estrutura que o NVDA lê. A confirmação auditiva está documentada como atividade complementar e posso demonstrar a armadilha ao vivo."
- *"axe-core pega tudo?"* → "Não. Ferramenta automática pega ~30-40% dos problemas. Por isso somei testes manuais de teclado — foi assim que achei a armadilha, que nenhuma ferramenta automática reporta."
- *"O IBGE tem dado de 2026?"* → "Não. O dado mais recente é o Censo 2022, publicado em 2023. O 2026 que aparece na fonte é o ano em que eu elaborei a tabela."
- *"Qual o achado mais importante?"* → "A armadilha de teclado de Araucária: viola o nível mínimo do WCAG e impede totalmente o uso por teclado."
