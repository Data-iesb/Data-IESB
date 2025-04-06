document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
  
    const linkAluno = document.getElementById("link-aluno");
    const linkLogin = document.getElementById("link-login");
    const linkCadastro = document.getElementById("link-cadastro");
    const linkSair = document.getElementById("link-sair");
  
    if (token) {
      if (linkLogin) linkLogin.style.display = "none";
      if (linkCadastro) linkCadastro.style.display = "none";
    } else {
      if (linkAluno) linkAluno.style.display = "none";
      if (linkSair) linkCadastro.style.display = "none";
    }
  
    if (linkSair) {
      linkSair.addEventListener("click", (e) => {
        e.preventDefault();
        localStorage.removeItem("token");
        window.location.reload();
      });
    }
  });