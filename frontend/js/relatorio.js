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
    .then((obj) => {
      const iframe = document.querySelector("iframe");
      iframe.src = `http://k8s-default-ingressi-73bd0705e3-102651203.sa-east-1.elb.amazonaws.com:8501/relatorio/${obj.relatorio.id}`;
    })
    .catch((err) => {
      console.error(err);
      alert("Erro ao carregar o relatório.");
    });
});
