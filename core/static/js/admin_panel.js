document.addEventListener("DOMContentLoaded", function() {
  // ====== VARIABLES ======
  let currentEntity = "users";
  let data = [];
  const tableHead = document.getElementById("table-head");
  const tableBody = document.getElementById("table-body");
  const modal = document.getElementById("modal");
  const modalTitle = document.getElementById("modal-title");
  const modalContent = document.getElementById("modal-content");
  const searchInput = document.getElementById("search-input");
  const addBtn = document.getElementById("add-btn");
  const saveBtn = document.getElementById("save-btn");
  const cancelBtn = document.getElementById("cancel-btn");

  // ====== MENU ======
  document.querySelectorAll(".admin-menu-item").forEach(btn => {
    btn.addEventListener("click", () => {
      currentEntity = btn.dataset.entity;
      document.getElementById("admin-title").innerText = btn.innerText;
      fetchData();
    });
  });

  // ====== FETCH DATA ======
  async function fetchData() {
    try {
      const res = await fetch(`/api/admin/${currentEntity}/`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
      });
      data = await res.json();
      renderTable();
    } catch(e){ console.error(e); }
  }

  // ====== RENDER TABLE ======
  function renderTable() {
    tableHead.innerHTML = "";
    tableBody.innerHTML = "";
    if(data.length === 0) return tableHead.innerHTML = "<th>Нет данных</th>";

    const keys = Object.keys(data[0]);
    const trHead = document.createElement("tr");
    keys.forEach(k=>{
      const th = document.createElement("th");
      th.innerText = k.charAt(0).toUpperCase()+k.slice(1);
      th.className = "px-4 py-2 text-left";
      trHead.appendChild(th);
    });
    const thAction = document.createElement("th");
    thAction.innerText = "Действия";
    thAction.className = "px-4 py-2";
    trHead.appendChild(thAction);
    tableHead.appendChild(trHead);

    data.forEach(item=>{
      const tr = document.createElement("tr");
      keys.forEach(k=>{
        const td = document.createElement("td");
        td.innerText = item[k];
        td.className = "px-4 py-2";
        tr.appendChild(td);
      });
      const tdAction = document.createElement("td");
      tdAction.className = "px-4 py-2 flex gap-2";
      const editBtn = document.createElement("button");
      editBtn.innerText = "Редактировать";
      editBtn.className = "bg-yellow-500 hover:bg-yellow-600 text-white px-2 py-1 rounded text-xs";
      editBtn.onclick = ()=> openEditModal(item);
      const delBtn = document.createElement("button");
      delBtn.innerText = "Удалить";
      delBtn.className = "bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-xs";
      delBtn.onclick = ()=> deleteItem(item.id);
      tdAction.appendChild(editBtn);
      tdAction.appendChild(delBtn);
      tr.appendChild(tdAction);
      tableBody.appendChild(tr);
    });
  }

  // ====== MODAL ======
  window.openAddModal = function() {
    modalTitle.innerText = `Добавить ${currentEntity}`;
    modalContent.innerHTML = generateForm({});
    modal.classList.remove("hidden");
  };

  window.openEditModal = function(item) {
    modalTitle.innerText = `Редактировать ${currentEntity}`;
    modalContent.innerHTML = generateForm(item);
    modal.classList.remove("hidden");
  };

  window.closeModal = function() {
    modal.classList.add("hidden");
  };

  cancelBtn.addEventListener("click", closeModal);

  // ====== FORM GENERATOR ======
  function generateForm(item){
    let html = '';
    for(const key in item){
      html += `<label class="block text-sm">${key}<input class="w-full bg-slate-800 border border-slate-700 px-2 py-1 rounded mt-1 mb-2" name="${key}" value="${item[key]||''}"/></label>`;
    }
    if(Object.keys(item).length===0){
      html += `<label class="block text-sm">Название<input class="w-full bg-slate-800 border border-slate-700 px-2 py-1 rounded mt-1 mb-2" name="name"/></label>`;
    }
    return html;
  }

  // ====== SAVE ======
  window.saveEntity = async function() {
    const inputs = modalContent.querySelectorAll("input, select");
    let body = {};
    inputs.forEach(i=> body[i.name]=i.value);
    let method = body.id ? "PUT" : "POST";
    let url = `/api/admin/${currentEntity}/${body.id ? body.id+'/' : ''}`;
    try{
      const res = await fetch(url,{
        method,
        headers:{
          "Content-Type":"application/json",
          "Authorization": `Bearer ${localStorage.getItem('admin_token')}`
        },
        body: JSON.stringify(body)
      });
      if(res.ok){ closeModal(); fetchData(); }
      else alert("Ошибка сохранения");
    }catch(e){ console.error(e); }
  };

  // ====== DELETE ======
  async function deleteItem(id){
    if(!confirm("Удалить запись?")) return;
    try{
      const res = await fetch(`/api/admin/${currentEntity}/${id}/`,{
        method:"DELETE",
        headers:{ "Authorization": `Bearer ${localStorage.getItem('admin_token')}` }
      });
      if(res.ok) fetchData();
    }catch(e){ console.error(e); }
  }

  // ====== SEARCH ======
  searchInput?.addEventListener("input", ()=>{
    const q = searchInput.value.toLowerCase();
    const filtered = data.filter(d=>Object.values(d).some(v=>v.toString().toLowerCase().includes(q)));
    tableBody.innerHTML = "";
    filtered.forEach(item=>{
      const keys = Object.keys(item);
      const tr = document.createElement("tr");
      keys.forEach(k=>{
        const td = document.createElement("td");
        td.innerText = item[k];
        td.className = "px-4 py-2";
        tr.appendChild(td);
      });
      const tdAction = document.createElement("td");
      tdAction.className = "px-4 py-2 flex gap-2";
      const editBtn = document.createElement("button");
      editBtn.innerText = "Редактировать";
      editBtn.className = "bg-yellow-500 hover:bg-yellow-600 text-white px-2 py-1 rounded text-xs";
      editBtn.onclick = ()=> openEditModal(item);
      const delBtn = document.createElement("button");
      delBtn.innerText = "Удалить";
      delBtn.className = "bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-xs";
      delBtn.onclick = ()=> deleteItem(item.id);
      tdAction.appendChild(editBtn);
      tdAction.appendChild(delBtn);
      tr.appendChild(tdAction);
      tableBody.appendChild(tr);
    });
  });

  // ====== INITIAL LOAD ======
  fetchData();
});
