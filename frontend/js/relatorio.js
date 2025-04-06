document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const relatorioId = params.get("id");

  if (!relatorioId) {
    alert("ID do relatório não fornecido.");
    return;
  }

  fetch(`http://127.0.0.1:5000/api/relatorios/${relatorioId}`)
    .then((res) => {
      if (!res.ok) {
        throw new Error("Relatório não encontrado.");
      }
      return res.json();
    })
    .then((relatorio) => {
      const iframe = document.querySelector("iframe");
      iframe.src = `../backend/uploads/${relatorio.caminho_pasta}/relatorio.html`;
    })
    .catch((err) => {
      console.error(err);
      alert("Erro ao carregar o relatório.");
    });
});

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