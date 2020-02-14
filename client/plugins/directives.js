import Vue from "vue";

Vue.directive("expand", {
  inserted: function(el, binding) {
    if (binding.value !== null) {
      function calcHeight() {
        const currentState = el.getAttribute("aria-expanded");

        el.classList.add("u-no-transition");
        el.removeAttribute("aria-expanded");
        el.style.height = null;
        el.style.height = el.clientHeight + "px";
        el.setAttribute("aria-expanded", currentState);

        setTimeout(function() {
          el.classList.remove("u-no-transition");
        });
      }

      el.classList.add("expand");
      el.setAttribute("aria-expanded", binding.value ? "true" : "false");
      calcHeight();
      window.addEventListener("resize", calcHeight);
    }
  },
  update: function(el, binding) {
    if (el.style.height && binding.value !== null) {
      el.setAttribute("aria-expanded", binding.value ? "true" : "false");
    }
  }
});

Vue.directive("click-outside", {
  bind(el, binding, vnode) {
    var vm = vnode.context;
    var callback = binding.value;

    el.clickOutsideEvent = function(event) {
      if (!(el == event.target || el.contains(event.target))) {
        return callback.call(vm, event);
      }
    };
    document.body.addEventListener("click", el.clickOutsideEvent);
  },
  unbind(el) {
    document.body.removeEventListener("click", el.clickOutsideEvent);
  }
});

Vue.directive("scroll-end", {
  /* fire event at scroll end with delay 150ms */
  bind(el, binding, vnode) {
    var vm = vnode.context;
    var callback = binding.value;
    var scrollTimer = -1;
    el.scrollEnd = function(event) {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(() => callback.call(vm, event), 150);
    };
    el.addEventListener("scroll", el.scrollEnd);
  },
  unbind(el) {
    el.removeEventListener("scroll", el.scrollEnd);
  }
});
