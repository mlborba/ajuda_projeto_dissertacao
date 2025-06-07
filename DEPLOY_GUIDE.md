# Guia de Deploy no Vercel

## Pré-requisitos

1. **Conta no Vercel**: Crie uma conta gratuita em https://vercel.com
2. **Chave da API do Google Gemini**: Obtenha em https://makersuite.google.com/app/apikey

## Método 1: Deploy via Interface Web (Recomendado)

### Passo 1: Preparar os Arquivos
1. Baixe todos os arquivos do projeto
2. Certifique-se de que a estrutura está assim:
   ```
   dissertacao-app/
   ├── index.html
   ├── api/
   │   └── gerar.py
   ├── requirements.txt
   ├── vercel.json
   ├── .env.example
   └── README.md
   ```

### Passo 2: Fazer Upload no Vercel
1. Acesse https://vercel.com/dashboard
2. Clique em "New Project"
3. Selecione "Upload" (não conecte ao Git ainda)
4. Arraste a pasta `dissertacao-app` ou selecione os arquivos
5. Clique em "Deploy"

### Passo 3: Configurar Variável de Ambiente
1. Após o deploy inicial, vá para o dashboard do projeto
2. Clique em "Settings" no menu superior
3. Selecione "Environment Variables" no menu lateral
4. Clique em "Add New"
5. Configure:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Sua chave da API do Gemini
   - **Environment**: Selecione "Production" (e "Development" se quiser testar)
6. Clique em "Save"

### Passo 4: Redesploy
1. Vá para a aba "Deployments"
2. Clique nos três pontos (...) do último deployment
3. Selecione "Redeploy"
4. Aguarde o processo terminar

## Método 2: Deploy via CLI

### Passo 1: Instalar Vercel CLI
```bash
npm install -g vercel
```

### Passo 2: Login
```bash
vercel login
```

### Passo 3: Deploy
```bash
cd dissertacao-app
vercel
```

### Passo 4: Configurar Variável de Ambiente
```bash
vercel env add GEMINI_API_KEY
```

## Método 3: Deploy via Git (Recomendado para Projetos Contínuos)

### Passo 1: Criar Repositório no GitHub
1. Crie um novo repositório no GitHub
2. Faça upload dos arquivos do projeto

### Passo 2: Conectar ao Vercel
1. No Vercel, clique em "New Project"
2. Selecione "Import Git Repository"
3. Conecte sua conta do GitHub
4. Selecione o repositório criado
5. Configure as variáveis de ambiente antes do deploy

## Obtendo a Chave da API do Gemini

1. Acesse https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Selecione um projeto existente ou crie um novo
5. Copie a chave gerada
6. **IMPORTANTE**: Mantenha esta chave segura e nunca a compartilhe

## Verificação do Deploy

Após o deploy bem-sucedido:

1. Acesse a URL fornecida pelo Vercel
2. Teste inserindo um problema de pesquisa
3. Clique em "Gerar Proposta Completa"
4. Verifique se a aplicação gera os resultados corretamente

## Solução de Problemas

### Erro: "Chave da API do Gemini não configurada"
- Verifique se a variável `GEMINI_API_KEY` foi configurada corretamente
- Certifique-se de que o valor não contém espaços extras
- Faça um redeploy após configurar a variável

### Erro: "Function timeout"
- A API do Gemini pode demorar para responder
- Isso é normal para prompts complexos
- O timeout padrão do Vercel é de 10 segundos para contas gratuitas

### Erro: "CORS"
- Verifique se o arquivo `api/gerar.py` inclui `flask-cors`
- Certifique-se de que `CORS(app)` está configurado

## Atualizações Futuras

Para atualizar a aplicação:

1. **Via Git**: Faça push das alterações para o repositório
2. **Via Interface**: Faça upload dos novos arquivos
3. **Via CLI**: Execute `vercel` novamente na pasta do projeto

## Limites da Conta Gratuita

- 100GB de largura de banda por mês
- 100 execuções de função por dia
- Timeout de 10 segundos por função
- 1 projeto simultâneo

Para uso intensivo, considere upgradar para um plano pago.

