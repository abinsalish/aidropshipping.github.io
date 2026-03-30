// Routing and simple frontend logic

// State
let currentUser = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setupRouting();
  setupInteractions();
  renderProducts(); // Mock
  
  // Hash change
  window.addEventListener('hashchange', setupRouting);

  // Initial load
  if(!window.location.hash) {
      window.location.hash = '#home';
  } else {
      setupRouting();
  }
});

function setupRouting() {
  const hash = window.location.hash || '#home';
  
  // Hide all pages
  document.querySelectorAll('.page').forEach(page => {
    page.classList.remove('active');
    page.classList.add('hidden');
  });

  // Show target page
  const targetId = `page-${hash.replace('#', '')}`;
  const targetPage = document.getElementById(targetId);
  if (targetPage) {
    targetPage.classList.remove('hidden');
    targetPage.classList.add('active');
  }

  // Update Nav Links
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === hash) {
      link.classList.add('active');
    }
  });
}

function setupInteractions() {
  // Mock login interaction (since Firebase isn't fully wired)
  const loginBtn = document.getElementById('login-google-btn');
  const logoutBtn = document.getElementById('logout-btn');
  const userProfile = document.getElementById('user-profile');
  
  loginBtn.addEventListener('click', () => {
    // Attempting login mockup
    loginBtn.classList.add('hidden');
    userProfile.classList.remove('hidden');
    document.getElementById('user-name').innerText = 'Admin User';
    document.getElementById('user-avatar').src = 'https://ui-avatars.com/api/?name=Admin+User&background=8b5cf6&color=fff';
    currentUser = { name: 'Admin User' };
    
    // Check if on home, redirect to dashboard
    if(window.location.hash === '#home') {
       window.location.hash = '#dashboard';
    }
  });

  logoutBtn.addEventListener('click', () => {
    loginBtn.classList.remove('hidden');
    userProfile.classList.add('hidden');
    currentUser = null;
    window.location.hash = '#home';
  });

  // AI Generation Mock
  const aiBtn = document.getElementById('generate-insights-btn');
  const aiBox = document.getElementById('ai-response-area');
  
  if (aiBtn) {
    aiBtn.addEventListener('click', async () => {
      aiBox.innerHTML = '<p class="gradient-text">Contacting Cloud Ollama Model...</p>';
      
      try {
        // Here we'll make a request to the FastAPI backend
        // const response = await fetch('http://localhost:8000/api/ai/insights');
        // const data = await response.json();
        
        setTimeout(() => {
          aiBox.innerHTML = `
            <p><strong>[Llama 3 Response]:</strong> Based on your dropshipping performance this week:</p>
            <ul>
              <li>Trend: Electronic accessories are surging by 24%</li>
              <li>Suggestion: Optimize pricing on "Smart Watch Pro" to maintain competitive margins.</li>
              <li>Warning: Shipping times from your primary supplier have increased. Consider alternative sourcing.</li>
            </ul>
          `;
        }, 1500); // Mock network delay
      } catch (e) {
        aiBox.innerHTML = '<p style="color:red;">Error reaching AI Endpoint.</p>';
      }
    });
  }
}

function renderProducts() {
  const products = [
    { name: 'Ultra-thin Wireless Charger', status: 'active', aiScore: 94 },
    { name: 'Ergonomic Standing Desk', status: 'active', aiScore: 88 },
    { name: 'Smart LED Light Strips', status: 'draft', aiScore: 71 },
    { name: 'Noise-Cancelling Earbuds', status: 'active', aiScore: 97 },
  ];

  const tbody = document.getElementById('product-list');
  if (!tbody) return;

  tbody.innerHTML = products.map(p => `
    <tr>
      <td><strong>${p.name}</strong></td>
      <td><span class="status-pill ${(p.status === 'active' ? 'active' : 'draft')}">${p.status.toUpperCase()}</span></td>
      <td>
        <span style="color: ${p.aiScore > 90 ? '#34d399' : '#fbbf24'}">
          ${p.aiScore}/100
        </span>
      </td>
      <td>
        <button class="btn secondary-btn" style="padding: 0.3rem 0.8rem; font-size: 0.8rem;">Edit</button>
      </td>
    </tr>
  `).join('');
}
