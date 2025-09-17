

let token = '';
let currentUser = null;

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('http://localhost:8000/api/token/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        token = data.access;
        fetchUserDetails();
    })
    .catch(err => alert('Login failed'));
}

function fetchUserDetails() {
    fetch('http://localhost:8000/api/users/', {
        headers: {'Authorization': `Bearer ${token}`}
    })
    .then(res => res.json())
    .then(users => {
        currentUser = users.find(u => u.username === document.getElementById('username').value);
        document.getElementById('loginDiv').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        document.getElementById('welcome').innerText = `Welcome ${currentUser.username}!`;

        if(currentUser.is_trainer){
            document.getElementById('trainerActions').style.display = 'block';
            fetchProjects(); // trainer sees all projects
        } else {
            fetchProjects(currentUser.id); // trainee sees only assigned
        }
    });
}

// Fetch and display projects
function fetchProjects(userId=null, filters={}) {
    let url = 'http://localhost:8000/api/projects/';
    let query = [];
    if(filters.due_date) query.push(`due_date=${filters.due_date}`);
    if(filters.priority) query.push(`priority=${filters.priority}`);
    if(query.length > 0) url += `?${query.join('&')}`;

    fetch(url, { headers: {'Authorization': `Bearer ${token}`}})
    .then(res => res.json())
    .then(projects => {
        if(userId) projects = projects.filter(p => p.assigned_to.id === userId);
        displayProjects(projects);
    });
}

// Display projects
function displayProjects(projects){
    const projectsDiv = document.getElementById('projects');
    projectsDiv.innerHTML = '';
    projects.forEach(p => {
        const div = document.createElement('div');
        div.className = 'project-card';
        let actions = '';
        if(currentUser.is_trainer){
            actions = `<button onclick="editProject(${p.id})">Edit</button>
                       <button onclick="deleteProject(${p.id})">Delete</button>`;
        } else if(currentUser.is_trainee){
            actions = `<button onclick="updateStatus(${p.id})">Update Status</button>`;
        }

        div.innerHTML = `
            <h3>${p.title}</h3>
            <p>${p.description}</p>
            <p>Status: ${p.status}</p>
            <p>Due: ${p.due_date}</p>
            <p>Priority: ${p.priority}</p>
            ${actions}
        `;
        projectsDiv.appendChild(div);
    });
}

// Trainer: Save project (create/update)
function saveProject(){
    const id = document.getElementById('projectId').value;
    const data = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        due_date: document.getElementById('due_date').value,
        priority: document.getElementById('priority').value,
        status: document.getElementById('status').value,
        assigned_to: currentUser.id // example assignment; can select trainee
    };
    let method = id ? 'PUT' : 'POST';
    let url = 'http://localhost:8000/api/projects/' + (id ? `${id}/` : '');

    fetch(url, {
        method: method,
        headers: {'Content-Type':'application/json','Authorization': `Bearer ${token}`},
        body: JSON.stringify(data)
    }).then(()=> fetchProjects());
}

// Trainer: Edit project
function editProject(id){
    fetch(`http://localhost:8000/api/projects/${id}/`, {headers: {'Authorization': `Bearer ${token}`}})
    .then(res => res.json())
    .then(p => {
        document.getElementById('projectId').value = p.id;
        document.getElementById('title').value = p.title;
        document.getElementById('description').value = p.description;
        document.getElementById('due_date').value = p.due_date;
        document.getElementById('priority').value = p.priority;
        document.getElementById('status').value = p.status;
    });
}

// Trainer: Delete project
function deleteProject(id){
    fetch(`http://localhost:8000/api/projects/${id}/`, {
        method: 'DELETE',
        headers: {'Authorization': `Bearer ${token}`}
    }).then(()=> fetchProjects());
}

// Trainee: Update project status
function updateStatus(id){
    const newStatus = prompt('Enter new status:');
    if(!newStatus) return;
    fetch(`http://localhost:8000/api/projects/${id}/`, {
        method: 'PATCH',
        headers: {'Content-Type':'application/json','Authorization': `Bearer ${token}`},
        body: JSON.stringify({status: newStatus})
    }).then(()=> fetchProjects(currentUser.id));
}

// Filter projects
function filterProjects(){
    const due_date = document.getElementById('filterDue').value;
    const priority = document.getElementById('filterPriority').value;
    fetchProjects(currentUser.is_trainee ? currentUser.id : null, {due_date, priority});
}
