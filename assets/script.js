// Mobile menu
const toggle = document.querySelector(".nav-toggle");
const nav = document.getElementById("nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
    toggle.textContent = open ? "✕" : "☰";
  });
  nav.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", false);
      toggle.textContent = "☰";
    })
  );
}

const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

// Quote forms (quick form at the top + full form at the bottom):
// validate required fields, then submit to Formspree
const rules = {
  name: (v) => v.trim().length > 1,
  phone: (v) => v.replace(/\D/g, "").length >= 10,
  address: (v) => v.trim().length > 4,
  email: (v) => v.trim() === "" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()),
};

document.querySelectorAll(".quote-form").forEach((form) => {
  const fields = Object.keys(rules).filter((name) => form.elements[name]);

  const check = (name) => {
    const input = form.elements[name];
    const ok = rules[name](input.value);
    input.classList.toggle("invalid", !ok);
    input.setAttribute("aria-invalid", !ok);
    return ok;
  };

  fields.forEach((name) => form.elements[name].addEventListener("blur", () => check(name)));

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (fields.map(check).includes(false)) {
      form.querySelector(".invalid").focus();
      return;
    }

    const button = form.querySelector("button[type=submit]");
    const label = button.textContent;
    button.disabled = true;
    button.textContent = "Sending…";

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
      });
      if (!res.ok) throw new Error(res.status);
      window.location.href = "/thank-you/";
    } catch (err) {
      button.disabled = false;
      button.textContent = label;
      const phone = document.querySelector('a[href^="tel:"]');
      alert("Sorry, something went wrong sending your request. Please call us" + (phone ? " at " + phone.textContent.replace("📞", "").trim() : "") + ".");
    }
  });
});
