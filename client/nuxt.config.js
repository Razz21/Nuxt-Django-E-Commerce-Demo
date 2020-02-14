// to use .env file variables
require("dotenv").config();
export default {
  mode: "universal",

  /*
   ** Headers of the page
   */
  head: {
    titleTemplate: "%s - TAKT Furnitures",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      {
        hid: "description",
        name: "description",
        content: process.env.npm_package_description || ""
      }
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }]
    // script: [{ src: "https://js.stripe.com/v3/" }]
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: "#ff0000" },
  /*
   ** Global CSS
   */
  css: [],
  styleResources: {
    scss: ["assets/scss/main.scss"] // no point to root directory
  },
  //pageTransition: { name: "fade-page", mode: "in-out" },
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [
    "~/plugins/auth.js",
    "~/plugins/vue-filters",
    "~/plugins/directives",
    "~/plugins/mixins"
  ],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: ["@nuxtjs/vuetify", "@nuxtjs/dotenv", "@nuxtjs/router-extras"],
  /*
   ** Nuxt.js modules
   */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    "@nuxtjs/axios",
    "@nuxtjs/proxy",
    "@nuxtjs/style-resources",
    "@nuxtjs/auth",
    // Doc: https://github.com/nuxt-community/dotenv-module
    "@nuxtjs/dotenv",
    "@nuxtjs/toast"
  ],
  /*
   ** Axios module configuration
   ** See https://axios.nuxtjs.org/options
   */
  axios: {
    credentials: true,
    proxy: true
    // baseURL: process.env.BASE_URL
  },
  proxy: {
    "/api/": {
      target: `${process.env.BASE_URL}/api/`,
      pathRewrite: { "^/api/": "" }
    },
    "/auth/": {
      target: `${process.env.BASE_URL}/api/auth/`,
      pathRewrite: { "^/auth/": "" }
    },
    "/media/": {
      target: `${process.env.BASE_URL}/media/`,
      pathRewrite: { "^/media/": "" }
    }
  },
  auth: {
    strategies: {
      local: {
        endpoints: {
          login: { url: "/auth/login/", method: "post", propertyName: "token" },
          logout: { url: "/auth/logout/", method: "post" },
          user: { url: "/auth/user/", method: "get", propertyName: false }
        },
        // tokenRequired: true,
        tokenType: "Token"
      }
    },
    watchLoggedIn: true,

    plugins: [],
    redirect: {
      login: "/login/",
      logout: "/",
      callback: "/login/",
      home: "/"
    }
  },
  router: {
    trailingSlash: true,
    // mode: "hash",

    extendRoutes(routes, resolve) {
      const productsIdx = routes.findIndex(route => route.path == "/products/");
      const child = routes[productsIdx].children;
      const newChildren = [
        ...child,
        {
          name: "products-category",
          path: "category/:slug/",
          component: "~/pages/products/index.vue"
        }
      ];
      routes[productsIdx].children = newChildren;
      routes.push({
        path: "*",
        redirect: "/"
      });
    }
  },
  /*
   ** Build configuration
   */
  vuetify: {
    customVariables: ["~/assets/variables.scss"],
    defaultAssets: {
      font: {
        family: "Prompt"
      }
    },
    treeShake: true,
    theme: {
      // dark: true,
      dark: false,
      themes: {
        dark: {
          primary: "#74AFBE",
          accent: "#AECED4",
          secondary: "#8F7575",
          success: "#4CAF50",
          info: "#2196F3",
          warning: "#FB8C00",
          error: "#FF5252"
        },
        light: {
          primary: "#FE7966",
          accent: "#6c698d",
          secondary: "#008487",
          success: "#4CAF50",
          info: "#2196F3",
          warning: "#FB8C00",
          error: "#FF5252",
          carbon: "#322f31",
          "primary-light": "#fff5f1",
          "white-color": "#fdfdfd",
          "gray-light": "#EAEAE6"
        }
      }
    }
  },
  toast: {
    position: "top-center",
    duration: 2000,
    register: [
      // Register custom toasts
    ]
  },
  build: {
    /*
     ** You can extend webpack config here
     */
    extractCSS: true,
    terser: {
      terserOptions: {
        compress: {
          drop_console: true
        }
      }
    },
    extend(config, ctx) {}
  },
  env: {}
};
