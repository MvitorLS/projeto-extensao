# 4 RESULTADOS E DISCUSSÕES

Esta seção apresenta os resultados obtidos por meio da varredura automatizada das páginas selecionadas, organizados por município e página analisada, seguidos de uma discussão comparativa dos padrões de falha identificados à luz das diretrizes WCAG 2.1 (W3C, 2018).

A coleta de dados foi realizada entre os dias 09 e 10 de junho de 2026 e abrangeu, para os cinco municípios selecionados, as três páginas definidas no escopo (inicial, serviço e contato), totalizando 15 páginas analisadas, auditadas com o motor axe-core via navegador automatizado (Microsoft Edge/Playwright). Os municípios de Curitiba, Pinhais e Araucária apresentaram impedimentos de acesso por meio de ferramentas simples de requisição HTTP (`curl`) durante a coleta inicial; a Seção 4.1 detalha como essas barreiras foram contornadas por meio de navegação automatizada com renderização completa de JavaScript.

## 4.1 Condições de Acesso aos Portais

Antes da análise de acessibilidade propriamente dita, verificou-se que nem todos os portais responderam de forma adequada às requisições de acesso, o que representa, em si, uma dimensão relevante do diagnóstico. O Quadro 3 sintetiza as condições observadas.

**Quadro 3 – Condições de acesso aos portais durante a coleta de dados**

| Município | Condição | Impacto para o cidadão |
|---|---|---|
| Curitiba | Bloqueio de requisições simples (`curl`, HTTP 403); acesso normal (HTTP 200) via navegador completo | Nenhum impacto direto ao usuário comum; possível impacto em auditorias automatizadas e mecanismos de busca |
| São José dos Pinhais | Acesso normal | Nenhum |
| Colombo | Redirecionamento para subdomínio (`prefeitura.colombo.pr.gov.br`) | Nenhum |
| Pinhais | Domínio oficial redireciona via JavaScript (~1s) para portal terceirizado `atendenet.pinhais.pr.gov.br` | Sem `<noscript>`: usuários/agentes sem JavaScript não acessam o portal |
| Araucária | Domínio oficial com certificado SSL inválido e sem rota válida; portal real hospedado em domínio totalmente distinto (`araucaria.atende.net`) | Barreira grave: navegador bloqueia o domínio oficial, e o domínio funcional não é descoberto a partir dele |

Fonte: Elaborado pelo autor (2026), com base em requisições HTTP (`curl`) e navegação automatizada (Microsoft Edge/Playwright).

O caso de Araucária merece destaque especial. O domínio oficial `www.araucaria.pr.gov.br` apresenta certificado SSL inválido (`ERR_TLS_CERT_ALTNAME_INVALID`), de modo que qualquer tentativa de acesso via HTTPS resulta em aviso de bloqueio de segurança emitido pelo navegador; mesmo contornando esse aviso, o servidor retorna mensagem de erro informando que "não é possível acessar o Atende.net através desse domínio". O portal efetivamente utilizado pela prefeitura está hospedado em `araucaria.atende.net` — domínio que não guarda relação nominal com `araucaria.pr.gov.br` e que não é referenciado a partir dele. Para cidadãos com menor familiaridade tecnológica — grupo que frequentemente inclui pessoas idosas, público com deficiência cognitiva ou usuários de dispositivos desatualizados —, tanto o aviso de segurança quanto a ausência de um caminho de descoberta para o portal real representam barreiras de acesso efetivas. Essa condição infringe indiretamente o princípio da **Robustez** do WCAG 2.1 (critério 4.1) e coloca o portal em desconformidade com os requisitos de segurança e disponibilidade exigidos pela legislação brasileira para sítios governamentais.

Observou-se ainda que, embora o domínio oficial de Curitiba retorne erro HTTP 403 para ferramentas de requisição simples como `curl` — mesmo com cabeçalhos que emulam um navegador —, o acesso por meio de um navegador automatizado completo (Microsoft Edge via Playwright) ocorreu normalmente (HTTP 200), tanto na página inicial quanto na carta de serviços. Esse comportamento sugere bloqueio baseado em *fingerprint* da requisição (possivelmente um *Web Application Firewall*), e não indisponibilidade real do portal para o cidadão comum; ainda assim, a prática pode prejudicar ferramentas de auditoria automatizada e mecanismos de busca que não emulem um navegador completo, com possíveis efeitos indiretos sobre a indexabilidade do conteúdo. Não foi localizada, dentro do domínio oficial de Curitiba, uma página de ouvidoria ou contato funcional: os endereços testados retornaram a página de erro padrão (HTTP 404, com status de resposta 200) do portal, motivo pelo qual a linha "Curitiba — Contato" da Tabela 1 apresenta valores residuais.

Já o caso de Pinhais revela uma migração completa da infraestrutura do portal institucional para a plataforma terceirizada Atende.net: o domínio oficial `www.pinhais.pr.gov.br` carrega uma página mínima que, após aproximadamente um segundo, redireciona via JavaScript para `atendenet.pinhais.pr.gov.br`. Não foi identificado mecanismo de *fallback* (como uma tag `<noscript>`) para usuários ou ferramentas que não executam JavaScript, o que caracteriza potencial violação do princípio de Robustez (4.1) do WCAG 2.1.

## 4.2 Resultados por Portal

### 4.2.1 Curitiba

A página inicial do portal de Curitiba apresentou o maior número de violações de impacto crítico entre os cinco municípios analisados (15 ao todo), conforme a Tabela 2.

**Tabela 2 – Erros de acessibilidade no portal de Curitiba**

| Critério WCAG 2.1 | Descrição da falha | Ocorrências |
|---|---|---|
| 1.1.1 — Conteúdo não textual | Imagens do carrossel "Guia Curitiba" (eventos) sem atributo `alt` | 8 |
| 4.1.2 — Nome, função, valor | Botões de navegação do carrossel principal (anterior/próximo) sem texto acessível | 7 |
| 1.4.3 — Contraste mínimo | Itens do menu superior (Acessibilidade, Transparência, Curitiba-Ouve, 156, Secretarias) com contraste insuficiente | 8 |
| 2.4.4 — Finalidade do link | Links sem texto: logotipo institucional (2 ocorrências, ambas apontando para a página inicial) e campo de busca sem rótulo | 11 |
| 2.4.1 — Ignorar blocos | `<iframe>` de conteúdo dinâmico incorporados sem atributo `title` | 2 |
| 4.1.2 — Nome, função, valor | Botão de leitura de página (`#ma-lerPaginaItem`) aninhado dentro de outro controle interativo | 1 |

Fonte: Elaborado pelo autor (2026), com base em auditoria axe-core.

As oito imagens do carrossel de eventos "Guia Curitiba" não possuem atributo `alt`, de modo que um usuário de leitor de tela não recebe qualquer informação sobre o conteúdo desses destaques. Da mesma forma, os sete botões de navegação do carrossel principal (setas "anterior" e "próximo") são implementados sem texto acessível, sendo anunciados por leitores de tela apenas como "botão", sem indicação de função — violação direta do critério 4.1.2.

A página da Carta de Serviços replicou nove das oito violações de contraste e dez das onze violações de `link-name` observadas na página inicial, além do mesmo problema de controle aninhado (`#ma-lerPaginaItem`), evidenciando que essas falhas decorrem do *template* (cabeçalho e menu) compartilhado entre as páginas do portal, e não de conteúdo específico de cada seção.

A auditoria de navegação por teclado (Etapa 2) revelou achado adicional relevante: o portal possui um link "Ir para o conteúdo" (`href="#acessibilidade"`), em conformidade com a recomendação do critério 2.4.1, porém esse link é apenas o **11º** elemento alcançado pela tecla Tab a partir do carregamento da página — atrás de itens como "Abrir menu de acessibilidade", "Portal da Transparência", "Curitiba-Ouve", "156", "Acesso à informação", "Secretarias", dois links do logotipo sem texto e "Entrar". Na prática, um usuário que dependa exclusivamente do teclado precisa pressionar Tab dez vezes antes de ter a opção de pular a barra superior, o que esvazia parcialmente a utilidade do recurso. Adicionalmente, 11 dos 12 elementos focalizáveis nessa sequência não exibem qualquer indicador visual de foco (contorno ou sombra), o que compromete a orientação de usuários com baixa visão que navegam por teclado.

### 4.2.2 São José dos Pinhais

A análise das páginas inicial e de contato do portal de São José dos Pinhais revelou padrões sistemáticos de não conformidade com os critérios WCAG 2.1, predominantemente relacionados ao princípio da **Perceptibilidade**. A Tabela 3 apresenta os erros identificados na página inicial.

**Tabela 3 – Erros de acessibilidade na página inicial de São José dos Pinhais**

| Critério WCAG 2.1 | Descrição da falha | Ocorrências |
|---|---|---|
| 1.1.1 — Conteúdo não textual | Imagens sem atributo `alt` (logo, botões A+/A-, ícone contraste, fotos de serviços) | 12 |
| 3.3.2 — Rótulos e instruções | Campo de busca sem `<label>` associado | 1 |
| 2.4.4 — Finalidade do link | Links vazios ou sem contexto ("Avançar", "Voltar", `<a href="#">`) | 7 |
| 4.1.2 — Nome, função, valor | Ausência completa de marcação ARIA | — |
| 1.3.1 — Informação e relações | Hierarquia de headings sem `<h1>` definido | — |

Fonte: Elaborado pelo autor (2026). Dados coletados via análise estrutural de HTML.

Entre as 12 imagens sem texto alternativo, encontram-se elementos de alta relevância semântica: o logotipo institucional da prefeitura, os botões de controle de tamanho de fonte (A+, A, A-) e o ícone de alto contraste — todos componentes da própria barra de acessibilidade do portal. A ironia desse achado é notável: os controles destinados a tornar o site mais acessível são, eles mesmos, inacessíveis a leitores de tela, pois não possuem descrição textual. Um usuário cego que utilize o NVDA, por exemplo, ouvirá apenas "link" ao navegar por esses botões, sem qualquer indicação de sua função.

A página de contato (Ouvidorias) replicou os mesmos padrões: 7 imagens sem `alt`, ausência de ARIA e hierarquia de headings indefinida, sugerindo que os problemas decorrem de decisões arquiteturais do sistema de gestão de conteúdo utilizado pelo portal, e não de falhas pontuais de implementação.

A auditoria axe-core (Tabela 1) acrescentou a essa análise 4 violações críticas da regra `aria-required-children` (critério 1.3.1) e 8 violações de contraste mínimo (critério 1.4.3, nível AA) na página inicial, além de 11 violações de `image-alt` na página de serviços (`financas.sjp.pr.gov.br`) — nenhuma delas perceptível por inspeção do HTML estático. A auditoria de navegação por teclado mostrou ainda que os primeiros nove elementos focalizáveis da página — três ícones de redes sociais, um link "Acessibilidade" e cinco botões da barra de acessibilidade (*Aumentar texto*, *Diminuir texto*, *Tamanho padrão*, *Alto contraste*, *Ativar Leitura de Texto*) — não exibem indicador visual de foco, totalizando 10 dos 12 elementos testados sem foco visível. Assim como observado para os atributos `alt`, a própria barra de acessibilidade do portal mostra-se, paradoxalmente, uma das áreas menos acessíveis ao teclado. Nenhum link "pular para o conteúdo" foi identificado entre os doze primeiros elementos focalizáveis.

### 4.2.3 Colombo

O portal de Colombo apresentou o conjunto mais amplo de tipos de falha entre os municípios analisados. Além dos erros estruturais comuns ao portal de São José dos Pinhais, foram identificadas violações adicionais relativas à operabilidade e à compreensibilidade do conteúdo. A Tabela 4 detalha os erros da página inicial.

**Tabela 4 – Erros de acessibilidade na página inicial de Colombo**

| Critério WCAG 2.1 | Descrição da falha | Ocorrências |
|---|---|---|
| 1.1.1 — Conteúdo não textual | Imagens sem `alt` (logo, ícones de serviços, redes sociais) | Múltiplas |
| 2.4.4 — Finalidade do link | Texto de link genérico "Clique aqui" | 10+ |
| 1.3.1 — Informação e relações | `<h3>` utilizados sem `<h1>` ou `<h2>` precedentes | — |
| 3.3.2 — Rótulos e instruções | Campo de busca sem `<label>` | 1 |
| 2.4.1 — Ignorar blocos | `<iframe>` incorporados sem atributo `title` | Sim |
| 4.1.2 — Nome, função, valor | Barra de acessibilidade dependente de JavaScript sem fallback | — |

Fonte: Elaborado pelo autor (2026). Dados coletados via análise estrutural de HTML.

O uso sistemático da expressão "Clique aqui" em mais de dez links distintos constitui uma violação direta do critério 2.4.4 do WCAG 2.1, que determina que o propósito de cada link deve ser determinável a partir do seu texto isoladamente. Para um usuário que navega por links utilizando leitor de tela — prática comum entre pessoas com deficiência visual —, ouvir repetidamente "Clique aqui, link" sem qualquer contexto torna a navegação no portal essencialmente inutilizável. Esse padrão é consistente com as 33 violações de `link-name` identificadas pela auditoria axe-core na página inicial (Tabela 1), majoritariamente associadas aos ícones de redes sociais do rodapé (`.a-facebook`, `.a-instagram`, `.a-youtube`) e confirmadas pela árvore de acessibilidade, que apontou 30 elementos interativos sem nome acessível em um total de 1.399 nós.

A página de autoatendimento de Colombo (hospedada na plataforma terceirizada Atende.net, em `colombo.atende.net`) foi auditada separadamente via axe-core, por se tratar de uma *Single Page Application* cujo conteúdo não está presente no HTML estático. Foram identificadas 27 violações da regra `aria-prohibited-attr` (critério 4.1.2) — atributos ARIA aplicados a elementos que não os admitem, fazendo com que leitores de tela possam ignorar ou interpretar incorretamente esses elementos — além de 10 violações de contraste mínimo (critério 1.4.3) e 1 botão sem nome acessível. Esse padrão de `aria-prohibited-attr` revelou-se comum à plataforma Atende.net como um todo, conforme discutido na Seção 4.4.

A página de contato de Colombo apresentou perfil menos crítico que a página inicial, com 2 imagens sem `alt`, 1 campo de formulário sem label e 5 links de redes sociais sem texto visível (consistente com as 11 violações de `link-name` reportadas na Tabela 1), mantendo, porém, os padrões de hierarquia de headings inconsistentes.

Em contraste com os demais municípios analisados, a página inicial de Colombo foi a única, entre as cinco, a apresentar um link "Pular para o conteúdo" (`href="#content"`) como primeiro elemento focalizável, exibindo indicador visual de foco (sombra) tanto nesse link quanto no item seguinte ("Acessibilidade") — prática alinhada ao critério 2.4.1 que poderia servir de referência aos demais portais. Entretanto, os nove elementos seguintes da barra de acessibilidade (*Aumentar Texto*, *Diminuir texto*, *Escala de cinza*, *Alto Contraste*, *Contraste Negativo*, *Fundo claro*, *Links Underline*, *Fonte legível*, *Reiniciar*) utilizam `href="#"` (âncoras vazias) e não exibem indicador de foco, repetindo o padrão observado nos demais portais.

### 4.2.4 Pinhais

O portal de Pinhais foi inteiramente migrado para a plataforma terceirizada Atende.net (`atendenet.pinhais.pr.gov.br`), para a qual o domínio institucional redireciona automaticamente (Seção 4.1). A Tabela 5 apresenta os erros identificados na página inicial, que totalizou 82 violações — o segundo maior valor entre os cinco municípios.

**Tabela 5 – Erros de acessibilidade no portal de Pinhais**

| Critério WCAG 2.1 | Descrição da falha | Ocorrências |
|---|---|---|
| 1.4.3 — Contraste mínimo | Textos e botões (*spans* de conteúdo, botões "Acessar no Sistema" e "Cadastro") com contraste insuficiente | 40 |
| 4.1.2 — Nome, função, valor | Ícones de compartilhamento em redes sociais no carrossel de destaques com atributos ARIA não permitidos | 33 |
| 1.1.1 — Conteúdo não textual | Cards de destaque ("Radar da Transparência", "Selo Diamante 2025", "Portal da Transparência") sem `alt` | 4 |
| 2.4.4 — Finalidade do link | Cards de destaque sem texto acessível (apenas imagem de fundo) | 4 |
| 4.1.2 — Nome, função, valor | Botão "Acessar no Sistema" sem texto acessível | 1 |

Fonte: Elaborado pelo autor (2026), com base em auditoria axe-core.

A página inicial apresentou 40 falhas de contraste mínimo (critério 1.4.3) — a maior incidência desse critério entre as páginas iniciais dos cinco municípios — distribuídas por elementos textuais e botões de acesso e cadastro, além de 33 violações de `aria-prohibited-attr` no carrossel de destaques, mesmo padrão observado em Araucária (Seção 4.2.5) por tratar-se da mesma plataforma.

As páginas de serviço (emissão de guias) e de contato (Fale Conosco) mantiveram o padrão de contraste insuficiente, com 13 e 43 ocorrências respectivamente — esta última a maior incidência de contraste entre as 15 páginas analisadas. Na página de Fale Conosco, 5 botões de impressão e compartilhamento em redes sociais (`.fa-print`, `.fa-facebook-square`, `.fa-square-x-twitter`) não possuem texto acessível, sendo anunciados por leitores de tela apenas como "botão".

A navegação por teclado revelou o melhor desempenho relativo entre os portais com barra de acessibilidade tradicional: os três primeiros itens focalizáveis ("Acesso à Informação", "Transparência", "Mapa do Site") preservam o contorno de foco padrão do navegador (apenas 7 dos 12 elementos testados ficaram sem indicador de foco, a menor proporção entre os portais não afetados por armadilha de teclado). Ainda assim, os cinco botões da barra de acessibilidade que os sucedem (*Aumentar Fonte*, *Diminuir Fonte*, *Restaurar Fonte*, *Alto Contraste*, *VLibras*) não exibem indicador de foco, e nenhum link "pular para o conteúdo" foi identificado nos doze primeiros elementos focalizáveis.

### 4.2.5 Araucária

O portal de Araucária está hospedado, assim como o de Pinhais, na plataforma terceirizada Atende.net (`araucaria.atende.net`); o domínio institucional `araucaria.pr.gov.br` encontra-se totalmente inacessível (Seção 4.1). A Tabela 6 resume os principais achados.

**Tabela 6 – Erros de acessibilidade no portal de Araucária**

| Critério WCAG 2.1 | Descrição da falha | Ocorrências |
|---|---|---|
| 2.1.2 — Sem armadilha de teclado | Modal de avisos captura o foco do teclado em ciclo fechado, impedindo acesso ao restante da página | — |
| 1.4.3 — Contraste mínimo | Links do menu superior ("Acesso à Informação", "Transparência", "Servidor") e demais elementos com contraste insuficiente (página inicial) | 63 |
| 4.1.2 — Nome, função, valor | Ícones de compartilhamento do carrossel com atributos ARIA não permitidos (página inicial) | 33 |
| 4.1.2 — Nome, função, valor | Botões de impressão/compartilhamento sem texto acessível (página de IPTU) | 4 |
| 4.1.2 — Nome, função, valor | Anexos da Ouvidoria com `aria-label="Anexo: undefined"` (valor literal "undefined") | 5 |
| 2.4.4 — Finalidade do link | Ícones de download de anexos sem texto acessível (Ouvidoria) | 5 |

Fonte: Elaborado pelo autor (2026), com base em auditoria axe-core e navegação por teclado.

Entre os portais analisados, Araucária apresentou o maior número de violações do critério 1.4.3 na página inicial — 63 ocorrências, incluindo os principais links de navegação institucional ("Acesso à Informação", "Transparência", "Servidor") — além do mesmo padrão de 33 violações `aria-prohibited-attr` no carrossel de destaques observado em Pinhais (Seção 4.4).

Na página da Ouvidoria, identificou-se um achado peculiar: os ícones de anexo de arquivos possuem o atributo `aria-label="Anexo: undefined"`, expondo a um leitor de tela o texto literal "undefined" — sintoma de uma variável de programação (provavelmente o nome do arquivo) que não foi preenchida corretamente antes de ser inserida no atributo. Trata-se de exemplo concreto de como falhas de implementação no *front-end* se traduzem diretamente em informação incorreta para usuários de tecnologia assistiva.

O achado mais grave, contudo, foi identificado pela auditoria de navegação por teclado: ao carregar a página inicial, um modal de avisos ("Avisos do Portal do Cidadão", com a chamada de destaque "IPTU 2026" e a opção "Não exibir este aviso novamente") captura o foco do teclado em um **ciclo fechado de seis elementos** — dos doze pressionamentos de Tab testados, o foco percorreu repetidamente a mesma sequência (ícone "Fechar Avisos", link da imagem, imagem "IPTU 2026", *checkbox* "não exibir novamente", rótulo e o próprio contêiner do modal), sem nunca alcançar o menu principal, o conteúdo da página ou o rodapé. Trata-se de uma **armadilha de teclado** (*keyboard trap*), violação direta do critério **2.1.2** do WCAG 2.1 — nível A, o nível mínimo de conformidade exigido pela legislação. Para um usuário que dependa exclusivamente do teclado, esse modal **impede completamente o uso do portal**: a única forma de fechá-lo é localizar e ativar o ícone "Fechar Avisos" (o primeiro elemento do ciclo), o que pode não ser evidente sem suporte visual ou auditivo adequado. Esse achado, isoladamente, já caracteriza descumprimento do nível mínimo (A) de conformidade ao WCAG 2.1 e, por extensão, do Art. 63 da Lei Brasileira de Inclusão da Pessoa com Deficiência (Lei nº 13.146/2015).

## 4.3 Navegação por Teclado: Síntese Comparativa

O Quadro 4 consolida os resultados da auditoria automatizada de navegação por teclado (Etapa 2) para a página inicial dos cinco portais.

**Quadro 4 – Síntese da auditoria de navegação por teclado (12 primeiros elementos focalizáveis, página inicial)**

| Município | Link "pular conteúdo" | Sem foco visível | Observação |
|---|---|---|---|
| Curitiba | Presente, mas é o 11º elemento | 11/12 | Barra superior precede o link de pular |
| SJP | Ausente | 10/12 | Barra de acessibilidade (9 itens) sem foco visível |
| Colombo | Presente, 1º elemento, com foco visível | 10/12 | Único portal com boa prática de *skip link* |
| Pinhais | Ausente | 7/12 | Melhor proporção de foco visível entre os 5 |
| Araucária | Ausente | 2/12* | *Foco preso em ciclo de 6 elementos (armadilha de teclado) |

Fonte: Elaborado pelo autor (2026), com base em automação de navegação por teclado (Playwright/Edge), 12 pressionamentos de Tab a partir do carregamento da página, 10 jun. 2026.

A síntese evidencia que a ausência de indicador visual de foco é a norma, e não a exceção, entre os portais analisados: em quatro dos cinco municípios, mais de 80% dos primeiros elementos focalizáveis não exibem qualquer realce ao receber o foco do teclado, dificultando a orientação de usuários com baixa visão ou deficiência motora que dependem do teclado para navegar. Chama atenção que, em três municípios (Curitiba, São José dos Pinhais e Pinhais), os primeiros elementos alcançados pela tecla Tab pertencem à própria barra de acessibilidade do portal — recurso destinado a ampliar a inclusão que, paradoxalmente, está entre os menos acessíveis ao teclado. Colombo destaca-se positivamente por ser o único portal a apresentar um link "Pular para o conteúdo" como primeiro elemento da página, com indicador de foco visível, prática que deveria ser adotada como referência pelos demais municípios.

Complementarmente, a extração da árvore de acessibilidade da página inicial de cada portal — estrutura de dados consultada por leitores de tela como o NVDA — quantificou o número de elementos interativos (botões, links, campos) expostos sem nome acessível: 6 em Curitiba, 3 em São José dos Pinhais, 30 em Colombo, 4 em Pinhais e 0 em Araucária, em um universo de 482 a 2.347 nós por página. Esses números são consistentes com as violações de `link-name` e `button-name` identificadas pelo axe-core (Tabela 1) e representam, na prática, controles que um usuário do NVDA ouviria apenas como "link" ou "botão", sem qualquer pista sobre sua função.

## 4.4 Padrões Transversais de Falha

A análise comparativa dos cinco portais permitiu identificar padrões de falha que se repetem de forma sistemática, independentemente do município, sugerindo que os problemas de acessibilidade são estruturais e não isolados. O Quadro 5 organiza esses padrões por princípio WCAG, indicando os municípios em que cada padrão foi observado.

**Quadro 5 – Padrões transversais de falha identificados nos portais analisados**

| Princípio WCAG | Critério | Padrão de falha | Municípios afetados |
|---|---|---|---|
| Perceptível | 1.4.3 | Contraste insuficiente entre texto/elemento e plano de fundo | Curitiba, SJP, Colombo, Pinhais, Araucária (5/5) |
| Operável | 2.4.4 | Links sem texto acessível (logotipos, ícones sociais, "Clique aqui") | Curitiba, SJP, Colombo, Pinhais, Araucária (5/5) |
| Robusto | 4.1.2 | Botões sem nome acessível (ícones de carrossel, impressão, redes sociais) | Curitiba, Colombo, Pinhais, Araucária (4/5) |
| Perceptível | 1.1.1 | Imagens/cards sem texto alternativo, inclusive elementos da barra de acessibilidade | Curitiba, SJP, Colombo, Pinhais (4/5) |
| Robusto | 4.1.2 | Atributos ARIA não permitidos (`aria-prohibited-attr`), específico da plataforma Atende.net | Colombo, Pinhais, Araucária (3/5) |
| Operável | — | Indicador visual de foco do teclado ausente na maioria dos elementos | Curitiba, SJP, Colombo (3/5; Pinhais e Araucária parcialmente) |
| Perceptível | 1.3.1 | `aria-required-children`: papéis ARIA sem os filhos obrigatórios | SJP (1/5) |
| Operável | 2.1.2 | Armadilha de teclado: modal captura o foco em ciclo fechado | Araucária (1/5) |

Fonte: Elaborado pelo autor (2026), com base em auditoria axe-core e navegação por teclado.

Esses resultados alinham-se com os achados de Silva (2022), que em estudo sobre portais governamentais brasileiros identificou os critérios 1.1.1 (texto alternativo) e 2.4.4 (finalidade do link) como as violações mais prevalentes em sítios do setor público. O presente estudo confirma esse padrão no contexto específico da Região Metropolitana de Curitiba — agora com os cinco municípios de maior população — sugerindo que a baixa conformidade com WCAG em portais governamentais municipais é um fenômeno sistêmico no Brasil. Adicionalmente, a cobertura do critério 1.4.3 (contraste mínimo), viabilizada pela auditoria axe-core, revelou que esse é o padrão de falha mais universal entre os cinco portais — presente nas 15 páginas analisadas — achado que análises baseadas exclusivamente em inspeção estrutural do HTML, como a relatada por Silva (2022), tipicamente não capturam.

Um achado adicional, não previsto no desenho original deste estudo, diz respeito à dependência de infraestrutura terceirizada: três dos cinco municípios analisados — Colombo (apenas no módulo de autoatendimento), Pinhais e Araucária (portais institucionais inteiros) — têm seus serviços digitais hospedados na mesma plataforma *Software as a Service*, a Atende.net. O padrão `aria-prohibited-attr` — 27 ocorrências em Colombo, 33 em Pinhais e 38 em Araucária (33 na página inicial e 5 na Ouvidoria) — é idêntico em forma e localização (ícones de compartilhamento do carrossel de destaques) nas três instâncias, indicando tratar-se de defeito do *template* ou componente de *front-end* fornecido pela própria plataforma, e não de falha cometida individualmente por cada prefeitura. Esse achado tem implicação prática relevante: uma única correção realizada pelo fornecedor da plataforma teria potencial de melhorar simultaneamente a acessibilidade de múltiplos portais municipais, evidenciando o papel estratégico que requisitos de acessibilidade em contratos de fornecimento de tecnologia para o setor público podem desempenhar.

Do ponto de vista do impacto real sobre o usuário, as falhas identificadas comprometem especialmente a experiência de três perfis de usuários com deficiência:

- **Usuários com deficiência visual** que utilizam leitores de tela (como o NVDA): a ausência de textos alternativos, de nomes acessíveis em links/botões e de marcação ARIA correta torna a navegação desorientada e incompleta. Em São José dos Pinhais e Colombo, os próprios recursos de acessibilidade (controle de fonte, alto contraste) e ícones de redes sociais são inacessíveis via leitor de tela.

- **Usuários com deficiência motora** que navegam exclusivamente pelo teclado: links vazios interrompem o fluxo de navegação por Tab, a ausência de indicador de foco dificulta a orientação, e no caso extremo de Araucária uma armadilha de teclado (Seção 4.2.5) impede integralmente o uso do portal.

- **Usuários com baixa visão ou deficiência cognitiva**: o contraste insuficiente — presente em 100% das páginas analisadas — e a hierarquia de headings/ARIA quebrada prejudicam a leitura e a compreensão da estrutura da página.

Diante do disposto no Art. 63 da Lei Brasileira de Inclusão da Pessoa com Deficiência (Lei nº 13.146/2015), que determina obrigatoriedade de acessibilidade nos sítios mantidos por órgãos de governo, os resultados obtidos evidenciam que os portais analisados encontram-se em desconformidade legal, além de representarem barreiras concretas ao exercício da cidadania digital por parte da população com deficiência.
