/* ── Icons ──────────────────────────────────────────────── */
const iconsReady = () => {
  if (window.lucide) window.lucide.createIcons();
};

/* ── Header scroll state ──────────────────────────────────── */
const header = document.querySelector("[data-header]");
if (header) {
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 12);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

/* ── Scroll-reveal ────────────────────────────────────────── */
const revealEls = document.querySelectorAll(
  ".feature-card, .service-card, .article-card, .portfolio-card, .event-card, " +
  ".testimonial-card, .stat-card, .timeline article, .section-heading, " +
  ".split-copy, .visual-panel, .page-hero > *, .contact-hero > *, .callout-band > *"
);
revealEls.forEach((el) => el.classList.add("reveal"));

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
);
revealEls.forEach((el) => observer.observe(el));

/* ── AI Particle canvas (hero background) ─────────────────── */
(function initParticles() {
  const hero = document.querySelector(".hero");
  if (!hero) return;

  const canvas = document.createElement("canvas");
  canvas.style.cssText =
    "position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1;opacity:0.55";
  hero.insertBefore(canvas, hero.firstChild);

  const ctx = canvas.getContext("2d");
  let W, H, particles;
  const COUNT = 60;
  const TEAL = "rgba(0,200,194,";
  const PURPLE = "rgba(139,92,246,";

  function resize() {
    W = canvas.width = hero.offsetWidth;
    H = canvas.height = hero.offsetHeight;
  }

  function rand(min, max) { return Math.random() * (max - min) + min; }

  function createParticles() {
    particles = Array.from({ length: COUNT }, () => ({
      x: rand(0, W), y: rand(0, H),
      vx: rand(-0.18, 0.18), vy: rand(-0.18, 0.18),
      r: rand(1, 2.5),
      color: Math.random() > 0.5 ? TEAL : PURPLE,
      alpha: rand(0.2, 0.65),
    }));
  }

  function drawConnections() {
    const maxDist = 130;
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < maxDist) {
          const a = (1 - dist / maxDist) * 0.18;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `${TEAL}${a})`;
          ctx.lineWidth = 0.6;
          ctx.stroke();
        }
      }
    }
  }

  function tick() {
    ctx.clearRect(0, 0, W, H);
    drawConnections();
    particles.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `${p.color}${p.alpha})`;
      ctx.fill();
    });
    requestAnimationFrame(tick);
  }

  resize();
  createParticles();
  tick();
  window.addEventListener("resize", () => { resize(); createParticles(); });
})();

/* ── Nav toggle ───────────────────────────────────────────── */
const navToggle = document.querySelector("[data-nav-toggle]");
const nav = document.querySelector("[data-nav]");
if (navToggle && nav) {
  navToggle.addEventListener("click", () => {
    nav.classList.toggle("open");
    const expanded = nav.classList.contains("open");
    navToggle.setAttribute("aria-label", expanded ? "Close navigation" : "Open navigation");
  });
}

/* ── Contact form ─────────────────────────────────────────── */
const contactForm = document.querySelector("[data-contact-form]");
if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const status = document.querySelector("[data-form-status]");
    contactForm.reset();
    if (status) status.textContent = "Inquiry received. The team will respond shortly.";
  });
}

/* ── Admin login / logout ─────────────────────────────────── */
const loginForm   = document.querySelector("[data-login-form]");
const loginPanel  = document.querySelector("[data-login-panel]");
const adminContent = document.querySelector("[data-admin-content]");
const logoutButton = document.querySelector("[data-logout]");

if (loginForm && loginPanel && adminContent) {
  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();
    loginPanel.hidden = true;
    adminContent.hidden = false;
  });
}

if (logoutButton && loginPanel && adminContent) {
  logoutButton.addEventListener("click", () => {
    adminContent.hidden = true;
    loginPanel.hidden = false;
  });
}

/* ── Animated counter for metric numbers ─────────────────── */
function animateCounter(el, target, duration) {
  const isFloat = target.includes(".");
  const num = parseFloat(target.replace(/[^0-9.]/g, ""));
  const suffix = target.replace(/[0-9.]/g, "");
  const start = performance.now();
  const step = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    const val = isFloat
      ? (num * ease).toFixed(1)
      : Math.round(num * ease);
    el.textContent = val + suffix;
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll(".metric-row strong, .stat-card strong").forEach((el) => {
        const original = el.textContent.trim();
        animateCounter(el, original, 1400);
      });
      counterObserver.unobserve(entry.target);
    });
  },
  { threshold: 0.4 }
);

document.querySelectorAll(".metric-row, .stat-grid").forEach((el) =>
  counterObserver.observe(el)
);

iconsReady();
