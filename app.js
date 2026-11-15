const photos = [
  { image: 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=1500&q=85', place: 'Parque Nacional Serengeti', country: 'Tanzania' },
  { image: 'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1500&q=85', place: 'Cinque Terre', country: 'Italia' },
  { image: 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1500&q=85', place: 'Lago di Braies', country: 'Dolomitas, Italia' },
  { image: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1500&q=85', place: 'Valle de Cocora', country: 'Quindío, Colombia' }
];
const destinationCards = [
  ['Patagonia', 'Chile y Argentina', 'photo-1464822759023-fed622ff2c3b'],
  ['Costa Amalfitana', 'Italia', 'photo-1516483638261-f4dbaf036963'],
  ['Valle de Cocora', 'Colombia', 'photo-1516026672322-bc52d61a55d5'],
  ['Santorini', 'Grecia', 'photo-1533105079780-92b9be482077']
];

const app = document.querySelector('#app');
let user = null;
let posts = [];
let suggestions = [];
let activeTab = 'feed';
let slide = 0;
let toastTimer;

async function api(path, { method = 'GET', body } = {}) {
  const options = { method, credentials: 'same-origin', headers: {} };
  if (body !== undefined) {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(body);
  }
  const response = await fetch(path, options);
  let data = {};
  try { data = await response.json(); } catch { /* empty response */ }
  if (!response.ok) {
    const error = new Error(data.error || 'No se pudo completar la solicitud.');
    error.status = response.status;
    throw error;
  }
  return data;
}

function esc(value = '') {
  return String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
}

function avatar(url, name) {
  return url ? `<img class="avatar" src="${esc(url)}" alt="" />` : `<span class="avatar">${esc((name || 'V').split(' ').map(x => x[0]).slice(0, 2).join('').toUpperCase())}</span>`;
}

function notify(message) {
  const toast = document.querySelector('#toast');
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2500);
}

function renderLanding() {
  app.innerHTML = `<header class="nav"><a class="brand" href="#" aria-label="TravelSnap inicio"><span class="brand-mark">✳</span>travel<span style="font-weight:400">snap</span></a><div class="nav-right"><a class="nav-link" href="#destinos">Inspiración</a><button class="btn btn-outline" data-auth="login">Iniciar sesión</button><button class="btn" data-auth="register">Crear cuenta</button></div></header>
  <div class="landing"><section class="hero"><div class="hero-copy"><span class="eyebrow">Una comunidad para viajeros</span><h1>El mundo,<br>desde <em>tu mirada.</em></h1><p>Guarda esos lugares que te cambiaron. Descubre tu próximo destino a través de las historias de quienes ya estuvieron ahí.</p><div class="hero-cta"><button class="btn" data-auth="register">Únete a TravelSnap <span aria-hidden="true">↗</span></button><button class="btn btn-outline" data-auth="login">Ya tengo cuenta</button></div><div class="hero-note">✦ &nbsp;Una foto puede inspirar el próximo viaje.</div></div>
  <div class="hero-visual"><img class="hero-image" id="heroImage" src="${photos[0].image}" alt="Paisaje de viaje en ${photos[0].place}"><div class="image-shade"></div><div class="photo-tag"><b>✳ &nbsp; Un mundo por descubrir</b>Inspiración de viajeros reales</div><div class="photo-caption"><small id="heroCountry">${photos[0].country}</small><strong id="heroPlace">${photos[0].place}</strong></div><div class="carousel-controls">${photos.map((_, i) => `<button class="carousel-dot ${i === 0 ? 'active' : ''}" data-slide="${i}" aria-label="Ver foto ${i + 1}"></button>`).join('')}</div></div></section>
  <section id="destinos"><div class="section-head"><div><span class="eyebrow">Ideas para tu próxima aventura</span><h2 class="serif">Un mundo ahí afuera</h2></div><span style="font-size:12px;color:#849087">Lugares que inspiran ✦</span></div><div class="destinations">${destinationCards.map(([city, country, id]) => `<div class="destination"><img loading="lazy" src="https://images.unsplash.com/${id}?auto=format&fit=crop&w=650&q=80" alt="${city}"><span><small>${country}</small>${city}</span></div>`).join('')}</div></section>
  <footer class="landing-footer"><span>© 2026 TravelSnap · Hecho para quienes siempre quieren ir más allá.</span><span>Tu próxima historia empieza con una foto. ✳</span></footer></div>`;
}

function postCard(post) {
  return `<article class="post-card"><div class="post-top">${avatar(post.avatar, post.name)}<div><div class="post-author">${esc(post.name)}</div><div class="post-meta">@${esc(post.handle)} · ${esc(post.date)}</div></div>${post.owner === 'me' ? `<button class="post-delete" data-delete="${esc(post.id)}" aria-label="Eliminar publicación" title="Eliminar publicación">Eliminar</button>` : ''}</div>
  <div class="post-image-wrap"><img class="post-image" src="${esc(post.image)}" alt="${esc(post.title)}" loading="lazy"><span class="post-location">⌖ &nbsp;${esc(post.city)}, ${esc(post.country)}</span></div>
  <div class="post-content"><h2 class="post-title">${esc(post.title)}</h2><p class="post-description">${esc(post.description)}</p><div class="post-actions"><button class="action ${post.liked ? 'liked' : ''}" data-like="${esc(post.id)}">${post.liked ? '♥' : '♡'} &nbsp;${post.likes} me gusta</button><button class="action" data-comments="${esc(post.id)}">◯ &nbsp; Comentar</button><button class="action right" data-share="${esc(post.id)}">↗ &nbsp; Compartir</button></div></div></article>`;
}

function renderApp() {
  const visiblePosts = activeTab === 'profile' ? posts.filter(post => post.owner === 'me') : posts;
  app.innerHTML = `<header class="app-nav"><div class="app-nav-inner"><a class="brand" href="#"><span class="brand-mark">✳</span>travel<span style="font-weight:400">snap</span></a><nav class="app-nav-links"><button data-tab="feed" class="${activeTab === 'feed' ? 'active' : ''}">Inicio</button><button data-tab="profile" class="${activeTab === 'profile' ? 'active' : ''}">Mi perfil</button></nav><div class="app-user">${avatar(null, user.name)}<div><div class="user-name">${esc(user.name)}</div><div class="quiet">Viajero/a</div></div><button class="btn btn-outline" style="padding:9px 13px;font-size:11px;margin-left:8px" data-logout>Salir</button></div></div></header>
  <div class="app-shell"><main class="app-main"><section><div class="feed-title"><div><span class="eyebrow">${activeTab === 'profile' ? 'Tu espacio viajero' : 'Tu dosis de inspiración'}</span><h1>${activeTab === 'profile' ? 'Mi perfil' : 'Explora el mundo'}</h1><p>${activeTab === 'profile' ? 'Tus historias de viaje, todas en un lugar.' : 'Historias frescas de viajeros como tú.'}</p></div><button class="btn" data-compose>＋ Publicar</button></div>${visiblePosts.length ? visiblePosts.map(postCard).join('') : `<div class="empty-state"><div class="serif">Todavía no hay publicaciones</div><p>Comparte tu primera aventura para empezar tu perfil.</p><button class="btn" data-compose>＋ Compartir una foto</button></div>`}</section>
  <aside class="sidebar"><div class="sidebar-card"><div class="side-label">Tu perfil viajero</div><h3>¡Qué bueno verte, ${esc(user.name.split(' ')[0])}!</h3><div class="sidebar-profile">${avatar(null, user.name)}<div><div class="user-name">${esc(user.name)}</div><div class="quiet">Una historia en cada destino.</div></div></div><button class="btn btn-outline" style="width:100%;font-size:11px;padding:9px" data-tab="profile">Ver mi perfil</button></div>
  <div class="sidebar-card"><div class="side-label">Comunidad</div><h3>Viajeros para seguir</h3>${suggestions.map(person => `<div class="sidebar-profile">${avatar(person.avatar, person.name)}<div><div class="user-name">${esc(person.name)}</div><div class="quiet">@${esc(person.handle)}</div></div><button class="btn btn-outline follow" data-follow="${esc(person.handle)}">${person.followed ? 'Siguiendo' : 'Seguir'}</button></div>`).join('')}</div><div class="sidebar-card side-note"><div class="side-label">Una nota de viaje</div><p>“No todos los que vagan están perdidos.”<br><strong>— J. R. R. Tolkien</strong></p></div></aside></main></div>`;
}

async function loadAppData() {
  const [postData, suggestionData] = await Promise.all([api('/api/posts'), api('/api/suggestions')]);
  posts = postData.posts;
  suggestions = suggestionData.suggestions;
  renderApp();
}

function openAuth(mode) {
  const register = mode === 'register';
  document.body.insertAdjacentHTML('beforeend', `<div class="modal-backdrop" id="modalBackdrop"><section class="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle"><button class="modal-close" data-close aria-label="Cerrar">×</button><span class="eyebrow">${register ? 'Empieza tu historia' : 'Qué bueno verte de nuevo'}</span><h2 id="modalTitle">${register ? 'Únete a TravelSnap' : 'Bienvenido de vuelta'}</h2><p>${register ? 'Crea tu cuenta y empieza a guardar los lugares que te mueven.' : 'Inicia sesión para volver a explorar tu comunidad viajera.'}</p>
  <form id="authForm" data-mode="${register ? 'register' : 'login'}">${register ? '<label class="field"><span>Tu nombre</span><input name="name" autocomplete="name" placeholder="¿Cómo te llamas?" required minlength="2" maxlength="80"></label>' : ''}<label class="field"><span>Correo electrónico</span><input name="email" type="email" autocomplete="email" placeholder="tu@correo.com" required></label><label class="field"><span>Contraseña</span><input name="password" type="password" autocomplete="${register ? 'new-password' : 'current-password'}" placeholder="${register ? 'Mínimo 8 caracteres' : 'Tu contraseña'}" required minlength="8"></label><div class="form-error" id="authError"></div><button class="btn" type="submit">${register ? 'Crear mi cuenta' : 'Iniciar sesión'} ↗</button></form><div class="modal-switch">${register ? '¿Ya tienes cuenta?' : '¿Primera vez por aquí?'} <button class="text-button" data-switch="${register ? 'login' : 'register'}">${register ? 'Inicia sesión' : 'Crea tu cuenta'}</button></div></section></div>`);
  document.querySelector('[name="email"]').focus();
}

function openCompose() {
  document.body.insertAdjacentHTML('beforeend', `<div class="modal-backdrop" id="modalBackdrop"><section class="modal" role="dialog" aria-modal="true"><button class="modal-close" data-close aria-label="Cerrar">×</button><span class="eyebrow">Comparte el camino</span><h2>Tu próxima historia</h2><p>Cuéntale a la comunidad sobre ese lugar especial.</p><form id="postForm"><label class="field"><span>URL de una fotografía</span><input name="image" type="url" placeholder="https://…" value="https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1200&q=85" required></label><label class="field"><span>Título</span><input name="title" placeholder="¿Qué hizo especial este lugar?" required maxlength="90"></label><label class="field"><span>Tu historia</span><textarea name="description" placeholder="Comparte un recuerdo o consejo…" required maxlength="300"></textarea></label><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px"><label class="field"><span>Ciudad</span><input name="city" placeholder="Ciudad" required maxlength="80"></label><label class="field"><span>País</span><input name="country" placeholder="País" required maxlength="80"></label></div><div class="form-error" id="postError"></div><button class="btn" type="submit">Compartir publicación ↗</button></form></section></div>`);
}

async function loadComments(postId) {
  const list = document.querySelector('#commentList');
  if (!list) return;
  list.innerHTML = '<div class="empty">Cargando comentarios…</div>';
  try {
    const result = await api(`/api/posts/${encodeURIComponent(postId)}/comments`);
    if (!document.querySelector('#commentList')) return;
    list.innerHTML = result.comments.length ? result.comments.map(comment => `<article class="comment-item">${avatar(comment.avatar, comment.name)}<div><div class="comment-author">${esc(comment.name)} <span>@${esc(comment.handle)}</span></div><p>${esc(comment.body)}</p><small>${esc(comment.created_at)}</small></div></article>`).join('') : '<div class="empty">Todavía no hay comentarios. ¡Sé el primero!</div>';
  } catch (error) {
    if (document.querySelector('#commentList')) list.innerHTML = `<div class="form-error">${esc(error.message)}</div>`;
  }
}

async function openComments(postId) {
  const post = posts.find(item => item.id === postId);
  if (!post) return;
  document.body.insertAdjacentHTML('beforeend', `<div class="modal-backdrop" id="modalBackdrop"><section class="modal comments-modal" role="dialog" aria-modal="true" aria-labelledby="commentsTitle"><button class="modal-close" data-close aria-label="Cerrar">×</button><span class="eyebrow">Conversación de viaje</span><h2 id="commentsTitle">Comentarios</h2><p class="comment-post-title">${esc(post.title)} · ${esc(post.city)}, ${esc(post.country)}</p><div class="comment-list" id="commentList"></div><form id="commentForm" data-post="${esc(post.id)}"><label class="field"><span>Escribe un comentario</span><textarea name="body" maxlength="1000" placeholder="Comparte una opinión o pregunta…" required></textarea></label><div class="form-error" id="commentError"></div><button class="btn" type="submit">Publicar comentario</button></form></section></div>`);
  await loadComments(postId);
}

function setSlide(index) {
  slide = index;
  const image = document.querySelector('#heroImage');
  if (!image) return;
  image.classList.add('fade');
  setTimeout(() => {
    const photo = photos[index];
    image.src = photo.image;
    document.querySelector('#heroCountry').textContent = photo.country;
    document.querySelector('#heroPlace').textContent = photo.place;
    image.classList.remove('fade');
    document.querySelectorAll('.carousel-dot').forEach((dot, i) => dot.classList.toggle('active', i === index));
  }, 220);
}

document.addEventListener('click', async event => {
  const auth = event.target.closest('[data-auth]');
  if (auth) return openAuth(auth.dataset.auth);
  if (event.target.closest('[data-close]') || event.target.id === 'modalBackdrop') return document.querySelector('#modalBackdrop')?.remove();
  const switchButton = event.target.closest('[data-switch]');
  if (switchButton) { const mode = switchButton.dataset.switch; document.querySelector('#modalBackdrop').remove(); return openAuth(mode); }
  const dot = event.target.closest('[data-slide]');
  if (dot) return setSlide(Number(dot.dataset.slide));
  const tab = event.target.closest('[data-tab]');
  if (tab) { activeTab = tab.dataset.tab; try { await loadAppData(); } catch (error) { notify(error.message); } return; }
  if (event.target.closest('[data-logout]')) {
    try { await api('/api/logout', { method: 'POST', body: {} }); user = null; posts = []; suggestions = []; renderLanding(); notify('Sesión cerrada. ¡Hasta el próximo viaje!'); }
    catch (error) { notify(error.message); }
    return;
  }
  if (event.target.closest('[data-compose]')) return openCompose();
  const deleteButton = event.target.closest('[data-delete]');
  if (deleteButton) {
    const post = posts.find(item => item.id === deleteButton.dataset.delete);
    if (post?.owner === 'me' && window.confirm('¿Quieres eliminar esta publicación? Esta acción no se puede deshacer.')) {
      try { await api(`/api/posts/${encodeURIComponent(post.id)}`, { method: 'DELETE' }); await loadAppData(); notify('Publicación eliminada.'); }
      catch (error) { notify(error.message); }
    }
    return;
  }
  const likeButton = event.target.closest('[data-like]');
  if (likeButton) {
    const post = posts.find(item => item.id === likeButton.dataset.like);
    if (!post) return;
    try { await api(`/api/posts/${encodeURIComponent(post.id)}/likes`, { method: post.liked ? 'DELETE' : 'POST', ...(post.liked ? {} : { body: {} }) }); await loadAppData(); }
    catch (error) { notify(error.message); }
    return;
  }
  const followButton = event.target.closest('[data-follow]');
  if (followButton) {
    const handle = followButton.dataset.follow;
    const person = suggestions.find(item => item.handle === handle);
    try { await api(`/api/follows/${encodeURIComponent(handle)}`, { method: person?.followed ? 'DELETE' : 'POST', ...(person?.followed ? {} : { body: {} }) }); await loadAppData(); }
    catch (error) { notify(error.message); }
    return;
  }
  const commentsButton = event.target.closest('[data-comments]');
  if (commentsButton) return openComments(commentsButton.dataset.comments);
  if (event.target.closest('[data-share]')) {
    try { await navigator.clipboard.writeText(location.href); notify('¡Enlace copiado para compartir!'); }
    catch { notify('Copia el enlace desde la barra del navegador para compartir.'); }
  }
});

document.addEventListener('submit', async event => {
  if (event.target.id === 'authForm') {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    const payload = { email: String(data.get('email')).trim(), password: String(data.get('password')) };
    const register = form.dataset.mode === 'register';
    if (register) payload.name = String(data.get('name')).trim();
    try {
      const result = await api(register ? '/api/register' : '/api/login', { method: 'POST', body: payload });
      user = result.user;
      activeTab = 'feed';
      document.querySelector('#modalBackdrop').remove();
      await loadAppData();
      notify(register ? '¡Tu cuenta quedó guardada en TravelSnap!' : '¡Qué bueno tenerte de vuelta!');
    } catch (error) {
      const target = document.querySelector('#authError');
      if (target) target.textContent = error.message;
    }
  }

  if (event.target.id === 'postForm') {
    event.preventDefault();
    const data = new FormData(event.target);
    const payload = Object.fromEntries(['image', 'title', 'description', 'city', 'country'].map(key => [key, String(data.get(key)).trim()]));
    try {
      await api('/api/posts', { method: 'POST', body: payload });
      document.querySelector('#modalBackdrop').remove();
      activeTab = 'feed';
      await loadAppData();
      notify('Tu historia ya forma parte del feed.');
    } catch (error) {
      const target = document.querySelector('#postError');
      if (target) target.textContent = error.message;
    }
  }

  if (event.target.id === 'commentForm') {
    event.preventDefault();
    const form = event.target;
    const postId = form.dataset.post;
    const body = String(new FormData(form).get('body') || '').trim();
    try {
      await api(`/api/posts/${encodeURIComponent(postId)}/comments`, { method: 'POST', body: { body } });
      form.reset();
      await loadComments(postId);
      notify('Comentario publicado.');
    } catch (error) {
      const target = document.querySelector('#commentError');
      if (target) target.textContent = error.message;
    }
  }
});

document.addEventListener('keydown', event => { if (event.key === 'Escape') document.querySelector('#modalBackdrop')?.remove(); });

async function initialize() {
  renderLanding();
  setInterval(() => setSlide((slide + 1) % photos.length), 5200);
  try {
    const result = await api('/api/me');
    user = result.user;
    await loadAppData();
  } catch (error) {
    if (error.status !== 401) notify('No se pudo conectar con TravelSnap. Comprueba que el servidor esté activo.');
  }
}

initialize();
