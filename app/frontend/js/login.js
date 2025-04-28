const API_URL = "http://ec2-3-82-1-192.compute-1.amazonaws.com/:80";

document.getElementById("form-login").addEventListener("submit", async (e) => {
    e.preventDefault();
  
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value.trim();
    const msgErro = document.getElementById("mensagem-erro");
  
    try {
      const resposta = await fetch(API_URL + "/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha })
      });
  
      const dados = await resposta.json();
  
      if (!resposta.ok) {
        msgErro.textContent = dados.erro || "Erro ao fazer login.";
        msgErro.classList.remove("d-none");
        return;
      }
  
      // Login bem-sucedido
      localStorage.setItem("token", dados.token);
      window.location.href = "aluno.html";
  
    } catch (erro) {
      msgErro.textContent = "Erro de conexão com o servidor.";
      msgErro.classList.remove("d-none");
      console.error(erro);
    }
  });
