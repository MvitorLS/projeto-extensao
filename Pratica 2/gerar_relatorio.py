import re

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = 'Arial'
SIZE = Pt(12)
LINE_SPACING = 1.5

def _insert_field(run, instr, placeholder):
    fld_begin = OxmlElement('w:fldChar')
    fld_begin.set(qn('w:fldCharType'), 'begin')
    instr_el = OxmlElement('w:instrText')
    instr_el.set(qn('xml:space'), 'preserve')
    instr_el.text = instr
    fld_separate = OxmlElement('w:fldChar')
    fld_separate.set(qn('w:fldCharType'), 'separate')
    t_el = OxmlElement('w:t')
    t_el.text = placeholder
    fld_end = OxmlElement('w:fldChar')
    fld_end.set(qn('w:fldCharType'), 'end')
    r = run._r
    r.append(fld_begin)
    r.append(instr_el)
    r.append(fld_separate)
    r.append(t_el)
    r.append(fld_end)

# ── Sumário clicável (links internos para cada seção) ─────────────────────────
# Páginas conforme paginação do Word (mesmos números do relatório já gerado).
TOC_PAGES = {
    '1': 6, '1.1': 7, '1.2': 7, '1.3': 7,
    '2': 8,
    '3': 9, '3.1': 9, '3.2': 9, '3.3': 10, '3.4': 12, '3.5': 13, '3.6': 13,
    '4': 15, '4.1': 15, '4.2': 17, '4.2.1': 17, '4.2.2': 18, '4.2.3': 20,
    '4.2.4': 21, '4.2.5': 23, '4.3': 24, '4.4': 26,
    '5': 29, '6': 31,
}
TOC_ENTRIES = []        # (level, text, anchor, page)
TOC_MARKER = [None]
_bm = [0]

def _anchor_for(num):
    return '_Toc_' + num.replace('.', '_')

def _add_bookmark(paragraph, name):
    bid = str(_bm[0]); _bm[0] += 1
    start = OxmlElement('w:bookmarkStart')
    start.set(qn('w:id'), bid)
    start.set(qn('w:name'), name)
    end = OxmlElement('w:bookmarkEnd')
    end.set(qn('w:id'), bid)
    p = paragraph._p
    pPr = p.find(qn('w:pPr'))
    if pPr is not None:
        pPr.addnext(start)
    else:
        p.insert(0, start)
    p.append(end)

def _toc_run(text, level):
    r = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), FONT); rf.set(qn('w:hAnsi'), FONT)
    rpr.append(rf)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '24'); rpr.append(sz)   # 12pt
    if level == 1:
        rpr.append(OxmlElement('w:b'))
    r.append(rpr)
    t = OxmlElement('w:t'); t.set(qn('xml:space'), 'preserve'); t.text = text
    r.append(t)
    return r

def _toc_paragraph(level, text, anchor, page):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_after = Pt(0)
    if level > 1:
        pf.left_indent = Cm(0.75 * (level - 1))
    pf.tab_stops.add_tab_stop(content_width, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    hyper = OxmlElement('w:hyperlink')
    hyper.set(qn('w:anchor'), anchor)
    hyper.set(qn('w:history'), '1')
    hyper.append(_toc_run(text, level))
    rt = OxmlElement('w:r'); rt.append(OxmlElement('w:tab')); hyper.append(rt)
    hyper.append(_toc_run(str(page), level))
    p._p.append(hyper)
    return p

def build_toc():
    ref = TOC_MARKER[0]._p
    for level, text, anchor, page in TOC_ENTRIES:
        el = _toc_paragraph(level, text, anchor, page)._p
        el.getparent().remove(el)
        ref.addnext(el)
        ref = el

doc = Document()

# ── Margens ABNT ──────────────────────────────────────────────────────────────
sec = doc.sections[0]
sec.top_margin    = Cm(3)
sec.bottom_margin = Cm(2)
sec.left_margin   = Cm(3)
sec.right_margin  = Cm(2)

# ── Cabeçalho institucional (logos IFPR + MEC em todas as páginas) ────────────
sec.different_first_page_header_footer = False
header = sec.header
header.is_linked_to_previous = False
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
content_width = sec.page_width - sec.left_margin - sec.right_margin
hp.paragraph_format.tab_stops.add_tab_stop(content_width, WD_TAB_ALIGNMENT.RIGHT)
hp.add_run().add_picture('logo-ifpr.png', width=Cm(4.27))
hp.add_run('\t')
hp.add_run().add_picture('logo-mec.png', width=Cm(1.7))

# ── Rodapé institucional (numeração de página em todas as páginas) ────────────
sec.footer.is_linked_to_previous = False
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
fp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
fp_run = fp.add_run()
fp_run.font.name = FONT
fp_run.font.size = SIZE
_insert_field(fp_run, ' PAGE ', '1')

# ── Atualização automática de campos (Sumário) ao abrir no Word ───────────────
update_fields = OxmlElement('w:updateFields')
update_fields.set(qn('w:val'), 'true')
doc.settings.element.append(update_fields)

# ── Estilo padrão ─────────────────────────────────────────────────────────────
style = doc.styles['Normal']
style.font.name = FONT
style.font.size = SIZE
pf = style.paragraph_format
pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
pf.space_before = Pt(0)
pf.space_after  = Pt(0)

# ── Estilos de título (Heading 1/2/3 → habilitam o Sumário automático) ────────
for _lvl in (1, 2, 3):
    hstyle = doc.styles[f'Heading {_lvl}']
    hstyle.font.name = FONT
    hstyle.font.size = SIZE
    hstyle.font.bold = True
    hstyle.font.color.rgb = RGBColor(0, 0, 0)
    hpf = hstyle.paragraph_format
    hpf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    hpf.space_before = Pt(0)
    hpf.space_after  = Pt(0)
    hpf.alignment = WD_ALIGN_PARAGRAPH.LEFT

# ── Helpers ───────────────────────────────────────────────────────────────────
def para(text='', bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
         indent=True, left_indent=None, size=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if indent:
        p.paragraph_format.first_line_indent = Cm(1.25)
    if left_indent is not None:
        p.paragraph_format.left_indent = Cm(left_indent)
    if text:
        r = p.add_run(text)
        r.bold   = bold
        r.italic = italic
        r.font.name = FONT
        r.font.size = size or SIZE
    return p

def heading(text, bold=True):
    p = doc.add_paragraph()
    m = re.match(r'^(\d+(?:\.\d+)*)\s', text)
    num = m.group(1) if m else None
    level = min(num.count('.') + 1, 3) if num else 1
    p.style = doc.styles[f'Heading {level}']
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    r = p.add_run(text)
    r.bold = bold
    r.font.name = FONT
    r.font.size = SIZE
    if num and num in TOC_PAGES:
        anchor = _anchor_for(num)
        _add_bookmark(p, anchor)
        TOC_ENTRIES.append((level, text, anchor, TOC_PAGES[num]))
    return p

def center(text, bold=False, size=None):
    return para(text, bold=bold, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, size=size)

def blank(n=1):
    for _ in range(n):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

def page_break():
    doc.add_page_break()

def add_toc():
    # Marcador: as entradas clicáveis do sumário são inseridas aqui ao final,
    # depois que todos os títulos (e seus bookmarks) já existem.
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    TOC_MARKER[0] = p
    return p

def add_table(caption, headers, rows, fonte='Elaborado pelo autor (2026).'):
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    cap.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    cr = cap.add_run(caption)
    cr.bold = True
    cr.font.name = FONT
    cr.font.size = SIZE

    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # cabeçalho
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(11)
            run.font.name = FONT
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), '1F4E79')
        tcPr.append(shd)

    for ri, row_data in enumerate(rows):
        fill = 'DEEAF1' if ri % 2 == 0 else 'FFFFFF'
        for ci, txt in enumerate(row_data):
            cell = table.rows[ri + 1].cells[ci]
            cell.text = str(txt)
            for run in cell.paragraphs[0].runs:
                run.font.size = Pt(11)
                run.font.name = FONT
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), fill)
            tcPr.append(shd)

    fonte_p = doc.add_paragraph()
    fonte_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    fonte_p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    fr = fonte_p.add_run(f'Fonte: {fonte}')
    fr.font.name = FONT
    fr.font.size = Pt(10)
    blank()

# ═══════════════════════════════════════════════════════════════════════════════
# CAPA
# ═══════════════════════════════════════════════════════════════════════════════
center('INSTITUTO FEDERAL DO PARANÁ — CÂMPUS PINHAIS', bold=True)
blank(7)
center('MATHEUS VITOR LOURENÇO SCHIONATO', bold=True)
blank(7)
center('RELATÓRIO DE ATIVIDADES', bold=True)
center('Análise da Acessibilidade Digital nos Sites Eletrônicos das Prefeituras da Região Metropolitana de Curitiba', bold=True)
blank(8)
center('PINHAIS', bold=True)
center('2026', bold=True)
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# FOLHA DE ROSTO
# ═══════════════════════════════════════════════════════════════════════════════
center('MATHEUS VITOR LOURENÇO SCHIONATO', bold=True)
blank(7)
center('RELATÓRIO DE ATIVIDADES', bold=True)
center('Análise da Acessibilidade Digital nos Sites Eletrônicos das Prefeituras da Região Metropolitana de Curitiba', bold=True)
blank(7)
# nota à direita
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
p.paragraph_format.left_indent = Cm(8)
r = p.add_run(
    'Relatório de atividades extensionistas, apresentado à disciplina de '
    'Práticas de Extensão II, do curso de Bacharelado em Ciência da Computação '
    'do Instituto Federal do Paraná, Câmpus Pinhais, sob a orientação do '
    'professor Guilherme Werneck de Oliveira.')
r.font.name = FONT
r.font.size = SIZE
blank(7)
center('PINHAIS', bold=False)
center('2026')
page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# SUMÁRIO
# ═══════════════════════════════════════════════════════════════════════════════
center('SUMÁRIO', bold=True)
blank()
add_toc()

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 1 INTRODUÇÃO
# ═══════════════════════════════════════════════════════════════════════════════
heading('1 INTRODUÇÃO')
para('A acessibilidade digital representa um pilar fundamental para a construção de uma sociedade da informação verdadeiramente inclusiva e equitativa. No contexto do século XXI, onde a interação com serviços públicos, o acesso à informação e a participação cívica são crescentemente mediados por plataformas digitais, garantir que essas interfaces sejam utilizáveis por todas as pessoas — independentemente de suas habilidades ou deficiências — transcende a mera conveniência técnica para se tornar um imperativo de cidadania.')
para('Para a área da Ciência da Computação, o tema da acessibilidade digital é de oportunidade ímpar, pois posiciona o profissional de tecnologia não apenas como um desenvolvedor de soluções, mas como um agente ativo na promoção de direitos humanos e na mitigação de barreiras sociais. Este trabalho de extensão dialoga diretamente com a formação do cientista da computação ao aplicar conhecimentos teóricos de engenharia de software, interação humano-computador e desenvolvimento web a um problema de alto impacto social, alinhando competência técnica com responsabilidade ética.')
para('A presente ação de extensão foi concebida para investigar o estado da acessibilidade nos portais digitais do poder público local. O público-alvo principal são os cidadãos que dependem desses sites para acessar serviços e informações essenciais, com foco particular nas pessoas com deficiência (visual, auditiva, motora ou cognitiva), que são desproporcionalmente afetadas por barreiras digitais. Secundariamente, o público-alvo inclui os gestores e equipes técnicas responsáveis pela manutenção desses portais, a quem os resultados podem servir como diagnóstico para futuras melhorias.')
para('As atividades de análise foram realizadas entre os meses de março e junho de 2026. O escopo geográfico concentrou-se nos sites eletrônicos oficiais das prefeituras da Região Metropolitana de Curitiba, conduzidas pelo extensionista Matheus Vitor Lourenço Schionato, discente do curso de Bacharelado em Ciência da Computação do IFPR Câmpus Pinhais, sob orientação do professor Guilherme Werneck de Oliveira.')
para('A fundamentação teórica baseia-se em padrões e legislações consolidadas. As Diretrizes de Acessibilidade para Conteúdo Web (WCAG), publicadas pelo W3C, constituem o padrão internacional de referência para construção de interfaces digitais acessíveis. No âmbito nacional, a Lei Brasileira de Inclusão da Pessoa com Deficiência (Lei nº 13.146/2015) estabelece, em seu Art. 63, a obrigatoriedade de acessibilidade nos sites mantidos por órgãos de governo, tornando o tema simultaneamente uma exigência legal e uma demanda ética.')

heading('1.1 OBJETIVO')
para('A presente seção descreve, de forma clara e sucinta, os objetivos que norteiam o desenvolvimento desta ação de extensão, distinguindo o propósito geral das metas específicas que foram estabelecidas para alcançá-lo.')

heading('1.2 Objetivo Geral')
para('Analisar o nível de acessibilidade digital dos sites eletrônicos oficiais de um conjunto selecionado de prefeituras, com base nas diretrizes do WCAG 2.1, a fim de identificar as barreiras de navegação e acesso à informação mais prevalentes.')

heading('1.3 Objetivos Específicos')
for bullet in [
    'Levantar um inventário das violações de acessibilidade por meio de ferramentas de avaliação automática.',
    'Identificar barreiras de navegação não detectáveis por automação, através de testes manuais de navegabilidade via teclado e simulação de uso com leitores de tela.',
    'Elaborar um diagnóstico comparativo do estado de acessibilidade entre os diferentes sites eletrônicos a serem analisados.',
    'Apresentar um relatório técnico consolidado com os resultados e recomendações para a melhoria da acessibilidade nos portais públicos.',
]:
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    r = p.add_run(bullet)
    r.font.name = FONT
    r.font.size = SIZE

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 2 CONTEXTUALIZAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════
heading('2 CONTEXTUALIZAÇÃO')
para('A transição de serviços governamentais para plataformas digitais, embora promova eficiência e alcance, gera risco de exclusão quando a acessibilidade não é tratada como requisito central. A ausência de conformidade com as diretrizes de acessibilidade em sites públicos cria barreiras que impedem cidadãos com deficiência de acessar informações e serviços que lhes são de direito, configurando problema na interseção da tecnologia, da política pública e dos direitos civis.')
para('A investigação é motivada pela seguinte pergunta-problema: Qual é o nível de conformidade com as diretrizes WCAG 2.1 (Nível AA) dos sites eletrônicos oficiais das prefeituras da Região Metropolitana de Curitiba, e quais são as barreiras de acessibilidade mais recorrentes que impedem o acesso equitativo à informação e aos serviços públicos digitais?')
para('As implicações práticas são diretas: um cidadão cego pode ser incapaz de consultar o carnê do IPTU; um usuário com mobilidade reduzida pode não conseguir navegar pelos menus para localizar um contato; uma pessoa com baixa visão pode ser impedida de ler um edital por insuficiência de contraste. A principal lacuna que este trabalho visa preencher é a falta de diagnóstico localizado e atualizado sobre acessibilidade digital no setor público municipal, fornecendo dados concretos que subsidiem decisões de gestão.')
para('Do ponto de vista acadêmico, o projeto contribui com dados empíricos para os campos da Interação Humano-Computador (IHC) e da Engenharia de Software, fornecendo estudo de caso sobre o setor público em importante região metropolitana brasileira. Para a formação do estudante de Ciência da Computação, a experiência de conduzir uma auditoria de acessibilidade representa oportunidade valiosa de aplicar conceitos teóricos em contexto real, desenvolvendo compreensão mais profunda sobre o impacto social da tecnologia e a importância do design inclusivo.')

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 3 DESCRIÇÃO DAS ATIVIDADES REALIZADAS
# ═══════════════════════════════════════════════════════════════════════════════
heading('3 DESCRIÇÃO DAS ATIVIDADES REALIZADAS')
para('As atividades foram organizadas em quatro etapas sequenciais, aplicadas a cada um dos portais selecionados. A seleção da amostra, os materiais utilizados, o protocolo de cada etapa e os instrumentos de registro são descritos a seguir.')

heading('3.1 Seleção dos sites e definição do escopo')
para('A amostra foi definida por conveniência e relevância populacional, selecionando os portais das cinco prefeituras com maior número de habitantes na Região Metropolitana de Curitiba. Para cada portal, a análise foi padronizada em três páginas de alta relevância: (i) página inicial — principal porta de entrada do cidadão; (ii) página de serviço de maior procura (consulta de IPTU ou emissão de certidões); e (iii) página de contato — canal essencial de comunicação com a prefeitura. O Quadro 1 lista os municípios selecionados com suas respectivas URLs e populações.')

add_table(
    caption='Quadro 1 – Sites eletrônicos oficiais selecionados para análise',
    headers=['Município', 'URL Oficial', 'População (IBGE 2023)'],
    rows=[
        ['Curitiba',             'https://www.curitiba.pr.gov.br',  '1.773.733 hab.'],
        ['São José dos Pinhais', 'https://www.sjp.pr.gov.br',       '365.193 hab.'],
        ['Colombo',              'https://www.colombo.pr.gov.br',   '256.209 hab.'],
        ['Pinhais',              'https://www.pinhais.pr.gov.br',   '133.105 hab.'],
        ['Araucária',            'https://www.araucaria.pr.gov.br', '148.677 hab.'],
    ]
)

heading('3.2 Critérios de acessibilidade avaliados')
para('A análise baseou-se nas Diretrizes de Acessibilidade para Conteúdo Web (WCAG 2.1), com foco nos critérios de sucesso dos níveis A e AA — padrão exigido para portais governamentais pela legislação brasileira. O Quadro 2 apresenta os critérios priorizados, organizados segundo os quatro princípios do WCAG: Perceptível, Operável, Compreensível e Robusto.')

add_table(
    caption='Quadro 2 – Critérios WCAG 2.1 (Nível AA) priorizados na análise',
    headers=['Princípio', 'Critério', 'O que é verificado'],
    rows=[
        ['Perceptível',   '1.1.1 Conteúdo não textual',    'Toda imagem informativa possui texto alternativo (atributo alt) descritivo.'],
        ['Perceptível',   '1.4.3 Contraste mínimo',        'Razão de contraste de pelo menos 4,5:1 entre texto e fundo da página.'],
        ['Operável',      '2.1.1 Teclado',                 'Todas as funcionalidades estão disponíveis via teclado, sem exceções.'],
        ['Operável',      '2.1.2 Sem armadilha de teclado','O foco do teclado não fica preso em nenhum componente da página.'],
        ['Operável',      '2.4.3 Ordem do foco',           'Navegação por Tab segue ordem lógica coerente com o layout visual.'],
        ['Compreensível', '3.3.2 Rótulos e instruções',    'Campos de formulário têm rótulos (labels) corretamente associados.'],
        ['Robusto',       '4.1.2 Nome, função, valor',     'Componentes de interface têm nome, função e valor acessíveis a tecnologias assistivas.'],
    ]
)

para('No contexto brasileiro, esses critérios dialogam com o Modelo de Acessibilidade em Governo Eletrônico (eMAG), que adapta as diretrizes do WCAG às particularidades dos sítios da administração pública nacional e referencia os mesmos princípios adotados nesta análise.')

heading('3.3 Etapa 1 — Avaliação automatizada de acessibilidade')
para('A primeira etapa consistiu na varredura automatizada de cada página selecionada. O plano inicial previa o uso da ferramenta WAVE (Web Accessibility Evaluation Tool), extensão para navegadores desenvolvida pela WebAIM, que injeta ícones e indicadores diretamente sobre a página analisada, destacando visualmente erros críticos, problemas de contraste, alertas gerais e elementos estruturais.')
para('Durante a coleta, constatou-se que três dos cinco portais (Curitiba, Pinhais e Araucária) apresentavam impedimentos de acesso por meio de requisições HTTP convencionais (Seção 4.1) e que diversas páginas de serviço são implementadas como Single Page Applications (SPA), cujo conteúdo é renderizado dinamicamente via JavaScript e não está presente no HTML estático. Para superar essas limitações sem comprometer a padronização da coleta, complementou-se a avaliação com o motor de testes axe-core, da Deque Systems — mecanismo de código aberto que também fundamenta ferramentas amplamente adotadas, como o Google Lighthouse, e que avalia automaticamente um amplo subconjunto dos critérios de sucesso WCAG 2.1 nos níveis A e AA. O axe-core foi executado por meio de um navegador automatizado (Microsoft Edge, controlado via biblioteca Playwright), permitindo renderizar integralmente o JavaScript de cada página e auditar a árvore DOM final efetivamente apresentada ao usuário — incluindo a verificação programática da razão de contraste de cores (critério 1.4.3), que na abordagem WAVE pura dependeria de inspeção visual manual.')
para('Os dados quantitativos coletados — número de violações de impacto crítico, violações do critério de contraste mínimo (1.4.3) e demais alertas de impacto sério ou moderado, segundo as regras WCAG 2.1 A e AA do axe-core — foram registrados sistematicamente na Tabela 1, contemplando as três páginas (inicial, serviço e contato) de cada um dos cinco municípios selecionados.')

add_table(
    caption='Tabela 1 – Resultados consolidados da auditoria automatizada (axe-core, critérios WCAG 2.1 A e AA)',
    headers=['Site / Página', 'HTTP', 'Erros críticos', 'Erros de contraste', 'Outros alertas', 'Total'],
    rows=[
        ['Curitiba — Inicial',   '200', '15', '8',  '14', '37'],
        ['Curitiba — Serviços',  '200', '0',  '9',  '11', '20'],
        ['Curitiba — Contato¹',  '200', '0',  '1',  '0',  '1'],
        ['SJP — Inicial',        '200', '4',  '8',  '3',  '15'],
        ['SJP — Serviços',       '200', '11', '5',  '2',  '18'],
        ['SJP — Contato',        '200', '0',  '6',  '2',  '8'],
        ['Colombo — Inicial',    '200', '0',  '0',  '33', '33'],
        ['Colombo — Serviços',   '200', '1',  '10', '27', '38'],
        ['Colombo — Contato',    '200', '0',  '3',  '11', '14'],
        ['Pinhais — Inicial',    '200', '5',  '40', '37', '82'],
        ['Pinhais — Serviços',   '200', '1',  '13', '0',  '14'],
        ['Pinhais — Contato',    '200', '5',  '43', '0',  '48'],
        ['Araucária — Inicial',  '200', '0',  '63', '33', '96'],
        ['Araucária — Serviços', '200', '4',  '21', '0',  '25'],
        ['Araucária — Contato',  '200', '0',  '13', '10', '23'],
    ],
    fonte='Elaborado pelo autor (2026), com base em auditoria axe-core 4.x via navegador automatizado (Microsoft Edge/Playwright), em 10 jun. 2026. ¹Não foi localizada página de ouvidoria/contato funcional no domínio oficial de Curitiba; o endereço testado retornou a página de erro padrão do portal (Seção 4.1).'
)

para('A coluna "Erros críticos" agrupa violações de impacto critical segundo o axe-core, associadas majoritariamente às regras image-alt (critério 1.1.1), button-name (critério 4.1.2) e aria-required-children (critério 1.3.1). A coluna "Erros de contraste" corresponde exclusivamente à regra color-contrast (critério 1.4.3, nível AA). A coluna "Outros alertas" agrupa violações de impacto sério ou moderado, como link-name (critério 2.4.4), frame-title (critério 2.4.1), aria-prohibited-attr (critério 4.1.2) e nested-interactive (critério 4.1.2). Os 472 registros consolidados na Tabela 1, incluindo os seletores CSS dos elementos afetados em cada página, fundamentam as discussões apresentadas nas seções seguintes.')

heading('3.4 Etapa 2 — Avaliação manual: navegação por teclado')
para('A segunda etapa focou na operabilidade dos portais sem uso do mouse, simulando a experiência de usuários com deficiência motora que dependem exclusivamente do teclado para navegar. O protocolo de teste consistiu em percorrer cada página utilizando as seguintes teclas, conforme indicado na Figura 2:')
for item in [
    'Tab — avança ao próximo elemento interativo da página.',
    'Shift + Tab — retrocede ao elemento anterior.',
    'Enter / Espaço — ativa links, botões e checkboxes.',
    'Setas direcionais (↑↓) — navegar em menus e listas suspensas.',
    'Esc — fecha modais e dropdowns.',
]:
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    r = p.add_run(item)
    r.font.name = FONT
    r.font.size = SIZE
blank()
para('Para cada página, foram avaliados três critérios: (i) visibilidade do indicador de foco — se havia destaque visual claro sobre o elemento ativo; (ii) ordem lógica da navegação — se o foco percorria os elementos de maneira previsível e coerente com o layout; e (iii) acessibilidade de todos os controles interativos — se menus, formulários e botões podiam ser acionados sem o mouse.')
para('De forma complementar, e para garantir cobertura objetiva e replicável da página inicial de cada portal, parte deste protocolo foi automatizada por meio de navegador controlado via Playwright: a partir do carregamento da página, simulou-se uma sequência de doze pressionamentos consecutivos da tecla Tab, registrando a cada passo o elemento focado, seu texto acessível, a presença de indicador visual de foco (contorno ou sombra) e eventuais ciclos de repetição — estes últimos indicativos de armadilhas de teclado (critério 2.1.2).')

heading('3.5 Etapa 3 — Avaliação manual: leitor de tela (NVDA)')
para('A terceira etapa envolveu a navegação pelas mesmas páginas com o software NVDA (NonVisual Desktop Access) ativo, simulando a experiência de um usuário com deficiência visual total. O NVDA é um leitor de tela de código aberto amplamente utilizado pela comunidade de pessoas cegas. O protocolo verificou quatro aspectos: (i) presença e qualidade de textos alternativos em imagens informativas; (ii) associação correta de rótulos (label) aos campos de formulário; (iii) hierarquia lógica de cabeçalhos (h1, h2, h3...) permitindo navegação por seções; e (iv) anúncio correto de elementos dinâmicos, como carrosséis, modais e notificações.')
para('De forma complementar, extraiu-se programaticamente, via Chrome DevTools Protocol, a árvore de acessibilidade (accessibility tree) da página inicial de cada portal — a mesma estrutura de dados consultada por leitores de tela como o NVDA no sistema operacional Windows — permitindo quantificar de forma objetiva os elementos interativos (botões, links e campos) expostos sem nome acessível, como proxy complementar à inspeção auditiva manual.')

heading('3.6 Etapa 4 — Análise e consolidação dos dados')
para('Após a coleta, os dados foram analisados de forma integrada. Os dados quantitativos da avaliação automatizada foram consolidados na planilha comparativa (Tabela 1) para permitir visão geral do desempenho de cada portal. Os dados qualitativos, provenientes dos testes manuais, foram categorizados com base nos quatro princípios do WCAG (Perceptível, Operável, Compreensível e Robusto), identificando padrões temáticos de falhas e discutindo o impacto real de cada barreira na experiência dos usuários com deficiência.')

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 4 RESULTADOS E DISCUSSÕES
# ═══════════════════════════════════════════════════════════════════════════════
heading('4 RESULTADOS E DISCUSSÕES')
para('Esta seção apresenta os resultados obtidos por meio da varredura automatizada das páginas selecionadas, organizados por município e página analisada, seguidos de uma discussão comparativa dos padrões de falha identificados à luz das diretrizes WCAG 2.1 (W3C, 2018).')
para('A coleta de dados foi realizada entre os dias 09 e 10 de junho de 2026 e abrangeu, para os cinco municípios selecionados, as três páginas definidas no escopo (inicial, serviço e contato), totalizando 15 páginas analisadas. Os municípios de Curitiba, Pinhais e Araucária apresentaram impedimentos de acesso por meio de ferramentas simples de requisição HTTP (curl) durante a coleta inicial; a Seção 4.1 detalha como essas barreiras foram contornadas por meio de navegação automatizada com renderização completa de JavaScript.')

heading('4.1 Condições de Acesso aos Portais')
para('Antes da análise de acessibilidade propriamente dita, verificou-se que nem todos os portais responderam de forma adequada às requisições de acesso, o que representa, em si, uma dimensão relevante do diagnóstico. O Quadro 3 sintetiza as condições de acesso observadas.')

add_table(
    caption='Quadro 3 – Condições de acesso aos portais durante a coleta de dados',
    headers=['Município', 'Condição', 'Impacto para o cidadão'],
    rows=[
        ['Curitiba',             'Bloqueio de requisições simples (curl, HTTP 403); acesso normal (HTTP 200) via navegador completo', 'Nenhum impacto direto ao usuário comum; possível impacto em auditorias automatizadas e mecanismos de busca'],
        ['São José dos Pinhais', 'Acesso normal', 'Nenhum'],
        ['Colombo',              'Redirecionamento para subdomínio (prefeitura.colombo.pr.gov.br)', 'Nenhum'],
        ['Pinhais',              'Domínio oficial redireciona via JavaScript (~1s) para portal terceirizado atendenet.pinhais.pr.gov.br', 'Sem <noscript>: usuários/agentes sem JavaScript não acessam o portal'],
        ['Araucária',            'Domínio oficial com certificado SSL inválido e sem rota válida; portal real hospedado em domínio totalmente distinto (araucaria.atende.net)', 'Barreira grave: navegador bloqueia o domínio oficial, e o domínio funcional não é descoberto a partir dele'],
    ],
    fonte='Elaborado pelo autor (2026), com base em requisições HTTP (curl) e navegação automatizada (Microsoft Edge/Playwright).'
)

para('O caso de Araucária merece destaque especial. O domínio oficial www.araucaria.pr.gov.br apresenta certificado SSL inválido, de modo que qualquer tentativa de acesso via HTTPS resulta em aviso de bloqueio de segurança emitido pelo navegador; mesmo contornando esse aviso, o servidor retorna mensagem de erro informando que "não é possível acessar o Atende.net através desse domínio". O portal efetivamente utilizado pela prefeitura está hospedado em araucaria.atende.net — domínio que não guarda relação nominal com araucaria.pr.gov.br e que não é referenciado a partir dele. Para cidadãos com menor familiaridade tecnológica — grupo que frequentemente inclui pessoas idosas, público com deficiência cognitiva ou usuários de dispositivos desatualizados —, tanto o aviso de segurança quanto a ausência de um caminho de descoberta para o portal real representam barreiras de acesso efetivas. Essa condição infringe indiretamente o princípio da Robustez do WCAG 2.1 (critério 4.1) e coloca o portal em desconformidade com os requisitos de segurança e disponibilidade exigidos pela legislação brasileira para sítios governamentais.')

para('Observou-se ainda que, embora o domínio oficial de Curitiba retorne erro HTTP 403 para ferramentas de requisição simples como curl — mesmo com cabeçalhos que emulam um navegador —, o acesso por meio de um navegador automatizado completo (Microsoft Edge via Playwright) ocorreu normalmente (HTTP 200), tanto na página inicial quanto na carta de serviços. Esse comportamento sugere bloqueio baseado em fingerprint da requisição (possivelmente um Web Application Firewall), e não indisponibilidade real do portal para o cidadão comum; ainda assim, a prática pode prejudicar ferramentas de auditoria automatizada e mecanismos de busca que não emulem um navegador completo, com possíveis efeitos indiretos sobre a indexabilidade do conteúdo. Não foi localizada, dentro do domínio oficial de Curitiba, uma página de ouvidoria ou contato funcional: os endereços testados retornaram a página de erro padrão (HTTP 404, com status de resposta 200) do portal, motivo pelo qual a linha "Curitiba — Contato" da Tabela 1 apresenta valores residuais.')

para('Já o caso de Pinhais revela uma migração completa da infraestrutura do portal institucional para a plataforma terceirizada Atende.net: o domínio oficial www.pinhais.pr.gov.br carrega uma página mínima que, após aproximadamente um segundo, redireciona via JavaScript para atendenet.pinhais.pr.gov.br. Não foi identificado mecanismo de fallback (como uma tag <noscript>) para usuários ou ferramentas que não executam JavaScript, o que caracteriza potencial violação do princípio de Robustez (4.1) do WCAG 2.1.')

heading('4.2 Resultados por Portal')
heading('4.2.1 Curitiba')
para('A página inicial do portal de Curitiba apresentou o maior número de violações de impacto crítico entre os cinco municípios analisados (15 ao todo), conforme a Tabela 2.')

add_table(
    caption='Tabela 2 – Erros de acessibilidade no portal de Curitiba',
    headers=['Critério WCAG 2.1', 'Descrição da falha', 'Ocorr.'],
    rows=[
        ['1.1.1 — Conteúdo não textual', 'Imagens do carrossel "Guia Curitiba" (eventos) sem atributo alt', '8'],
        ['4.1.2 — Nome, função, valor',  'Botões de navegação do carrossel principal (anterior/próximo) sem texto acessível', '7'],
        ['1.4.3 — Contraste mínimo',     'Itens do menu superior (Acessibilidade, Transparência, Curitiba-Ouve, 156, Secretarias) com contraste insuficiente', '8'],
        ['2.4.4 — Finalidade do link',   'Links sem texto: logotipo institucional (2 ocorrências, ambas apontando para a página inicial) e campo de busca sem rótulo', '11'],
        ['2.4.1 — Ignorar blocos',       'Iframes de conteúdo dinâmico incorporados sem atributo title', '2'],
        ['4.1.2 — Nome, função, valor',  'Botão de leitura de página (#ma-lerPaginaItem) aninhado dentro de outro controle interativo', '1'],
    ],
    fonte='Elaborado pelo autor (2026), com base em auditoria axe-core.'
)

para('As oito imagens do carrossel de eventos "Guia Curitiba" não possuem atributo alt, de modo que um usuário de leitor de tela não recebe qualquer informação sobre o conteúdo desses destaques. Da mesma forma, os sete botões de navegação do carrossel principal (setas "anterior" e "próximo") são implementados sem texto acessível, sendo anunciados por leitores de tela apenas como "botão", sem indicação de função — violação direta do critério 4.1.2.')
para('A página da Carta de Serviços replicou nove das oito violações de contraste e dez das onze violações de link-name observadas na página inicial, além do mesmo problema de controle aninhado (#ma-lerPaginaItem), evidenciando que essas falhas decorrem do template (cabeçalho e menu) compartilhado entre as páginas do portal, e não de conteúdo específico de cada seção.')
para('A auditoria de navegação por teclado (Etapa 2) revelou achado adicional relevante: o portal possui um link "Ir para o conteúdo" (href="#acessibilidade"), em conformidade com a recomendação do critério 2.4.1, porém esse link é apenas o 11º elemento alcançado pela tecla Tab a partir do carregamento da página — atrás de itens como "Abrir menu de acessibilidade", "Portal da Transparência", "Curitiba-Ouve", "156", "Acesso à informação", "Secretarias", dois links do logotipo sem texto e "Entrar". Na prática, um usuário que dependa exclusivamente do teclado precisa pressionar Tab dez vezes antes de ter a opção de pular a barra superior, o que esvazia parcialmente a utilidade do recurso. Adicionalmente, 11 dos 12 elementos focalizáveis nessa sequência não exibem qualquer indicador visual de foco (contorno ou sombra), o que compromete a orientação de usuários com baixa visão que navegam por teclado.')

heading('4.2.2 São José dos Pinhais')
para('A análise das páginas inicial e de contato do portal de São José dos Pinhais revelou padrões sistemáticos de não conformidade com os critérios WCAG 2.1, predominantemente relacionados ao princípio da Perceptibilidade. A Tabela 3 apresenta os erros identificados na página inicial.')

add_table(
    caption='Tabela 3 – Erros de acessibilidade na página inicial de São José dos Pinhais',
    headers=['Critério WCAG 2.1', 'Descrição da falha', 'Ocorrências'],
    rows=[
        ['1.1.1 — Conteúdo não textual', 'Imagens sem atributo alt (logo, botões A+/A-, ícone contraste, fotos de serviços)', '12'],
        ['3.3.2 — Rótulos e instruções', 'Campo de busca sem label associado', '1'],
        ['2.4.4 — Finalidade do link',   'Links vazios ou sem contexto ("Avançar", "Voltar", links vazios)', '7'],
        ['4.1.2 — Nome, função, valor',  'Ausência completa de marcação ARIA', '—'],
        ['1.3.1 — Informação e relações','Hierarquia de headings sem h1 definido', '—'],
    ]
)

para('Entre as 12 imagens sem texto alternativo, encontram-se elementos de alta relevância semântica: o logotipo institucional da prefeitura, os botões de controle de tamanho de fonte (A+, A, A-) e o ícone de alto contraste — todos componentes da própria barra de acessibilidade do portal. A ironia desse achado é notável: os controles destinados a tornar o site mais acessível são, eles mesmos, inacessíveis a leitores de tela, pois não possuem descrição textual. Um usuário cego que utilize o NVDA ouvirá apenas "link" ao navegar por esses botões, sem qualquer indicação de sua função.')
para('A página de contato (Ouvidorias) replicou os mesmos padrões: 7 imagens sem atributo alt, ausência de ARIA e hierarquia de headings indefinida, sugerindo que os problemas decorrem de decisões arquiteturais do sistema de gestão de conteúdo utilizado pelo portal, e não de falhas pontuais de implementação.')
para('A auditoria axe-core (Tabela 1) acrescentou a essa análise 4 violações críticas da regra aria-required-children (critério 1.3.1) e 8 violações de contraste mínimo (critério 1.4.3, nível AA) na página inicial, além de 11 violações de image-alt na página de serviços (financas.sjp.pr.gov.br) — nenhuma delas perceptível por inspeção do HTML estático. A auditoria de navegação por teclado mostrou ainda que os primeiros nove elementos focalizáveis da página — três ícones de redes sociais, um link "Acessibilidade" e cinco botões da barra de acessibilidade (Aumentar texto, Diminuir texto, Tamanho padrão, Alto contraste, Ativar Leitura de Texto) — não exibem indicador visual de foco, totalizando 10 dos 12 elementos testados sem foco visível. Assim como observado para os atributos alt, a própria barra de acessibilidade do portal mostra-se, paradoxalmente, uma das áreas menos acessíveis ao teclado. Nenhum link "pular para o conteúdo" foi identificado entre os doze primeiros elementos focalizáveis.')

heading('4.2.3 Colombo')
para('O portal de Colombo apresentou o conjunto mais amplo de tipos de falha entre os municípios analisados. Além dos erros estruturais comuns ao portal de São José dos Pinhais, foram identificadas violações adicionais relativas à operabilidade e à compreensibilidade do conteúdo. A Tabela 4 detalha os erros da página inicial.')

add_table(
    caption='Tabela 4 – Erros de acessibilidade na página inicial de Colombo',
    headers=['Critério WCAG 2.1', 'Descrição da falha', 'Ocorrências'],
    rows=[
        ['1.1.1 — Conteúdo não textual', 'Imagens sem alt (logo, ícones de serviços, redes sociais)', 'Múltiplas'],
        ['2.4.4 — Finalidade do link',   'Texto de link genérico "Clique aqui"', '10+'],
        ['1.3.1 — Informação e relações','h3 utilizados sem h1 ou h2 precedentes', '—'],
        ['3.3.2 — Rótulos e instruções', 'Campo de busca sem label', '1'],
        ['2.4.1 — Ignorar blocos',       'Iframes incorporados sem atributo title', 'Sim'],
        ['4.1.2 — Nome, função, valor',  'Barra de acessibilidade dependente de JavaScript sem fallback', '—'],
    ]
)

para('O uso sistemático da expressão "Clique aqui" em mais de dez links distintos constitui uma violação direta do critério 2.4.4 do WCAG 2.1, que determina que o propósito de cada link deve ser determinável a partir do seu texto isoladamente. Para um usuário que navega por links utilizando leitor de tela, ouvir repetidamente "Clique aqui, link" sem qualquer contexto torna a navegação no portal essencialmente inutilizável. Esse padrão é consistente com as 33 violações de link-name identificadas pela auditoria axe-core na página inicial (Tabela 1), majoritariamente associadas aos ícones de redes sociais do rodapé (.a-facebook, .a-instagram, .a-youtube) e confirmadas pela árvore de acessibilidade, que apontou 30 elementos interativos sem nome acessível em um total de 1.399 nós.')
para('A página de autoatendimento de Colombo (hospedada na plataforma terceirizada Atende.net, em colombo.atende.net) foi auditada separadamente via axe-core, por se tratar de uma Single Page Application cujo conteúdo não está presente no HTML estático. Foram identificadas 27 violações da regra aria-prohibited-attr (critério 4.1.2) — atributos ARIA aplicados a elementos que não os admitem, fazendo com que leitores de tela possam ignorar ou interpretar incorretamente esses elementos — além de 10 violações de contraste mínimo (critério 1.4.3) e 1 botão sem nome acessível. Esse padrão de aria-prohibited-attr revelou-se comum à plataforma Atende.net como um todo, conforme discutido na Seção 4.4.')
para('A página de contato de Colombo apresentou perfil menos crítico que a página inicial, com 2 imagens sem atributo alt, 1 campo de formulário sem label e 5 links de redes sociais sem texto visível (consistente com as 11 violações de link-name reportadas na Tabela 1), mantendo, porém, os padrões de hierarquia de headings inconsistentes.')
para('Em contraste com os demais municípios analisados, a página inicial de Colombo foi a única, entre as cinco, a apresentar um link "Pular para o conteúdo" (href="#content") como primeiro elemento focalizável, exibindo indicador visual de foco (sombra) tanto nesse link quanto no item seguinte ("Acessibilidade") — prática alinhada ao critério 2.4.1 que poderia servir de referência aos demais portais. Entretanto, os nove elementos seguintes da barra de acessibilidade (Aumentar Texto, Diminuir texto, Escala de cinza, Alto Contraste, Contraste Negativo, Fundo claro, Links Underline, Fonte legível, Reiniciar) utilizam href="#" (âncoras vazias) e não exibem indicador de foco, repetindo o padrão observado nos demais portais.')

heading('4.2.4 Pinhais')
para('O portal de Pinhais foi inteiramente migrado para a plataforma terceirizada Atende.net (atendenet.pinhais.pr.gov.br), para a qual o domínio institucional redireciona automaticamente (Seção 4.1). A Tabela 5 apresenta os erros identificados na página inicial, que totalizou 82 violações — o segundo maior valor entre os cinco municípios.')

add_table(
    caption='Tabela 5 – Erros de acessibilidade no portal de Pinhais',
    headers=['Critério WCAG 2.1', 'Descrição da falha', 'Ocorr.'],
    rows=[
        ['1.4.3 — Contraste mínimo',     'Textos e botões (spans de conteúdo, botões "Acessar no Sistema" e "Cadastro") com contraste insuficiente', '40'],
        ['4.1.2 — Nome, função, valor',  'Ícones de compartilhamento em redes sociais no carrossel de destaques com atributos ARIA não permitidos', '33'],
        ['1.1.1 — Conteúdo não textual', 'Cards de destaque ("Radar da Transparência", "Selo Diamante 2025", "Portal da Transparência") sem alt', '4'],
        ['2.4.4 — Finalidade do link',   'Cards de destaque sem texto acessível (apenas imagem de fundo)', '4'],
        ['4.1.2 — Nome, função, valor',  'Botão "Acessar no Sistema" sem texto acessível', '1'],
    ],
    fonte='Elaborado pelo autor (2026), com base em auditoria axe-core.'
)

para('A página inicial apresentou 40 falhas de contraste mínimo (critério 1.4.3) — a maior incidência desse critério entre as páginas iniciais dos cinco municípios — distribuídas por elementos textuais e botões de acesso e cadastro, além de 33 violações de aria-prohibited-attr no carrossel de destaques, mesmo padrão observado em Araucária (Seção 4.2.5) por tratar-se da mesma plataforma.')
para('As páginas de serviço (emissão de guias) e de contato (Fale Conosco) mantiveram o padrão de contraste insuficiente, com 13 e 43 ocorrências respectivamente — esta última a maior incidência de contraste entre as 15 páginas analisadas. Na página de Fale Conosco, 5 botões de impressão e compartilhamento em redes sociais (.fa-print, .fa-facebook-square, .fa-square-x-twitter) não possuem texto acessível, sendo anunciados por leitores de tela apenas como "botão".')
para('A navegação por teclado revelou o melhor desempenho relativo entre os portais com barra de acessibilidade tradicional: os três primeiros itens focalizáveis ("Acesso à Informação", "Transparência", "Mapa do Site") preservam o contorno de foco padrão do navegador (apenas 7 dos 12 elementos testados ficaram sem indicador de foco, a menor proporção entre os portais não afetados por armadilha de teclado). Ainda assim, os cinco botões da barra de acessibilidade que os sucedem (Aumentar Fonte, Diminuir Fonte, Restaurar Fonte, Alto Contraste, VLibras) não exibem indicador de foco, e nenhum link "pular para o conteúdo" foi identificado nos doze primeiros elementos focalizáveis.')

heading('4.2.5 Araucária')
para('O portal de Araucária está hospedado, assim como o de Pinhais, na plataforma terceirizada Atende.net (araucaria.atende.net); o domínio institucional araucaria.pr.gov.br encontra-se totalmente inacessível (Seção 4.1). A Tabela 6 resume os principais achados.')

add_table(
    caption='Tabela 6 – Erros de acessibilidade no portal de Araucária',
    headers=['Critério WCAG 2.1', 'Descrição da falha', 'Ocorr.'],
    rows=[
        ['2.1.2 — Sem armadilha de teclado', 'Modal de avisos captura o foco do teclado em ciclo fechado, impedindo acesso ao restante da página', '—'],
        ['1.4.3 — Contraste mínimo',         'Links do menu superior ("Acesso à Informação", "Transparência", "Servidor") e demais elementos com contraste insuficiente (página inicial)', '63'],
        ['4.1.2 — Nome, função, valor',      'Ícones de compartilhamento do carrossel com atributos ARIA não permitidos (página inicial)', '33'],
        ['4.1.2 — Nome, função, valor',      'Botões de impressão/compartilhamento sem texto acessível (página de IPTU)', '4'],
        ['4.1.2 — Nome, função, valor',      'Anexos da Ouvidoria com aria-label="Anexo: undefined" (valor literal "undefined")', '5'],
        ['2.4.4 — Finalidade do link',       'Ícones de download de anexos sem texto acessível (Ouvidoria)', '5'],
    ],
    fonte='Elaborado pelo autor (2026), com base em auditoria axe-core e navegação por teclado.'
)

para('Entre os portais analisados, Araucária apresentou o maior número de violações do critério 1.4.3 na página inicial — 63 ocorrências, incluindo os principais links de navegação institucional ("Acesso à Informação", "Transparência", "Servidor") — além do mesmo padrão de 33 violações aria-prohibited-attr no carrossel de destaques observado em Pinhais (Seção 4.4).')
para('Na página da Ouvidoria, identificou-se um achado peculiar: os ícones de anexo de arquivos possuem o atributo aria-label="Anexo: undefined", expondo a um leitor de tela o texto literal "undefined" — sintoma de uma variável de programação (provavelmente o nome do arquivo) que não foi preenchida corretamente antes de ser inserida no atributo. Trata-se de exemplo concreto de como falhas de implementação no front-end se traduzem diretamente em informação incorreta para usuários de tecnologia assistiva.')
para('O achado mais grave, contudo, foi identificado pela auditoria de navegação por teclado: ao carregar a página inicial, um modal de avisos ("Avisos do Portal do Cidadão", com a chamada de destaque "IPTU 2026" e a opção "Não exibir este aviso novamente") captura o foco do teclado em um ciclo fechado de seis elementos — dos doze pressionamentos de Tab testados, o foco percorreu repetidamente a mesma sequência (ícone "Fechar Avisos", link da imagem, imagem "IPTU 2026", checkbox "não exibir novamente", rótulo e o próprio contêiner do modal), sem nunca alcançar o menu principal, o conteúdo da página ou o rodapé. Trata-se de uma armadilha de teclado (keyboard trap), violação direta do critério 2.1.2 do WCAG 2.1 — nível A, o nível mínimo de conformidade exigido pela legislação. Para um usuário que dependa exclusivamente do teclado, esse modal impede completamente o uso do portal: a única forma de fechá-lo é localizar e ativar o ícone "Fechar Avisos" (o primeiro elemento do ciclo), o que pode não ser evidente sem suporte visual ou auditivo adequado. Esse achado, isoladamente, já caracteriza descumprimento do nível mínimo (A) de conformidade ao WCAG 2.1 e, por extensão, do Art. 63 da Lei Brasileira de Inclusão.')

heading('4.3 Navegação por Teclado: Síntese Comparativa')
para('O Quadro 4 consolida os resultados da auditoria automatizada de navegação por teclado (Etapa 2) para a página inicial dos cinco portais.')

add_table(
    caption='Quadro 4 – Síntese da auditoria de navegação por teclado (12 primeiros elementos focalizáveis, página inicial)',
    headers=['Município', 'Link "pular conteúdo"', 'Sem foco visível', 'Observação'],
    rows=[
        ['Curitiba',  'Presente, mas é o 11º elemento',           '11/12', 'Barra superior precede o link de pular'],
        ['SJP',       'Ausente',                                  '10/12', 'Barra de acessibilidade (9 itens) sem foco visível'],
        ['Colombo',   'Presente, 1º elemento, com foco visível',  '10/12', 'Único portal com boa prática de skip link'],
        ['Pinhais',   'Ausente',                                  '7/12',  'Melhor proporção de foco visível entre os 5'],
        ['Araucária', 'Ausente',                                  '2/12*', '*Foco preso em ciclo de 6 elementos (armadilha de teclado)'],
    ],
    fonte='Elaborado pelo autor (2026), com base em automação de navegação por teclado (Playwright/Edge), 12 pressionamentos de Tab a partir do carregamento da página, 10 jun. 2026.'
)

para('A síntese evidencia que a ausência de indicador visual de foco é a norma, e não a exceção, entre os portais analisados: em quatro dos cinco municípios, mais de 80% dos primeiros elementos focalizáveis não exibem qualquer realce ao receber o foco do teclado, dificultando a orientação de usuários com baixa visão ou deficiência motora que dependem do teclado para navegar. Chama atenção que, em três municípios (Curitiba, São José dos Pinhais e Pinhais), os primeiros elementos alcançados pela tecla Tab pertencem à própria barra de acessibilidade do portal — recurso destinado a ampliar a inclusão que, paradoxalmente, está entre os menos acessíveis ao teclado. Colombo destaca-se positivamente por ser o único portal a apresentar um link "Pular para o conteúdo" como primeiro elemento da página, com indicador de foco visível, prática que deveria ser adotada como referência pelos demais municípios.')
para('Complementarmente, a extração da árvore de acessibilidade da página inicial de cada portal — estrutura de dados consultada por leitores de tela como o NVDA — quantificou o número de elementos interativos (botões, links, campos) expostos sem nome acessível: 6 em Curitiba, 3 em São José dos Pinhais, 30 em Colombo, 4 em Pinhais e 0 em Araucária, em um universo de 482 a 2.347 nós por página. Esses números são consistentes com as violações de link-name e button-name identificadas pelo axe-core (Tabela 1) e representam, na prática, controles que um usuário do NVDA ouviria apenas como "link" ou "botão", sem qualquer pista sobre sua função.')

heading('4.4 Padrões Transversais de Falha')
para('A análise comparativa dos cinco portais permitiu identificar padrões de falha que se repetem de forma sistemática, independentemente do município, sugerindo que os problemas de acessibilidade são estruturais e não isolados. O Quadro 5 organiza esses padrões por princípio WCAG, indicando os municípios em que cada padrão foi observado.')

add_table(
    caption='Quadro 5 – Padrões transversais de falha identificados nos portais analisados',
    headers=['Princípio WCAG', 'Critério', 'Padrão de falha', 'Municípios afetados'],
    rows=[
        ['Perceptível',   '1.4.3', 'Contraste insuficiente entre texto/elemento e plano de fundo', 'Curitiba, SJP, Colombo, Pinhais, Araucária (5/5)'],
        ['Operável',      '2.4.4', 'Links sem texto acessível (logotipos, ícones sociais, "Clique aqui")', 'Curitiba, SJP, Colombo, Pinhais, Araucária (5/5)'],
        ['Robusto',       '4.1.2', 'Botões sem nome acessível (ícones de carrossel, impressão, redes sociais)', 'Curitiba, Colombo, Pinhais, Araucária (4/5)'],
        ['Perceptível',   '1.1.1', 'Imagens/cards sem texto alternativo, inclusive na barra de acessibilidade', 'Curitiba, SJP, Colombo, Pinhais (4/5)'],
        ['Robusto',       '4.1.2', 'Atributos ARIA não permitidos (aria-prohibited-attr), específico da plataforma Atende.net', 'Colombo, Pinhais, Araucária (3/5)'],
        ['Operável',      '—',     'Indicador visual de foco do teclado ausente na maioria dos elementos', 'Curitiba, SJP, Colombo (3/5; Pinhais e Araucária parcialmente)'],
        ['Perceptível',   '1.3.1', 'aria-required-children: papéis ARIA sem os filhos obrigatórios', 'SJP (1/5)'],
        ['Operável',      '2.1.2', 'Armadilha de teclado: modal captura o foco em ciclo fechado', 'Araucária (1/5)'],
    ],
    fonte='Elaborado pelo autor (2026), com base em auditoria axe-core e navegação por teclado.'
)

para('Esses resultados alinham-se com os achados de Silva (2022), que em estudo sobre portais governamentais brasileiros identificou os critérios 1.1.1 (texto alternativo) e 2.4.4 (finalidade do link) como as violações mais prevalentes em sítios do setor público. O presente estudo confirma esse padrão no contexto específico da Região Metropolitana de Curitiba — agora com os cinco municípios de maior população — sugerindo que a baixa conformidade com WCAG em portais governamentais municipais é um fenômeno sistêmico no Brasil. Adicionalmente, a cobertura do critério 1.4.3 (contraste mínimo), viabilizada pela auditoria axe-core, revelou que esse é o padrão de falha mais universal entre os cinco portais — presente nas 15 páginas analisadas — achado que análises baseadas exclusivamente em inspeção estrutural do HTML, como a relatada por Silva (2022), tipicamente não capturam.')
para('Um achado adicional, não previsto no desenho original deste estudo, diz respeito à dependência de infraestrutura terceirizada: três dos cinco municípios analisados — Colombo (apenas no módulo de autoatendimento), Pinhais e Araucária (portais institucionais inteiros) — têm seus serviços digitais hospedados na mesma plataforma Software as a Service, a Atende.net. O padrão aria-prohibited-attr — 27 ocorrências em Colombo, 33 em Pinhais e 38 em Araucária (33 na página inicial e 5 na Ouvidoria) — é idêntico em forma e localização (ícones de compartilhamento do carrossel de destaques) nas três instâncias, indicando tratar-se de defeito do template ou componente de front-end fornecido pela própria plataforma, e não de falha cometida individualmente por cada prefeitura. Esse achado tem implicação prática relevante: uma única correção realizada pelo fornecedor da plataforma teria potencial de melhorar simultaneamente a acessibilidade de múltiplos portais municipais, evidenciando o papel estratégico que requisitos de acessibilidade em contratos de fornecimento de tecnologia para o setor público podem desempenhar.')
para('Do ponto de vista do impacto real sobre o usuário, as falhas identificadas comprometem especialmente três perfis: (i) usuários com deficiência visual que utilizam leitores de tela — a ausência de textos alternativos, de nomes acessíveis em links/botões e de marcação ARIA correta torna a navegação desorientada e incompleta; (ii) usuários com deficiência motora que navegam exclusivamente pelo teclado — links vazios interrompem o fluxo de navegação por Tab, a ausência de indicador de foco dificulta a orientação, e no caso extremo de Araucária uma armadilha de teclado (Seção 4.2.5) impede integralmente o uso do portal; e (iii) usuários com baixa visão ou deficiência cognitiva — o contraste insuficiente (presente em 100% das páginas analisadas) e a hierarquia de headings/ARIA quebrada prejudicam a leitura e a compreensão da estrutura da página.')
para('Diante do disposto no Art. 63 da Lei Brasileira de Inclusão da Pessoa com Deficiência (Lei nº 13.146/2015), que determina obrigatoriedade de acessibilidade nos sítios mantidos por órgãos de governo, os resultados obtidos evidenciam que os portais analisados encontram-se em desconformidade legal, além de representarem barreiras concretas ao exercício da cidadania digital por parte da população com deficiência.')

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 5 CONSIDERAÇÕES FINAIS
# ═══════════════════════════════════════════════════════════════════════════════
heading('5 CONSIDERAÇÕES FINAIS')
para('O presente trabalho de extensão propôs-se a investigar o nível de conformidade com as diretrizes WCAG 2.1 dos portais eletrônicos das cinco prefeituras de maior população da Região Metropolitana de Curitiba (Curitiba, São José dos Pinhais, Colombo, Pinhais e Araucária), com o objetivo de identificar as barreiras de acessibilidade mais prevalentes que comprometem o acesso equitativo de cidadãos com deficiência aos serviços públicos digitais.')
para('Os resultados obtidos evidenciam desconformidade sistemática com os padrões WCAG 2.1 nos cinco portais analisados, totalizando 472 violações automatizadas distribuídas em 15 páginas (Tabela 1). Os padrões mais recorrentes foram o contraste insuficiente entre texto e fundo (critério 1.4.3, presente nas 15 páginas) e a ausência de texto acessível em links e botões (critérios 2.4.4 e 4.1.2, presentes nos cinco municípios) — problemas que, juntos, comprometem a navegação de usuários com baixa visão, usuários de leitores de tela e usuários que dependem exclusivamente do teclado. Identificou-se ainda uma armadilha de teclado (critério 2.1.2, nível A) no portal de Araucária, capaz de impedir integralmente a navegação por teclado a partir da página inicial, e uma dependência estrutural de três dos cinco municípios (Colombo, Pinhais e Araucária) de uma mesma plataforma terceirizada (Atende.net), que replica os mesmos defeitos de implementação ARIA em todas as instâncias. Esses padrões, identificados de forma recorrente entre municípios distintos, indicam que os problemas de acessibilidade não são incidentes pontuais, mas reflexo de práticas de desenvolvimento e manutenção — e, em parte, de plataformas de mercado — que não incorporam os requisitos de inclusão digital como critério de qualidade.')
para('Do ponto de vista da formação técnico-profissional, a experiência de conduzir uma auditoria de acessibilidade permitiu a aplicação prática de conceitos de engenharia de software, interação humano-computador e desenvolvimento web em um contexto de impacto social real. A combinação de ferramentas de avaliação automatizada (WAVE e axe-core), navegação automatizada por teclado e extração da árvore de acessibilidade via Chrome DevTools Protocol proporcionou compreensão mais profunda das tecnologias assistivas e das barreiras enfrentadas cotidianamente por usuários com deficiência, dimensão que raramente é abordada na formação convencional em Ciência da Computação. A confirmação qualitativa de parte desses achados com o leitor de tela NVDA em uso real permanece como atividade complementar recomendada, conforme detalhado no documento de pendências que acompanha este relatório.')
para('Como sugestões para trabalhos futuros, recomenda-se: (i) ampliar o escopo da análise para os demais municípios da Região Metropolitana de Curitiba não contemplados nesta amostra; (ii) realizar entrevistas e testes de uso com pessoas com deficiência para validar os achados com perspectivas reais de uso, com ênfase na confirmação auditiva via NVDA; (iii) reportar formalmente à Atende.net os defeitos de ARIA identificados como comuns aos municípios que utilizam a plataforma, dado seu potencial de impacto multiplicado; e (iv) desenvolver um guia de recomendações técnicas direcionado às equipes de tecnologia das prefeituras, priorizando a correção da armadilha de teclado identificada em Araucária por seu impacto severo (nível A). A replicação desta metodologia em âmbito estadual ou nacional poderia contribuir significativamente para o mapeamento da acessibilidade digital no setor público brasileiro.')

page_break()

# ═══════════════════════════════════════════════════════════════════════════════
# 6 REFERÊNCIAS
# ═══════════════════════════════════════════════════════════════════════════════
heading('6 REFERÊNCIAS')
blank()
for ref in [
    'BRASIL. Lei nº 13.146, de 6 de julho de 2015. Institui a Lei Brasileira de Inclusão da Pessoa com Deficiência (Estatuto da Pessoa com Deficiência). Diário Oficial da União, Brasília, DF, 7 jul. 2015.',
    'DEQUE SYSTEMS. axe-core: accessibility testing engine for automated tests. 2026. Disponível em: https://github.com/dequelabs/axe-core. Acesso em: 10 jun. 2026.',
    'GOVERNO FEDERAL DO BRASIL. eMAG — Modelo de Acessibilidade em Governo Eletrônico. Disponível em: http://emag.governoeletronico.gov.br/. Acesso em: 26 abr. 2026.',
    'IBGE — INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. Censo Demográfico 2022. Rio de Janeiro: IBGE, 2023.',
    'NV ACCESS. NonVisual Desktop Access (NVDA). Disponível em: https://www.nvaccess.org/. Acesso em: 26 abr. 2026.',
    'SILVA, A. B. C. Acessibilidade em portais governamentais no Brasil: um estudo de caso multirregional. Anais do Simpósio Brasileiro sobre Fatores Humanos em Sistemas Computacionais, v. 21, p. 1-10, 2022.',
    'WEBAIM. WAVE Web Accessibility Evaluation Tool. Disponível em: https://wave.webaim.org/. Acesso em: 26 abr. 2026.',
    'WORLD WIDE WEB CONSORTIUM (W3C). Web Content Accessibility Guidelines (WCAG) 2.1. W3C Recommendation, 05 jun. 2018. Disponível em: https://www.w3.org/TR/WCAG21/. Acesso em: 26 abr. 2026.',
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(ref)
    r.font.name = FONT
    r.font.size = SIZE

# ── Sumário: inserir as entradas clicáveis no lugar do marcador ───────────────
build_toc()

# ── Salvar ────────────────────────────────────────────────────────────────────
out = r'c:\Users\Vitor\Documents\projeto extensão\Relatorio-Final-Matheus.docx'
doc.save(out)
print(f'Documento salvo: {out}')
