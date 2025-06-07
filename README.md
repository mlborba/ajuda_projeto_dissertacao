# Apoio à Construção da Dissertação

Uma aplicação web que utiliza IA para auxiliar na criação de propostas de dissertação acadêmica.

## Funcionalidades

- Geração automática de objetivos gerais e específicos
- Criação de justificativa detalhada
- Sugestão de metodologia aplicável
- Lista de principais pesquisadores e obras relevantes
- Refinamento de seções individuais

## Tecnologias Utilizadas

- **Frontend**: HTML, CSS (Tailwind), JavaScript
- **Backend**: Flask (Python)
- **IA**: Google Gemini API
- **Deploy**: Vercel

## Configuração Local

1. Clone ou baixe os arquivos do projeto
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure a variável de ambiente:
   ```bash
   export GEMINI_API_KEY="sua_chave_api_aqui"
   ```
4. Execute a aplicação:
   ```bash
   python api/gerar.py
   ```
5. Acesse `http://localhost:5000`

## Deploy no Vercel

### Pré-requisitos
- Conta no Vercel (https://vercel.com)
- Chave da API do Google Gemini

### Passos para Deploy

1. **Instale o Vercel CLI** (opcional):
   ```bash
   npm install -g vercel
   ```

2. **Faça upload dos arquivos**:
   - Acesse https://vercel.com/dashboard
   - Clique em "New Project"
   - Faça upload da pasta do projeto ou conecte um repositório Git

3. **Configure a variável de ambiente**:
   - No dashboard do Vercel, vá para Settings > Environment Variables
   - Adicione uma nova variável:
     - Name: `GEMINI_API_KEY`
     - Value: sua chave da API do Gemini
     - Environment: Production (e Development se necessário)

4. **Deploy**:
   - O Vercel detectará automaticamente a configuração
   - O deploy será feito automaticamente
   - Você receberá uma URL pública para acessar a aplicação

### Obtendo a Chave da API do Gemini

1. Acesse https://makersuite.google.com/app/apikey
2. Crie uma nova chave de API
3. Copie a chave gerada
4. Configure no Vercel conforme instruções acima

## Estrutura do Projeto

```
dissertacao-app/
├── index.html          # Frontend da aplicação
├── api/
│   └── gerar.py        # Backend Flask
├── requirements.txt    # Dependências Python
├── vercel.json        # Configuração do Vercel
└── README.md          # Este arquivo
```

## Uso da Aplicação

1. Acesse a aplicação web
2. Digite seu problema de pesquisa no campo de texto
3. Clique em "Gerar Proposta Completa"
4. Aguarde a geração dos resultados
5. Use os botões de cópia para copiar seções específicas
6. Use o campo "Refinar" para melhorar seções individuais

## Suporte

Para problemas ou dúvidas, verifique:
- Se a chave da API está configurada corretamente
- Se todas as dependências estão instaladas
- Se há conectividade com a internet para acessar a API do Gemini

