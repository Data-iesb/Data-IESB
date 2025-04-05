const API_URL = "http://localhost:5000";

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("token");
    console.log(localStorage)
  
    if (!token) {
      window.location.href = "login.html";
      return;
    }
  
    try {
      const resp = await fetch(API_URL+"/api/aluno/me", {
        headers: { Authorization: `Bearer ${token}` }
      });
  
      if (!resp.ok) throw new Error("Não autorizado");
  
      const aluno = await resp.json();
  
      document.getElementById("aluno-nome").textContent = aluno.nome;
      document.getElementById("aluno-email").textContent = aluno.email;
      document.getElementById("aluno-curso").textContent = aluno.curso;
      document.getElementById("aluno-periodo").textContent = aluno.periodo + "º";

      carregarRelatoriosDoAluno();
  
    } catch (erro) {
      console.error(erro);
    }
  });

  async function carregarRelatoriosDoAluno() {
  const token = localStorage.getItem("token");
  const container = document.getElementById("meus-relatorios");
  container.innerHTML = "";

  try {
    const resp = await fetch("/api/relatorios/me", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!resp.ok) throw new Error("Erro ao carregar relatórios.");

    const relatorios = await resp.json();

    if (relatorios.length === 0) {
      container.innerHTML = "<p>Nenhum relatório publicado ainda.</p>";
      return;
    }

    relatorios.forEach(r => {
      const card = document.createElement("div");
      card.className = "col-6 col-md-4 col-lg-3";
      card.innerHTML = `
        <div class="relatorio-card p-0">
          <div style="height: 120px; overflow: hidden;">
            <img src="/uploads/${r.caminho_pasta}/capa.jpg" class="w-100 h-100" style="object-fit: cover;" alt="Capa do relatório">
          </div>
          <div class="p-2">
            <h5 class="mb-1">${r.assunto}</h5>
            <p class="text-muted" style="font-size: 0.85rem;">${r.descricao || "Sem descrição"}</p>
            <a href="/uploads/${r.caminho_pasta}/relatorio.html" target="_blank" class="btn btn-sm btn-outline-danger me-1">Ver</a>
            <button class="btn btn-sm btn-outline-secondary" onclick="deletarRelatorio(${r.id})">Excluir</button>
          </div>
        </div>
      `;
      container.appendChild(card);
    });

  } catch (erro) {
    console.error(erro);
    container.innerHTML = "<p class='text-danger'>Erro ao carregar relatórios.</p>";
  }
}



async function carregarRelatoriosDoAluno() {
    const token = localStorage.getItem("token");
    const container = document.getElementById("meus-relatorios");
    container.innerHTML = "";

    console.log("aqui")
  
    try {
      const resp = await fetch(API_URL + "/api/relatorios/me", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
  
      if (!resp.ok) throw new Error("Erro ao carregar relatórios.");
  
      const relatorios = await resp.json();
  
      if (relatorios.length === 0) {
        container.innerHTML = "<p>Nenhum relatório publicado ainda.</p>";
        return;
      }
  
      relatorios.forEach(r => {
        const card = document.createElement("div");
        card.className = "col-6 col-md-4 col-lg-3";
        card.innerHTML = `
          <div class="relatorio-card p-0">
            <div style="height: 120px; overflow: hidden;">
              <img src="/uploads/${r.caminho_pasta}/capa.jpg" class="w-100 h-100" style="object-fit: cover;" alt="Capa do relatório">
            </div>
            <div class="p-2">
              <h5 class="mb-1">${r.assunto}</h5>
              <p class="text-muted" style="font-size: 0.85rem;">${r.descricao || "Sem descrição"}</p>
              <a href="/uploads/${r.caminho_pasta}/relatorio.html" target="_blank" class="btn btn-sm btn-outline-danger me-1">Ver</a>
              <button class="btn btn-sm btn-outline-secondary" onclick="deletarRelatorio(${r.id})">Excluir</button>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
  
} catch (erro) {
    console.error(erro);
    container.innerHTML = "<p class='text-danger'>Erro ao carregar relatórios.</p>";
}
}



async function deletarRelatorio(id) {
const confirmar = confirm("Tem certeza que deseja excluir este relatório?");
if (!confirmar) return;

const token = localStorage.getItem("token");

try {
    const resposta = await fetch(API_URL + `/api/relatorios/${id}`, {
    method: "DELETE",
    headers: {
        Authorization: `Bearer ${token}`
    }
    });

    const resultado = await resposta.json();

    if (!resposta.ok) {
    alert(resultado.erro || "Erro ao excluir relatório.");
    return;
    }

    alert("Relatório excluído com sucesso.");
    carregarRelatoriosDoAluno();

} catch (erro) {
    console.error(erro);
    alert("Erro ao excluir relatório.");
}
}

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