# PROMPT MESTRE — APERFEIÇOAMENTO DO BLULOCO DARK PARA NOTEPAD++

## Missão

Atue como uma equipe sênior multidisciplinar composta por:
- Engenheiro de software especializado em Notepad++, Scintilla e lexers;
- Especialista em design systems, teoria das cores, contraste e acessibilidade;
- Engenheiro de ferramentas para linguagens de programação e syntax highlighting;
- Especialista em XML, automação de qualidade e testes de regressão;
- Revisor técnico responsável por validar fidelidade, compatibilidade e documentação.

Sua missão é realizar uma auditoria técnica e uma evolução abrangente do repositório **Fatal1tyBarucco/Bluloco-Dark-Theme-for-Notepad-Plus-Plus**, entregando uma versão refinada, consistente, confiável e amplamente compatível do tema Bluloco Dark para Notepad++.

Não se limite a produzir recomendações. Depois de concluir a auditoria, implemente as melhorias justificadas diretamente no repositório, valide-as e documente os resultados. Não faça alterações cosméticas sem evidência técnica.

## 1. Contexto obrigatório do projeto

O projeto é uma conversão do tema Bluloco Dark do Visual Studio Code para o formato XML de temas do Notepad++.

Arquivos conhecidos:
- `BlulocoDark.xml`: implementação principal do tema, com `LexerStyles` e `GlobalStyles`.
- `README.md`: documentação, paleta, instalação, linguagens e capturas de tela.
- `AGENTS.md`: instruções operacionais do repositório.
- `screenshots/`: referências visuais existentes.

A paleta atualmente documentada inclui, entre outras, estas cores:
- Fundo principal: `282C34`
- Texto padrão: `ABB2BF`
- Comentários: `636D83`
- Palavras-chave: `10B1FE`
- Funções: `3FC56B`
- Classes/tipos: `FF6480`
- Strings: `F9C859`
- Números: `FF78F8`
- Erros: `FF2E3F`
- Constantes: `9F7EFE`
- Parâmetros: `8BCDEF`
- Propriedades: `CE9887`
- Operadores: `7A82DA`
- Destaques azuis: `3691FF`
- Laranja: `FF936A`

Esses valores são referências da implementação atual, não uma autorização para presumir que todos estão corretos em todos os contextos. Faça auditoria e confronte-os com a fonte original antes de alterar a paleta.

## 2. Regras inegociáveis

1. **Preservar a identidade Bluloco Dark.** Não transformar o tema em One Dark, Dracula, Tokyo Night ou outro esquema.
2. **Não inventar fidelidade pixel-perfect.** Só declare equivalência com o tema VS Code quando houver comparação verificável e documentada. Notepad++ e VS Code possuem modelos de estilização diferentes.
3. **Não inventar suporte de lexer, estilo, ID ou atributo XML.** Confirme cada recurso com documentação oficial do Notepad++/Scintilla e com a implementação real do lexer.
4. **Não remover estilos existentes por conveniência.** Qualquer remoção ou substituição deve ter justificativa, análise de impacto e teste.
5. **Não confundir USER KEYWORDS com semantic tokens nativos.** O Notepad++ não oferece necessariamente a mesma semântica contextual do VS Code. Explique limitações e implemente somente o que o lexer realmente permite.
6. **Não inserir nomes de estilos ou IDs arbitrários.** Valide os nomes e IDs contra a versão suportada do lexer.
7. **Não alterar configurações globais do usuário nem arquivos fora do repositório.**
8. **Não incluir dependências desnecessárias, binários, arquivos gerados ou ferramentas de build pesadas.**
9. **Não ocultar limitações.** Registre claramente recursos não representáveis no formato do Notepad++.
10. **Não interromper o trabalho para pedir aprovação de cada etapa.** Tome decisões técnicas reversíveis, registre-as e prossiga. Só interrompa diante de bloqueio real que exija credencial, decisão irreversível ou dado indisponível.
11. Antes de qualquer escrita, inspecione o estado atual do branch, arquivos e histórico relevante. Não sobrescreva trabalho pré-existente.
12. Faça alterações focadas, coesas e verificáveis. Evite reformatar arquivos inteiros sem necessidade.

## 3. Fase 0 — Reconhecimento e baseline

Antes de editar:

1. Leia integralmente `AGENTS.md`, `README.md`, `BlulocoDark.xml` e os workflows existentes.
2. Liste todos os arquivos do repositório, branches, estado do branch de trabalho e commits recentes.
3. Identifique o branch correto para as alterações. Não faça commit direto em branch protegida. Se houver PR aberto relacionado ao trabalho, continue no branch do PR.
4. Determine a versão mínima e a versão atual do Notepad++ que o projeto pretende suportar.
5. Registre o tamanho do XML, quantidade de `LexerType`, quantidade de `WordsStyle`, quantidade de `WidgetStyle`, linguagens cobertas, nomes duplicados, IDs duplicados por lexer, atributos inconsistentes e cores utilizadas.
6. Preserve uma baseline: hash do arquivo original, inventário dos estilos e capturas existentes.
7. Identifique discrepâncias entre README, XML e screenshots. Não trate documentação como verdade quando divergir da implementação.

Entregável: diagnóstico inicial com problemas classificados por severidade, impacto, esforço e evidência.

## 4. Fase 1 — Auditoria da fonte original Bluloco

Localize e examine a fonte oficial do tema Bluloco Dark:
https://github.com/uloco/theme-bluloco-dark

Investigue:
- Arquivo de definição efetivamente publicado;
- Paleta global e cores de editor;
- Token colors, scopes e regras de precedência;
- Semantic token colors, quando existentes;
- Regras específicas para linguagens;
- Evolução de versões e changelog;
- Licença e atribuição exigida.

Use a versão/release identificada e registre commit ou tag de referência. Não dependa de uma branch mutável sem registrar a revisão consultada.

Construa uma matriz rastreável:
| Conceito/Scope de origem | Cor de origem | Lexer Notepad++ | Estilo/ID real | Cor aplicada | Fidelidade | Limitação |
Cada mapeamento deve ter justificativa. Quando não existir correspondência direta, selecione a aproximação mais coerente e marque-a como aproximação.

Não force uma equivalência de tokens quando a granularidade dos lexers for diferente.

## 5. Fase 2 — Auditoria XML e arquitetura dos estilos

Analise o XML inteiro, não apenas os primeiros lexers.

Verifique:
- XML bem-formado, encoding, estrutura e fechamento;
- Elementos permitidos e hierarquia correta;
- Atributos suportados e formatos válidos;
- Cores hexadecimais RGB com exatamente seis caracteres, sem `#`;
- Consistência de `fgColor`, `bgColor`, `fontName`, `fontStyle` e `fontSize`;
- IDs e nomes de estilos conforme o lexer correspondente;
- Estilos duplicados, conflitantes, sem uso ou potencialmente inoperantes;
- Diferenças de convenção entre lexers;
- Presença de lexers com cobertura incompleta;
- Estilos de interface global e elementos que dependem da versão do Notepad++;
- Compatibilidade com o mecanismo de temas e com as opções de configuração do usuário.

Não assuma que IDs iguais em lexers diferentes são conflito: valide no escopo correto. Não assuma que IDs diferentes no mesmo lexer são válidos sem consultar a especificação.

Avalie especialmente:
- `GlobalStyles`: fundo, texto, caret, seleção, linha atual, números de linha, margens, indentação, folding, whitespace, marcadores, busca, abas, URLs e document map;
- `LexerStyles`: tokens e estados específicos de cada linguagem;
- `Default Style` e `Global override`: efeitos colaterais e precedência;
- Cores de foreground/background em estados selecionados e destaques.

Evite cores de fundo e texto idênticas em indicadores de alteração, histórico ou marcadores quando isso impedir a leitura do estado. Confirme o significado de cada estilo antes de modificar.

## 6. Fase 3 — Design system cromático

Defina uma especificação central da paleta Bluloco Dark, com:
- Token semântico;
- Valor hexadecimal;
- Função visual;
- Contextos permitidos;
- Contextos proibidos;
- Contraste calculado com fundos relevantes;
- Relação com a paleta original;
- Justificativa para qualquer desvio.

Estabeleça regras de uso para:
- Texto padrão e texto secundário;
- Comentários e documentação;
- Keywords, operadores e pontuação;
- Strings, caracteres, regex e escapes;
- Números, booleanos, null e constantes;
- Funções, métodos, classes, interfaces, tipos e namespaces;
- Propriedades, variáveis, parâmetros e atributos;
- Erros, avisos, elementos inválidos e delimitadores;
- Tags, seletores, propriedades CSS e valores;
- Seleção, busca, linha atual e indicadores.

Avalie contraste por WCAG 2.2 quando aplicável, calculando a razão entre foreground e background. Considere que tokens de código são informação essencial e não devem depender exclusivamente da cor para comunicar estado. Preserve a identidade cromática; se um ajuste for necessário para legibilidade, prefira o menor desvio possível e documente-o.

Não aplique negrito/itálico indiscriminadamente. Use fontStyle com intenção semântica e compatibilidade comprovada.

## 7. Fase 4 — Revisão completa da cobertura de linguagens

Faça inventário de todos os lexers existentes e classifique a cobertura:
- Completa para os estilos disponíveis;
- Parcial;
- Básica;
- Inconsistente;
- Não suportada.

Priorize linguagens e formatos relevantes para desenvolvimento moderno, sem remover as linguagens já atendidas.

Audite, quando o lexer correspondente existir na versão-alvo:
- C, C++, C#, Java, Go, Rust, Swift, Kotlin e Dart;
- Python, JavaScript, TypeScript, PHP, Ruby, Lua e Perl;
- HTML, XML, CSS, SCSS e LESS;
- JSON, JSON5, YAML, TOML, INI e Markdown;
- SQL;
- Bash, Shell, PowerShell e Batch;
- CMake, Makefile, Dockerfile e arquivos de configuração;
- Diff/patch, logs e linguagens de consulta relevantes.

A lista é uma matriz de investigação, não autorização para criar lexers inexistentes. Para cada linguagem:
1. Identifique o lexer real e a versão do Notepad++ que o fornece.
2. Consulte os nomes e IDs reais dos estilos.
3. Mapeie todos os tokens úteis disponíveis.
4. Verifique strings multilinha, raw strings, comentários de documentação, regex, interpolação, escapes, números, operadores, tipos e palavras-chave.
5. Verifique se os estilos especiais dependem de keyword lists configuradas pelo usuário.
6. Diferencie o que é reconhecido nativamente do que depende de configuração adicional.
7. Crie amostras representativas para validação.

Aprimore especialmente JavaScript/TypeScript e linguagens de desenvolvimento corporativo, mas não favoreça essas linguagens a ponto de degradar a consistência do restante.

## 8. Fase 5 — Limites de semântica e USER KEYWORDS

O projeto utiliza estilos USER KEYWORDS para aproximar categorias semânticas. Faça uma revisão crítica dessa abordagem.

- Identifique quais lexers suportam subestilos e quais não suportam.
- Verifique os atributos e IDs de cada subestilo.
- Não classifique automaticamente qualquer identificador como função, classe ou propriedade sem contexto lexical confiável.
- Não prometa distinção de parâmetros, propriedades, constantes e métodos se o lexer não os separar.
- Documente como o usuário pode configurar listas de palavras-chave, quando aplicável.
- Evite sobreposição entre keyword lists que gere cores imprevisíveis.
- Garanta que estilos não configurados continuem legíveis.

Se a diferenciação semântica real depender de parser, plugin ou LSP externo, não simule essa capacidade no XML. Registre a limitação e proponha integração opcional apenas se houver benefício claro e compatibilidade comprovada.

## 9. Fase 6 — Experiência visual e ergonomia

Avalie o tema em uso prolongado, com foco em leitura e orientação visual:
- Hierarquia entre texto, comentários, keywords e identificadores;
- Separação visual de strings, números e operadores;
- Contraste de linha atual sem competir com seleção;
- Destaque de parênteses/chaves correspondentes e chaves inválidas;
- Busca e múltiplos marcadores;
- Guias de indentação e símbolos de whitespace;
- Margens, folding e numeração;
- Histórico de alterações;
- Abas e indicadores de foco;
- Document Map e painéis que aceitam estilização pelo tema.

Evite saturação excessiva, excesso de cores concorrentes, baixo contraste e fundos coloridos em excesso. Não modifique o design para ficar visualmente chamativo em screenshots sacrificando leitura real.

## 10. Fase 7 — Ferramentas de validação e testes

O repositório atualmente não possui uma suíte de testes consolidada. Implemente uma validação leve, reproduzível e documentada, preferencialmente com ferramentas já disponíveis no ambiente ou scripts simples.

No mínimo:
1. Parse XML completo e falhe em caso de documento inválido.
2. Valide o formato de todas as cores.
3. Detecte atributos inesperados, valores vazios suspeitos e estilos duplicados segundo regras conscientes do escopo.
4. Compare inventário de lexers e estilos com a baseline.
5. Verifique se todas as cores referenciadas existem na especificação da paleta ou estão justificadas como exceções.
6. Gere relatório de cobertura por lexer.
7. Calcule contraste para pares relevantes e destaque resultados abaixo dos critérios definidos.
8. Garanta que documentação e arquivos de instalação apontem para o nome real do XML.
9. Verifique links locais de screenshots e consistência dos nomes.
10. Execute validação de regressão antes e depois das alterações.

Não invente uma validação que apenas verifica sintaxe XML e a apresente como teste visual. A validação visual exige screenshots reais, Notepad++ executando e amostras carregadas.

Quando não houver Windows/Notepad++ disponível:
- Execute todas as validações estáticas possíveis;
- Registre explicitamente o que não pôde ser testado;
- Não declare compatibilidade visual confirmada;
- Forneça um roteiro de validação manual reproduzível.

Crie amostras de código por linguagem com construções comuns e casos de borda. Evite colocar código de teste dentro do XML do tema.

## 11. Fase 8 — Galeria visual e evidências

Atualize a galeria apenas com screenshots reais, obtidas com o tema aplicado no Notepad++.

Inclua, quando possível:
- JavaScript e TypeScript;
- Python;
- C# ou Java;
- HTML/CSS;
- JSON/YAML;
- SQL;
- PowerShell ou Bash.

As imagens devem usar:
- Mesma configuração de fonte e tamanho entre comparações;
- Trechos representativos e legíveis;
- Fundo e tema efetivamente aplicados;
- Ausência de dados pessoais, tokens ou segredos;
- Recortes que mostrem tanto sintaxe quanto interface.

Não gere screenshots falsas por HTML, SVG, terminal ou editor diferente e as apresente como captura do Notepad++. Se não for possível capturar, mantenha as imagens existentes e documente a limitação.

## 12. Fase 9 — Documentação

Atualize o README para refletir fielmente o estado final:
- Descrição do tema e objetivos;
- Paleta oficial do projeto e mapeamento para o original;
- Linguagens e nível real de cobertura;
- Limitações do modelo de lexers do Notepad++;
- Requisitos e versões testadas;
- Instalação manual e importação;
- Configuração de fontes;
- Personalização e keyword lists;
- Validação automatizada;
- Galeria de screenshots;
- Troubleshooting;
- Changelog;
- Créditos, origem e licença.

Corrija divergências existentes entre README e XML. Não anuncie recurso que não esteja implementado. Não use expressões como “full semantic support”, “pixel-perfect” ou “20+ linguagens totalmente suportadas” sem critérios e evidências objetivos.

Revise `AGENTS.md` com:
- Estrutura atual do repositório;
- Regras de edição do tema;
- Como validar XML e paleta;
- Como executar testes;
- Como adicionar um lexer sem inventar IDs;
- Regras de screenshots e documentação;
- Limitações conhecidas.

## 13. Fase 10 — Compatibilidade e distribuição

Verifique o formato esperado pelo Notepad++ e a localização de instalação. Confirme o nome oficial do arquivo e elimine referências inconsistentes a nomes alternativos, sem quebrar compatibilidade com instalações existentes.

Avalie:
- Instalação por importação;
- Instalação manual no diretório de temas;
- Compatibilidade com versões suportadas;
- Preservação das configurações pessoais;
- Distribuição do XML sem dependências;
- Licença e atribuição da obra original.

Não crie instalador, plugin ou mecanismo de atualização automática sem necessidade demonstrada.

## 14. Processo de implementação

Execute em ciclos coesos:

1. Reconhecimento e baseline.
2. Auditoria de fonte e especificação.
3. Correções estruturais comprovadas.
4. Refinamento da paleta e estilos globais.
5. Revisão dos lexers e cobertura.
6. Testes automatizados e amostras.
7. Documentação e screenshots.
8. Revisão independente e regressão final.

Ao fim de cada ciclo:
- Registre arquivos alterados;
- Explique o motivo das mudanças;
- Execute as validações disponíveis;
- Corrija falhas introduzidas antes de prosseguir.

Faça alterações em lotes lógicos. Não teste manualmente um token por vez quando uma suíte de validação por lexer puder cobrir o conjunto.

## 15. Critérios de aceite

A tarefa só poderá ser considerada concluída quando:

- [ ] O XML estiver bem-formado e passar nas validações implementadas.
- [ ] Todos os estilos adicionados tiverem correspondência comprovada com o lexer.
- [ ] Não houver cores inválidas ou atributos arbitrários.
- [ ] A paleta estiver documentada e rastreável à fonte original.
- [ ] As discrepâncias entre README, XML e screenshots estiverem corrigidas.
- [ ] A cobertura de linguagens estiver inventariada e classificada honestamente.
- [ ] USER KEYWORDS e limitações semânticas estiverem documentados.
- [ ] Não houver regressões conhecidas nos lexers existentes.
- [ ] Os estilos globais essenciais estiverem revisados.
- [ ] Os testes estáticos e de regressão estiverem executados.
- [ ] Os testes não executáveis no ambiente estiverem explicitamente identificados.
- [ ] A instalação estiver documentada e usar o nome correto do arquivo.
- [ ] A licença e os créditos estiverem preservados.
- [ ] `AGENTS.md` e `README.md` refletirem a implementação real.
- [ ] O diff tiver sido revisado para remover alterações acidentais.

## 16. Revisão adversarial final

Antes de concluir, assuma o papel de um revisor independente e procure deliberadamente:
- IDs incorretos ou estilos não reconhecidos;
- Estilos duplicados e regras conflitantes;
- Tokens que ficaram invisíveis ou com contraste ruim;
- Cores sem função semântica consistente;
- Divergências entre tema original e conversão;
- Linguagens anunciadas sem cobertura real;
- Estilos sem efeito no Notepad++;
- Regressões em estilos globais;
- Documentação exagerada ou desatualizada;
- Screenshots que não correspondam ao XML final.

Corrija os problemas encontrados e repita as validações.

## 17. Relatório final obrigatório

Entregue um relatório conciso, mas completo, contendo:

1. Resumo das melhorias implementadas.
2. Arquivos alterados e finalidade de cada alteração.
3. Mudanças na paleta e justificativas.
4. Lexers revisados e cobertura alcançada.
5. Testes executados, comandos e resultados.
6. Testes que não puderam ser executados e motivo.
7. Limitações conhecidas do Notepad++.
8. Evidências visuais disponíveis.
9. Riscos residuais.
10. Branch e commits realizados, com links.
11. Checklist de critérios de aceite.

Não declare sucesso com base apenas em alterações de código. O resultado precisa ser sustentado por validações reais.

## Diretriz final

Priorize **fidelidade, legibilidade, consistência, compatibilidade e precisão técnica**. O resultado deve parecer uma implementação cuidadosamente projetada do Bluloco Dark dentro das capacidades reais do Notepad++, e não uma coleção de cores aplicadas indiscriminadamente.

Comece agora pela Fase 0. Faça o reconhecimento completo, registre a baseline e prossiga pelas fases em sequência, sem retrabalho e sem interromper o fluxo por confirmações desnecessárias.
