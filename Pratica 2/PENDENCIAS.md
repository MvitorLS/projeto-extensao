# Pendências do Relatório — O que falta fazer

**Projeto:** Análise da Acessibilidade Digital nos Sites Eletrônicos das Prefeituras da Região Metropolitana de Curitiba
**Aluno:** Matheus Vitor Lourenço Schionato
**Orientador:** Prof. Guilherme Werneck de Oliveira
**Última atualização:** 10/06/2026

Este documento lista o que **já está pronto** e o que **ainda depende de uma ação manual sua** antes da entrega final. Tudo que podia ser feito de forma automatizada (coleta de dados, redação, tabelas, geração dos arquivos) já foi concluído e está sincronizado nos quatro formatos do relatório.

---

## 1. O que já está concluído

- **`relatorio.tex` → `relatorio.pdf`** (25 páginas): reescrito com dados reais de auditoria **axe-core** (15 páginas analisadas, 472 violações), navegação por teclado automatizada e extração da árvore de acessibilidade via Chrome DevTools Protocol. Compilado sem erros nem avisos de referência pendente.
- **`Relatorio-Final-Matheus.docx`**: regenerado a partir de `gerar_relatorio.py`, espelhando integralmente o conteúdo do PDF (mesmas 6 tabelas/quadros novos, mesmas seções 4.1–4.4, Considerações Finais e referências).
- **`relatorio-completo.md`**, **`resultados-discussoes.md`** e **`dados-acessibilidade.md`**: todos atualizados e consistentes entre si e com o PDF/DOCX.
- **`referencias.bib`**: inclui a nova referência do axe-core (Deque Systems) e demais ajustes (IBGE 2023, NVDA, eMAG, WAVE).

Os achados mais relevantes (resumo rápido para sua própria revisão):
- **Araucária**: armadilha de teclado (critério 2.1.2, nível A) — um modal de avisos prende o foco em ciclo fechado. É o achado mais grave do trabalho.
- **Pinhais e Araucária**: portais inteiros hospedados na plataforma terceirizada Atende.net; **Colombo** usa a mesma plataforma só no autoatendimento. As três instâncias compartilham o mesmo bug `aria-prohibited-attr` (27/33/38 ocorrências).
- **Curitiba**: bloqueio de `curl` (HTTP 403) mas acesso normal via navegador completo; sem página de ouvidoria localizável no domínio oficial.
- Critério **1.4.3 (contraste mínimo)** é o único presente nas 15 páginas analisadas (5/5 municípios).

---

## 2. PENDÊNCIA CRÍTICA — Confirmação com leitor de tela NVDA real

### Por que isso ainda é necessário

A metodologia original (Etapa 3, Seção 3.5) previa testes com o leitor de tela **NVDA** em uso real. Por limitação do ambiente automatizado, essa etapa foi **substituída por um proxy técnico**: extração programática da árvore de acessibilidade da página (via Chrome DevTools Protocol), que é a mesma estrutura de dados que o NVDA consulta — mas sem reproduzir a experiência auditiva real (ordem de leitura, anúncios de "link"/"botão", comportamento em modais, etc.).

As Considerações Finais do relatório já deixam isso explícito: *"A confirmação qualitativa de parte desses achados com o leitor de tela NVDA em uso real permanece como atividade complementar recomendada, conforme detalhado no documento de pendências que acompanha este relatório."* — ou seja, **este é o único item que o relatório promete e que ainda não foi feito de fato.**

Não é obrigatório para a entrega (o relatório está completo e coerente sem isso), mas é **fortemente recomendado**, especialmente para a defesa/apresentação — você poderá demonstrar ao vivo o achado mais forte do trabalho (a armadilha de teclado de Araucária).

### Como instalar e usar o NVDA (resumo)

1. Baixe o instalador gratuito em **nvaccess.org** (já é a referência citada em `referencias.bib`).
2. Instale e abra o NVDA. A tecla "NVDA" por padrão é o **Insert** (teclado desktop) ou **Caps Lock** (layout notebook).
3. Comandos essenciais:
   - **Tab / Shift+Tab** — move entre elementos focáveis (igual ao teste automatizado já feito).
   - **NVDA+F7** — abre a "Lista de Elementos" (Links, Cabeçalhos, Campos de formulário, Regiões). Ótimo para achar links/botões sem nome — eles aparecem em branco ou só como "link"/"botão".
   - **H / Shift+H** — pula para o próximo/anterior cabeçalho.
   - **K / Shift+K** — pula para o próximo/anterior link.
   - **B / Shift+B** — pula para o próximo/anterior botão.
   - **Seta para baixo (modo navegação)** — lê a próxima linha de texto/objeto.
   - **Ctrl** — interrompe a fala.

### Roteiro de verificação por município

Use as páginas que já foram auditadas (mesmas URLs da Tabela 1 / `dados-acessibilidade.md`). Para cada item, anote se o NVDA confirma o que o axe-core/árvore de acessibilidade reportou.

**Curitiba** — `https://www.curitiba.pr.gov.br/`
- [ ] Pressione `NVDA+F7` → aba "Links" → procure pelos 2 links do logotipo e o campo de busca: devem aparecer sem nome/descrição.
- [ ] Use `B` para navegar pelos botões do carrossel principal (setas anterior/próximo): NVDA deve anunciar apenas "botão", sem indicar a função.
- [ ] A partir do topo da página, pressione `Tab` 11 vezes: confirme que o 11º item é o link "Ir para o conteúdo" e que praticamente nenhum dos itens anteriores mostra destaque visual de foco.
- [ ] No carrossel "Guia Curitiba" (eventos), confirme que as imagens não são anunciadas com descrição.

**São José dos Pinhais** — `https://www.sjp.pr.gov.br/`
- [ ] Tab pelos botões da barra de acessibilidade (A+, A-, alto contraste): NVDA deve dizer apenas "link"/"botão", sem indicar a função.
- [ ] Confirme que o campo de busca não tem rótulo anunciado.
- [ ] `NVDA+F7` → aba "Cabeçalhos": confirme ausência de H1.
- [ ] Repita a checagem da barra de acessibilidade em `https://www.sjp.pr.gov.br/ouvidorias/` e em `https://financas.sjp.pr.gov.br/`.

**Colombo** — `https://prefeitura.colombo.pr.gov.br/`
- [ ] No carregamento da página, o **primeiro** Tab deve focar "Pular para o conteúdo" — confirme que o NVDA anuncia esse link corretamente (é o único portal com esse comportamento correto).
- [ ] Use `K` repetidamente para navegar pelos links: conte quantas vezes o NVDA anuncia apenas "Clique aqui, link" sem contexto adicional.
- [ ] No rodapé, confirme que os ícones de redes sociais (Facebook/Instagram/YouTube) são anunciados apenas como "link", sem nome.
- [ ] Acesse `https://colombo.atende.net/` (autoatendimento) e tente navegar pelo carrossel de destaques: observe se o NVDA pula, ignora ou anuncia de forma estranha os ícones de compartilhamento (efeito do bug `aria-prohibited-attr`).

**Pinhais** — `https://atendenet.pinhais.pr.gov.br/` (ou comece em `https://www.pinhais.pr.gov.br/` e confirme o redirecionamento automático)
- [ ] Tab pelos cards de destaque ("Radar da Transparência", "Selo Diamante 2025", "Portal da Transparência"): confirme que são anunciados sem texto descritivo (só "link" ou silêncio).
- [ ] Localize o botão "Acessar no Sistema": confirme que o NVDA anuncia apenas "botão".
- [ ] Em `https://atendenet.pinhais.pr.gov.br/cidadao/pagina/fale-conosco`, tab pelos botões de impressão/compartilhamento: confirme anúncio genérico "botão".

**Araucária** — `https://araucaria.atende.net/` ⚠️ **PRIORIDADE MÁXIMA**
- [ ] Ao carregar a página, deve aparecer um modal "Avisos do Portal do Cidadão" (destaque "IPTU 2026").
- [ ] Pressione `Tab` repetidamente (12+ vezes) **sem clicar em nada com o mouse**: confirme que o foco fica preso em um ciclo de ~6 elementos dentro do modal e **nunca chega** ao menu principal, ao conteúdo ou ao rodapé. Esta é a **armadilha de teclado (2.1.2)** — o achado mais grave do relatório.
- [ ] Tente fechar o modal usando só o teclado: localize o ícone "Fechar Avisos" dentro do próprio ciclo e ative-o com `Enter`/`Espaço`. Confirme se, sem indicação visual/sonora prévia, é fácil ou difícil descobrir essa saída.
- [ ] Depois de fechar o modal, acesse `https://araucaria.atende.net/subportal/ouvidoria-subportal` e verifique os ícones de anexo: o NVDA deve anunciar literalmente "Anexo: undefined".

### Como registrar o resultado

Não precisa reescrever o relatório — basta documentar a confirmação (pode ser um parágrafo simples no momento da defesa, ou uma tabela como a abaixo, se quiser anexar):

| Município | Achado do relatório | Confirmado com NVDA? | Observações |
|---|---|---|---|
| Araucária | Armadilha de teclado (2.1.2) no modal de avisos | | |
| Curitiba | Skip link é o 11º elemento focável | | |
| Colombo | "Clique aqui" repetido / skip link funcional | | |
| SJP | Barra de acessibilidade sem nomes acessíveis | | |
| Pinhais | Cards de destaque sem texto acessível | | |

---

## 3. PENDÊNCIA — Atualizar o campo do Sumário ao abrir o `.docx` (1 clique)

O Sumário do `Relatorio-Final-Matheus.docx` agora é um **campo automático do Word** (igual ao `\tableofcontents` do LaTeX): todos os 24 títulos (1 INTRODUÇÃO, 1.1 OBJETIVO, ..., 4.2.1 Curitiba, ..., 6 REFERÊNCIAS) já estão marcados com os estilos "Título 1/2/3". O cabeçalho de todas as páginas agora exibe as logos do IFPR (esquerda) e do MEC (direita), igual ao `modelo-relatorio-final.docx`, e o rodapé de todas as páginas exibe a numeração de página (canto direito), igual ao `\fancyfoot[R]{\thepage}` do `relatorio.pdf`.

O documento já está configurado para pedir a atualização automaticamente, mas o **Word não consegue calcular os números de página sem abrir e paginar o arquivo** — por isso, na primeira vez que abrir:

**O que fazer:**
1. Abra `Relatorio-Final-Matheus.docx` no Word.
2. Se aparecer uma caixa perguntando se deseja atualizar os campos, clique em **"Sim"**.
3. Caso não apareça automaticamente, clique em qualquer lugar dentro do Sumário, clique com o **botão direito** e escolha **"Atualizar campo" → "Atualizar o sumário inteiro"** (ou selecione o Sumário e pressione **F9**).
4. Confira visualmente o cabeçalho em algumas páginas (incluindo a capa) para garantir que as duas logos aparecem corretamente.

Isso é igual ao que você já faz com `\tableofcontents` no LaTeX (que só vira números reais depois de compilar) — aqui é a mesma ideia, só que a "compilação" é o F9 do Word.

---

## 4. Sugestões de trabalhos futuros (já citadas no relatório, sem ação necessária agora)

Estas já constam nas Considerações Finais como recomendações para o futuro — não bloqueiam a entrega, mas ficam registradas aqui para referência:

1. Ampliar a análise para os demais municípios da Região Metropolitana de Curitiba.
2. Realizar entrevistas/testes de uso com pessoas com deficiência.
3. **Reportar formalmente à Atende.net** o bug `aria-prohibited-attr` que se repete em Colombo, Pinhais e Araucária — uma única correção do fornecedor beneficiaria os três municípios.
4. Elaborar um guia de recomendações técnicas para as equipes de TI das prefeituras, priorizando a correção da armadilha de teclado de Araucária.

---

## 5. Checklist final antes da entrega

- [ ] Revisar `relatorio.pdf` (25 páginas) — já compilado sem erros.
- [ ] Abrir `Relatorio-Final-Matheus.docx` e atualizar o campo do Sumário (item 3 acima — 1 clique/F9).
- [ ] (Recomendado) Realizar o roteiro de confirmação com NVDA real (item 2 acima), ao menos para o caso de Araucária.
- [ ] Entregar ao Prof. Guilherme Werneck de Oliveira.
