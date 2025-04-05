const API_URL = "http://127.0.0.1:5000/api/relatorios";
let paginaAtual = 1;

document.addEventListener("DOMContentLoaded", () => {
  carregarRelatorios(paginaAtual);
});

function carregarRelatorios(pagina) {
  fetch(`${API_URL}?page=${pagina}`)
    .then(response => {
      if (!response.ok) throw new Error("Erro ao buscar relatórios.");
      return response.json();
    })
    .then(relatorios => {
      exibirRelatorios(relatorios);
      document.getElementById("pagina-atual").textContent = pagina;
      paginaAtual = pagina;
    })
    .catch(err => {
      console.error(err);
      document.getElementById("relatorios-container").innerHTML = `<p class="text-danger">Erro ao carregar relatórios.</p>`;
    });
}

function exibirRelatorios(relatorios) {
  const container = document.getElementById("relatorios-container");
  container.innerHTML = "";

  relatorios.forEach(r => {
    const card = document.createElement("div");
    card.className = "col-6 col-md-4 col-lg-3";
    card.innerHTML = `
      <div class="relatorio-card p-0">
        <div style="height: 120px; overflow: hidden;">
          <img src="/uploads/${r.caminho_pasta}/capa.jpg"
            onerror="this.onerror=null; this.src='https://picsum.photos/300/120?grayscale'"
            class="w-100 h-100"
            style="object-fit: cover;"
            alt="Capa do relatório">
        </div>
        <div class="p-2">
          <h5>${r.assunto}</h5>
          <p>${r.descricao || "Sem descrição"}</p>
          <a href="/uploads/${r.caminho_pasta}/relatorio.html" class="btn btn-sm btn-outline-danger mt-2">Ver relatório</a>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

function mudarPagina(incremento) {
  const novaPagina = paginaAtual + incremento;
  if (novaPagina < 1) return;
  carregarRelatorios(novaPagina);
}



document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  const linkAluno = document.getElementById("link-aluno");
  const linkLogin = document.getElementById("link-login");
  const linkCadastro = document.getElementById("link-cadastro");
  const linkSair = document.getElementById("link-sair");

  if (token) {
    if (linkAluno) linkAluno.classList.remove("d-none");
    if (linkLogin) linkLogin.classList.add("d-none");
    if (linkCadastro) linkCadastro.classList.add("d-none");
    if (linkSair) linkSair.classList.remove("d-none");
  } else {
    if (linkAluno) linkAluno.classList.add("d-none");
    if (linkLogin) linkLogin.classList.remove("d-none");
    if (linkCadastro) linkCadastro.classList.remove("d-none");
    if (linkSair) linkSair.classList.add("d-none");
  }

  if (linkSair) {
    linkSair.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("token");
      window.location.reload();
    });
  }
});