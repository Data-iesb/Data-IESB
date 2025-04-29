document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const relatorioId = params.get("id");

  if (!relatorioId) {
    alert("ID do relatório não fornecido.");
    return;
  }

  fetch(config.API_URL + `/api/relatorios/${relatorioId}`)
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