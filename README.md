# Conteúdo do README

# 📊 Data IESB

Plataforma web para alunos do curso de Ciência de Dados do IESB publicarem e visualizarem **relatórios interativos em HTML**.

---

## 🚀 Funcionalidades

- Cadastro de alunos com senha criptografada
- Autenticação via token JWT
- Publicação de relatórios em HTML
- Listagem de todos os relatórios publicados
- Associação de relatórios com o autor e metadados (data e assunto)

---

## 🧱 Arquitetura

- **Frontend**: HTML, CSS, JavaScript puro
- **Backend**: Python + Flask
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT
- **Armazenamento**: Relatórios HTML salvos localmente em `/uploads/`

---

## 📦 Instalação e Execução Local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/data-iesb.git
cd data-iesb
```

### 2. Configure o ambiente Python
  
### 3. Configure variáveis de ambiente
   
### 4. Execute o servidor
   
## 🛠️ Banco de Dados

## ✅ Fluxo do MVP
- Aluno se cadastra (POST /api/aluno)

- Aluno faz login e recebe um token JWT

- Aluno publica um relatório HTML (POST /api/relatorios)

- Qualquer usuário pode visualizar relatórios (GET /api/relatorios)

## 🛡️ Segurança
- Senhas armazenadas com hash

- Tokens JWT com expiração

- Uploads com nomes únicos

- Rotas protegidas por JWT (@jwt_required())

## 📚 Créditos
- Este projeto é parte do curso de Ciência de Dados do IESB.

- Desenvolvido como um MVP para publicação de relatórios interativos.

## 📄 Licença
- MIT

