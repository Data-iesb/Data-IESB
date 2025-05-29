let paginaAtual = 1;

document.addEventListener("DOMContentLoaded", () => {
  carregarRelatorios(paginaAtual);
});

function carregarRelatorios(pagina) {
  fetch(config.API_URL + `/api/relatorios?page=${pagina}`)
    .then(response => {
      console.log(response);
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
    <a href="relatorio.html?id=${r.id}" class="text-decoration-none text-dark">
      <div class="relatorio-card p-0">
        <div style="height: 120px; overflow: hidden;">
        
          <img src="/static/${r.caminho_pasta}/capa.jpg" class="w-100 h-100" style="object-fit: cover;" alt="Capa do relatório">
        </div>
        <div class="p-2">
          <h5 class="mb-1">${r.assunto}</h5>
          <p class="text-muted" style="font-size: 0.85rem;">${r.descricao || "Sem descrição"}</p>
          <a href="../backend/uploads/${r.caminho_pasta}/relatorio.html" target="_blank" class="btn btn-sm btn-outline-danger me-1">Ver</a>
          <button class="btn btn-sm btn-outline-secondary" onclick="deletarRelatorio(${r.id})">Excluir</button>
        </div>
      </div>
    </a>
    `;
    container.appendChild(card);
  });
}

function mudarPagina(incremento) {
  const novaPagina = paginaAtual + incremento;
  if (novaPagina < 1) return;
  carregarRelatorios(novaPagina);
}