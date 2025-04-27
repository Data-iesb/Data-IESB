const API_URL = "http://127.0.0.1:5000";

document.getElementById("form-relatorio").addEventListener("submit", async (e) => {
    e.preventDefault();
  
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Você precisa estar logado para publicar um relatório.");
      return;
    }
  
    const titulo = document.getElementById("titulo").value;
    const descricao = document.getElementById("descricao").value;
    const assunto = document.getElementById("assunto").value;
    const arquivo = document.getElementById("arquivo").files[0];
    const capa = document.getElementById("capa").files[0];
  
    const formData = new FormData();
    formData.append("titulo", titulo);
    formData.append("descricao", descricao);
    formData.append("assunto", assunto);
    formData.append("arquivo", arquivo);
    formData.append("capa", capa);
  
    const mensagemErro = document.getElementById("mensagem-erro");
    const mensagemSucesso = document.getElementById("mensagem-sucesso");
  
    try {
      const resposta = await fetch(API_URL + "/api/relatorios", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      });
  
      const resultado = await resposta.json();
  
      if (!resposta.ok) {
        mensagemErro.textContent = resultado.erro || "Erro ao enviar relatório.";
        mensagemErro.classList.remove("d-none");
        mensagemSucesso.classList.add("d-none");
        return;
      }
  
      mensagemSucesso.textContent = "Relatório publicado com sucesso!";
      mensagemSucesso.classList.remove("d-none");
      mensagemErro.classList.add("d-none");
      document.getElementById("form-relatorio").reset();
  
    } catch (erro) {
      console.error(erro);
      mensagemErro.textContent = "Erro ao conectar com o servidor.";
      mensagemErro.classList.remove("d-none");
      mensagemSucesso.classList.add("d-none");
    }
  });
  