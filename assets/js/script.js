(() => {
  "use strict";

  // ----- Scroll Reveal -----
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  // ----- Header shadow on scroll -----
  const header = document.getElementById("siteHeader");
  const onScrollHeader = () => {
    if (!header) return;
    if (window.scrollY > 8) header.classList.add("is-scrolled");
    else header.classList.remove("is-scrolled");
  };
  window.addEventListener("scroll", onScrollHeader, { passive: true });
  onScrollHeader();

  // ----- Floating CTA visibility -----
  const floating = document.getElementById("floatingCta");
  const heroSection = document.getElementById("hero");
  const finalCta = document.getElementById("cta-final");

  if (floating && heroSection && "IntersectionObserver" in window) {
    let pastHero = false;
    let inFinal = false;

    const heroObs = new IntersectionObserver(
      ([entry]) => {
        pastHero = !entry.isIntersecting && entry.boundingClientRect.top < 0;
        update();
      },
      { threshold: 0 }
    );
    heroObs.observe(heroSection);

    if (finalCta) {
      const finalObs = new IntersectionObserver(
        ([entry]) => {
          inFinal = entry.isIntersecting;
          update();
        },
        { threshold: 0.18 }
      );
      finalObs.observe(finalCta);
    }

    const update = () => {
      if (pastHero && !inFinal) floating.classList.add("is-visible");
      else floating.classList.remove("is-visible");
    };
  }

  // ----- Smooth anchor scrolling with header offset -----
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id.length <= 1) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const offset = (header?.offsetHeight || 0) + 8;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: "smooth" });
    });
  });
})();
