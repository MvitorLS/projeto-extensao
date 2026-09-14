# Dados de Acessibilidade — Análise Automatizada

**Projeto:** Análise da Acessibilidade Digital nos Sites Eletrônicos das Prefeituras da Região Metropolitana de Curitiba
**Autor:** Matheus Vitor Lourenço Schionato
**Data da coleta:** 09–10/06/2026
**Método:** Auditoria automatizada com **axe-core 4.x** (Deque Systems) executada via navegador completo (Microsoft Edge, automatizado com Playwright), aplicando as regras WCAG 2.1 nível A e AA; navegação por teclado automatizada (12 pressionamentos de Tab a partir do carregamento da página) e extração da árvore de acessibilidade via Chrome DevTools Protocol (`Accessibility.getFullAXTree`), utilizada como *proxy* para a experiência do leitor de tela NVDA.
**Escopo:** 5 municípios × 3 páginas (inicial, serviço, contato) = 15 páginas analisadas.

> Este documento consolida os dados brutos (contagens, seletores CSS, sequência de tabulação) que fundamentam as Tabelas 1–6 e os Quadros 3–5 do relatório final (`relatorio.tex` / `relatorio-completo.md` / `resultados-discussoes.md`). Os três documentos do relatório já refletem integralmente estes dados; este arquivo serve como referência de apoio/auditoria.

---

## 1. Condições de Acesso aos Portais

| Município | Condição observada | Impacto para o cidadão |
|---|---|---|
| Curitiba | `curl` retorna HTTP 403 (provável bloqueio por *fingerprint*/WAF); navegador completo (Edge/Playwright) acessa normalmente, HTTP 200 | Nenhum impacto direto ao usuário comum; possível impacto em auditorias automatizadas e indexação por buscadores |
| São José dos Pinhais | Acesso normal, HTTP 200 | Nenhum |
| Colombo | Redirecionamento automático para `prefeitura.colombo.pr.gov.br`, HTTP 200 | Nenhum |
| Pinhais | `www.pinhais.pr.gov.br` carrega página mínima e redireciona via JavaScript (~1s) para `atendenet.pinhais.pr.gov.br`; sem `<noscript>` de *fallback* | Usuários/agentes sem JavaScript não acessam o portal — possível violação do princípio de Robustez (4.1) |
| Araucária | `www.araucaria.pr.gov.br` com certificado SSL inválido (`ERR_TLS_CERT_ALTNAME_INVALID`) e sem rota válida; portal real hospedado em domínio sem relação nominal, `araucaria.atende.net` | Barreira grave: aviso de bloqueio de segurança no domínio oficial; portal funcional não é descoberto a partir dele |

**Notas:**

- **Curitiba:** não foi localizada, dentro do domínio oficial, uma página de ouvidoria/contato funcional — os endereços testados (`/ouvidoria`, `/fale-conosco`, etc.) retornam a página de erro padrão do portal (HTTP 404 com *status code* de resposta 200), o que explica os valores residuais (1 erro de contraste) na linha "Curitiba — Contato" da Tabela Consolidada (Seção 4).
- **Pinhais:** a migração do domínio institucional para a plataforma terceirizada Atende.net é completa — todas as três páginas analisadas (inicial, emissão de guias, fale conosco) estão em `atendenet.pinhais.pr.gov.br`.
- **Araucária:** o domínio `araucaria.pr.gov.br` está efetivamente inacessível; a auditoria foi realizada inteiramente em `araucaria.atende.net`. Mesmo contornando o aviso de SSL, o servidor retorna mensagem informando que "não é possível acessar o Atende.net através desse domínio".

---

## 2. Resultados por Página — Auditoria axe-core (WCAG 2.1 A/AA)

Para cada página, são listadas as regras violadas (`impact`, *tags* WCAG, número de nós afetados) e exemplos de seletores CSS dos elementos identificados pelo axe-core. Onde aplicável, são preservados também os achados da análise estrutural de HTML realizada na coleta inicial (09/06/2026).

### 2.1 Curitiba — `https://www.curitiba.pr.gov.br`

#### Página Inicial (`curitiba_home`)

| Regra axe-core | Critério WCAG | Impacto | Nós | Exemplos de seletor |
|---|---|---|---|---|
| `image-alt` | 1.1.1 | critical | 8 | `#cphMasterPortal_ucEventosGuiaCuritiba_rptEventos_ucEventoGuia_0_hplLink_0 > .velop > img` (carrossel "Guia Curitiba") |
| `button-name` | 4.1.2 | critical | 7 | `.owl-prev`, `.owl-next`, `.entry-point-left-arrow` (setas do carrossel principal) |
| `color-contrast` | 1.4.3 | serious | 8 | `.painel > ul > li:nth-child(1) > a[target="_parent"]` (itens do menu superior) |
| `link-name` | 2.4.4 | serious | 11 | `.linkTituloPaginaMenuUnicoPmc`, `#cphMasterTopo_ucTopoHome_ucFormularioBusca_lnbBusca`, `a[href$="noticias.xml"]` |
| `frame-title` | 2.4.1 | serious | 2 | `.i-amphtml-fill-content,iframe[i-amphtml-iframe-position="0"]` |
| `nested-interactive` | 4.1.2 | serious | 1 | `#ma-lerPaginaItem` (botão "ler página" aninhado em outro controle) |

**Total: 15 erros críticos, 8 de contraste, 14 outros alertas → 37 (Tabela Consolidada).**

#### Página de Serviços — Carta de Serviços (`curitiba_servicos`, `?categoria=1`)

| Regra axe-core | Critério WCAG | Impacto | Nós | Exemplos de seletor |
|---|---|---|---|---|
| `color-contrast` | 1.4.3 | serious | 9 | `.painel > ul > li:nth-child(1) > a[target="_parent"]` |
| `link-name` | 2.4.4 | serious | 10 | `#cphMasterPortal_lnkBusca`, `a[href$="noticias.xml"]`, `li:nth-child(2) > a[rel="me"][itemprop="sameAs"][target="_blank"]` |
| `nested-interactive` | 4.1.2 | serious | 1 | `#ma-lerPaginaItem` |

**Total: 0 erros críticos, 9 de contraste, 11 outros alertas → 20 (Tabela Consolidada).** Nove das oito violações de contraste e dez das onze de `link-name` repetem as encontradas na página inicial — confirma que as falhas decorrem do *template* de cabeçalho/menu compartilhado.

#### Página de Contato (`curitiba_contato`)

Não foi localizada página de ouvidoria/contato funcional (Seção 1). O endereço testado retorna a página de erro padrão (HTTP 404 / *status* 200), que herda o mesmo *template* de cabeçalho e apresenta **1 violação residual de `color-contrast`**.

**Total: 0 erros críticos, 1 de contraste, 0 outros alertas → 1 (Tabela Consolidada).**

---

### 2.2 São José dos Pinhais — `https://www.sjp.pr.gov.br`

#### Página Inicial (`sjp_home`)

**Achados da análise estrutural de HTML (09/06/2026):**

| Critério WCAG | Problema | Quantidade | Exemplos |
|---|---|---|---|
| 1.1.1 Conteúdo não textual | Imagens sem `alt` | 12 | Logo, botões A+/A-, ícone de contraste, fotos de mapa, FAQ, carta de serviços, linha divisória |
| 3.3.2 Rótulos e instruções | Campo de busca sem `<label>` | 1 | `<input>` sem identificação acessível |
| 2.4.4 Finalidade do link | Links vazios ou sem contexto | 7 | Botões "Avançar/Voltar" do banner sem texto; `<a href="#">` vazio |
| 4.1.2 Nome, função, valor | ARIA ausente | — | Nenhum `role`, `aria-label` ou `aria-labelledby` identificado |
| 1.3.1 Informação e relações | Hierarquia de headings quebrada | — | Ausência de `<h1>` claro; títulos de seções sem estrutura lógica |

**Achados da auditoria axe-core (10/06/2026):**

| Regra axe-core | Critério WCAG | Impacto | Nós |
|---|---|---|---|
| `aria-required-children` | 1.3.1 | critical | 4 |
| `color-contrast` | 1.4.3 | serious | 8 |
| `link-name` | 2.4.4 | serious | 3 |

**Total: 4 erros críticos, 8 de contraste, 3 outros alertas → 15 (Tabela Consolidada).** As 4 violações de `aria-required-children` e as 8 de `color-contrast` não são perceptíveis por inspeção do HTML estático — somente a auditoria axe-core as revelou.

#### Página de Serviços (`sjp_servicos`, `https://financas.sjp.pr.gov.br/#/`)

> Na coleta inicial (09/06/2026), esta URL retornava uma página padrão de *framework* (JHipster) ao `curl`, sem o conteúdo real do serviço de IPTU. A auditoria axe-core via navegador completo (10/06/2026), que renderiza a aplicação JavaScript, identificou:

| Regra axe-core | Critério WCAG | Impacto | Nós |
|---|---|---|---|
| `color-contrast` | 1.4.3 | serious | 5 |
| `image-alt` | 1.1.1 | critical | 11 |
| `link-name` | 2.4.4 | serious | 2 |

**Total: 11 erros críticos, 5 de contraste, 2 outros alertas → 18 (Tabela Consolidada).**

#### Página de Contato / Ouvidorias (`sjp_contato`, `https://www.sjp.pr.gov.br/ouvidorias/`)

**Achados da análise estrutural de HTML (09/06/2026):**

| Critério WCAG | Problema | Quantidade | Exemplos |
|---|---|---|---|
| 1.1.1 Conteúdo não textual | Imagens sem `alt` | 7 | Logotipo, linha divisória, rodapé, logo azul, selo PNTP, ícones A+/A- |
| 4.1.2 Nome, função, valor | ARIA ausente | — | Nenhum atributo ARIA detectado |
| 1.3.1 Informação e relações | Hierarquia de headings indefinida | — | Título "Ouvidorias" sem tag semântica clara; sem `<h1>` explícito |
| 2.4.4 Finalidade do link | Links de ícones sociais sem texto | 5 | Links de redes sociais com texto muito curto ou dependente de imagem sem alt |

**Achados da auditoria axe-core (10/06/2026):**

| Regra axe-core | Critério WCAG | Impacto | Nós |
|---|---|---|---|
| `color-contrast` | 1.4.3 | serious | 6 |
| `link-name` | 2.4.4 | serious | 2 |

**Total: 0 erros críticos, 6 de contraste, 2 outros alertas → 8 (Tabela Consolidada).**

---

### 2.3 Colombo — `https://prefeitura.colombo.pr.gov.br`

#### Página Inicial (`colombo_home`)

**Achados da análise estrutural de HTML (09/06/2026):**

| Critério WCAG | Problema | Quantidade | Exemplos |
|---|---|---|---|
| 1.1.1 Conteúdo não textual | Imagens sem `alt` | Múltiplas | Logo da prefeitura, imagem "O que procura?", ícones de serviços, ícones de redes sociais |
| 2.4.4 Finalidade do link | Links com texto genérico "Clique aqui" | 10+ | Links de notícias e serviços sem contexto descritivo |
| 1.3.1 Informação e relações | Hierarquia de headings quebrada | — | Múltiplos `<h3>` sem `<h1>` ou `<h2>` precedentes |
| 3.3.2 Rótulos e instruções | Campo de busca sem label | 1 | Imagem usada como campo de busca sem formulário acessível |
| 2.4.1 Ignorar blocos | `<iframe>` sem `title` | Sim | Formulários/serviços incorporados sem atributo `title` |
| 4.1.2 Nome, função, valor | ARIA mínimo | — | Barra de acessibilidade dependente de JavaScript; ícones de navegação sem `aria-label` |

**Achados da auditoria axe-core (10/06/2026):**

| Regra axe-core | Critério WCAG | Impacto | Nós | Exemplos de seletor |
|---|---|---|---|---|
| `link-name` | 2.4.4 | serious | 33 | `.a-facebook`, `.a-instagram`, `.a-youtube` (ícones de redes sociais do rodapé) |

**Total: 0 erros críticos, 0 de contraste, 33 outros alertas → 33 (Tabela Consolidada).** O padrão "Clique aqui" identificado na análise estrutural é consistente com as 33 violações de `link-name` confirmadas pelo axe-core e com os 30 elementos sem nome acessível detectados na árvore de acessibilidade (Seção 4, total de 1.399 nós).

#### Página de Serviços — Autoatendimento (`colombo_servicos`, `https://colombo.atende.net/`)

> Página renderizada como *Single Page Application* (SPA); o HTML estático não contém o conteúdo real da interface. A auditoria axe-core via navegador completo (10/06/2026), que aguarda a renderização do JavaScript, identificou:

| Regra axe-core | Critério WCAG | Impacto | Nós |
|---|---|---|---|
| `aria-prohibited-attr` | 4.1.2 | serious | 27 |
| `button-name` | 4.1.2 | critical | 1 |
| `color-contrast` | 1.4.3 | serious | 10 |

**Total: 1 erro crítico, 10 de contraste, 27 outros alertas → 38 (Tabela Consolidada).**

> **Nota sobre o achado anterior "MUNIC?PIO":** a coleta inicial (09/06/2026) registrara um problema aparente de codificação de caracteres no título da página (`MUNIC?PIO` em vez de `MUNICÍPIO`). A auditoria axe-core (10/06/2026) **não reproduziu esse problema como falha de acessibilidade** — o título da página (`Portal do Cidadão - MUNICÍPIO DE COLOMBO/PR`) está corretamente codificado em UTF-8 quando renderizado pelo navegador completo; o caractere `?` observado na coleta inicial era um artefato da ferramenta de captura de texto utilizada (terminal sem suporte a UTF-8), não um defeito do site. O achado foi substituído pelos resultados reais de `aria-prohibited-attr`, `button-name` e `color-contrast` acima, que se mostraram **comuns às três instâncias da plataforma Atende.net** auditadas (Colombo, Pinhais, Araucária — Seção 5).

#### Página de Contato (`colombo_contato`, `.../fale-com-a-prefeitura-de-colombo/`)

**Achados da análise estrutural de HTML (09/06/2026):**

| Critério WCAG | Problema | Quantidade | Exemplos |
|---|---|---|---|
| 1.1.1 Conteúdo não textual | Imagens sem `alt` | 2 | Logo da prefeitura (2 versões) sem atributo `alt` |
| 3.3.2 Rótulos e instruções | Seletor de mês sem `<label>` | 1 | `<select>` com opções "junho 2026" sem label associado |
| 2.4.4 Finalidade do link | Links sociais vazios | 5 | Links Facebook, Instagram, YouTube sem texto visível |
| 4.1.2 Nome, função, valor | ARIA mínimo | 1 | Apenas o botão "Acessibilidade" possui `aria-label` |
| 1.3.1 Informação e relações | Headings sem hierarquia consistente | — | `<h3>` usados para notícias; título "FALE COM A PREFEITURA" sem tag semântica correta |

**Achados da auditoria axe-core (10/06/2026):**

| Regra axe-core | Critério WCAG | Impacto | Nós |
|---|---|---|---|
| `color-contrast` | 1.4.3 | serious | 3 |
| `link-name` | 2.4.4 | serious | 11 |

**Total: 0 erros críticos, 3 de contraste, 11 outros alertas → 14 (Tabela Consolidada).** As 11 violações de `link-name` são consistentes com os 5 links sociais sem texto identificados na análise estrutural, somados a outros links de navegação sem nome acessível.

---

### 2.4 Pinhais — `https://atendenet.pinhais.pr.gov.br`

> Plataforma terceirizada Atende.net (Seção 1). As três páginas a seguir foram auditadas via axe-core com navegador completo (10/06/2026).

#### Página Inicial (`pinhais_portal`)

| Regra axe-core | Critério WCAG | Impacto | Nós | Exemplos de seletor |
|---|---|---|---|---|
| `aria-prohibited-attr` | 4.1.2 | serious | 33 | `.cloned.owl-item:nth-child(1) > .container-destaque > .area-compartilhamento > .area-compartilhamento > .social-ativo.share.fa-share-alt` (ícones de compartilhamento do carrossel) |
| `button-name` | 4.1.2 | critical | 1 | `.area-botao > button` ("Acessar no Sistema") |
| `color-contrast` | 1.4.3 | serious | 40 | `.text-content > span`, `.btn-acesso-usuario`, `.btn-cadastro` |
| `image-alt` | 1.1.1 | critical | 4 | `li[title="Radar da Transparência Pública"] > .card-conteudo-midia.default.card-conteudo > .card-background`, `li[title="Selo Diamante 2025"] > ...`, `.midia_card[title="Portal da Transparência"] > ...` |
| `link-name` | 2.4.4 | serious | 4 | mesmos 3 *cards* de destaque acima (link sem texto além da imagem de fundo) |

**Total: 5 erros críticos, 40 de contraste, 37 outros alertas → 82 (Tabela Consolidada).** Maior incidência de `color-contrast` entre as páginas iniciais dos cinco municípios.

#### Página de Serviços — Emissão de Guias (`pinhais_guias`)

`https://atendenet.pinhais.pr.gov.br/autoatendimento/servicos/e-emissao-de-guias`

| Regra axe-core | Critério WCAG | Impacto | Nós | Exemplos de seletor |
|---|---|---|---|---|
| `button-name` | 4.1.2 | critical | 1 | `.area-botao > button` |
| `color-contrast` | 1.4.3 | serious | 13 | `.text-content > span`, `label[for="pesquisa"]`, `li:nth-child(1) > .lk-politica-uso.anc-cookie` |

**Total: 1 erro crítico, 13 de contraste, 0 outros alertas → 14 (Tabela Consolidada).**

#### Página de Contato — Fale Conosco (`pinhais_faleconosco`)

`https://atendenet.pinhais.pr.gov.br/cidadao/pagina/fale-conosco`

| Regra axe-core | Critério WCAG | Impacto | Nós | Exemplos de seletor |
|---|---|---|---|---|
| `button-name` | 4.1.2 | critical | 5 | `.fa-print`, `.buttons-wrapper > .fa-facebook-square.fab`, `.fa-square-x-twitter` |
| `color-contrast` | 1.4.3 | serious | 43 | `.text-content > span`, `span > span:nth-child(3) > a[rel="noopener"][target="_blank"]`, `span > span:nth-child(2) > a` |

**Total: 5 erros críticos, 43 de contraste, 0 outros alertas → 48 (Tabela Consolidada).** Maior incidência de `color-contrast` entre as 15 páginas analisadas.

---

### 2.5 Araucária — `https://araucaria.atende.net`

> Plataforma terceirizada Atende.net (Seção 1); domínio institucional `araucaria.pr.gov.br` inacessível. As três páginas a seguir foram auditadas via axe-core com navegador completo (10/06/2026).

#### Página Inicial (`araucaria_portal`)

| Regra axe-core | Critério WCAG | Impacto | Nós | Exemplos de seletor |
|---|---|---|---|---|
| `aria-prohibited-attr` | 4.1.2 | serious | 33 | `.cloned.owl-item:nth-child(1) > .container-destaque > .area-compartilhamento > .area-compartilhamento > .social-ativo.share.fa-share-alt` |
| `color-contrast` | 1.4.3 | serious | 63 | `a[aria-label="Acesso à Informação"][title="Clique para acessar"][target="_blank"]`, `a[aria-label="Transparência"]`, `a[aria-label="Servidor"]` |

**Total: 0 erros críticos, 63 de contraste, 33 outros alertas → 96 (Tabela Consolidada).** Maior incidência de `color-contrast` entre as páginas iniciais dos cinco municípios. **Adicionalmente**, a navegação por teclado revelou uma **armadilha de teclado (critério 2.1.2)** nesta página — ver Seção 3.

#### Página de Serviços — IPTU 2026 (`araucaria_iptu`)

`https://araucaria.atende.net/cidadao/pagina/iptu-2026`

| Regra axe-core | Critério WCAG | Impacto | Nós | Exemplos de seletor |
|---|---|---|---|---|
| `button-name` | 4.1.2 | critical | 4 | `.fa-print`, `.buttons-wrapper > .fa-facebook-square.fab`, `.fa-square-x-twitter` |
| `color-contrast` | 1.4.3 | serious | 21 | `a[aria-label="Acesso à Informação"][title="Clique para acessar"][target="_blank"]`, `a[aria-label="Transparência"]`, `a[aria-label="Servidor"]` |

**Total: 4 erros críticos, 21 de contraste, 0 outros alertas → 25 (Tabela Consolidada).**

#### Página de Contato — Ouvidoria (`araucaria_ouvidoria`)

`https://araucaria.atende.net/subportal/ouvidoria-subportal`

| Regra axe-core | Critério WCAG | Impacto | Nós | Exemplos de seletor |
|---|---|---|---|---|
| `aria-prohibited-attr` | 4.1.2 | serious | 5 | `tbody:nth-child(2) > tr > td:nth-child(1) > div > .miniatura-arquivo[tab-index="0"][aria-label="Anexo: undefined"]` (e mais 2 análogos) |
| `color-contrast` | 1.4.3 | serious | 13 | `a[aria-label="Portal do Cidadão"]`, `a[aria-label="Acessibilidade"]`, `.titulo` |
| `link-name` | 2.4.4 | serious | 5 | `tbody:nth-child(2) > tr > td:nth-child(3) > .icon-dwnl.fa-download.fas` (e mais 2 análogos) |

**Total: 0 erros críticos, 13 de contraste, 10 outros alertas → 23 (Tabela Consolidada).**

> **Achado específico:** os ícones de anexo de arquivo possuem `aria-label="Anexo: undefined"` — o texto literal "undefined" (valor de variável de programação não preenchido) é exposto a leitores de tela, em vez do nome real do arquivo anexado.

---

## 3. Tabela Consolidada (= Tabela 1 do relatório)

| Site / Página | HTTP | Erros críticos | Erros de contraste | Outros alertas | Total |
|---|---|---|---|---|---|
| Curitiba — Inicial | 200 | 15 | 8 | 14 | 37 |
| Curitiba — Serviços | 200 | 0 | 9 | 11 | 20 |
| Curitiba — Contato¹ | 200 | 0 | 1 | 0 | 1 |
| SJP — Inicial | 200 | 4 | 8 | 3 | 15 |
| SJP — Serviços | 200 | 11 | 5 | 2 | 18 |
| SJP — Contato | 200 | 0 | 6 | 2 | 8 |
| Colombo — Inicial | 200 | 0 | 0 | 33 | 33 |
| Colombo — Serviços | 200 | 1 | 10 | 27 | 38 |
| Colombo — Contato | 200 | 0 | 3 | 11 | 14 |
| Pinhais — Inicial | 200 | 5 | 40 | 37 | 82 |
| Pinhais — Serviços | 200 | 1 | 13 | 0 | 14 |
| Pinhais — Contato | 200 | 5 | 43 | 0 | 48 |
| Araucária — Inicial | 200 | 0 | 63 | 33 | 96 |
| Araucária — Serviços | 200 | 4 | 21 | 0 | 25 |
| Araucária — Contato | 200 | 0 | 13 | 10 | 23 |
| **TOTAL (15 páginas)** | — | **40** | **243** | **189** | **472** |

¹ Não foi localizada página de ouvidoria/contato funcional no domínio oficial de Curitiba (Seção 1).

**Legenda:**
- **Erros críticos**: violações de impacto *critical* — majoritariamente `image-alt` (1.1.1), `button-name` (4.1.2) e `aria-required-children` (1.3.1).
- **Erros de contraste**: violações de `color-contrast` (1.4.3, nível AA).
- **Outros alertas**: violações de impacto *serious*/*moderate* — `link-name` (2.4.4), `frame-title` (2.4.1), `aria-prohibited-attr` (4.1.2), `nested-interactive` (4.1.2).

Fonte: auditoria axe-core 4.x via Microsoft Edge/Playwright, 10/06/2026.

---

## 4. Navegação por Teclado e Árvore de Acessibilidade (proxy NVDA)

Metodologia: 12 pressionamentos consecutivos da tecla **Tab** a partir do carregamento da página inicial de cada município, registrando para cada elemento focalizado: tag HTML, `role` ARIA, texto/nome acessível, `href`, presença de indicador visual de foco (`outline`/`box-shadow`). Adicionalmente, extraiu-se a árvore de acessibilidade completa (`Accessibility.getFullAXTree` via CDP) para contar nós totais e elementos interativos sem nome acessível.

### 4.1 Síntese (= Quadro 4 do relatório)

| Município | Link "pular conteúdo" | Sem foco visível | Nós na árvore A11y | Sem nome acessível |
|---|---|---|---|---|
| Curitiba | Presente, mas é o 11º elemento | 11/12 | 698 | 6 |
| São José dos Pinhais | Ausente | 10/12 | 482 | 3 |
| Colombo | Presente, 1º elemento, com foco visível | 10/12 | 1.399 | 30 |
| Pinhais | Ausente | 7/12 | 2.245 | 4 |
| Araucária | Ausente | 2/12* | 2.347 | 0 |

\* Foco preso em ciclo de 6 elementos (armadilha de teclado, critério 2.1.2) — ver Seção 4.2.5.

### 4.2 Sequência detalhada de tabulação (12 primeiros Tabs), por município

#### 4.2.1 Curitiba — `https://www.curitiba.pr.gov.br/`

`skipLink=False | alvos únicos de foco=11 | sem indicador de foco=11/12 | árvore: 698 nós, 6 sem nome acessível`

| Tab | Elemento | Texto / Nome | `href` | Foco visível |
|---|---|---|---|---|
| 1 | `<button>` | "Abrir menu de acessibilidade" | — | **Sim** (outline 0px, *shadow*) |
| 2 | `<a>` | "Acessibilidade" | `/conteudo/acessibilidade` | Não |
| 3 | `<a>` | "Portal da Transparência" | `transparencia.curitiba.pr.gov.br` | Não |
| 4 | `<a>` | "Curitiba-Ouve" | `/lei13460/` | Não |
| 5 | `<a>` | "156" | `156.curitiba.pr.gov.br` | Não |
| 6 | `<a>` | "Acesso à informação" | `/leiacessoinformacao` | Não |
| 7 | `<a>` | "Secretarias" | `/secretarias/` | Não |
| 8 | `<a>` | *(sem texto)* | `curitiba.pr.gov.br` (logo) | Não |
| 9 | `<a>` | *(sem texto)* | `curitiba.pr.gov.br` (logo) | Não |
| 10 | `<a>` | "Entrar" | `/Login` | Não |
| 11 | `<a>` | **"Ir para o conteúdo"** | `#acessibilidade` | Não |
| 12 | `<input>` | *(campo de busca)* | — | Não |

#### 4.2.2 São José dos Pinhais — `https://www.sjp.pr.gov.br/`

`skipLink=False | alvos únicos de foco=12 | sem indicador de foco=10/12 | árvore: 482 nós, 3 sem nome acessível`

| Tab | Elemento | Texto / Nome | `href` | Foco visível |
|---|---|---|---|---|
| 1 | `<a>` | "Instagram" | `instagram.com/prefeiturasjp/` | Não |
| 2 | `<a>` | "Facebook-f" | `facebook.com/Prefeitura.SJP` | Não |
| 3 | `<a>` | "Youtube" | `youtube.com/user/tvprefeiturasjp` | Não |
| 4 | `<a>` | "Acessibilidade" | `/acessibilidade/` | Não |
| 5 | `<button>` | "Aumentar texto" | — | Não |
| 6 | `<button>` | "Diminuir texto" | — | Não |
| 7 | `<button>` | "Tamanho padrão" | — | Não |
| 8 | `<button>` | "Alto contraste" | — | Não |
| 9 | `<button>` | "Ativar Leitura de Texto" | — | Não |
| 10 | `<a>` | *(sem texto, logo)* | `sjp.pr.gov.br` | Não |
| 11 | `<button>` | "O que você procura?" | — | **Sim** |
| 12 | `<a>` | "Portal da Transparência" | `transparencia.sjp.pr.gov.br/...` | **Sim** |

Nenhum link "pular para o conteúdo" entre os 12 primeiros elementos. Os 9 primeiros (3 ícones sociais + "Acessibilidade" + 5 botões da barra de acessibilidade) não exibem foco visível.

#### 4.2.3 Colombo — `https://prefeitura.colombo.pr.gov.br/`

`skipLink=True | alvos únicos de foco=12 | sem indicador de foco=10/12 | árvore: 1.399 nós, 30 sem nome acessível`

| Tab | Elemento | Texto / Nome | `href` | Foco visível |
|---|---|---|---|---|
| 1 | `<a role="link">` | **"Pular para o conteúdo"** | `#content` | **Sim** (outline 5px, *shadow*) |
| 2 | `<a role="link">` | "Acessibilidade" | `javascript:void(0);` | **Sim** (outline 5px, *shadow*) |
| 3 | `<a role="link">` | "Aumentar Texto" | `#` | Não |
| 4 | `<a role="link">` | "Diminuir texto" | `#` | Não |
| 5 | `<a role="link">` | "Escala de cinza" | `#` | Não |
| 6 | `<a role="link">` | "Alto Contraste" | `#` | Não |
| 7 | `<a role="link">` | "Contraste Negativo" | `#` | Não |
| 8 | `<a role="link">` | "Fundo claro" | `#` | Não |
| 9 | `<a role="link">` | "Links Underline" | `#` | Não |
| 10 | `<a role="link">` | "Fonte legível" | `#` | Não |
| 11 | `<a role="link">` | "Reiniciar" | `#` | Não |
| 12 | `<a role="link">` | "Mapa do site" | `/mapa-do-site/` | Não |

Único portal com *skip link* funcional como 1º elemento e indicador de foco visível (também no 2º elemento). Os 9 itens seguintes da barra de acessibilidade usam `href="#"` e não exibem foco visível.

#### 4.2.4 Pinhais — `https://atendenet.pinhais.pr.gov.br/`

`skipLink=False | alvos únicos de foco=12 | sem indicador de foco=7/12 | árvore: 2.245 nós, 4 sem nome acessível`

| Tab | Elemento | Texto / Nome | `href` | Foco visível |
|---|---|---|---|---|
| 1 | `<a>` | "Acesso à Informação" | `pinhais.atende.net/cidadao/acesso-informacao` | **Sim** (outline auto 1px) |
| 2 | `<a>` | "Transparência" | `pinhais.atende.net/transparencia` | **Sim** |
| 3 | `<a>` | "Mapa do Site" | `pinhais.atende.net/cidadao/mapa-do-site` | **Sim** |
| 4 | `<button>` | "Aumentar Fonte" | — | Não |
| 5 | `<button>` | "Diminuir Fonte" | — | Não |
| 6 | `<button>` | "Restaurar Fonte" | — | Não |
| 7 | `<button>` | "Alto Contraste" | — | Não |
| 8 | `<button>` | "VLibras" | — | Não |
| 9 | `<a>` | "Acessibilidade" | — | **Sim** |
| 10 | `<a>` | "Mapa do Site" | `/cidadao/mapa-do-site` | **Sim** |
| 11 | `<button>` | "Acessar no Sistema" | — | Não |
| 12 | `<button>` | "Abrir Menu" | — | Não |

Melhor proporção de foco visível entre os portais sem armadilha de teclado (5/12 com foco visível). Nenhum *skip link* identificado.

#### 4.2.5 Araucária — `https://araucaria.atende.net/` — **ARMADILHA DE TECLADO (2.1.2)**

`skipLink=False | alvos únicos de foco=6 (ciclo fechado) | sem indicador de foco=2/12 | árvore: 2.347 nós, 0 sem nome acessível`

| Tab | Elemento | Texto / Nome | Foco visível |
|---|---|---|---|
| 1 | `<i>` | "Fechar Avisos" | **Sim** |
| 2 | `<a>` | *(sem texto)* → `/cidadao/pagina/iptu-2026` | **Sim** |
| 3 | `<img>` | "IPTU 2026" | **Sim** |
| 4 | `<input>` | *(checkbox, valor "on")* | **Sim** |
| 5 | `<label>` | "Não exibir este aviso novamente." | **Sim** |
| 6 | `<div role="dialog">` | "Avisos do Portal do Cidadão" | Não |
| 7 | `<i>` | "Fechar Avisos" *(repete Tab 1)* | **Sim** |
| 8 | `<a>` | *(repete Tab 2)* | **Sim** |
| 9 | `<img>` | "IPTU 2026" *(repete Tab 3)* | **Sim** |
| 10 | `<input>` | *(repete Tab 4)* | **Sim** |
| 11 | `<label>` | *(repete Tab 5)* | **Sim** |
| 12 | `<div role="dialog">` | *(repete Tab 6)* | Não |

A partir do carregamento da página, o foco entra imediatamente no modal de avisos "Avisos do Portal do Cidadão" (chamada "IPTU 2026", *checkbox* "Não exibir este aviso novamente") e percorre repetidamente o **mesmo ciclo de 6 elementos**, sem nunca alcançar o menu principal, o conteúdo da página ou o rodapé. **Violação direta do critério 2.1.2 (Sem Armadilha de Teclado), nível A** — a única forma de prosseguir é localizar e ativar visualmente o ícone "Fechar Avisos" (Tab 1/7), o que não está ao alcance de um usuário que dependa exclusivamente do teclado e não tenha indicação sonora/visual da função desse ícone.

---

## 5. Padrões Transversais de Falha (= Quadro 5 do relatório)

| Princípio WCAG | Critério | Padrão de falha | Municípios afetados |
|---|---|---|---|
| Perceptível | 1.4.3 | Contraste insuficiente entre texto/elemento e plano de fundo | Curitiba, SJP, Colombo, Pinhais, Araucária (5/5) |
| Operável | 2.4.4 | Links sem texto acessível (logotipos, ícones sociais, "Clique aqui") | Curitiba, SJP, Colombo, Pinhais, Araucária (5/5) |
| Robusto | 4.1.2 | Botões sem nome acessível (ícones de carrossel, impressão, redes sociais) | Curitiba, Colombo, Pinhais, Araucária (4/5) |
| Perceptível | 1.1.1 | Imagens/cards sem texto alternativo, inclusive na barra de acessibilidade | Curitiba, SJP, Colombo, Pinhais (4/5) |
| Robusto | 4.1.2 | `aria-prohibited-attr` — específico da plataforma Atende.net | Colombo, Pinhais, Araucária (3/5) |
| Operável | — | Indicador visual de foco do teclado ausente na maioria dos elementos | Curitiba, SJP, Colombo (3/5; Pinhais e Araucária parcialmente) |
| Perceptível | 1.3.1 | `aria-required-children`: papéis ARIA sem os filhos obrigatórios | SJP (1/5) |
| Operável | 2.1.2 | Armadilha de teclado: modal captura o foco em ciclo fechado | Araucária (1/5) |

**Achado de infraestrutura compartilhada — plataforma Atende.net:** Colombo (módulo de autoatendimento), Pinhais e Araucária (portais institucionais inteiros) são hospedados na mesma plataforma SaaS. O padrão `aria-prohibited-attr` é idêntico em forma e localização (ícones de compartilhamento do carrossel de destaques) nas três instâncias — 27 ocorrências em Colombo, 33 em Pinhais, 38 em Araucária (33 na página inicial + 5 na Ouvidoria) — indicando defeito do *template*/componente fornecido pela plataforma, não falha individual de cada prefeitura. Uma única correção do fornecedor beneficiaria simultaneamente os três municípios.

---

## 6. Referências cruzadas com o relatório final

| Conteúdo deste arquivo | Seção/Tabela correspondente em `relatorio.tex` |
|---|---|
| Seção 1 (Condições de acesso) | Seção 4.1, Quadro 3 (`qua:acesso`) |
| Seção 2.1 (Curitiba) | Seção 4.2.1, Tabela 2 (`tab:curitiba`) |
| Seção 2.2 (SJP) | Seção 4.2.2, Tabela 3 (`tab:sjp`) |
| Seção 2.3 (Colombo) | Seção 4.2.3, Tabela 4 (`tab:colombo`) |
| Seção 2.4 (Pinhais) | Seção 4.2.4, Tabela 5 (`tab:pinhais`) |
| Seção 2.5 (Araucária) | Seção 4.2.5, Tabela 6 (`tab:araucaria`) |
| Seção 3 (Tabela Consolidada) | Seção 3.3, Tabela 1 (`tab:wave`) |
| Seção 4 (Teclado / Árvore A11y) | Seção 4.3, Quadro 4 (`qua:teclado`) |
| Seção 5 (Padrões transversais) | Seção 4.4, Quadro 5 (`qua:padroes`) |
